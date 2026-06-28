"""
Feasibility test — OpenAI image gen + WeasyPrint PDF.
Replaces Higgsfield for image generation + PDF rendering in MatchiICM.
"""
import os, json, base64, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def test_openai_image():
    """Generate agent portrait via OpenAI GPT Image 2."""
    from openai import OpenAI

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
    if not client.api_key:
        print("FAIL: OPENAI_API_KEY not set in env")
        return None

    print("[1/3] Generating agent portrait via gpt-image-2...")
    try:
        response = client.images.generate(
            model="gpt-image-2",
            prompt=(
                "Professional real estate agent headshot, female, age 35-45, "
                "dark hair, warm smile, white blouse, clean studio background, "
                "soft lighting, head and shoulders, 1024x1024, photorealistic"
            ),
            n=1,
            size="1024x1024",
            response_format="b64_json",
        )
        img_b64 = response.data[0].b64_json
        out_path = ROOT / "scripts" / "test_output" / "test_portrait.png"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(base64.b64decode(img_b64))
        print(f"  OK → {(out_path)}  ({out_path.stat().st_size} bytes)")
        return out_path
    except Exception as e:
        print(f"  FAIL: {e}")
        return None


def test_weasyprint_pdf():
    """Generate Hebrew brochure PDF via WeasyPrint."""
    from markdown import markdown
    from weasyprint import HTML

    print("[2/3] Generating Hebrew brochure PDF...")

    md_brochure = """\
# דירת 4 חדרים בחיפה — רחוב מוריה 12

<div dir="rtl" style="direction: rtl; text-align: right; font-family: Arial, sans-serif;">

## פרטי הנכס

| פרט | ערך |
|-----|------|
| **כתובת** | מוריה 12, חיפה |
| **חדרים** | 4 |
| **קומה** | 3 מתוך 5 |
| **שטח** | 110 מ"ר |
| **מחיר** | 1,750,000 ₪ |
| **מרפסת** | שמש, 12 מ"ר |

## תיאור

דירה מוארת ומשופצת בלב שכונת אחוזה. סלון מרווח, מטבח מעוצב,
מזגנים בכל החדרים, חניה צמודה. קרוב לגנים, בתי ספר ותחבורה ציבורית.

## פרטי הסוכן

**דנה לוי** | סוכנת נדל"ן בכירה | לוי נכסים
📞 050-1234567 | 📧 dana@levi-nadlan.co.il

</div>
"""
    html = f"""\
<!DOCTYPE html>
<html dir="rtl" lang="he">
<head><meta charset="utf-8">
<style>
body {{ direction: rtl; font-family: Arial, sans-serif; max-width: 700px; margin: 40px auto; }}
h1 {{ text-align: center; color: #1a365d; }}
h2 {{ color: #2d3748; border-bottom: 2px solid #ed8936; padding-bottom: 4px; }}
table {{ width: 100%; border-collapse: collapse; margin: 12px 0; }}
td, th {{ border: 1px solid #cbd5e0; padding: 8px 12px; text-align: right; }}
th {{ background: #edf2f7; }}
</style></head>
<body>
{markdown(md_brochure, extensions=["extra", "tables"])}
</body>
</html>"""

    try:
        out_path = ROOT / "scripts" / "test_output" / "test_brochure.pdf"
        HTML(string=html).write_pdf(str(out_path))
        print(f"  OK → {out_path}  ({out_path.stat().st_size} bytes)")
        return out_path
    except Exception as e:
        print(f"  FAIL: {e}")
        return None


if __name__ == "__main__":
    print("=" * 50)
    print("MatchiICM Feasibility Test")
    print("=" * 50)

    results = {}
    results["image"] = test_openai_image()
    results["pdf"] = test_weasyprint_pdf()

    print()
    print("[3/3] Summary:")
    for k, v in results.items():
        status = "✅ PASS" if v else "❌ FAIL"
        path = v if v else "—"
        print(f"  {status} | {k}: {path}")

    all_pass = all(results.values())
    print(f"\n{'ALL PASS' if all_pass else 'SOME FAILED'}")
    sys.exit(0 if all_pass else 1)
