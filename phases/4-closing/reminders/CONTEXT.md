# Workflow: Reminders - Showing / Meeting Reminders

Trigger: "תזכורת / שלח תזכורת / אשר פגישה / reminder".

Sends reminders for upcoming showings/meetings via WhatsApp. Reliability =
remind only real upcoming events, once, with opt-out respect.

State: 🟡 partial - WhatsApp send not yet wired.

## Pipeline
| Stage | Action | Layer |
| --- | --- | --- |
| 01-load | Find upcoming events needing a reminder | MCP `list_events` |
| 02-compose | Write the reminder message (HE) | LLM + `_config/voice.md` |
| 03-send | Send via WhatsApp | 🟡 Not yet wired - fallback to `output/send-log.json` |
| 04-confirm | Human gate + mark reminded | MCP `update_event` (set `reminder_sent=true`) |

## Reliability Contract
- 01 selects only events in the reminder window where `reminder_sent=false` via live MCP query.
- 03 sends once; 04 flips `reminder_sent=true` (no double-pinging).
- Message uses brand voice; includes time, address, agent contact.

## Execution Layer
| Capability | Tool | Status |
| --- | --- | --- |
| Calendar read | MCP `list_events` | 🟢 Live |
| Message compose | LLM + `_config/voice.md` | Available |
| WhatsApp send | 🟡 Not yet wired | Fallback: write `send-log.json` |
| Reminder marker | MCP `update_event` | 🟢 Live |

## Freshness
01 writes `01-load/output/_run.json` {run_id, source, event_count, fetched_at}.
