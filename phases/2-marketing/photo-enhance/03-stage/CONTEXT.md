# Stage 03 — Stage

Virtually furnish empty rooms in brand style.

## Inputs
- `02-declutter/output/decluttered.json` (ALL photos with needs_staging flags)
- `_config/voice.md` (brand palette, mood)

## Process (OpenAI)
1. For photos with `needs_staging: true`:
   - Build prompt: "virtual home staging, [room_type], [style from voice.md],
     realistic furniture, natural lighting, wide angle, professional real estate photo".
   - Call OpenAI `generate_image` (GPT Image 2).
2. For photos with `needs_staging: false` → copy through with status "pass-through".
3. Write `output/staged.json` — [{photo_id, brief, out_path, illustrative: true, status}].

## Environment
- `OPENAI_API_KEY` — injected by Hermes. Never stored in workspace.

## Outputs
- `output/staged.json`

## Human gate
Show staged rooms. Approve set.

## Pitfalls
| Over-staging looks fake | Keep description realistic; label illustrative |
| API rate limit | GPT Image 2: 1 image/sec. Process sequentially |
