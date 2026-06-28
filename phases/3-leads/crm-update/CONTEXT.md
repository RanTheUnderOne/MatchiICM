# Workflow: CRM Update - Kanban Stage Transitions

Trigger: "עדכן CRM / קנבן / שנה סטטוס ליד / move lead".

Applies lead stage transitions on the CRM kanban with an audit trail. Reliability = legal transitions only + full audit, no silent overwrites.

## Pipeline

| Stage | Action | Execution | Input | Output |
| --- | --- | --- | --- | --- |
| 01-load | Load current lead states | MCP | `list_leads` (with stage) | `output/current.json` + `_run.json` |
| 02-transition | Compute requested stage changes (validate legality) | LLM | current.json + `_config/crm-rules.md` | `output/transitions.json` |
| 03-write | Apply changes + audit log | Script | transitions.json | `output/updated-leads.json` + `output/audit-log.json` |
| 04-approve | Human gate before commit | Human | updated-leads.json + audit-log.json | `output/_approval.json` |

## Inputs

- (MCP) `list_leads` on `https://prod-mcp.nadlanai.org/mcp` - fetches leads with current `stage`.
- (LLM) Chat intent / user request - e.g. "שנה סטטוס L-1 ל-contact".
- `_config/crm-rules.md` - adjacency matrix of allowed transitions.

## Process

1. **01-load** (MCP): Call `list_leads` with `stage` field → `output/current.json`.
2. **02-transition** (LLM): Parse chat intent for lead_id + target stage. Validate vs `_config/crm-rules.md` adjacency matrix.
3. **03-write** (Script): `py scripts/mcp_crm_run.py --write` - atomic stage update + audit log insert via MCP.
4. **04-approve** (Human): Confirm batch before CRM commit.

## Outputs

- `01-load/output/_run.json`
- `03-write/output/audit-log.json`
- `04-approve/output/_approval.json`

## Human gate

Stage 04-approve is mandatory before `--write` flag commits to DB.

## Reliability Contract

- 02 only allows legal transitions (per `_config/crm-rules.md` adjacency matrix).
- 03 writes an audit entry per change (who/when/from/to). No silent overwrite.
- Approval at 04 before any write reaches the real CRM.
- `--write` flag controls DB commit; dry-run without flag for preview.

## Pitfalls

| Illegal stage jump | Validate against allowed transitions before write |
| `--write` flag omitted | Script runs in dry-run mode (no DB changes) |
| Audit trail missing | Every transition must write an audit record in the same atomic operation |
