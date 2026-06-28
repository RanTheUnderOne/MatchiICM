# Stage 01 - Load

Load current lead states from MCP inventory.

## Inputs

- (MCP) `list_leads` on `https://prod-mcp.nadlanai.org/mcp` - fetches leads with current `stage` field.

## Process

1. (MCP) Call `list_leads` - fetch all leads including `stage`.
2. Write `output/current.json` - `[{id, name, stage, last_updated}]`.
3. Write `output/_run.json` `{run_id, source, lead_count, fetched_at}`.

## Outputs

- `output/current.json`
- `output/_run.json`

## Human gate

Show current stage distribution (e.g. new: 12, contacted: 5, qualified: 3). Confirm before transitions.

## Pitfalls

| MCP unavailable | Workflow cannot proceed; no mock fallback for live state |
| `stage` field missing on some leads | Default to "new"; flag for review |
