# Stage 04 - Approve

Human gate before leads enter the CRM inventory.

## Inputs

- `03-dedupe/output/deduped-leads.json`

## Process

1. (Human) Agent reviews each lead - approve, reject, or edit.
2. (MCP) For each approved lead, call `add_new_potential_property` on `https://prod-mcp.nadlanai.org/mcp` to commit to CRM.
3. Write `output/approved-leads.json` (approved subset).
4. Write `output/_approval.json` `{approver, timestamp, approved_count, rejected_count}`.

## Outputs

- `output/approved-leads.json`
- `output/_approval.json`

## Human gate

Mandatory. No lead enters CRM without explicit approval.

## Pitfalls

| MCP write fails | Log error; retry on next run; approved-leads.json preserves state |
| Duplicate slips through | Human catches; reject button available |
