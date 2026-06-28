# Stage 03 - Rank

Top matches per lead + per property.

## Inputs

- `02-match/output/matches.json`

## Process

1. (Script) Same `py scripts/mcp_match_run.py` run also outputs rankings.
2. For each lead, top 3 properties by fit score.
3. For each property, top 3 leads by fit score.
4. Tie-break: lower price wins.

## Outputs

- `output/ranked-matches.json` `{by_lead:{...}, by_property:{...}}`

## Human gate

Review top matches. Confirm before approval.

## Pitfalls

| Tie on fit and price | Add secondary tie-break: days_on_market (older wins) |
| Many leads with same top property | Expected; approval stage decides which outreach to prioritize |
