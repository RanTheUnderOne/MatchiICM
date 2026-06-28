# Stage 01 - Load

Load leads to score from MCP inventory.

## Inputs

- (MCP) `list_leads` on `https://prod-mcp.nadlanai.org/mcp`
- Fallback: `_mock/leads.json`

## Process

1. (MCP) Call `list_leads` to fetch all active leads with scoring fields (intent, budget, timeline, last_contact, stage).
2. On MCP failure: load `_mock/leads.json`.
3. Write `output/leads.json` - leads ready for scoring.
4. Write `output/_run.json` `{run_id, source, lead_count, fetched_at, mock_fallback}`.

## Outputs

- `output/leads.json`
- `output/_run.json`

## Human gate

Show lead count. Confirm before scoring.

## Pitfalls

| MCP unavailable | Fallback to mock; log warning |
| Empty lead set | Halt workflow; no-op |
