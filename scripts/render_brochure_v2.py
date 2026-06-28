"""
ICM brochure/03-layout v2 — Distinctive design.
Heebo Hebrew font, full-bleed hero, typographic price, dual staging images.
"""
import json, base64, sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent


def b64img(path):
    if not path or not Path(path).exists():
        return ""
    suffix = Path(path).suffix.lower().replace(".", "")
    mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png"}.get(suffix, "png")
    data = base64.b64encode(Path(path).read_bytes()).decode()
    return f"data:image/{mime};base64,{data}"


def build_html(prop, agent, hero_b64, staging_b64, portrait_b64):
    price_num = f"{prop['asking_price']:,}"
    currency = "₪/חודש" if prop["transaction_type"] == "rent" else "₪"
    sqm_price = round(prop["asking_price"] / prop["size_sqm"])

    hl_rows = [
        ("עסקה",       "מכירה" if prop["transaction_type"] == "sale" else "השכרה"),
        ("שטח נטו",    f"{prop['size_sqm']} מ″ר"),
        ("מחיר למ″ר", f"₪{sqm_price:,}"),
        ("ימים בשוק",  str(prop["days_on_market"])),
        ("עמלה",       f"{prop.get('fee_pct', 2)}%"),
        ("בלעדיות",    f"{prop.get('exclusivity_months', 3)} חודשים"),
    ]
    highlights_html = "\n".join(
        f'<div class="hl-item"><span class="hl-key">{k}</span><span class="hl-val">{v}</span></div>'
        for k, v in hl_rows
    )

    specs = [
        ("חדרים",      str(prop["rooms"])),
        ("מ״ר",        str(prop["size_sqm"])),
        ("קומה",       f"{prop['floor']}/{prop['total_floors']}"),
        ("מרפסת",      "כן" if prop.get("balcony") else "לא"),
        ("חניה",       "כן" if prop.get("parking") else "לא"),
        ("מעלית",      "כן" if prop.get("elevator") else "לא"),
        ("משופץ",      "כן" if prop.get("renovated") else "לא"),
        ("ארנונה",     f"₪{prop['arnona_monthly']}"),
    ]

    specs_cells = "\n".join(
        f"""<div class="spec-cell">
          <div class="spec-val">{v}</div>
          <div class="spec-lbl">{k}</div>
        </div>"""
        for k, v in specs
    )

    hero_css  = f"background-image: url('{hero_b64}');" if hero_b64 else "background: #1A3A52;"
    staging_section = ""
    if staging_b64:
        staging_section = f"""
        <div class="staging-wrap">
          <img class="staging-img" src="{staging_b64}" alt="הדמיית עיצוב">
          <div class="staging-note">הדמיה לצורך המחשה בלבד</div>
        </div>"""

    portrait_html = ""
    if portrait_b64:
        portrait_html = f'<img class="agent-photo" src="{portrait_b64}" alt="{agent["full_name"]}">'

    desc = (
        f"דירה {'משופצת ומוארת' if prop.get('renovated') else 'במצב שמור'} "
        f"בלב שכונת {prop['neighborhood']}. "
        f"{'מרפסת שמש עם נוף פתוח. ' if prop.get('balcony') else ''}"
        f"{'חניה צמודה. ' if prop.get('parking') else ''}"
        f"{'מעלית בבניין. ' if prop.get('elevator') else ''}"
        f"שטח {prop['size_sqm']} מ\"ר נטו, קומה {prop['floor']} מתוך {prop['total_floors']}. "
        f"קרוב לגנים, בתי ספר ותחבורה ציבורית. "
        f"מחיר למ\"ר: ₪{sqm_price:,}."
    )

    return f"""<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@200;400;700;800&display=swap" rel="stylesheet">
<style>
*, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
  font-family: 'Heebo', 'Segoe UI', Arial, sans-serif;
  direction: rtl;
  background: #FAF8F5;
  color: #1A202C;
  width: 210mm;
}}

/* ── HEADER STRIP ── */
.top-strip {{
  background: #1A3A52;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 28px;
}}
.agency {{ color: #fff; font-size: 15px; font-weight: 700; letter-spacing: 0.5px; }}
.exclusivity-badge {{
  background: #4AA9C0;
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: 2px;
  letter-spacing: 1.5px;
  text-transform: uppercase;
}}

/* ── HERO ── */
.hero {{
  position: relative;
  height: 260px;
  background-size: cover;
  background-position: center;
  {hero_css}
}}
.hero-overlay {{
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to top,
    rgba(26,58,82,0.88) 0%,
    rgba(26,58,82,0.30) 55%,
    rgba(0,0,0,0.05) 100%
  );
}}
.hero-content {{
  position: absolute;
  bottom: 0;
  right: 0;
  left: 0;
  padding: 28px 32px 24px;
}}
.hero-address {{
  color: #4AA9C0;
  font-size: 12px;
  font-weight: 400;
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-bottom: 6px;
}}
.hero-title {{
  color: #fff;
  font-size: 24px;
  font-weight: 800;
  line-height: 1.25;
  margin-bottom: 14px;
  max-width: 80%;
}}
/* Price as typographic statement */
.price-block {{
  display: flex;
  align-items: baseline;
  gap: 6px;
}}
.price-num {{
  color: #fff;
  font-size: 52px;
  font-weight: 200;   /* ultra-light — the signature tension */
  letter-spacing: -1px;
  line-height: 1;
}}
.price-currency {{
  color: #4AA9C0;
  font-size: 16px;
  font-weight: 700;
  align-self: flex-end;
  padding-bottom: 8px;
}}
.price-sqm {{
  color: rgba(255,255,255,0.55);
  font-size: 12px;
  font-weight: 400;
  align-self: flex-end;
  padding-bottom: 10px;
}}

/* ── TEAL ACCENT RULE ── */
.accent-rule {{
  height: 4px;
  background: linear-gradient(90deg, #4AA9C0 0%, #1A3A52 100%);
}}

/* ── SPECS STRIP ── */
.specs-strip {{
  background: #fff;
  display: flex;
  border-bottom: 1px solid #E2EAF0;
}}
.spec-cell {{
  flex: 1;
  padding: 14px 8px 12px;
  text-align: center;
  border-left: 1px solid #E2EAF0;
}}
.spec-cell:last-child {{ border-left: none; }}
.spec-val {{
  font-size: 20px;
  font-weight: 800;
  color: #1A3A52;
  line-height: 1;
}}
.spec-lbl {{
  font-size: 10px;
  font-weight: 400;
  color: #6B8A9E;
  margin-top: 3px;
  letter-spacing: 0.5px;
}}

/* ── BODY ── */
.body-section {{
  padding: 26px 32px 0;
}}

.section-label {{
  font-size: 10px;
  font-weight: 700;
  color: #4AA9C0;
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-bottom: 8px;
}}

.body-cols {{
  display: flex;
  gap: 28px;
  align-items: flex-start;
}}
.desc-col {{
  flex: 1.4;
}}
.desc-text {{
  font-size: 13.5px;
  font-weight: 400;
  color: #374151;
  line-height: 1.85;
}}

.highlights-col {{
  flex: 1;
  background: #EEF4F7;
  border-radius: 6px;
  padding: 16px 18px;
}}
.hl-title {{
  font-size: 11px;
  font-weight: 700;
  color: #1A3A52;
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 2px solid #4AA9C0;
}}
.hl-item {{
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  border-bottom: 1px solid rgba(74,169,192,0.15);
  font-size: 12.5px;
}}
.hl-item:last-child {{ border-bottom: none; }}
.hl-key {{ color: #6B8A9E; font-weight: 400; }}
.hl-val {{ color: #1A3A52; font-weight: 700; }}

/* ── STAGING ── */
.staging-wrap {{
  position: relative;
  margin: 24px 0 0;
}}
.staging-img {{
  width: 100%;
  height: 200px;
  object-fit: cover;
  display: block;
}}
.staging-note {{
  position: absolute;
  bottom: 0; left: 0; right: 0;
  background: rgba(26,58,82,0.75);
  color: rgba(255,255,255,0.8);
  font-size: 10px;
  text-align: center;
  padding: 5px;
  letter-spacing: 0.5px;
}}

/* ── DIVIDER ── */
.thin-divider {{
  height: 1px;
  background: #D1E3ED;
  margin: 0 32px;
}}

/* ── AGENT BAND ── */
.agent-band {{
  background: #1A3A52;
  padding: 22px 32px;
  display: flex;
  align-items: center;
  gap: 20px;
  margin-top: 24px;
}}
.agent-photo {{
  width: 72px;
  height: 72px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #4AA9C0;
  flex-shrink: 0;
}}
.agent-info {{ flex: 1; }}
.agent-name {{
  color: #fff;
  font-size: 20px;
  font-weight: 800;
  line-height: 1.1;
}}
.agent-role {{
  color: #4AA9C0;
  font-size: 11px;
  font-weight: 400;
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-top: 3px;
}}
.agent-contacts {{
  display: flex;
  gap: 20px;
  margin-top: 10px;
}}
.contact-item {{
  display: flex;
  flex-direction: column;
}}
.contact-lbl {{
  color: rgba(255,255,255,0.4);
  font-size: 9px;
  letter-spacing: 1.5px;
  text-transform: uppercase;
}}
.contact-val {{
  color: #fff;
  font-size: 13px;
  font-weight: 700;
  margin-top: 2px;
}}
.license-pill {{
  background: rgba(74,169,192,0.2);
  color: #4AA9C0;
  border: 1px solid #4AA9C0;
  border-radius: 3px;
  font-size: 10px;
  padding: 4px 10px;
  align-self: center;
  white-space: nowrap;
}}

/* ── FOOTER ── */
.footer {{
  background: #12283A;
  color: rgba(255,255,255,0.3);
  font-size: 9px;
  text-align: center;
  padding: 8px;
  letter-spacing: 0.5px;
}}
</style>
</head>
<body>

<!-- Top strip -->
<div class="top-strip">
  <span class="agency">{agent['agency']}</span>
  <span class="exclusivity-badge">בלעדיות</span>
</div>

<!-- Hero -->
<div class="hero">
  <div class="hero-overlay"></div>
  <div class="hero-content">
    <div class="hero-address">📍 {prop['address']}, {prop['neighborhood']}, {prop['city']}</div>
    <div class="hero-title">{prop['title']}</div>
    <div class="price-block">
      <div class="price-num">{price_num}</div>
      <div class="price-currency">{currency}</div>
      <div class="price-sqm">· ₪{sqm_price:,} למ״ר</div>
    </div>
  </div>
</div>

<!-- Accent rule -->
<div class="accent-rule"></div>

<!-- Specs -->
<div class="specs-strip">
{specs_cells}
</div>

<!-- Body -->
<div class="body-section">

  <div class="section-label" style="margin-top:20px;">על הנכס</div>

  <div class="body-cols">
    <div class="desc-col">
      <p class="desc-text">{desc}</p>
    </div>
    <div class="highlights-col">
      <div class="hl-title">בלטות עיקריות</div>
      {highlights_html}
    </div>
  </div>

  {staging_section}
</div>

<div class="thin-divider" style="margin-top:24px;"></div>

<!-- Agent -->
<div class="agent-band">
  {portrait_html}
  <div class="agent-info">
    <div class="agent-name">{agent['full_name']}</div>
    <div class="agent-role">{agent['title']}</div>
    <div class="agent-contacts">
      <div class="contact-item">
        <span class="contact-lbl">טלפון</span>
        <span class="contact-val">{agent['phone']}</span>
      </div>
      <div class="contact-item">
        <span class="contact-lbl">אימייל</span>
        <span class="contact-val">{agent['email']}</span>
      </div>
    </div>
  </div>
  <div class="license-pill">{agent['license']}</div>
</div>

<!-- Footer -->
<div class="footer">
  {agent['agency']} · {datetime.now().strftime('%d/%m/%Y')} · כל הפרטים כפופים לאימות ·
  הדמיות הן לצורך המחשה בלבד ואינן מחייבות
</div>

</body>
</html>"""


