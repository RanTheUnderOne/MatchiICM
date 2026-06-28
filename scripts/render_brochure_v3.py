"""
ICM brochure/03-layout v3 — Canvas Design / Museum Quality
Philosophy: "Mediterranean Threshold" — the property as aperture, not advertisement.
Golden ratio divider, museum frame, price as ultra-thin typographic statement.
"""
import json, base64
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


def build_html(prop, agent, hero_b64, portrait_b64):
    price_num = f"{prop['asking_price']:,}"
    currency_lbl = "לחודש" if prop["transaction_type"] == "rent" else "למכירה"
    sqm_price = round(prop["asking_price"] / prop["size_sqm"])

    hero_css = f"background-image: url('{hero_b64}');" if hero_b64 else "background: #0D2B3E;"

    portrait_html = ""
    if portrait_b64:
        portrait_html = f'<img class="agent-photo" src="{portrait_b64}" alt="">'

    three_specs = [
        (str(prop["rooms"]),     "חדרים"),
        (f"{prop['size_sqm']}", "מ״ר"),
        (f"₪{sqm_price:,}",     "למ״ר"),
    ]
    specs_html = "\n".join(
        f"""<div class="spec-item">
          <div class="spec-num">{v}</div>
          <div class="spec-lbl">{k}</div>
        </div>"""
        for v, k in three_specs
    )

    return f"""<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@100;300;400;900&display=swap" rel="stylesheet">
<style>
*, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
  font-family: 'Heebo', 'Segoe UI', Arial, sans-serif;
  direction: rtl;
  background: #F9F7F4;
  color: #0D2B3E;
  width: 210mm;
  min-height: 297mm;
  position: relative;
}}

/* ── MUSEUM FRAME — the outer margin is the design ── */
.canvas {{
  position: relative;
  margin: 14mm;
  min-height: calc(297mm - 28mm);
  display: flex;
  flex-direction: column;
  border: 1px solid #E2DDD6;
}}

/* ── HEADER — ultra-minimal ── */
.canvas-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 18px;
  background: #F9F7F4;
}}
.agency-id {{
  font-size: 9px;
  font-weight: 900;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: #0D2B3E;
}}
.prop-id {{
  font-size: 9px;
  font-weight: 100;
  color: #9BA8B0;
  letter-spacing: 2px;
}}

/* ── HERO IMAGE — aperture, not photo ── */
.hero {{
  position: relative;
  height: 172mm;     /* ~61.8% of inner canvas height — golden ratio */
  {hero_css}
  background-size: cover;
  background-position: center top;
  flex-shrink: 0;
}}
.hero-vignette {{
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    rgba(13,43,62,0.04) 0%,
    rgba(13,43,62,0.0) 40%,
    rgba(13,43,62,0.55) 100%
  );
}}
/* Top-left label on image */
.hero-label {{
  position: absolute;
  top: 16px;
  right: 18px;
  background: rgba(249,247,244,0.92);
  padding: 4px 12px;
  font-size: 9px;
  font-weight: 900;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: #0D2B3E;
}}
/* City tag bottom-right */
.hero-city {{
  position: absolute;
  bottom: 18px;
  left: 18px;
  color: rgba(249,247,244,0.7);
  font-size: 10px;
  font-weight: 300;
  letter-spacing: 1.5px;
}}

/* ── GOLDEN RULE — signature element ── */
.golden-rule {{
  height: 2px;
  background: #C9A96E;
  flex-shrink: 0;
}}

/* ── LOWER SECTION ── */
.lower {{
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 0;
  background: #F9F7F4;
}}

/* Price row */
.price-row {{
  display: flex;
  align-items: flex-end;
  padding: 20px 20px 0;
  gap: 10px;
  border-bottom: 1px solid #E8E4DF;
  padding-bottom: 16px;
}}
.price-currency-lbl {{
  font-size: 9px;
  font-weight: 900;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: #C9A96E;
  padding-bottom: 11px;
  flex-shrink: 0;
}}
.price-number {{
  font-size: 64px;
  font-weight: 100;       /* ultra-thin — statement */
  color: #0D2B3E;
  letter-spacing: -2px;
  line-height: 1;
  flex: 1;
}}
.price-shekel {{
  font-size: 18px;
  font-weight: 100;
  color: #9BA8B0;
  padding-bottom: 10px;
}}

/* Title + address */
.title-row {{
  padding: 16px 20px 0;
}}
.prop-title {{
  font-size: 18px;
  font-weight: 900;
  color: #0D2B3E;
  line-height: 1.2;
  letter-spacing: -0.3px;
}}
.prop-address {{
  font-size: 11px;
  font-weight: 300;
  color: #7B9E87;
  margin-top: 4px;
  letter-spacing: 0.5px;
}}

/* Specs — 3 numbers, no icons */
.specs-row {{
  display: flex;
  gap: 0;
  padding: 16px 20px 16px;
  border-top: 1px solid #E8E4DF;
  margin-top: 16px;
}}
.spec-item {{
  flex: 1;
  text-align: center;
  border-left: 1px solid #E8E4DF;
  padding: 0 12px;
}}
.spec-item:last-child {{ border-left: none; }}
.spec-num {{
  font-size: 26px;
  font-weight: 900;
  color: #0D2B3E;
  line-height: 1;
}}
.spec-lbl {{
  font-size: 9px;
  font-weight: 300;
  color: #9BA8B0;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  margin-top: 3px;
}}

/* ── AGENT FOOTER — minimal, ground level ── */
.agent-footer {{
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 20px;
  background: #0D2B3E;
  margin-top: auto;
}}
.agent-photo {{
  width: 44px;
  height: 44px;
  border-radius: 50%;
  object-fit: cover;
  border: 1.5px solid #C9A96E;
  flex-shrink: 0;
  filter: grayscale(20%);
}}
.agent-name {{
  color: #F9F7F4;
  font-size: 14px;
  font-weight: 900;
  letter-spacing: 0.3px;
}}
.agent-sub {{
  color: #C9A96E;
  font-size: 9px;
  font-weight: 300;
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-top: 2px;
}}
.agent-contact {{
  margin-right: auto;
  text-align: left;
  color: rgba(249,247,244,0.5);
  font-size: 10px;
  font-weight: 300;
  line-height: 1.7;
  letter-spacing: 0.3px;
}}

/* ── OUTER FRAME LABEL ── */
.frame-date {{
  position: absolute;
  bottom: 8mm;
  left: 0;
  right: 0;
  text-align: center;
  font-size: 8px;
  font-weight: 100;
  color: #BDB8B1;
  letter-spacing: 2px;
}}
</style>
</head>
<body>

<div class="canvas">

  <!-- Header -->
  <div class="canvas-header">
    <span class="agency-id">{agent['agency']}</span>
    <span class="prop-id">{prop['id']} · {currency_lbl}</span>
  </div>

  <!-- Hero aperture -->
  <div class="hero">
    <div class="hero-vignette"></div>
    <div class="hero-label">{'נכס למכירה' if prop['transaction_type'] == 'sale' else 'להשכרה'}</div>
    <div class="hero-city">{prop['neighborhood']} · {prop['city']}</div>
  </div>

  <!-- Golden ratio rule -->
  <div class="golden-rule"></div>

  <!-- Lower canvas -->
  <div class="lower">

    <!-- Price as typographic statement -->
    <div class="price-row">
      <div class="price-number">{price_num}</div>
      <div class="price-shekel">₪</div>
      <div class="price-currency-lbl">{currency_lbl}</div>
    </div>

    <!-- Title -->
    <div class="title-row">
      <div class="prop-title">{prop['title']}</div>
      <div class="prop-address">📍 {prop['address']}, {prop['neighborhood']}</div>
    </div>

    <!-- 3 specs only -->
    <div class="specs-row">
{specs_html}
    </div>

    <!-- Agent band -->
    <div class="agent-footer">
      {portrait_html}
      <div>
        <div class="agent-name">{agent['full_name']}</div>
        <div class="agent-sub">{agent['title']}</div>
      </div>
      <div class="agent-contact">
        {agent['phone']}<br>{agent['email']}
      </div>
    </div>

  </div>

</div>

<div class="frame-date">{agent['agency']} · {datetime.now().strftime('%Y')} · {agent['license']}</div>

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
    props    = json.loads((ROOT / "_mock/properties.json").read_text(encoding="utf-8"))["properties"]
    agent    = json.loads((ROOT / "_mock/agent.json").read_text(encoding="utf-8"))["agent"]

    hero_b64     = b64img(ROOT / "phases/2-marketing/photo-enhance/03-stage/output/staged-living-v1-modern.png")
    portrait_b64 = b64img(ROOT / "phases/1-exclusivity/agent-profile/03-portrait/output/portrait-v1-studio.png")

    for prop in props:
        pid = prop["id"]
        print(f"Rendering v3 {pid} — {prop['title']}...")
        html = build_html(prop, agent, hero_b64, portrait_b64)
        out = ROOT / f"phases/2-marketing/brochure/03-layout/output/brochure-v3-{pid}.pdf"
        render(html, out)
        print(f"  OK → {out}  ({out.stat().st_size:,} bytes)")

    print("Done.")
