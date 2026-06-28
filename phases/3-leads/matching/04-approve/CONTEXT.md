# Stage 04 - Approve

Human gate on outreach suggestions.

## Inputs

- `03-rank/output/ranked-matches.json`

## Process

1. (Human) Agent reviews matches - approve which to act on, loop back if needed.
2. Write `output/approved-matches.json` - approved match pairs.
3. Write `output/_approval.json` `{approver, timestamp, match_count}`.

## Outputs

- `output/approved-matches.json`
- `output/_approval.json`

## Human gate

Mandatory before any outreach. No match acted on without approval.

## Pitfalls

| False positive match | Human can reject; log for scoring improvement |
| Stale approval | Timestamp in _approval.json; flag if >24h old |
