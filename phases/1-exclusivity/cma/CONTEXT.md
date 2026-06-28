# Workflow: CMA - Comparative Market Analysis

Trigger: "תכין דוח שוק / ניתוח מחיר / CMA / השוואת מחיר".

Produces credible market-analysis report. Reliability = data, not promises.
Every number traces to a source.

## Pipeline
| Stage | Action | Execution |
|---|---|---|
| 01-subject | Identify subject property | MCP: `search_real_estate_properties` |
| 02-research | Gather comparable sales + neighborhood stats | MCP: `get_property_full_details` + web research cache to `_research/` |
| 03-analyze | Deterministic math: adjustments, value range, confidence | Script: `py scripts/cma_analyze.py` |
| 04-report | Narrative Hebrew report with citations + range | LLM + `_config/voice.md` |
| 05-approve | Human gate - review, edit, send | - |

## Reliability Contract
- 03 math = deterministic script. Not LLM. Reproducible.
- 04 cites every comp source. Presents RANGE, never false precision.
- 04 includes confidence band (High/Medium/Low) from 03.
- Human gate at 05 mandatory before anything reaches property owner.

## Freshness
Data-fetch stage = **02-research**. Writes `02-research/output/_run.json`:
`{run_id, source, fetched_at, counts:{comps}}`.
03 refuses without current `_run.json`.

## Rules
`_config/cma-rules.md` - comp selection, adjustment table, value/confidence formulas.
