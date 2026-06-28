# Stage 03 - Write

Apply stage changes and write audit log (dry-run or commit).

## Inputs

- `02-transition/output/transitions.json`

## Process

1. (Script) Run `py scripts/mcp_crm_run.py --write` - applies legal transitions and writes audit records in a single atomic operation via MCP.
   - Without `--write`: dry-run mode (preview only, no DB changes).
   - Without `--write` flag: no DB changes occur.
2. Each transition writes an audit entry: `{lead_id, from, to, by, at}`.
3. Write `output/updated-leads.json` - leads after transition.
4. Write `output/audit-log.json` - full audit trail of this batch.

## Outputs

- `output/updated-leads.json`
- `output/audit-log.json`

## Human gate

Show what will be written (dry-run preview). Approve at 04 before actual commit with `--write`.

## Pitfalls

| `--write` flag omitted | Script runs dry-run; no DB changes committed |
| Partial failure | Atomic operation: all transitions succeed or none |
| Concurrent edits | `list_leads` stage field is source of truth at load time; re-run if stale |
