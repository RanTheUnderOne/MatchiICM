# Stage 02 — Declutter

Remove clutter, personal items, and messy backgrounds.

## Inputs
- `01-intake/output/photos.json`
- `_config/voice.md` (brand mood)

## Process (OpenAI `images.edit`)
Endpoint: `POST https://api.openai.com/v1/images/edits` (multipart/form-data).
Model: `gpt-image-2`. No mask — edit whole image.

1. Process ALL photos:
   - `cluttered` / `personal items` → upload image, prompt: "clean empty room,
     remove all clutter and personal items, freshly painted walls,
     same room structure and lighting, professional real estate photo".
   - `dim lighting` → upload image, prompt: "same room, brighten,
     natural daylight, warm professional tone".
   - `bare room, needs staging` → pass through with `needs_staging: true`.
   - `issues: []` (clean) → pass through with `needs_staging: false`.
2. Save returned image as `output/{photo_id}-clean.png`.
3. Write `output/decluttered.json` — [{photo_id, room, brief, out_path, needs_staging, status}].
   ALL photos appear here. Stage 03 reads this list.

## Environment
- `OPENAI_API_KEY` — injected by Hermes. Never stored in workspace.

## Outputs
- `output/decluttered.json`

## Human gate
Show per-photo action. Approve before staging.

## Pitfalls
| Removing real fixtures | Only remove movable clutter, never built-ins |
| API timeout | Fallback to pass-through with status "skipped" |
| Dropping clean photos | Pass ALL photos through — stage 03 needs full set |