def render(html, out_path):
    from playwright.sync_api import sync_playwright
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 794, "height": 1123})
        page.set_content(html, wait_until="networkidle")
        page.pdf(
            path=str(out_path),
            format="A4",
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
        )
        browser.close()


if __name__ == "__main__":
    props  = json.loads((ROOT / "_mock/properties.json").read_text(encoding="utf-8"))["properties"]
    agent  = json.loads((ROOT / "_mock/agent.json").read_text(encoding="utf-8"))["agent"]

    hero_path    = ROOT / "phases/2-marketing/photo-enhance/03-stage/output/staged-living-v2-family.png"
    staging_path = ROOT / "phases/2-marketing/photo-enhance/03-stage/output/staged-living-v1-modern.png"
    portrait_path = ROOT / "phases/1-exclusivity/agent-profile/03-portrait/output/portrait-v1-studio.png"

    hero_b64    = b64img(hero_path)
    staging_b64 = b64img(staging_path)
    portrait_b64 = b64img(portrait_path)

    for prop in props:
        pid = prop["id"]
        print(f"Rendering v2 {pid}...")
        html = build_html(prop, agent, hero_b64, staging_b64, portrait_b64)
        out = ROOT / f"phases/2-marketing/brochure/03-layout/output/brochure-v2-{pid}.pdf"
        render(html, out)
        print(f"  OK → {out}  ({out.stat().st_size:,} bytes)")

    print("Done.")
