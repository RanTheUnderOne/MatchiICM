# Stage 02 - Compose

Write the reminder message.

## Inputs
- `01-load/output/due-reminders.json`
- `_config/voice.md`

## Process
1. Per event: short Hebrew reminder with date/time, address, agent contact.
2. Keep brand voice; polite + clear; include reschedule option.

## Outputs
- `output/messages.json` - [{event_id, to, text}].

## Audit
Run before writing `output/messages.json`. Revise until all pass.

- [ ] Every message has: datetime, address, agent name, phone
- [ ] Reschedule option included in each message
- [ ] Brand voice from `_config/voice.md` - polite, clear, not pushy
- [ ] Agent signature from `agent.json` appended
- [ ] Hebrew text: natural, native-level (no translation artifacts)

## Human gate
Show drafted messages. Approve before send.
