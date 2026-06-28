# Stage 04 - Approve

Human gate on the prioritized lead list.

## Inputs

- `03-bucket/output/buckets.json`

## Process

1. (Human) Agent reviews priorities - can loop back if a score looks wrong.
2. Write `output/prioritized-leads.json` - final ranked list.
3. Write `output/_approval.json` `{approver, timestamp, lead_count}`.

## Outputs

- `output/prioritized-leads.json`
- `output/_approval.json`

## Human gate

Mandatory. Prioritized list confirmed before downstream actions (matching, outreach).

## Pitfalls

| Score disagreement | Human can flag → re-score with adjusted rules |
| Stale approval | Timestamp in _approval.json; flag if >24h old |
