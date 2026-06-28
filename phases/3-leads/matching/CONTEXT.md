# Workflow: Matching - Lead <-> Property Fit

Trigger: "התאם ליד לנכס / matching / איזה נכס לליד".

Matches leads to inventory properties by deterministic fit score. Reliability = explainable match math, not vibes.

## Pipeline

| Stage | Action | Execution | Input | Output |
| --- | --- | --- | --- | --- |
| 01-load | Load leads + properties | MCP | `list_leads` + `search_real_estate_properties` | `output/match-input.json` + `_run.json` |
| 02-match | Deterministic fit per (lead, property) | Script | match-input.json + `_config/match-rules.md` | `output/matches.json` |
| 03-rank | Top matches per lead + per property | Script | matches.json | `output/ranked-matches.json` |
| 04-approve | Human gate → outreach suggestions | Human | ranked-matches.json | `output/approved-matches.json` + `_approval.json` |

## Inputs

- (MCP) `list_leads` on `https://prod-mcp.nadlanai.org/mcp`
- (MCP) `search_real_estate_properties` on `https://prod-mcp.nadlanai.org/mcp`
- `_config/match-rules.md` - hard constraints + soft factor weights.

## Process

1. **01-load** (MCP): Call `list_leads` + `search_real_estate_properties`. Build `{"leads":[...], "properties":[...]}` → `match-input.json`.
2. **02-match** (Script): `py scripts/mcp_match_run.py` - engine `match.py`. Hard constraints + soft factors → fit 0-100.
3. **03-rank** (Script): Same script outputs top-3 per lead + per property. Tie-break: lower price.
4. **04-approve** (Human): Agent approves matches → outreach suggestions.

## Outputs

- `01-load/output/_run.json`
- `04-approve/output/approved-matches.json`
- `04-approve/output/_approval.json`

## Human gate

Stage 04-approve is mandatory before any outreach.

## Reliability Contract

- 02 fit score is a pure function (budget within range, rooms, city, neighborhood, intent vs listing type). Explainable per factor.
- No match suggested that violates a hard constraint (e.g. rent lead vs sale).
- 03 tie-breaking is deterministic: lower price wins.

## Pitfalls

| Large NxM matrix (1000 leads x 500 props = 500K pairs) | Script handles in batch; O(N*M) limited by _config cap |
| Stale property data | 01-load fetches fresh from MCP each run |
