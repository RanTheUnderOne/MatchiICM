# Workflow: Social Posts — Multi-Platform Property Posts

Trigger: "תכין פוסט / רשתות חברתיות / פוסט פייסבוק / אינסטגרם".

Generates platform-ready posts (image + caption) for a property or the agent
brand. Reliability = predicted performance before publish + brand consistency.

## Pipeline
| Stage | Action | Execution |
| --- | --- | --- |
| 01-brief | Pick subject + angle + target platforms | MCP `get_property_full_details` + `_mock/agent.json` fallback |
| 02-generate | Make post image(s) + caption per platform | OpenAI `generate_image` + LLM caption (HE) |
| 03-predict | Score expected performance | LLM virality estimate (hook, retention, platform fit) |
| 04-approve | Human gate → schedule/publish | Human gate. Publishing API 🔴 discover |

## Environment
- `OPENAI_API_KEY` — injected by Hermes. Never stored in workspace.

## Reliability Contract
- Captions use only true property facts (from 01).
- 03 attaches LLM-estimated performance score so agent picks best variant.
- Brand palette from `_config/voice.md`.

## Freshness
01 writes `01-brief/output/_run.json` {run_id, source, fetched_at, counts}.
