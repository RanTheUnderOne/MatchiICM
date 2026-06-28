# Stage 01 - Intake

Collect the source photos for one property.

## Inputs
- MCP `get_property_full_details` (production facts)
- `_mock/photos.json` (MOCK fallback if MCP unavailable)

## Process (MCP)
1. Wipe stale output: `rm -f output/*.json`.
2. Call MCP `get_property_full_details` for property facts + photo list. Fallback to `_mock/photos.json` on MCP failure.
3. Load photos for the property. Keep paths + flagged issues as-is.
4. Write `output/photos.json` + `output/_run.json`
   {run_id, source, photo_count, fetched_at}.

## Outputs
- `output/photos.json`
- `output/_run.json`

## Human gate
Show photo count + per-photo issues. Confirm the set before editing.

## Pitfalls
| MCP unavailable | Fallback to `_mock/photos.json` silently |
