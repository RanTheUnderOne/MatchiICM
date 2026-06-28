# Stage 01 - Gather

Collect property facts and the best photos for the brochure.

## Inputs
- MCP `get_property_full_details` (production facts)
- `_mock/properties.json` (MOCK fallback if MCP unavailable)
- `_mock/agent.json` (agent contact line for footer)

## Process (MCP)
1. Wipe stale output.
2. Call MCP `get_property_full_details` for property facts + photo list. Fallback to `_mock/properties.json` on MCP failure.
3. Pick the subject property; extract sellable facts (rooms, size, floor,
   balcony, parking, renovated, neighborhood, price, standout features).
4. Pick 3-5 best photos (prefer exterior, living, kitchen - skip bare/staging).
5. Extract agent contact block (name, phone, email) from `_mock/agent.json`.
6. Write `output/brochure-data.json` + `output/_run.json`.

## Outputs
- `output/brochure-data.json`
- `output/_run.json`

## Human gate
Show the facts + chosen photos. Confirm before copywriting.

## Pitfalls
| MCP unavailable | Fallback to `_mock/properties.json` silently |
