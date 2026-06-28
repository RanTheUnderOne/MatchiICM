# Stage 04 - Confirm

Human gate + mark events reminded via Google Calendar.

## Inputs
- `03-send/output/send-log.json`
- MCP Google Calendar `update_event`

## Process
1. Agent confirms sends.
2. For each sent event, call MCP `update_event` to set `reminder_sent=true`.
3. Write `output/_approval.json` - {confirmed_by, at, event_ids[]}.

## Outputs
- `output/_approval.json`

## Human gate
Mandatory. Prevents double-reminding.
