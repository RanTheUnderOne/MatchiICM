#!/usr/bin/env python3
"""ICM Facebook group scanner wired to Apify + prod MCP.

1. Scrapes Facebook group posts via Apify REST API (or loads pre-scraped JSON)
2. Parses Hebrew/English posts with deterministic regex for real estate signals
3. Dedupes against existing MCP properties + potential properties
4. Calls add_new_potential_property for each new lead
5. Dry-run by default; --write commits to prod DB

Usage:
  py scripts/mcp_facebook_scan_run.py --fb-group-url "https://www.facebook.com/groups/12345/"
  py scripts/mcp_facebook_scan_run.py --raw-json _mock/fb-groups-raw.json
  py scripts/mcp_facebook_scan_run.py --fb-group-url URL --write
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mcp_client import MCPClient, DEFAULT_USER

try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

SCRIPT_DIR = Path(__file__).resolve().parent
MOCK_DIR = SCRIPT_DIR.parent / "_mock"
OUT_DIR = SCRIPT_DIR.parent / "phases/3-leads/facebook-scan/output"

APIFY_API = "https://api.apify.com/v2"
FB_SCRAPER_ACTOR = "apify/facebook-groups-scraper"

# ── Regex extractors ──

# Price patterns: ₪1,500,000 / 1,500,000 ש״ח / 1500000 / 1.5M / 4500 לחודש
PRICE_RE = re.compile(
    r"(?:₪\s*|מחיר\s*:?\s*|תקציב\s*:?\s*|עד\s*|ב\s*)?"
    r"(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?:אלף|K|[kK])?"
    r"\s*(?:ש״ח|שח|₪|ש\"ח)?"
    r"(?:\s*(?:לחודש|לחוד|בחודש|חודשי))?"
)

# More structured: "1.6 מיליון" / "2.1M" / "2,150,000"
PRICE_MILLION_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*(?:M|מיליון|מליון)\b", re.IGNORECASE
)

PRICE_SIMPLE_RE = re.compile(
    r"(?:₪|ש[״\"]ח|שח|מחיר|תקציב|מחפש[ת]?\s+(?:עד|ב)|עד)\s*"
    r"(\d{1,3}(?:,\d{3})*(?:\.\d+)?)"
    r"(?:\s*(?:K|אלף))?"
)

# Rooms: "3 חדרים" / "2BR" / "סטודיו" / "4.5 חד׳"
ROOMS_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*(?:חדרים|חד׳|חד'|חדר|rooms?|BR|bedrooms?)", re.IGNORECASE
)
STUDIO_RE = re.compile(r"\b(?:סטודיו|סטודיו|studio)\b", re.IGNORECASE)

# City: known Israeli cities
CITIES = [
    "חיפה", "תל אביב", "ת\"א", "ירושלים", "באר שבע", "נתניה", "חולון",
    "פתח תקווה", "פ\"ת", "אשדוד", "ראשון לציון", "ראשל\"צ", "רמת גן",
    "הרצליה", "כפר סבא", "רעננה", "חדרה", "נהריה", "עכו", "כרמיאל",
    "אילת", "מודיעין", "בית שמש", "לוד", "רמלה", "קריות", "הדר",
    "גבעתיים", "קריית אונו", "קריית אתא", "גבעת שמואל", "אור יהודה",
    "יהוד", "בני ברק", "קריית מוצקין", "קריית ים", "קריית ביאליק",
    "נשר", "טירת הכרמל", "יקנעם", "מגדל העמק", "עפולה", "בית שאן",
    "צפת", "טבריה", "קריית שמונה", "דימונה", "ירוחם", "מצפה רמון",
    "כרמל", "נווה שאנן", "מרכז", "נאות",
    # Ramat Gan neighborhoods
    "רמת חן", "תל יהודה", "נחלת גנים", "שיכון הצנחנים", "רמת עמידר",
    # Givatayim neighborhoods
    "גבעת רמבם", "ארלוזורוב",
    # Tel Aviv neighborhoods
    "פלורנטין", "נווה צדק", "כרם התימנים", "רמת אביב",
]
# NOTE: \b fails with Hebrew prefixes (ב/ל/מ/ה/ו). Use non-capturing
# prefix alternation: allow optional single-char prefix before city.
CITY_RE = re.compile(
    r"(?:^|\s|[בלמהו])(?:" + "|".join(re.escape(c) for c in CITIES) + r")(?:\s|$|[,.]|$)",
    re.IGNORECASE
)

# Phone numbers
PHONE_RE = re.compile(
    r"(?:0(?:5[0-9]|2|3|4|6|7|8|9))"
    r"(?:[-\s.]?\d{3,4}){2,3}"
    r"\d?"
)

# Address: רחוב X 12 / X 12 קומה Y
ADDRESS_RE = re.compile(
    r"(?:רחוב|רח׳|רח'|ברחוב)\s+([֐-׿\w\s]+?)(?:\s+\d+)?(?:\s*,|\s+ב|$)",
    re.IGNORECASE
)

# Transaction type
SALE_RE = re.compile(
    r"\b(?:לקנות|לרכוש|קנייה|רכישה|למכירה|מכירה|מוכר|מוכרת|sale|buy|purchase)\b",
    re.IGNORECASE
)
RENT_RE = re.compile(
    r"\b(?:להשכיר|לשכור|שכירות|השכרה|משכיר|להשכרה|rent|rental)\b",
    re.IGNORECASE
)

# Area: "105 מ״ר" / "52m²" / "120 sqm" / "105 מטר"
AREA_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*(?:מ״ר|מטר|מ\"ר|מר|ממר|sqm|m²|m2|sq\.?\s*m)",
    re.IGNORECASE
)

# Floor: "קומה 3" / "floor 2"
FLOOR_RE = re.compile(
    r"(?:קומה|floor)\s*(\d+)", re.IGNORECASE
)

# Spam filter
SPAM_WORDS = ["הלוואות", "ללא ריבית", "לחצו כאן", "הלוואה מיידית",
              "click here", "free money", "get rich", "loan"]
SPAM_RE = re.compile("|".join(re.escape(w) for w in SPAM_WORDS), re.IGNORECASE)


def parse_price(text):
    """Extract numeric price from text. Returns (amount, is_monthly)."""
    # "1.6 מיליון" / "2.1M"
    m = PRICE_MILLION_RE.search(text)
    if m:
        return int(float(m.group(1)) * 1_000_000), False

    # Find structured prices
    for m in PRICE_SIMPLE_RE.finditer(text):
        raw = m.group(1).replace(",", "")
        try:
            val = float(raw)
            is_monthly = "חודש" in text[m.start():m.end()+20] or "חודשי" in text[m.start():m.end()+20]
            # If value < 100, could be in thousands or millions
            if val < 100:
                near = text[max(0,m.start()-10):m.end()+10]
                if "אלף" in near or "K" in near.upper():
                    val *= 1000
                elif val < 50:
                    # "תקציב 2.1" = 2.1 million ₪ (common Hebrew shorthand)
                    val *= 1_000_000
            return int(val), is_monthly
        except ValueError:
            continue

    # Generic number matching — look for 4-7 digit numbers likely to be prices
    for m in re.finditer(r"\b(\d{1,3}(?:,\d{3}){1,2})\b", text):
        raw = m.group(1).replace(",", "")
        val = int(raw)
        if 1000 <= val <= 50_000_000:
            is_monthly = "חודש" in text[m.start():m.end()+30] or "חודשי" in text[m.start():m.end()+30]
            return val, is_monthly

    return None, False


def parse_rooms(text):
    """Extract room count."""
    m = STUDIO_RE.search(text)
    if m:
        return 1.0
    m = ROOMS_RE.search(text)
    if m:
        return float(m.group(1))
    return None


def parse_city(text):
    """Extract city name."""
    m = CITY_RE.search(text)
    if m:
        raw = m.group(0).strip()
        # Strip Hebrew prefix char (ב/ל/מ/ה/ו) if present
        if raw and raw[0] in "בלמהו":
            raw = raw[1:]
        # Normalize
        if raw in ("ת\"א",):
            return "תל אביב"
        if raw in ("פ\"ת",):
            return "פתח תקווה"
        if raw in ("ראשל\"צ",):
            return "ראשון לציון"
        return raw
    return None


def parse_phone(text):
    """Extract Israeli phone number."""
    m = PHONE_RE.search(text)
    return m.group(0) if m else None


def parse_transaction_type(text):
    """Determine sale vs rent."""
    is_sale = SALE_RE.search(text)
    is_rent = RENT_RE.search(text)
    if is_sale and not is_rent:
        return "sale"
    if is_rent and not is_sale:
        return "rent"
    # Check for price words
    if "מחיר" in text or "לקנות" in text:
        return "sale"
    if "שכירות" in text or "לשכור" in text or "להשכיר" in text:
        return "rent"
    return None


def parse_area(text):
    """Extract square meters."""
    m = AREA_RE.search(text)
    return float(m.group(1)) if m else None


def parse_floor(text):
    """Extract floor number."""
    m = FLOOR_RE.search(text)
    return int(m.group(1)) if m else None


def is_spam(text):
    """Check if post is spam."""
    return bool(SPAM_RE.search(text))


def extract_lead(post):
    """Parse a single Facebook post into a lead record (or None)."""
    text = post.get("text", "").strip()
    if not text or len(text) < 10:
        return None
    if is_spam(text):
        return None

    price, is_monthly = parse_price(text)
    rooms = parse_rooms(text)
    city = parse_city(text)
    phone = parse_phone(text)
    tx_type = parse_transaction_type(text)
    area = parse_area(text)
    floor = parse_floor(text)

    # Must have at least one strong signal
    if not any([price, rooms, city, phone]):
        return None

    # Scoring: how confident we are this is a real estate post
    signals = sum(1 for s in [price, rooms, city, tx_type] if s is not None)
    if signals < 2:
        return None

    return {
        "source": "facebook",
        "author": post.get("author", ""),
        "text": text[:500],
        "fb_id": post.get("id", ""),
        "ts": post.get("ts", ""),
        "extracted": {
            "price": price,
            "price_monthly": is_monthly,
            "rooms": rooms,
            "city": city,
            "phone": phone,
            "transaction_type": tx_type,
            "area_sqm": area,
            "floor": floor,
        },
        "signals": signals,
    }


def normalize_post(post):
    """Normalize Apify or mock post format to internal shape {author, text, id, ts}."""
    return {
        "author": post.get("user", {}).get("name") or post.get("author") or post.get("user.name", ""),
        "text": post.get("text", ""),
        "id": post.get("url") or post.get("id") or post.get("fb_id", ""),
        "ts": post.get("time") or post.get("ts", ""),
    }


def load_posts_from_file(path):
    """Load posts from JSON file, auto-detect format (mock or Apify dataset)."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    raw = data.get("posts") or data
    if not isinstance(raw, list):
        raw = [raw]
    return [normalize_post(p) for p in raw]


