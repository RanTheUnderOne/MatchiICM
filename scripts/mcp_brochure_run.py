#!/usr/bin/env python3
"""ICM brochure renderer wired to prod MCP.
Pulls property data + images from MCP, renders museum-quality v3 brochure PDF.

Usage:
  py scripts/mcp_brochure_run.py --property-id 1
  py scripts/mcp_brochure_run.py --property-id 1 --out my-brochure.pdf
  py scripts/mcp_brochure_run.py --list              # list available properties
"""
import argparse
import base64
import json
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mcp_client import MCPClient, DEFAULT_USER, parse_repr
from render_brochure_v3 import build_html, render

try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

OUT_DIR = Path(__file__).resolve().parent.parent / "phases/2-marketing/brochure/03-layout/output"
AGENT_PATH = Path(__file__).resolve().parent.parent / "_mock/agent.json"

# MCP field name → brochure engine field name
PROP_MAP = {
    "id": "id",
    "title": "title",
    "transaction_type": "transaction_type",
    "city": "city",
    "neighborhood": "neighborhood",
    "rooms": "rooms",
    "price": "asking_price",       # MCP: price, engine: asking_price
    "area_sqm": "size_sqm",        # MCP: area_sqm, engine: size_sqm
}


def download_as_b64(url):
    """Download image from URL and return as data:image/... base64 string."""
    req = urllib.request.Request(url, headers={"User-Agent": "matchi-icm/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = resp.read()
    mime = resp.headers.get("Content-Type", "image/jpeg")
    b64 = base64.b64encode(data).decode()
    return f"data:image/{mime.split('/')[-1]};base64,{b64}"


def load_agent():
    """Load agent profile from mock (no agent tool in MCP yet)."""
    if AGENT_PATH.exists():
        return json.loads(AGENT_PATH.read_text(encoding="utf-8"))["agent"]
    # fallback
    return {
        "id": "A-00", "full_name": "סוכן נדל״ן", "title": "משווק",
        "agency": "Matchi", "phone": "", "email": "",
        "license": "00000",
    }


def map_property(mcp_prop):
    """Map MCP property dict to brochure engine prop dict."""
    prop = {}
    for mcp_key, engine_key in PROP_MAP.items():
        val = mcp_prop.get(mcp_key)
        if val is not None and engine_key == "rooms":
            val = int(val)
        if val is not None:
            prop[engine_key] = val
    # address: not in MCP, synthesize
    prop["address"] = mcp_prop.get("address") or f"{mcp_prop.get('neighborhood','')}, {mcp_prop.get('city','')}"
    return prop


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--property-id", type=int, help="Property ID to render")
    ap.add_argument("--list", action="store_true", help="List available property IDs")
    ap.add_argument("--user", default=DEFAULT_USER)
    ap.add_argument("--out", help="Output PDF path (default: auto)")
    args = ap.parse_args()

    c = MCPClient(user_id=args.user)
    print(f"MCP session {c.session[:8]}… user={c.user_id}")

    if args.list:
        listing = c.call("search_real_estate_properties",
                         {"user_id": c.user_id, "limit": 50})
        # MCP returns text: "ID: 1 | [SALE] ... in city (, neighborhood) | Rooms: 4 | Price: 2,150,000"
        rows = []
        for line in listing.strip().split("\n"):
            m = re.match(r"ID:\s*(\d+)\s*\|\s*\[(\w+)\].*?in\s+(\S+)\s*\(,\s*(.*?)\)\s*\|\s*Rooms:\s*([\d.]+)\s*\|\s*Price:\s*([\d,]+)", line)
            if m:
                rows.append({
                    "id": int(m.group(1)),
                    "transaction_type": m.group(2).lower(),
                    "city": m.group(3),
                    "neighborhood": m.group(4),
                    "rooms": float(m.group(5)),
                    "price": m.group(6).replace(",", ""),
                })
        print(f"\n{len(rows)} properties:")
        for r in rows:
            price = int(float(r["price"]))
            print(f"  #{r['id']}: {r['city']}, {r['neighborhood']} "
                  f"({int(r['rooms'])} חד׳, {r['transaction_type']}, ₪{price:,})")
        return

    if not args.property_id:
        ap.error("--property-id required (or use --list)")

    pid = args.property_id

    # 1. Fetch property
    print(f"\nFetching property #{pid}…")
    raw = c.call("get_property_full_details", {"property_id": pid, "user_id": c.user_id})
    mcp_prop = parse_repr(raw) if isinstance(raw, str) else raw
    prop = map_property(mcp_prop)
    print(f"  {prop['title']} — {prop['city']}, {prop['neighborhood']} "
          f"({prop['rooms']} חד׳, {prop['size_sqm']}מ״ר, ₪{prop['asking_price']:,})")

    # 2. Fetch images
    print(f"\nFetching images…")
    imgs_raw = c.call("get_property_images", {"property_id": pid, "user_id": c.user_id})
    imgs = json.loads(imgs_raw) if isinstance(imgs_raw, str) else imgs_raw
    print(f"  {len(imgs)} image(s) found")

    hero_b64 = ""
    for img in imgs:
        url = img.get("url")
        if not url:
            continue
        print(f"  Downloading {url[:80]}…")
        try:
            b64 = download_as_b64(url)
            if img.get("is_primary") or not hero_b64:
                hero_b64 = b64  # first image = hero (or primary)
            print(f"    OK ({len(b64):,} chars)")
        except Exception as e:
            print(f"    FAIL: {e}")

    # 3. Agent
    agent = load_agent()
    print(f"  Agent: {agent['full_name']} ({agent['agency']})")

    # 4. Render
    print(f"\nRendering…")
    html = build_html(prop, agent, hero_b64, portrait_b64="")
    out_path = Path(args.out) if args.out else OUT_DIR / f"brochure-mcp-{pid}.pdf"
    render(html, out_path)
    print(f"  OK → {out_path}  ({out_path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
