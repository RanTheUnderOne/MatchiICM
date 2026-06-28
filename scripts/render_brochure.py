"""
ICM Stage: brochure/03-layout — Professional PDF brochure
Playwright + HTML → A4 PDF with embedded images, Hebrew RTL.
"""
import json, base64, sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent


def b64img(path):
    """Embed image as base64 data URL."""
    if not path or not Path(path).exists():
        return ""
    suffix = Path(path).suffix.lower().replace(".", "")
    mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png"}.get(suffix, "png")
    data = base64.b64encode(Path(path).read_bytes()).decode()
    return f"data:image/{mime};base64,{data}"


def build_html(prop, agent, hero_img_path, staging_img_path, portrait_img_path):
    hero    = b64img(hero_img_path)
    staging = b64img(staging_img_path)
    portrait = b64img(portrait_img_path)

    price_fmt = f"{prop['asking_price']:,} ₪"
    if prop["transaction_type"] == "rent":
        price_fmt += "/חודש"

    specs = [
        ("🛏", f"{prop['rooms']} חדרים"),
        ("📐", f"{prop['size_sqm']} מ\"ר"),
        ("🏢", f"קומה {prop['floor']}/{prop['total_floors']}"),
        ("🔑", "משופץ" if prop.get("renovated") else "מקורי"),
        ("🚗", "חניה" if prop.get("parking") else "ללא חניה"),
        ("🏗", "מעלית" if prop.get("elevator") else "ללא מעלית"),
        ("🌿", "מרפסת" if prop.get("balcony") else "ללא מרפסת"),
        ("💰", f"ארנונה {prop['arnona_monthly']} ₪/חודש"),
    ]

    specs_html = "\n".join(
        f'<div class="spec"><span class="icon">{e}</span><span>{t}</span></div>'
        for e, t in specs
    )

    staging_section = ""
    if staging:
        staging_section = f"""
        <div class="section-title">הדמיית עיצוב</div>
        <div class="staging-img">
          <img src="{staging}" alt="הדמיה">
          <div class="staging-badge">הדמיה בלבד — לצורך המחשה</div>
        </div>"""

    portrait_html = ""
    if portrait:
        portrait_html = f'<img class="agent-photo" src="{portrait}" alt="{agent["full_name"]}">'

    hero_html = ""
    if hero:
        hero_html = f'<img class="hero-img" src="{hero}" alt="נכס">'
    else:
        hero_html = '<div class="hero-placeholder"></div>'

    return f"""<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
<meta charset="utf-8">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
  font-family: 'Segoe UI', Arial, sans-serif;
  direction: rtl;
  color: #1a202c;
  background: #fff;
}}

/* ── Header bar ── */
.header {{
  background: #1B4965;
  padding: 14px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}}
.agency-name {{
  color: #fff;
  font-size: 17px;
  font-weight: 700;
  letter-spacing: 0.5px;
}}
.header-tag {{
  color: #62B6CB;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
}}

/* ── Hero image ── */
.hero-img {{
  width: 100%;
  height: 240px;
  object-fit: cover;
  display: block;
}}
.hero-placeholder {{
  width: 100%;
  height: 240px;
  background: linear-gradient(135deg, #1B4965 0%, #62B6CB 100%);
}}

/* ── Price badge ── */
.price-banner {{
  background: #1B4965;
  color: #fff;
  text-align: center;
  padding: 10px;
  font-size: 26px;
  font-weight: 800;
  letter-spacing: 1px;
}}
.price-banner span {{
  color: #62B6CB;
}}

/* ── Title block ── */
.title-block {{
  padding: 20px 24px 8px;
  border-bottom: 3px solid #62B6CB;
}}
.property-title {{
  font-size: 22px;
  font-weight: 800;
  color: #1B4965;
  line-height: 1.3;
}}
.property-address {{
  font-size: 14px;
  color: #718096;
  margin-top: 4px;
}}

/* ── Specs grid ── */
.specs {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0;
  background: #f7fafc;
  border-bottom: 1px solid #e2e8f0;
}}
.spec {{
  padding: 12px 8px;
  text-align: center;
  font-size: 12px;
  color: #2d3748;
  border-left: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}}
.spec:last-child {{ border-left: none; }}
.spec .icon {{ font-size: 18px; }}

/* ── Body ── */
.body {{ padding: 20px 24px; }}

.section-title {{
  font-size: 13px;
  font-weight: 700;
  color: #62B6CB;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 8px;
  margin-top: 18px;
}}

.description {{
  font-size: 14px;
  line-height: 1.8;
  color: #4a5568;
}}

/* ── Staging image ── */
.staging-img {{
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  margin-bottom: 4px;
}}
.staging-img img {{
  width: 100%;
  height: 220px;
  object-fit: cover;
  display: block;
}}
.staging-badge {{
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(27, 73, 101, 0.85);
  color: #fff;
  font-size: 11px;
  text-align: center;
  padding: 5px;
}}

/* ── Divider ── */
.divider {{
  height: 2px;
  background: linear-gradient(90deg, #62B6CB, #1B4965, #62B6CB);
  margin: 20px 0;
  opacity: 0.3;
}}

/* ── Agent card ── */
.agent-card {{
  background: #1B4965;
  border-radius: 10px;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 16px;
}}
.agent-photo {{
  width: 68px;
  height: 68px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #62B6CB;
  flex-shrink: 0;
}}
.agent-info {{
  color: #fff;
  flex: 1;
}}
.agent-name {{
  font-size: 18px;
  font-weight: 700;
}}
.agent-title {{
  color: #62B6CB;
  font-size: 12px;
  margin-top: 2px;
}}
.agent-contacts {{
  margin-top: 8px;
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: #cbd5e0;
}}
.agent-contacts span {{ display: flex; align-items: center; gap: 4px; }}

/* ── Footer ── */
.footer {{
  background: #2d3748;
  color: #718096;
  text-align: center;
  font-size: 10px;
  padding: 8px;
  margin-top: 20px;
}}
</style>
</head>
<body>

<!-- Header -->
<div class="header">
  <div class="agency-name">{agent['agency']}</div>
  <div class="header-tag">נכס למכירה • בלעדיות</div>
</div>

<!-- Hero -->
{hero_html}

<!-- Price Banner -->
<div class="price-banner">
  <span>{price_fmt}</span>
</div>

<!-- Title -->
<div class="title-block">
  <div class="property-title">{prop['title']}</div>
  <div class="property-address">📍 {prop['address']}, {prop['neighborhood']}, {prop['city']}</div>
</div>

<!-- Specs -->
<div class="specs">
{specs_html}
</div>

<!-- Body -->
<div class="body">

  <div class="section-title">תיאור הנכס</div>
  <div class="description">
    דירה {"משופצת ומוארת" if prop.get('renovated') else "במצב שמור"} בלב שכונת {prop['neighborhood']}.
    {"מרפסת שמש ענקית עם נוף פתוח. " if prop.get('balcony') else ""}
    {"חניה צמודה. " if prop.get('parking') else ""}
    {"מעלית בבניין. " if prop.get('elevator') else ""}
    שטח {prop['size_sqm']} מ"ר נטו, קומה {prop['floor']} מתוך {prop['total_floors']}.
    קרוב לגנים, בתי ספר ותחבורה ציבורית.
    ימים בשוק: {prop['days_on_market']}.
  </div>

  {staging_section}

  <div class="divider"></div>

  <!-- Agent Card -->
  <div class="section-title">הסוכן המטפל</div>
  <div class="agent-card">
    {portrait_html}
    <div class="agent-info">
      <div class="agent-name">{agent['full_name']}</div>
      <div class="agent-title">{agent['title']} | {agent['agency']}</div>
      <div class="agent-contacts">
        <span>📞 {agent['phone']}</span>
        <span>✉ {agent['email']}</span>
        <span>🪪 {agent['license']}</span>
      </div>
    </div>
  </div>

</div>

<!-- Footer -->
<div class="footer">
  מסמך זה הופק על ידי {agent['agency']} • {datetime.now().strftime('%d/%m/%Y')} •
  כל הפרטים כפופים לאימות. אין לראות בהדמיות תיאור מדויק של הנכס.
</div>

</body>
</html>"""


