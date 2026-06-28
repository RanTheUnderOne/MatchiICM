# Workflow: Photo Enhance — Declutter + Virtual Staging

Trigger: "הסר רהיטים / שפר תמונות / home staging / עיצוב דירה לצילום".

Turns raw property photos into clean, market-ready images. Reliability = the
property stays truthful (no fake square meters or fixtures) — declutter,
relight, stage empty rooms only.

## Pipeline
| Stage | Action | Execution |
| --- | --- | --- |
| 01-intake | Collect source photos + flag issues | MCP `get_property_full_details` + `_mock/photos.json` fallback |
| 02-declutter | Remove clutter / background / personal items | OpenAI `generate_image` (GPT Image 1 edit mode) |
| 03-stage | Virtually furnish empty rooms in brand style | OpenAI `generate_image` (GPT Image 1) |
| 04-approve | Human gate → publishable set | Human gate |

## Environment
- `OPENAI_API_KEY` — injected by Hermes. Never stored in workspace.

## Reliability Contract
- Never alter structural reality (no removing walls, no resizing rooms).
- Staging is labeled as illustrative when used on empty rooms.
- Brand look from `_config/voice.md` (palette, mood).

## Freshness
01 writes `01-intake/output/_run.json` {run_id, source, photo_count, fetched_at}.
