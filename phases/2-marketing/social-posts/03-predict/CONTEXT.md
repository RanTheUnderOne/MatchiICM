# Stage 03 — Predict

Estimate post performance via LLM analysis. No external API needed.

## Inputs
- `02-generate/output/posts.json`

## Process (LLM)
1. Per post, LLM analyzes: hook strength, retention risk, emotional appeal,
   platform fit, Hebrew quality, hashtag relevance.
2. Score each dimension 1-10. Aggregate to 0-100 virality estimate.
3. Attach prediction: {virality_score, strengths[], weaknesses[], recommendation}.
4. Write `output/scored-posts.json` — posts + prediction fields.

## Outputs
- `output/scored-posts.json`

## Human gate
Show ranked posts. Agent picks which to publish.

## Pitfalls
| LLM overconfidence | Scores are estimates — not measured. Flag as "LLM estimate" |
| Missing platform context | Compare against platform-specific best practices |