def scrape_facebook_group(group_url, apify_token, limit=50):
    """Run Apify Facebook Groups scraper and return parsed posts."""
    print(f"  Launching Apify scraper for {group_url}…")

    # Start run
    run_input = {
        "groups": [{"url": group_url}],
        "resultsLimit": limit,
        "maxPosts": limit,
    }
    req = urllib.request.Request(
        f"{APIFY_API}/acts/{FB_SCRAPER_ACTOR}/runs",
        data=json.dumps(run_input).encode("utf-8"),
        method="POST",
    )
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {apify_token}")
    req.add_header("User-Agent", "matchi-icm/1.0")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            run_data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        raise RuntimeError(f"Apify API error {e.code}: {body}")

    run_id = run_data["data"]["id"]
    print(f"  Run ID: {run_id} — waiting for completion…")

    # Poll for completion (max 120s)
    for _ in range(24):
        time.sleep(5)
        req = urllib.request.Request(
            f"{APIFY_API}/acts/{FB_SCRAPER_ACTOR}/runs/{run_id}",
            method="GET",
        )
        req.add_header("Authorization", f"Bearer {apify_token}")
        req.add_header("User-Agent", "matchi-icm/1.0")
        with urllib.request.urlopen(req, timeout=30) as resp:
            status_data = json.loads(resp.read().decode())
        status = status_data["data"]["status"]
        if status in ("SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"):
            break
        print(f"    …{status}")

    if status != "SUCCEEDED":
        raise RuntimeError(f"Apify run {status}: {status_data['data'].get('statusMessage', '')}")

    # Fetch dataset
    dataset_id = status_data["data"]["defaultDatasetId"]
    print(f"  Dataset: {dataset_id} — fetching items…")
    req = urllib.request.Request(
        f"{APIFY_API}/datasets/{dataset_id}/items?clean=true",
        method="GET",
    )
    req.add_header("Authorization", f"Bearer {apify_token}")
    req.add_header("User-Agent", "matchi-icm/1.0")
    with urllib.request.urlopen(req, timeout=30) as resp:
        items = json.loads(resp.read().decode())

    print(f"  Got {len(items)} posts from Apify")
    return items


