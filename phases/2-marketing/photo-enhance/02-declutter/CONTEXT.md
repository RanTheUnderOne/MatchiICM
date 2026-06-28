# Stage 02 - Declutter

Remove clutter, personal items, and messy backgrounds.

## Inputs
- `01-intake/output/photos.json`
- `_config/voice.md` (brand mood)

## Process (MCP)
1. Process ALL photos from the input list:
   - Clutter issues (`"cluttered"`, `"personal items"`, `"unmade bed"`, ...) → declutter via Higgsfield `remove_background` + `generate_image` (inpaint).
   - Lighting issues (`"dim lighting"`) → relight via Higgsfield `generate_image` with lighting preset.
   - `"bare room, needs staging"` → pass through as-is with `needs_staging: true`.
   - `issues: []` (clean) → pass through with `needs_staging: false`.
2. Call Higgsfield MCP `remove_background` for background cleanup, `generate_image` with inpaint for clutter removal.
3. Write `output/decluttered.json` - [{photo_id, room, brief, out_path, needs_staging, status}].
   ALL photos appear here (edited, relit, or pass-through). Stage 03 reads this list.

## Outputs
- `output/decluttered.json`

## Human gate
Show per-photo action (declutter / relight / pass-through / stage). Approve before staging.

## Pitfalls
| Removing real fixtures | Only remove movable clutter, never built-ins |
| Dropping empty/clean photos | Pass ALL photos through - stage 03 needs the full set |
| MCP outage | Fallback to mock request briefs in `_mock/` |
