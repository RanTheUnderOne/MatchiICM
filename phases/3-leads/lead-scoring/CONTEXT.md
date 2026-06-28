# Workflow: Lead Scoring - Deterministic Lead Prioritization

Trigger: "דרג לידים / lead scoring / אילו לידים חמים".

Scores leads 0-100 and buckets them (hot/warm/cold) by deterministic rules. Reliability = math in a script, not LLM guessing. Reproducible + explainable.

## Pipeline

| Stage | Action | Execution | Input | Output |
| --- | --- | --- | --- | --- |
| 01-load | Load leads | MCP | `list_leads` | `output/leads.json` + `_run.json` |
| 02-score | Deterministic score (budget fit, timeline, recency, intent) | Script | leads.json + `_config/lead-rules.md` | `output/scored-leads.json` |
| 03-bucket | Hot / warm / cold by thresholds | Script | scored-leads.json | `output/buckets.json` |
| 04-approve | Human gate → prioritized list | Human | buckets.json | `output/prioritized-leads.json` + `_approval.json` |

## Inputs

- (MCP) `list_leads` on `https://prod-mcp.nadlanai.org/mcp` - fetches all active leads.
- Fallback: `_mock/leads.json` when MCP unavailable.
- `_config/lead-rules.md` - factor weights + bucket thresholds.

## Process

1. **01-load** (MCP): Call `list_leads` → `output/leads.json`. Fallback to `_mock/leads.json`. Write `_run.json`.
2. **02-score** (Script): `py scripts/mcp_lead_score_run.py` - engine `lead_score.py`. Deterministic 0-100 per lead using factor table.
3. **03-bucket** (Script): Same script outputs buckets. Thresholds from `_config/lead-rules.md`: >=70 hot, 40-69 warm, <40 cold.
4. **04-approve** (Human): Review prioritized list. Confirm.

## Outputs

- `01-load/output/_run.json`
- `04-approve/output/prioritized-leads.json`
- `04-approve/output/_approval.json`

## Human gate

Stage 04-approve is mandatory. Prioritized list reviewed before action.

## Reliability Contract

- 02 score is a pure function of fields (script), reproducible, explainable.
- Each score carries its factor breakdown (why this number).
- Thresholds live in `_config/lead-rules.md`, not hardcoded.

## Pitfalls

| Stale leads scored | 01-load must filter leads updated within N days |
| Missing fields → score 0 | Script handles nulls gracefully (0 points per factor) |
