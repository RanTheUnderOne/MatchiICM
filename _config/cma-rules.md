# CMA Rules - Deterministic Analysis

Stable reference for the cma workflow's analyze stage. The math is fixed and
reproducible. The LLM writes narrative only - it does NOT compute prices.

## Comparable Selection
- Same neighborhood first. Same city as fallback.
- Same room count ±0.5.
- Size within ±20% of subject sqm.
- Sold within last 6 months preferred; active listings allowed as secondary.
- Minimum 3 comps to produce a CMA. Below 3 → flag "insufficient data".

## Adjustments (applied to each comp's price/sqm before averaging)
| Factor | Adjustment |
| --- | --- |
| Floor diff (per floor, no elevator) | ±0.5% |
| Floor diff (per floor, with elevator) | ±0.2% |
| Balcony present vs absent | ±2% |
| Parking present vs absent | ±3% |
| Renovated vs standard | ±5% |
| Sold > 3mo ago | apply neighborhood trend % |

## Value Estimate
- estimated_price_per_sqm = adjusted average of comps.
- estimated_value = estimated_price_per_sqm × subject_size_sqm.
- Always present a RANGE: estimated_value ±5% (low / mid / high).
- Never present a single false-precision number.

## Price Position
- asking_vs_estimate = (asking_price − estimated_mid) / estimated_mid.
- > +5% → "מעל השוק" | −5%..+5% → "מחיר שוק" | < −5% → "מתחת לשוק".

## Confidence Score (0–100)
- +20 each comp beyond minimum 3 (cap +40).
- −15 if any source disagreement flag.
- −20 if subject differs from comps on a non-adjustable factor.
- Report confidence band: High ≥75, Medium 50–74, Low <50.
