# Stage 04 - Approve

Human gate before the CRM is actually updated.

## Inputs

- `03-write/output/updated-leads.json`
- `03-write/output/audit-log.json`

## Process

1. (Human) Agent reviews the batch - approve all, reject, or loop back.
2. After approval, the `--write` flag must be passed to `scripts/mcp_crm_run.py` for actual DB commit.
3. Write `output/_approval.json` `{approver, timestamp, approved_transitions, rejected_transitions}`.

## Outputs

- `output/_approval.json`

## Human gate

Mandatory. No CRM write without explicit approval. The `--write` flag is the commit gate.

## Pitfalls

| Skipped approval | No CRM write happens without _approval.json + --write flag |
| Stale approval | Timestamp in _approval.json; flag if >1h old (CRM state may have changed) |
