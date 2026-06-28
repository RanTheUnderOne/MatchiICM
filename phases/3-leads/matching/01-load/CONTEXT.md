# Stage 01 - Load

Load leads + properties from MCP inventory.

## Inputs

- (MCP) `list_leads` on `https://prod-mcp.nadlanai.org/mcp`
- (MCP) `search_real_estate_properties` on `https://prod-mcp.nadlanai.org/mcp`

## Process

1. (MCP) Call `list_leads` - fetch all leads with match fields (budget, rooms, city, neighborhood, intent).
2. (MCP) Call `search_real_estate_properties` - fetch all properties (price, rooms, city, neighborhood, listing_type).
3. Build `{"leads":[...], "properties":[...]}` - exact shape expected by `scripts/match.py --input`.
4. Write `output/match-input.json`.
5. Write `output/_run.json` `{run_id, lead_count, property_count, fetched_at}`.

## Outputs

- `output/match-input.json` - shape: `{"leads":[...], "properties":[...]}`
- `output/_run.json`

## Human gate

Show counts (N leads x M properties). Confirm before matching.

## Pitfalls

| Large NxM can be expensive | Add max-leads / max-properties cap in _run.json |
| MCP call fails on one endpoint | Retry individually; fallback to cached or empty set |
