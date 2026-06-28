# Workflow: Brochure - HE/EN Property One-Pager

Trigger: "תכין ברושור / עלון לנכס / brochure".

Builds a bilingual (Hebrew + English) property brochure. Reliability = every
fact comes from the property record, never invented; copy follows brand voice.

## Pipeline
| Stage | Action | Execution |
| --- | --- | --- |
| 01-gather | Pull property facts + best photos | MCP `get_property_full_details` + `_mock/properties.json` fallback |
| 02-copy | Write HE + EN copy (headline, highlights, blurb) | LLM + `_config/voice.md` |
| 03-layout | Assemble one-pager (museum-quality PDF) | Script `py scripts/mcp_brochure_run.py --property-id <id>` via Playwright |
| 04-approve | Human gate -> export | Human gate |

## Reliability Contract
- 02 uses ONLY facts present in 01 output. No invented amenities.
- HE and EN say the same thing (no drift between languages).
- Brand colors / contact line from `_config/voice.md`.

## MCP & Tools
- Production MCP: `https://prod-mcp.nadlanai.org/mcp`
- Data MCP: `get_property_full_details` for property facts

## Freshness
01 writes `01-gather/output/_run.json` {run_id, source, fetched_at, counts}.