def render_pdf(html, out_path):
    from playwright.sync_api import sync_playwright
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html, wait_until="networkidle")
        page.pdf(
            path=str(out_path),
            format="A4",
            print_background=True,
            margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"},
        )
        browser.close()


if __name__ == "__main__":
    props = json.loads((ROOT / "_mock/properties.json").read_text(encoding="utf-8"))["properties"]
    agent = json.loads((ROOT / "_mock/agent.json").read_text(encoding="utf-8"))["agent"]

    # Portrait path
    portrait_path = ROOT / "phases/1-exclusivity/agent-profile/03-portrait/output/portrait-v1-studio.png"

    for prop in props:
        pid = prop["id"]
        print(f"Rendering {pid}: {prop['title']}...")

        # Staging image (use generated if P-1001, else None)
        staging_path = None
        hero_path = None
        if pid == "P-1001":
            staging_path = ROOT / "phases/2-marketing/photo-enhance/03-stage/output/staged-living-v1-modern.png"
            hero_path    = ROOT / "phases/2-marketing/photo-enhance/03-stage/output/staged-living-v2-family.png"
        elif pid == "P-1003":
            staging_path = ROOT / "phases/2-marketing/photo-enhance/03-stage/output/staged-living-v1-modern.png"
            hero_path    = ROOT / "phases/2-marketing/photo-enhance/03-stage/output/staged-living-v2-family.png"

        html = build_html(prop, agent, hero_path, staging_path, portrait_path)

        out = ROOT / f"phases/2-marketing/brochure/03-layout/output/brochure-design-{pid}.pdf"
        render_pdf(html, out)
        print(f"  OK → {out}  ({out.stat().st_size:,} bytes)")

    print("\nDone.")
