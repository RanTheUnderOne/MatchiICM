# Stage 03 - Predict

Score expected performance so the agent picks the best variant.

## Inputs
- `02-generate/output/posts.json`

## Process (MCP)
1. Per post, call Higgsfield MCP `virality_predictor` to score {hook, retention_risk, score}.
2. Attach prediction results to each post.
3. Write `output/scored-posts.json` - posts + prediction fields.

## Outputs
- `output/scored-posts.json`

## Human gate
Show ranked posts. Agent picks which to publish.

## Pitfalls
| MCP outage | Fallback to placeholder scores; flag as unscored |
