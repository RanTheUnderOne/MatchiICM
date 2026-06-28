# Stage 01 - Brief

Pick the subject, angle, and target platforms.

## Inputs
- MCP `get_property_full_details` (production facts)
- `_mock/agent.json` (agent info fallback)

## Process (MCP)
1. Wipe stale output.
2. Call MCP `get_property_full_details` for property facts. Fallback to `_mock/properties.json` on MCP failure.
3. Choose subject (property or agent brand) + 1-2 angles + platforms
   (facebook, instagram).
4. Write `output/brief.json` + `output/_run.json`.

## Outputs
- `output/brief.json` - {subject, angles[], platforms[]}.
- `output/_run.json`

## Human gate
Confirm angle + platforms before generating.

## Pitfalls
| MCP unavailable | Fallback to `_mock/properties.json` silently |
