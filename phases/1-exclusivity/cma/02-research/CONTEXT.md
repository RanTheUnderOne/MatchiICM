# Stage 02 - Research

Gather comparable sales + neighborhood stats for subject property.

## Inputs
- `01-subject/output/subject.json` - subject property.
- MCP: `get_property_full_details` for subject + similar properties.
- Cache: `_research/*.md` - dated market data (reuse if fresh).
- Fallback: `_mock/market-data.json`, `_mock/properties.json`.

## Process (MCP + Web)
1. Query MCP `search_real_estate_properties` for same city/neighborhood, similar specs.
2. For each candidate comp: call MCP `get_property_full_details`.
3. If MCP data insufficient → web research (nadlan.gov.il, yad2, madlan).
   Cache results to `_research/<area>-comps.md` with date.
4. Select 3-6 best comps per `_config/cma-rules.md`:
   same neighborhood, rooms ±0.5, size ±20%, sold <6mo preferred + active as secondary.
5. Capture each comp's source (nadlan.gov.il / yad2 / madlan) for citation.
6. Record source-disagreement flags for triangulation.

## Outputs
- `output/comps.json` - MUST match schema `cma_analyze.py` expects:
  ```json
  {
    "neighborhood_stats": {"avg_price_per_sqm": 15200, "avg_days_on_market": 31, "trend_3mo_pct": 1.8},
    "source_disagreement": false,
    "comps": [
      {"id":"C-201","rooms":4,"size_sqm":90,"floor":2,"balcony":true,"parking":false,
       "renovated":false,"status":"sold","price":1380000,"sold_date":"2026-04-10","source":"nadlan.gov.il"}
    ]
  }
  ```
  `trend_3mo_pct` = NUMBER (1.8, not "+1.8%"). Active comps use `asking_price`. Every comp needs `source`.
- `output/_run.json` - `{run_id, source, fetched_at, counts:{comps}}`.

## Human gate
Show comp table + sources. Agent can add/remove comps before analysis.

## Pitfalls
| <3 comps | Widen to city. Flag "insufficient data" |
| Stale cache (>30d) | Re-fetch, don't reuse |
| One source only | Lower confidence. Note no triangulation |
| MCP unreachable | Fallback to `_mock/`, log warning |
