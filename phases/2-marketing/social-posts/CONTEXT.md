# Workflow: Social Posts - Multi-Platform Property Posts

Trigger: "תכין פוסט / רשתות חברתיות / פוסט פייסבוק / אינסטגרם".

Generates platform-ready posts (image + caption) for a property or the agent
brand. Reliability = predicted performance before publish + brand consistency.

## Pipeline
| Stage | Action | Execution |
| --- | --- | --- |
| 01-brief | Pick subject + angle + target platforms | MCP `get_property_full_details` + `_mock/agent.json` fallback |
| 02-generate | Make post image(s) + caption per platform | Higgsfield MCP `generate_image` + LLM caption (HE) |
| 03-predict | Score expected performance | Higgsfield MCP `virality_predictor` |
| 04-approve | Human gate -> schedule/publish | Human gate. Publishing API 🔴 discover |

## Reliability Contract
- Captions use only true property facts (from 01).
- 03 attaches a predicted-performance score so the agent picks the best variant.
- Agent visuals reuse Soul ID; brand palette from `_config/voice.md`.

## MCP & Tools
- Production MCP: `https://prod-mcp.nadlanai.org/mcp`
- Higgsfield MCP tools: `generate_image`, `generate_video`, `motion_control`, `remove_background`, `virality_predictor`, `reframe`
- Data MCP: `get_property_full_details` for property facts

## Freshness
01 writes `01-brief/output/_run.json` {run_id, source, fetched_at, counts}.
