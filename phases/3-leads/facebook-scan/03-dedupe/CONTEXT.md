# Stage 03 - Dedupe

Drop duplicates against existing lead inventory.

## Inputs

- `02-extract/output/extracted-leads.json`
- (MCP) Existing inventory via `list_leads` on `https://prod-mcp.nadlanai.org/mcp`

## Process

1. (MCP) Call `list_leads` to fetch all existing leads.
2. Match new vs existing by:
   - **Phone**: if extracted phone matches existing → duplicate.
   - **Text similarity**: same city + rooms + budget combination across posts.
3. Mark each new lead: `new` or `duplicate-of:<id>`.
4. New leads get `source=facebook` metadata field.
5. Keep only the `new` set for approval.

## Outputs

- `output/deduped-leads.json` - new leads + dedupe annotations.

## Human gate

Show new vs duplicate counts. Confirm before approval.

## Pitfalls

| No phone in FB post | Fall back to text similarity (city+rooms+budget combo) |
| MCP `list_leads` fails | Read local `_mock/leads.json` as fallback |
| False duplicate match | Flag near-duplicates for human review instead of auto-skip |
