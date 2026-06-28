# Stage 02 - Score

Deterministic 0-100 score per lead via rule engine.

## Inputs

- `01-load/output/leads.json`
- `_config/lead-rules.md` (exact factor weights + bucket thresholds)

## Process

1. (Script) Run `py scripts/mcp_lead_score_run.py` - engine `scripts/lead_score.py`.
2. Per lead, compute per-factor points using the table in `_config/lead-rules.md`:
   - timeline (0-1mo=30, 1-3mo=20, 3-6mo=10, >6mo=0)
   - intent match (buy=20, rent=10)
   - budget realistic (present+in-range=20, present+unclear=10, missing=0)
   - recency of last_contact (<=7d=20, 8-30d=10, >30d=0)
   - stage (qualified=10, contacted=5, new=2, won/lost=0)
   Total = sum capped at 100.
3. Script reads `_config/lead-rules.md` weights, writes scored leads with factor breakdown.
4. Verified on mock: L-4=95, L-1=87, L-2=82, L-3=75.

## Outputs

- `output/scored-leads.json` `[{id, score, factors:{...}}]`

## Human gate

Review scores + factor breakdown. Confirm before bucketing.

## Pitfalls

| LLM "guesses" a score | Score must come from the rule table, explainable - this is a deterministic script |
| Missing factor fields | Script assigns 0 for nulls; logs warning |
