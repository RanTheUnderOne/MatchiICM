# Workflow: Scheduling - Showings & Meetings

Trigger: "קבע פגישה / תיאום צפייה / showing / יומן".

Books showings/meetings against availability and confirms. Reliability = no
double-booking; only offered slots that are actually free.

State: 🟢 Google Calendar MCP live.

## Pipeline
| Stage | Action | Layer |
| --- | --- | --- |
| 01-request | Capture who/what/when-ish | LLM parse chat intent + `_mock/scheduling-request.json` fallback |
| 02-slots | Query busy blocks → propose free slots | MCP `list_events` + `suggest_time` |
| 03-book | Re-check free → create event with attendees | MCP `create_event` |
| 04-confirm | Human gate + update event (send invites) | MCP `update_event` + Human gate |

## Reliability Contract
- 02 only offers slots that don't collide with busy blocks via live MCP query.
- 03 re-checks before write (no double-book).
- Confirmation at 04 before invites are sent.

## Execution Layer
| Capability | Tool | Status |
| --- | --- | --- |
| Calendar read | MCP `list_events` | 🟢 Live |
| Slot suggestion | MCP `suggest_time` | 🟢 Live |
| Event create | MCP `create_event` | 🟢 Live |
| Event update | MCP `update_event` | 🟢 Live |
| Chat intent parse | LLM | Available |

## Freshness
02 writes `02-slots/output/_run.json` {run_id, source, fetched_at, counts}.