def dedupe_against_mcp(lead, existing_leads):
    """Check if lead already exists in MCP by phone or author match."""
    phone = lead["extracted"].get("phone")
    author = lead.get("author", "")
    text = lead.get("text", "")

    for existing in existing_leads:
        # Phone match
        if phone and existing.get("phone") == phone:
            return True, existing.get("id", "?")
        # Author name match (same person, different posts)
        if author and existing.get("full_name", "") == author:
            return True, existing.get("id", "?")
        # Text similarity (same post)
        if text[:50] in (existing.get("raw_description", "") or ""):
            return True, existing.get("id", "?")

    return False, None


def load_existing_from_mcp(c):
    """Load existing leads + potential properties from MCP for dedup."""
    # Load leads
    try:
        leads = c.call("list_leads", {"user_id": c.user_id, "limit": 200})
    except Exception:
        leads = []

    # Load potential properties
    try:
        raw = c.call("get_potential_property_details", {"user_id": c.user_id})
    except Exception:
        raw = []

    all_existing = list(leads)
    if isinstance(raw, list):
        all_existing.extend(raw)
    elif isinstance(raw, dict):
        all_existing.append(raw)

    return all_existing


def main():
    ap = argparse.ArgumentParser()
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--fb-group-url", help="Facebook group URL to scrape")
    src.add_argument("--raw-json", help="Path to pre-scraped JSON (mock or Apify output)")
    ap.add_argument("--user", default=DEFAULT_USER)
    ap.add_argument("--write", action="store_true", help="commit new leads to prod DB")
    ap.add_argument("--apify-token", help="Apify API token (or set APIFY_TOKEN env)")
    ap.add_argument("--limit", type=int, default=30, help="Max posts to scrape")
    args = ap.parse_args()

    t0 = time.time()
    print(f"Facebook Scan — {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # 1. Get posts
    if args.fb_group_url:
        token = args.apify_token or os.environ.get("APIFY_TOKEN")
        if not token:
            print("ERROR: --apify-token required (or set APIFY_TOKEN env)")
            print("  Without token, use --raw-json with pre-scraped data.")
            sys.exit(1)
        try:
            posts = scrape_facebook_group(args.fb_group_url, token, args.limit)
        except Exception as e:
            print(f"Apify scrape failed: {e}")
            sys.exit(1)
    else:
        raw_path = Path(args.raw_json)
        if not raw_path.exists():
            print(f"File not found: {raw_path}")
            sys.exit(1)
        posts = load_posts_from_file(raw_path)
        print(f"Loaded {len(posts)} posts from {raw_path}")

    # 2. Extract
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    leads = []
    for post in posts:
        lead = extract_lead(post)
        if lead:
            leads.append(lead)

    print(f"\nExtracted {len(leads)} real-estate leads from {len(posts)} posts:")
    for l in leads:
        e = l["extracted"]
        price_str = f"₪{e['price']:,}" if e.get('price') else "?₪"
        area_str = f"{e['area_sqm']}m²" if e.get('area_sqm') else "?m²"
        rooms_str = f"{e['rooms']}R" if e.get('rooms') else "?R"
        print(f"  {l['author']}: "
              f"{rooms_str}, {area_str}, "
              f"{price_str} {'/mo' if e.get('price_monthly') else ''}"
              f" — {e.get('city') or '?'} "
              f"📞{e.get('phone') or '—'}")

    if not leads:
        print("No leads to process. Done.")
        return

    # Save extracted
    (OUT_DIR / "extracted.json").write_text(
        json.dumps(leads, ensure_ascii=False, indent=2), encoding="utf-8")

    # 3. Connect to MCP for dedup
    print(f"\nConnecting to MCP for dedup…")
    c = MCPClient(user_id=args.user)
    existing = load_existing_from_mcp(c)
    print(f"  {len(existing)} existing leads/properties in MCP")

    # 4. Dedupe + write
    new_count = 0
    dup_count = 0
    results = []

    for lead in leads:
        is_dup, dup_id = dedupe_against_mcp(lead, existing)
        entry = {
            "author": lead["author"],
            "extracted": lead["extracted"],
            "is_duplicate": is_dup,
            "duplicate_of": dup_id,
            "written": False,
        }

        if is_dup:
            print(f"  DUP: {lead['author']} — matches existing #{dup_id}")
            dup_count += 1
            results.append(entry)
            continue

        print(f"  NEW: {lead['author']} — {lead['text'][:80]}…", end="")
        new_count += 1

        if args.write:
            try:
                e = lead["extracted"]
                c.call("add_new_potential_property", {
                    "user_id": c.user_id,
                    "source": "facebook",
                    "raw_description": lead["text"],
                    "contact_name": lead["author"],
                    "phone": e.get("phone") or "",
                    "city": e.get("city") or "",
                    "rooms": e.get("rooms"),
                    "price": e.get("price"),
                    "transaction_type": e.get("transaction_type") or "",
                    "area_sqm": e.get("area_sqm"),
                })
                entry["written"] = True
                print(" [written]")
            except Exception as e:
                print(f" [FAIL: {e}]")
        else:
            print("")

        results.append(entry)

    # 5. Save results
    (OUT_DIR / "scan-results.json").write_text(json.dumps({
        "stats": {"total_posts": len(posts), "extracted": len(leads),
                  "new": new_count, "duplicates": dup_count},
        "results": results,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    elapsed = time.time() - t0
    print(f"\n{'='*50}")
    print(f"Scan: {len(posts)} posts → {len(leads)} leads → "
          f"{new_count} new, {dup_count} dup")
    print(f"Elapsed: {elapsed:.1f}s")

    if not args.write:
        print("(dry-run — no DB writes. Re-run with --write to commit.)")


if __name__ == "__main__":
    main()
