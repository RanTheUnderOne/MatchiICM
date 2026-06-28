# Stage 03 — Stage

Virtually furnish empty rooms in brand style.

## Inputs
- `02-declutter/output/decluttered.json` (ALL photos with needs_staging flags)
- `_config/voice.md` (brand palette, mood)

## Process (OpenAI `images.edit`)
Endpoint: `POST https://api.openai.com/v1/images/edits` (multipart/form-data).
Model: `gpt-image-2`. No mask — edit whole image.

1. For photos with `needs_staging: true`:
   - Upload image, prompt: "virtual home staging, [room_type],
     add [style from voice.md] furniture, realistic scale and lighting,
     same room structure, wide angle, professional real estate photo".
2. For photos with `needs_staging: false` → copy through with status "pass-through".
3. Save returned image as `output/{photo_id}-staged.png`.
4. Write `output/staged.json` — [{photo_id, brief, out_path, illustrative: true, status}].

## Environment
- `OPENAI_API_KEY` — injected by Hermes. Never stored in workspace.

## Outputs
- `output/staged.json`

## Human gate
Show staged rooms. Approve set.

## Pitfalls
| Over-staging looks fake | Keep description realistic; label illustrative |
| API rate limit | GPT Image 2: 1 image/sec. Process sequentially |
