# Stage 03 - Bucket

Hot / warm / cold by thresholds from config.

## Inputs

- `02-score/output/scored-leads.json`

## Process

1. (Script) Same `py scripts/mcp_lead_score_run.py` run also outputs buckets.
2. Apply thresholds from `_config/lead-rules.md`: >=70 hot, 40-69 warm, <40 cold.
3. Sort within each bucket by score descending.

## Outputs

- `output/buckets.json` `{hot:[...], warm:[...], cold:[...]}`

## Human gate

Show bucket counts + top hot leads. Confirm before approval.

## Pitfalls

| Threshold change mid-campaign | Thresholds live in `_config/lead-rules.md`; re-run to re-bucket |
| Empty bucket | Expected; no action needed for that tier |
