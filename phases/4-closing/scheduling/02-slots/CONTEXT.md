# Stage 02 - Slots

Compute free slots within the requested window via Google Calendar.

## Inputs
- `01-request/output/request.json`
- MCP Google Calendar `list_events` (query busy blocks)
- MCP Google Calendar `suggest_time` (propose free slots)

## Process
1. Call MCP `list_events` on the requested window → get busy blocks.
2. Call MCP `suggest_time` with duration + busy blocks → get free slot proposals.
3. Fallback: if MCP unavailable, read `_mock/calendar.json`.
4. Write `output/slots.json` + `output/_run.json`.

## Outputs
- `output/slots.json` - [{start, end}].
- `output/_run.json`

## Human gate
Show candidate slots. Agent/lead picks one.

## Pitfalls
| Offering a busy slot | Always subtract busy blocks first via live MCP query |
