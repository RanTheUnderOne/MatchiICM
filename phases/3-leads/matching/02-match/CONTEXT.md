# Stage 02 - Match

Deterministic fit score per (lead, property) pair.

## Inputs

- `01-load/output/match-input.json`
- `_config/match-rules.md` (hard constraints + soft weights)

## Process

1. (Script) Run `py scripts/mcp_match_run.py` - engine `scripts/match.py`.
2. Hard constraints (from `_config/match-rules.md`):
   - intent must match transaction_type (buy→sale, rent→rent).
   - lead.city must match property.city (exact).
   - rooms within ±1. Violation → blocked:true, no soft score.
3. Soft score (budget=40, neighborhood=30, rooms_exact=20, days_on_market=10):
   - budget semantics: lead.budget is hard max. asking_price <= budget → 40pts; within 10% above → 20pts; else → 0pts.
4. Verified on mock: L-1→P-1001(85), L-2→P-1004(100), L-3→P-1005(100), L-4→P-1001(85).

## Outputs

- `output/matches.json` `[{lead_id, property_id, fit, factors:{...}, blocked?}]`

## Human gate

Review match table (fit scores, block reasons). Confirm before ranking.

## Pitfalls

| Suggesting a blocked match | Hard constraints filter BEFORE scoring |
| Budget edge cases | lead.budget treated as hard max; flag 0-budget leads for manual review |
