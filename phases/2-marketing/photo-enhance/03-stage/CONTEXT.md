# Stage 03 - Stage

Virtually furnish empty rooms in brand style.

## Inputs
- `02-declutter/output/decluttered.json` (ALL photos incl. pass-throughs with needs_staging)
- `_config/voice.md`

## Process (MCP)
1. For photos with `needs_staging: true` → build a staging brief (furniture style, palette from `_config/voice.md`). Call Higgsfield MCP `generate_image` with a staging preset.
2. For photos with `needs_staging: false` → copy through with status "pass-through".
3. Empty rooms pass through with `needs_staging: true` flag - they are staged, not skipped.
4. Write `output/staged.json` - [{photo_id, brief, out_path, illustrative:true, status}].

## Outputs
- `output/staged.json`

## Human gate
Show staged rooms. Approve set.

## Pitfalls
| Over-staging looks fake | Keep realistic scale; label illustrative |
| MCP outage | Fallback to mock staging briefs in `_mock/` |
