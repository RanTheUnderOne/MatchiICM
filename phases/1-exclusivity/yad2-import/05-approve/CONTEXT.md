# Stage 05 - Approve (Human Gate)

## Execution Layer
Human + MCP - agent approves, then MCP `add_new_potential_property` persists.

## Inputs
- `04-validate/output/validated-listings.json`

## Process
1. Present `ready` and `needs_review` buckets.
2. Agent approves which listings enter inventory; edits `needs_review` items.
3. On approval - call MCP `add_new_potential_property` for each approved
   listing to persist to inventory.
4. Track accepted vs rejected listings in approval record.

## Outputs
- `output/approved-listings.json`
- `output/_approval.json` - {approved_by, approved_at, accepted_count,
  rejected_count}.

## Rule
No listing enters inventory without agent approval.

## Pitfalls
| Agent approves without reviewing | Enforce explicit review for `needs_review` items |
| MCP persist fails | Log failed listings - retry on next workflow run |
