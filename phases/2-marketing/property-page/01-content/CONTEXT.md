# Stage 01 - Content

Assemble everything the page needs.

## Inputs
- MCP `get_property_full_details` (production facts)
- `_mock/properties.json` (MOCK fallback if MCP unavailable)
- `_mock/agent.json` (contact block)
- Canonical reuse (if previously run in same session):
  - `phases/2-marketing/photo-enhance/04-approve/output/approved-photos.json` (preferred photos)
  - `phases/2-marketing/brochure/02-copy/output/copy.json` (preferred copy)
  - If these files don't exist, generate minimal facts + photos from mock directly.

## Process (MCP)
1. Wipe stale output.
2. Call MCP `get_property_full_details` for property facts. Fallback to `_mock/properties.json` on MCP failure.
3. Reuse approved photos from photo-enhance and copy from brochure when available.
4. Collect facts, photos, sections (overview, features, location, contact).
5. Write `output/page-content.json` + `output/_run.json`.

## Outputs
- `output/page-content.json`
- `output/_run.json`

## Human gate
Confirm content set before building the page.

## Pitfalls
| MCP unavailable | Fallback to `_mock/properties.json` silently |
