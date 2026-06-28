# Workflow: Contract Sign - Exclusivity / Sale Signature

Trigger: "חתימה / חוזה / שלח לחתימה / digital signature".

Prepares a contract from a template, sends for digital signature, tracks status.
Reliability = filled from real record + human approval + NOT legal advice.

State: 🟡 partial - signature provider not yet chosen.

## Pipeline
| Stage | Action | Layer |
| --- | --- | --- |
| 01-prepare | Fill template with deal facts | MCP `get_property_full_details` + LLM |
| 02-send | Send for digital signature | 🔴 discover+approve needed (Hatima / DocuSign / SignNow) |
| 03-track | Track signature status | 🔴 same provider's poll/webhook; mock for now |
| 04-confirm | Human confirm + archive signed doc | Human gate |

## Reliability Contract
- 01 fills ONLY from the record via MCP `get_property_full_details`; blank fields flagged, never invented.
- MCP fallback: `_mock/contract-template.md` for template; `_mock/properties.json` + `_mock/agent.json` if MCP unavailable.
- Output labeled: MOCK / not legal advice; final wording needs lawyer sign-off.
- Nothing "sent" for real without approval; provider TBD (discover + approve).

## Execution Layer
| Capability | Tool | Status |
| --- | --- | --- |
| Property details fetch | MCP `get_property_full_details` | Available |
| Template fill | LLM (fill {{placeholders}}) | Available |
| Signature send | 🔴 discover+approve needed | Open decision |
| Signature track | 🔴 same provider's poll/webhook | Mock now |

## Freshness
01 writes `01-prepare/output/_run.json` {run_id, source, fetched_at, counts}.
