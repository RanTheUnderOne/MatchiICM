"""
POC Runner — Real ICM stages with OpenAI images + WeasyPrint PDFs.
Follows ICM pattern: read inputs → process → write outputs → human gate.
"""
import os, json, base64, sys, subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent

# ── Helpers ──────────────────────────────────────────────

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def save_json(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_image(b64_data, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(base64.b64decode(b64_data))
    return path

def openai_client():
    from openai import OpenAI
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))

def generate_image(client, prompt, size="1024x1024", n=1):
    """Call gpt-image-2 and return list of b64 strings.
    gpt-image models always return b64_json — no response_format param."""
    response = client.images.generate(
        model="gpt-image-2",
        prompt=prompt,
        n=n,
        size=size,
    )
    return [d.b64_json for d in response.data]

def stage_header(stage_path, name):
    print(f"\n{'='*60}")
    print(f"  {stage_path}")
    print(f"  {name}")
    print(f"{'='*60}")

# ── Stage 1: agent-profile/03-portrait ──────────────────

def stage_portrait(client):
    """Generate real agent portrait. ICM: agent-profile/03-portrait"""
    stage = "phases/1-exclusivity/agent-profile/03-portrait"
    stage_header(stage, "Agent Portrait — gpt-image-2")

    # Read inputs (mock soul-id, voice config)
    agent = load_json(ROOT / "_mock/agent.json")["agent"]
    voice = (ROOT / "_config/voice.md").read_text(encoding="utf-8")

    print(f"  Agent: {agent['full_name']}")
    print(f"  Soul ID: {agent['soul_id']} (mock — no face reference)")

    prompts = [
        # Variant A: Studio headshot
        (
            "v1-studio",
            "Professional real estate agent headshot, female, age 35, "
            "dark brown hair pulled back, warm confident smile, "
            "navy blue blazer over white blouse, "
            "clean studio background with soft gradient lighting, "
            "head and shoulders portrait, photorealistic, "
            "Canon EOS R5, 85mm f/1.2, soft bokeh"
        ),
        # Variant B: Office context
        (
            "v2-office",
            "Professional real estate agent in modern office, female, age 35, "
            "dark hair, warm smile, navy blue blazer, "
            "sitting at a minimalist desk, laptop visible, "
            "branded background with subtle real estate elements, "
            "natural window light from the side, photorealistic, "
            "editorial portrait style"
        ),
        # Variant C: Outdoor/urban
        (
            "v3-outdoor",
            "Professional female real estate agent, age 35, "
            "dark hair, confident expression, casual-professional attire, "
            "standing in front of a modern apartment building in Haifa, "
            "golden hour warm sunlight, Mediterranean trees in background, "
            "full upper body, photorealistic, editorial quality"
        ),
    ]

    results = []
    for variant_id, prompt in prompts:
        print(f"\n  Generating {variant_id}...")
        try:
            imgs = generate_image(client, prompt, "1024x1024")
            out_path = ROOT / stage / "output" / f"portrait-{variant_id}.png"
            save_image(imgs[0], out_path)
            print(f"    OK → {out_path}  ({out_path.stat().st_size} bytes)")
            results.append({
                "variant": variant_id,
                "prompt": prompt,
                "image_path": str(out_path.relative_to(ROOT)),
                "status": "generated"
            })
        except Exception as e:
            print(f"    FAIL: {e}")
            results.append({"variant": variant_id, "error": str(e), "status": "failed"})

    # Write ICM output
    portrait_output = {
        "stage": "03-portrait",
        "run_at": datetime.now().isoformat(),
        "agent": agent["full_name"],
        "variants": results
    }
    save_json(portrait_output, ROOT / stage / "output" / "portrait.json")
    print(f"\n  Output: {stage}/output/portrait.json")
    return results

# ── Stage 2: photo-enhance/03-stage ──────────────────────

