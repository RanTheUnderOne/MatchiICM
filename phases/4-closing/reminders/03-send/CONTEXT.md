# Stage 03 - Send

Send the reminders via WhatsApp.

## Inputs
- `02-compose/output/messages.json`

## Process
1. 🟡 WhatsApp send not yet wired. Fallback: write send log to `output/send-log.json`.
2. Write `output/send-log.json` - {event_id, to, channel:"whatsapp", status}.

## Outputs
- `output/send-log.json`.

## Human gate
Confirm recipients before a real send.
