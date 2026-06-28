# Workflow: Video - Short Property Reel

Trigger: "תכין סרטון / וידאו לנכס / property video".

Produces a short property video/reel. Reliability = consistent agent identity
(Soul ID) + truthful footage; no fabricated rooms.

## Pipeline
| Stage | Action | Execution |
| --- | --- | --- |
| 01-script | Write short shot-by-shot script + voiceover | LLM + `_config/voice.md`. 5-8 shots: hook, exterior, rooms, standout, outro |
| 02-generate | Generate / animate shots | Higgsfield MCP `generate_video` + `motion_control` (agent shots use soul_id) |
| 03-assemble | Order shots, add captions + brand outro | Higgsfield MCP `reframe` (9:16). LLM for captions |
| 04-approve | Human gate | Human gate |

## Reliability Contract
- Agent on-camera identity reuses the Soul ID from agent-profile (same face).
- Shots reflect real rooms (from approved photos), not invented spaces.
- Brand outro + palette from `_config/voice.md`.

## MCP & Tools
- Production MCP: `https://prod-mcp.nadlanai.org/mcp`
- Higgsfield MCP tools: `generate_image`, `generate_video`, `motion_control`, `remove_background`, `virality_predictor`, `reframe`

## Freshness
01 writes `01-script/output/_run.json` {run_id, source, fetched_at, counts}.
