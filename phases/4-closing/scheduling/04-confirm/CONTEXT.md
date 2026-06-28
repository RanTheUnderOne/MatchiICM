# Stage 04 - Confirm

Human gate + send invites.

## Inputs
- `03-book/output/booking.json`
- MCP Google Calendar `update_event`

## Process
1. Agent confirms the booking.
2. Call MCP `update_event` to send invites with attendees.
3. Track RSVP status (pending / accepted / declined).
4. Write `output/_approval.json` {confirmed_by, at, event_id}.

## Outputs
- `output/_approval.json`

## Human gate
Mandatory before invites are sent. Track RSVP after.
