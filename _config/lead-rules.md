# Lead Scoring Rules

Used by `phases/3-leads/lead-scoring/02-score/` and `scripts/lead_score.py` (planned).
Each factor produces a sub-score; total is the sum capped at 100.

## Factor Weights (total = 100 points)

| Factor | Max pts | Rule |
| --- | --- | --- |
| timeline | 30 | 0-1mo = 30, 0-3mo = 25, 1-3mo = 20, 3-6mo = 10, >6mo/6mo+/unknown = 0 |
| intent match | 20 | buy = 20, rent = 10 |
| budget realistic | 20 | present AND within market range = 20; present but unclear range = 10; missing = 0 |
| recency (last_contact) | 20 | <=7 days ago = 20, 8-30 days = 10, >30 days = 0 |
| stage | 10 | qualified = 10, contacted = 5, new = 2, won/lost = 0 |

## Market Range (budget realistic check)
- Buy budget: 800,000 – 5,000,000 ₪ is in range.
- Rent budget: 2,500 – 15,000 ₪/mo is in range.
- Budget is the lead's stated `budget` field. If absent → 0 pts for that factor.

## Recency Calculation
- Use current run date. `last_contact` field (ISO date) vs today.

## Bucket Thresholds
| Bucket | Score range |
| --- | --- |
| hot  | 70 – 100 |
| warm | 40 – 69  |
| cold | 0  – 39  |

## Explainability
Every scored lead MUST carry a `factors` object with each factor's awarded points,
so any score can be reproduced by hand from the rules above.