def stage_staging(client):
    """Generate virtual staging image. ICM: photo-enhance/03-stage"""
    stage = "phases/2-marketing/photo-enhance/03-stage"
    stage_header(stage, "Virtual Staging — gpt-image-2")

    voice = (ROOT / "_config/voice.md").read_text(encoding="utf-8")
    colors = {"primary": "#1B4965", "accent": "#62B6CB"}

    # We stage the empty room (ph-4 from props.json P-1001)
    prompts = [
        (
            "v1-modern",
            "Empty living room, 4x5 meters, white walls, light wood floor, "
            "large window on the left letting in natural light, "
            "virtually staged with: modern gray L-shaped sofa, glass coffee table, "
            "a few decorative cushions in deep blue (#1B4965), "
            "abstract wall art with cyan accents (#62B6CB), "
            "indoor plant in corner, minimalist floor lamp, "
            "warm and inviting atmosphere, photorealistic interior rendering, "
            "real estate photography style, 1024x1024"
        ),
        (
            "v2-family",
            "Medium living room with white walls and wood-look tiles, "
            "window facing garden view, "
            "virtually staged with: comfortable beige fabric sofa, "
            "wooden dining table with 4 chairs visible in open-plan area, "
            "deep blue (#1B4965) accent wall on one side, "
            "family-friendly decor, children's art frames on wall, "
            "warm ambient lighting, photorealistic interior, "
            "real estate listing photography"
        ),
    ]

    results = []
    for variant_id, prompt in prompts:
        print(f"\n  Generating {variant_id}...")
        try:
            imgs = generate_image(client, prompt, "1024x1024")
            out_path = ROOT / stage / "output" / f"staged-living-{variant_id}.png"
            save_image(imgs[0], out_path)
            print(f"    OK → {out_path}  ({out_path.stat().st_size} bytes)")
            results.append({
                "variant": variant_id,
                "photo_id": "ph-4",
                "room": "living",
                "prompt": prompt,
                "image_path": str(out_path.relative_to(ROOT)),
                "status": "staged"
            })
        except Exception as e:
            print(f"    FAIL: {e}")
            results.append({"variant": variant_id, "error": str(e), "status": "failed"})

    staged_output = {
        "stage": "03-stage",
        "run_at": datetime.now().isoformat(),
        "property_id": "P-1001",
        "variants": results
    }
    save_json(staged_output, ROOT / stage / "output" / "staged.json")
    print(f"\n  Output: {stage}/output/staged.json")
    return results

# ── Stage 3: brochure/03-layout ─────────────────────────

def stage_brochure():
    """Generate Hebrew PDF brochures via WeasyPrint. ICM: brochure/03-layout"""
    stage = "phases/2-marketing/brochure/03-layout"
    stage_header(stage, "Brochure PDF — WeasyPrint")

    from markdown import markdown
    from playwright.sync_api import sync_playwright

    # Properties for brochures
    properties = load_json(ROOT / "_mock/properties.json")["properties"]
    agent = load_json(ROOT / "_mock/agent.json")["agent"]

    brochure_props = [p for p in properties if p["id"] in ("P-1001", "P-1003")]

    results = []
    for prop in brochure_props:
        variant_id = prop["id"]
        print(f"\n  Rendering brochure for {variant_id} — {prop['title']}")

        price_fmt = f"{prop['asking_price']:,}".replace(",", ",")
        if prop["transaction_type"] == "rent":
            price_str = f"{price_fmt} ₪/חודש"
        else:
            price_str = f"{price_fmt} ₪"

        md = f"""\
# {prop['title']}

<div dir="rtl" style="direction: rtl; text-align: right; font-family: Arial, sans-serif;">

## פרטי הנכס

| פרט | ערך |
|-----|------|
| **כתובת** | {prop['address']}, {prop['city']} |
| **שכונה** | {prop['neighborhood']} |
| **חדרים** | {prop['rooms']} |
| **שטח** | {prop['size_sqm']} מ"ר |
| **קומה** | {prop['floor']} מתוך {prop['total_floors']} |
| **מחיר** | {price_str} |
| **מרפסת** | {"כן" if prop.get("balcony") else "לא"} |
| **חניה** | {"כן" if prop.get("parking") else "לא"} |
| **מעלית** | {"כן" if prop.get("elevator") else "לא"} |
| **משופץ** | {"כן" if prop.get("renovated") else "לא"} |
| **ארנונה** | {prop['arnona_monthly']} ₪/חודש |
| **ימים בשוק** | {prop['days_on_market']} |

## תיאור

{prop['title']} — דירה {"משופצת ומוארת" if prop.get("renovated") else "במצב שמור"} בלב שכונת {prop['neighborhood']}.
{"מרפסת שמש," if prop.get("balcony") else ""}
{"חניה צמודה," if prop.get("parking") else ""}
{"מעלית," if prop.get("elevator") else ""}
קרוב לגנים, בתי ספר ותחבורה ציבורית.

## פרטי יצירת קשר

**{agent['full_name']}** | {agent['title']} | {agent['agency']}
📞 {agent['phone']} | 📧 {agent['email']}
רשיון: {agent['license']}

</div>
"""
        html = f"""\
<!DOCTYPE html>
<html dir="rtl" lang="he">
<head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400;600;700&display=swap');
body {{
    direction: rtl;
    font-family: 'Rubik', Arial, sans-serif;
    max-width: 210mm;
    margin: 0 auto;
    padding: 20px;
    color: #1a202c;
}}
h1 {{
    text-align: center;
    color: #1B4965;
    font-size: 24px;
    border-bottom: 3px solid #62B6CB;
    padding-bottom: 12px;
    margin-bottom: 24px;
}}
h2 {{
    color: #1B4965;
    font-size: 18px;
    border-right: 4px solid #62B6CB;
    padding-right: 12px;
    margin-top: 24px;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0;
}}
td, th {{
    border: 1px solid #cbd5e0;
    padding: 8px 12px;
    text-align: right;
}}
td:first-child {{
    background: #edf2f7;
    font-weight: bold;
    width: 30%;
}}
</style></head>
<body>
{markdown(md, extensions=["extra", "tables"])}
</body>
</html>"""
        try:
            out_path = ROOT / stage / "output" / f"brochure-{variant_id}.pdf"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.set_content(html, wait_until="networkidle")
                page.pdf(path=str(out_path), format="A4",
                         print_background=True,
                         margin={"top": "10mm", "bottom": "10mm",
                                 "left": "10mm", "right": "10mm"})
                browser.close()
            print(f"    OK → {out_path}  ({out_path.stat().st_size} bytes)")
            results.append({
                "property_id": variant_id,
                "pdf_path": str(out_path.relative_to(ROOT)),
                "status": "rendered"
            })
        except Exception as e:
            print(f"    FAIL: {e}")
            results.append({"property_id": variant_id, "error": str(e), "status": "failed"})

    brochure_output = {
        "stage": "03-layout",
        "run_at": datetime.now().isoformat(),
        "brochures": results
    }
    save_json(brochure_output, ROOT / stage / "output" / "brochure.json")
    print(f"\n  Output: {stage}/output/brochure.json")
    return results

