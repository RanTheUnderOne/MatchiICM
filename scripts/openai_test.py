#!/usr/bin/env python3
"""Quick test — OpenAI GPT Image 2 generation."""
import urllib.request, json, os, sys, time, base64

API_KEY = os.environ.get("OPENAI_API_KEY", "")
if not API_KEY:
    print("Set OPENAI_API_KEY env var")
    sys.exit(1)

def generate(prompt, output_name):
    payload = json.dumps({
        "model": "gpt-image-2",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024",
    }).encode()

    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=payload,
        headers={"Authorization": f"Bearer {API_KEY}",
                 "Content-Type": "application/json"},
        method="POST"
    )

    t0 = time.time()
    resp = urllib.request.urlopen(req, timeout=120)
    r = json.loads(resp.read())
    elapsed = time.time() - t0

    if "data" in r:
        data = r["data"][0]
        os.makedirs("_test_output", exist_ok=True)
        # gpt-image-2 returns b64_json by default
        if data.get("b64_json"):
            img_bytes = base64.b64decode(data["b64_json"])
            path = f"_test_output/{output_name}.png"
            with open(path, "wb") as f:
                f.write(img_bytes)
            size_kb = len(img_bytes) / 1024
            print(f"OK ({elapsed:.1f}s): {path} ({size_kb:.0f} KB)")
        elif data.get("url"):
            print(f"OK ({elapsed:.1f}s): {data['url']}")
        return True
    else:
        print(f"ERR: {json.dumps(r, indent=2)[:500]}")
        return False

if __name__ == "__main__":
    print("Test 1: Agent headshot...")
    generate(
        "Professional real estate agent headshot, business attire, "
        "clean neutral gray background, soft studio lighting, confident expression, "
        "portrait photography style",
        "agent-headshot"
    )
    print("Test 2: Staged living room...")
    generate(
        "Professional real estate photo, bright modern living room, "
        "virtual home staging with elegant contemporary furniture, "
        "neutral beige palette, natural daylight, wide angle lens, photorealistic, "
        "no people, no text no watermark",
        "staged-living-room"
    )
    print("Done.")
