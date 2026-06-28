# Stage 04 - Approve

Human gate before the page goes public.

## Inputs
- `02-build/output/page.html`
- `03-chat/output/chat-kb.json`

## Process (Human gate)
1. Agent reviews page + chat boundary (loop back if needed).
2. Write `output/_approval.json` {approved_by, approved_at, url?}.

## Outputs
- `output/_approval.json`

## Human gate
Mandatory. No public publish without approval.
