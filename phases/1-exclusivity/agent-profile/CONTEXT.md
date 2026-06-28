# Workflow: Agent Profile - Branded Profile + AI Portrait

Trigger: "תכין לי כרטיס סוכן / פרופיל / תמונת פרופיל".

Builds a branded agent profile card plus a professional AI portrait. Reliability
here = visual consistency: the same agent face across every asset (card, video,
posts), via Higgsfield Soul ID.

Production MCP endpoint: https://prod-mcp.nadlanai.org/mcp

## Pipeline
| Stage | Action | Execution Layer | Tool |
| --- | --- | --- | --- |
| 01-intake | Collect agent details | Script | Onboarding questionnaire / local config |
| 02-soul-id | Train a consistent character from agent photos | MCP | Higgsfield `show_characters(action:train)` + `generate_image` |
| 03-portrait | Generate professional portrait(s) | MCP | Higgsfield `generate_image` with soul_id |
| 04-profile-card | Assemble branded card | LLM | OpenAI + `_config/voice.md` |
| 05-approve | Human gate | Human | - |

## Reliability Contract
- Soul ID locks one face/identity → every future visual (video, posts) reuses
  the same `soul_id`. No "different person each time".
- Portraits are real generated assets (when connected), not stock.
- 04 follows brand: colors, logo watermark, contact line from `_config/voice.md`.

## MCP Fallback
If Higgsfield MCP is unreachable, stages 02 and 03 fall back to LLM-generated
descriptors (no image output). A `fallback: true` flag is set in the stage
output JSON. Downstream stages respect the flag and use placeholders.

## Run Protocol
Each stage writes its output to `output/` and records a `_run.json` with
`{run_id, stage, execution_layer, status, timestamp}`. Downstream stages
validate the freshness of their inputs before proceeding.
