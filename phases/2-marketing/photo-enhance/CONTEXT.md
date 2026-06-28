# Workflow: Photo Enhance - Declutter + Virtual Staging

Trigger: "הסר רהיטים / שפר תמונות / home staging / עיצוב דירה לצילום".

Turns raw property photos into clean, market-ready images. Reliability = the
property stays truthful (we don't fake square meters or fixtures) - we declutter,
relight, and stage empty rooms only.

## Pipeline
| Stage | Action | Execution |
| --- | --- | --- |
| 01-intake | Collect source photos + flag issues | MCP `get_property_full_details` + `_mock/photos.json` fallback |
| 02-declutter | Remove clutter / background / personal items | Higgsfield MCP `remove_background` + `generate_image` (inpaint) |
| 03-stage | Virtually furnish empty rooms in brand style | Higgsfield MCP `generate_image` (staging preset) |
| 04-approve | Human gate -> publishable set | Human gate |

## Reliability Contract
- Never alter structural reality (no removing walls, no resizing rooms).
- Staging is labeled as illustrative when used on empty rooms.
- Brand look from `_config/voice.md` (palette, mood).

## MCP & Tools
- Production MCP: `https://prod-mcp.nadlanai.org/mcp`
- Higgsfield MCP tools: `generate_image`, `generate_video`, `motion_control`, `remove_background`, `virality_predictor`, `reframe`
- Data MCP: `get_property_full_details` for property facts

## Freshness
01 writes `01-intake/output/_run.json` {run_id, source, photo_count, fetched_at}.
