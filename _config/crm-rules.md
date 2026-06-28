# CRM Stage Transition Rules

Used by `phases/3-leads/crm-update/02-transition/`.

## Legal Stages
`new` → `contacted` → `qualified` → `won` | `lost`

## Allowed Transitions (adjacency matrix)
| From | Allowed to |
| --- | --- |
| new | contacted, lost |
| contacted | qualified, lost |
| qualified | won, lost |
| won | (terminal - no further transition) |
| lost | (terminal - no further transition) |

## Rules
- Backward moves are NOT allowed (e.g. qualified → new is illegal).
- Skipping stages is NOT allowed (e.g. new → won is illegal).
- `lost` is reachable from `new`, `contacted`, or `qualified` (abandon at any point).
- `won` and `lost` are terminal states - no transition out.

## Rejection
An illegal transition → `legal: false` + `reason: "illegal: <from>→<to>"`.
Log it; do NOT apply it; do NOT ask the user again (record and move on).

## Audit
Every applied transition must produce an audit entry:
`{ lead_id, from, to, by, at }` - recorded in `output/audit-log.json`.
`by` field = the operator performing the transition (agent name / system / TEST-MODE).
