# Lead–Property Match Rules

Used by `phases/3-leads/matching/02-match/` and `scripts/match.py` (planned).

## Hard Constraints (block match if violated)
1. `lead.intent` must match `property.transaction_type`
   (buy lead → sale property; rent lead → rent property).
2. `lead.city` must match `property.city` (exact).
3. `lead.rooms` must be within ±1 of `property.rooms`.

Any violation → `blocked: true`, no soft score computed.

## Budget Semantics
- `lead.budget` is a **hard maximum** (lead will not pay above it).
- A property `asking_price` ≤ `lead.budget` is within budget.
- A property within 10% above `lead.budget` scores partial (see soft table).

## Soft Score Factors (max 100 pts; only for non-blocked pairs)

| Factor | Max pts | Rule |
| --- | --- | --- |
| budget fit | 40 | asking_price ≤ budget → 40; within 10% above → 20; >10% above → 0 |
| neighborhood match | 30 | lead.neighborhood == property.neighborhood → 30; else 0 |
| rooms exact | 20 | exact match → 20; ±1 (already passed hard check) → 10 |
| days_on_market | 10 | ≤14 days → 10; 15-30 → 5; >30 → 0 |

Note: "recency" removed from soft factors (no recency field on a lead-property pair).

## Tie-Break
If two properties have equal fit score for a lead, prefer lower `asking_price`.

## Explainability
Every match MUST carry a `factors` object with each factor's awarded points.
`blocked` pairs carry a `blocked_reason` string.
