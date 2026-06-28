# Stage 01 - Load

Find upcoming events that need a reminder via Google Calendar.

## Inputs
- MCP Google Calendar `list_events` (query events in next 24h)
- `_mock/calendar.json` (fallback if MCP unavailable)

## Process
1. Wipe stale output.
2. Call MCP `list_events` for next 24h range.
3. Filter events where `reminder_sent=false` (or equivalent extended property).
4. Fallback: if MCP unavailable, read `_mock/calendar.json` (mock showing S-1 within 24h).
5. Write `output/due-reminders.json` + `output/_run.json`.

## Outputs
- `output/due-reminders.json`
- `output/_run.json`

## Human gate
Show which events are due. Confirm before composing.
