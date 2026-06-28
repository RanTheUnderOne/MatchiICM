# Stage 01 - Subject

Identify property for CMA. Normalize for analysis.

## Inputs
- User message (property by address, id, or description).
- MCP: `search_real_estate_properties` on `https://prod-mcp.nadlanai.org/mcp`.
  Fallback: `_mock/properties.json` (only if MCP unreachable).

## Process (MCP)
1. Parse user reference (e.g. "הרצל 12", "P-1001").
2. Call MCP `search_real_estate_properties` with query.
3. If ambiguous or not found - ask user, never guess.
4. Extract subject fields: id, address, city, neighborhood, rooms, size_sqm,
   floor, balcony, parking, elevator, renovated, asking_price, days_on_market.

## Outputs
- `output/subject.json` - normalized subject property.

## Human gate
Show identified subject. Confirm right property before researching.

## Pitfalls
| Two properties match | Ask which - never assume |
| Size or rooms missing | Flag; CMA needs size_sqm for price/sqm |
| MCP unreachable | Fallback to `_mock/properties.json`, log warning |
