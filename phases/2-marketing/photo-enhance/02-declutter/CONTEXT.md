# Stage 02 — Declutter

Remove clutter, personal items, and messy backgrounds.

## Inputs
- `01-intake/output/photos.json`
- `_config/voice.md` (brand mood)

## Process (OpenAI)
1. Process ALL photos:
   - `cluttered` / `personal items` → OpenAI `generate_image` (GPT Image 1 edit mode) —
     prompt: "remove clutter and personal items, clean professional look, same room structure".
   - `dim lighting` → OpenAI `generate_image` — prompt: "brighten, natural daylight, warm tone".
   - `bare room, needs staging` → pass through with `needs_staging: true`.
   - `issues: []` (clean) → pass through with `needs_staging: false`.
2. Write `output/decluttered.json` — [{photo_id, room, brief, out_path, needs_staging, status}].
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
