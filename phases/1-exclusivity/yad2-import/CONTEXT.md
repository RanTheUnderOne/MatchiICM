# Workflow: Yad2 Import - Structured Property Intake

Trigger: "ייבא נכסים מ-yad2 / סנכרון יד2".

Pulls listings from Yad2 and turns messy text into clean structured properties,
enriched and validated. Reliability = every field normalized + red-flagged, not
trusted blindly.

Production MCP endpoint: https://prod-mcp.nadlanai.org/mcp

## Pipeline
| Stage | Action | Execution Layer | Tool |
| --- | --- | --- | --- |
| 01-fetch | Pull raw listings | Script / MCP | Apify MCP Yad2 scraper actor |
| 02-structure | Normalize messy text → clean fields | LLM | OpenAI + parsing rules |
| 03-enrich | Add price/sqm, neighborhood context, distances | Script / MCP | MCP `search_real_estate_properties` + web fallback |
| 04-validate | Red flags, completeness score | LLM | OpenAI + checks |
| 05-approve | Human gate → into inventory | Human / MCP | MCP `add_new_potential_property` |

## Reliability Contract
- 02 parses "1,450,000 ₪" → 1450000, "קומה 3 מתוך 5" → floor 3/total 5,
  detects sale vs rent from price magnitude + keywords.
- 03 computes price/sqm vs neighborhood average (from MCP or web), flags outliers.
- 04 scores completeness and flags red flags (missing size, suspicious price).
- Nothing enters inventory without approval at 05.

## MCP Fallback
If Apify MCP is unreachable at stage 01, fall back to local `_mock/` data
with a `fallback: true` flag. Other stages fall back to web search or local
research files as noted per stage.

## Freshness
01 writes `01-fetch/output/_run.json` {run_id, source, listing_count, fetched_at}.
Every stage checks input freshness before proceeding.
