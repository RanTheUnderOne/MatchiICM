# Stage 02 - Soul ID (Consistent Character)

Train a persistent visual identity for the agent. This is what makes every
future visual show the SAME face.

## Execution Layer
MCP - Higgsfield Soul ID training via `show_characters(action:train)`.

## Inputs
- `01-intake/output/agent.json` (photo_refs)

## Process
1. Validate photo_refs (10–20 well-lit, varied angles recommended).
2. Upload photos to Higgsfield, call `show_characters(action:train)` to
   train the Soul ID.
3. Capture the returned `soul_id` from the training response.
4. On success, write output with `soul_id`. On MCP failure, fall back to
   LLM descriptor with `fallback: true`.

## Outputs
- `output/soul-id.json` - {soul_id, photos_used, status, fallback}.

## Human gate
Show the trained identity preview. Confirm before generating portraits.

## Pitfalls
| < 10 photos | Weak identity lock - warn the agent |
| Inconsistent photos (different people) | Soul ID degrades - use one person only |
| MCP timeout / failure | Fall back to LLM descriptor; set fallback flag |
