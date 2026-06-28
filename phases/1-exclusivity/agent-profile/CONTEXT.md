# Workflow: Agent Profile — Branded Profile + AI Portrait

Trigger: "תכין לי כרטיס סוכן / פרופיל / תמונת פרופיל".

Builds a branded agent profile card plus professional AI portrait. Consistency =
face descriptor as prompt prefix, reused across all stages. No training needed.

## Pipeline
| Stage | Action | Execution Layer | Tool |
| --- | --- | --- | --- |
| 01-intake | Collect agent details | Human | Onboarding questionnaire / local config |
| 02-face-id | Extract face descriptor from photos | LLM | Analyze photos → consistent text descriptor |
| 03-portrait | Generate professional portrait(s) | OpenAI | `generate_image` (DALL-E 3) with face descriptor |
| 04-profile-card | Assemble branded card | LLM | OpenAI + `_config/voice.md` |
| 05-approve | Human gate | Human | — |

## Environment
- `OPENAI_API_KEY` — injected by Hermes. Never stored in workspace.

## Reliability Contract
- Face descriptor locks visual identity → every portrait has the same face.
- Portraits are real generated assets (when API connected), not stock.
- 04 follows brand: colors, logo watermark, contact line from `_config/voice.md`.

## Run Protocol
Each stage writes its output to `output/` and records a `_run.json` with
`{run_id, stage, execution_layer, status, timestamp}`.
