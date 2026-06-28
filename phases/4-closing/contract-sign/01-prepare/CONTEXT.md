# Stage 01 - Prepare

Fill the contract template with deal facts via MCP.

## Inputs
- `_mock/contract-template.md` (template with {{placeholders}})
- MCP `get_property_full_details` (property data)
- `_mock/agent.json` (agent_name, license)

## Placeholder → source mapping
| Placeholder | Source |
| --- | --- |
| {{agent_name}} | `agent.full_name` |
| {{license}} | `agent.license` |
| {{owner_name}} | `property.owner.name` |
| {{property_address}} | `property.address` |
| {{city}} | `property.city` |
| {{months}} | `property.exclusivity_months` |
| {{fee_pct}} | `property.fee_pct` |

## Process
1. Wipe stale output.
2. Identify the target property (agent specifies or default first).
3. Call MCP `get_property_full_details` for property data.
4. Fill ALL {{placeholders}} from property data using mapping above.
5. Flag any missing field - never invent.
6. Fallback: if MCP unavailable, read `_mock/properties.json`.
7. Write `output/draft-contract.md` + `output/_run.json`.

## Outputs
- `output/draft-contract.md`
- `output/_run.json`

## Human gate
Show the draft + any unfilled fields. Confirm before sending.

## Audit
Run before writing `output/draft-contract.md`. Revise until all pass.

- [ ] All `{{placeholders}}` resolved - zero remain (grep `{{`)
- [ ] Every filled value traceable to MCP or `agent.json`
- [ ] No invented legal terms - flagged blanks documented
- [ ] Agent name + license correct
- [ ] Property address complete (street, city, neighborhood)
- [ ] Fee % and exclusivity months present

## Pitfalls
| Invented legal terms | Only fill from record; flag blanks |
