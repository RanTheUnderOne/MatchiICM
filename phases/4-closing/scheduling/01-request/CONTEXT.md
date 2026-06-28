# Stage 01 - Request

Capture the meeting request from chat intent.

## Inputs
- Chat intent (user message like "קבע צפייה" / "תאם פגישה")
- `_mock/leads.json` (resolve the lead)
- `_mock/scheduling-request.json` (fallback if intent parse fails)

## Process
1. Wipe stale output.
2. Parse chat intent → resolve lead + property + desired window + duration.
3. If intent parse fails, fall back to `_mock/scheduling-request.json`.
4. Write `output/request.json`.

## Outputs
- `output/request.json` - {lead_id, property_id, window, duration_min}.

## Human gate
Confirm the request details before checking slots.
