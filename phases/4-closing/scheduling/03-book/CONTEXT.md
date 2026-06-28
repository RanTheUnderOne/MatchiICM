# Stage 03 - Book

Tentatively book the chosen slot via Google Calendar.

## Inputs
- `02-slots/output/slots.json`
- chosen slot (from human gate)
- MCP Google Calendar `list_events` (re-check free)
- MCP Google Calendar `create_event`

## Process
1. Re-check the slot is still free via MCP `list_events`.
2. Call MCP `create_event` with title, time, attendees (lead + agent).
3. Write `output/booking.json`.

## Outputs
- `output/booking.json` - {event_id, slot, lead_id, property_id, status:"tentative"}.

## Human gate
Show the tentative booking. Confirm at 04.
