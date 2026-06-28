# Stage 03 - Enrich

Add derived context to each structured listing.

## Execution Layer
Script / MCP - MCP `search_real_estate_properties` + web fallback.

## Inputs
- `02-structure/output/structured-listings.json`

## Process
1. Compute price_per_sqm (if size + price present).
2. Call MCP `search_real_estate_properties` for neighborhood averages.
3. Compare each listing's price/sqm to neighborhood avg → mark
   above/at/below.
4. If MCP unavailable, fall back to web search or `_research/` local files
   with `fallback: true` flag.
5. Mark outliers (price/sqm > ±25% of neighborhood avg) for review.

## Outputs
- `output/enriched-listings.json` - structured + price_per_sqm,
  vs_neighborhood, outlier_flag, fallback.

## Human gate
Show enrichment + outliers. Confirm before validate.

## Pitfalls
| No neighborhood data available | Flag warning - proceed with city-level average only |
| Stale comp data | Check _run.json freshness of research data |
| MCP query returns empty | Fall back to web search |