# ── Stage 4: social-posts/02-generate ────────────────────

def stage_social(client):
    """Generate social post images. ICM: social-posts/02-generate"""
    stage = "phases/2-marketing/social-posts/02-generate"
    stage_header(stage, "Social Posts — gpt-image-2")

    # Read property context for the post
    voice = (ROOT / "_config/voice.md").read_text(encoding="utf-8")

    prompts = [
        (
            "v1-fb-property",
            "Facebook real estate post image, 1200x1200 square, "
            "showing a modern renovated 4-room apartment in Haifa, "
            "bright living room with large windows, light wood flooring, "
            "minimalist decor, warm golden hour light streaming in, "
            "text overlay area in bottom third (clean space for Hebrew text), "
            "professional real estate photography, inviting atmosphere, "
            "brand colors: deep navy blue (#1B4965) and teal (#62B6CB) accents, "
            "photorealistic, warm tones"
        ),
        (
            "v2-ig-lifestyle",
            "Instagram square post 1080x1080 real estate lifestyle, "
            "couple drinking coffee on a sunny balcony overlooking Haifa bay, "
            "Mediterranean view, plants on balcony railing, "
            "warm morning light, aspirational lifestyle photography, "
            "subtle brand: navy blue (#1B4965) and cyan (#62B6CB) throw pillows, "
            "photorealistic, bright, airy, editorial quality"
        ),
    ]

    results = []
    for variant_id, prompt in prompts:
        print(f"\n  Generating {variant_id}...")
        try:
            imgs = generate_image(client, prompt, "1024x1024")
            out_path = ROOT / stage / "output" / f"social-{variant_id}.png"
            save_image(imgs[0], out_path)
            print(f"    OK → {out_path}  ({out_path.stat().st_size} bytes)")
            results.append({
                "variant": variant_id,
                "prompt": prompt,
                "image_path": str(out_path.relative_to(ROOT)),
                "status": "generated"
            })
        except Exception as e:
            print(f"    FAIL: {e}")
            results.append({"variant": variant_id, "error": str(e), "status": "failed"})

    posts_output = {
        "stage": "02-generate",
        "run_at": datetime.now().isoformat(),
        "variants": results
    }
    save_json(posts_output, ROOT / stage / "output" / "posts.json")
    print(f"\n  Output: {stage}/output/posts.json")
    return results

# ── Main ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  MatchiICM POC — Real Tools via ICM Stages")
    print(f"  {datetime.now().isoformat()}")
    print("=" * 60)

    client = openai_client()

    results = {}

    # 1. Portrait (3 variants)
    results["portrait"] = stage_portrait(client)

    # 2. Staging (2 variants)
    results["staging"] = stage_staging(client)

    # 3. Brochure PDF (2 properties)
    results["brochure"] = stage_brochure()

    # 4. Social posts (2 variants)
    results["social"] = stage_social(client)

    # Summary
    print(f"\n{'='*60}")
    print("  POC Summary")
    print(f"{'='*60}")
    total_ok = 0
    total_fail = 0
    for category, items in results.items():
        ok = sum(1 for i in items if i.get("status") in ("generated", "staged", "rendered"))
        fail = sum(1 for i in items if i.get("status") == "failed")
        total_ok += ok
        total_fail += fail
        print(f"  {category}: {ok} OK, {fail} FAIL")

    print(f"\n  Total: {total_ok} OK, {total_fail} FAIL")
    print(f"  Output dirs under phases/*/.../output/")
    sys.exit(0 if total_fail == 0 else 1)
