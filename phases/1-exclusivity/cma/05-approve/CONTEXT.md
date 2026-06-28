# Stage 05 - Approve (Human Gate)

Compliance boundary. Nothing reaches property owner without agent's
explicit approval.

## Inputs
- `04-report/output/cma-report.md`

## Process (Human gate)
1. Present final report to agent in chat.
2. Agent can: approve as-is / edit markdown / reject and rerun stage.
3. On approval - mark ready to send via WhatsApp.

## Outputs
- `output/approved-cma-report.md` - approved version.
- `output/_approval.json` - `{approved_by, approved_at, edits_made}`.

## Rule
No autonomous send. Agent decides. EU AI Act human-oversight point +
exclusivity-pitch quality gate.
