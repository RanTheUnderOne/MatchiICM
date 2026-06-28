# Stage 04 - Validate

Score completeness and flag red flags before anything enters inventory.

## Execution Layer
LLM - OpenAI with validation rules.

## Inputs
- `03-enrich/output/enriched-listings.json`

## Process
1. Completeness score (0–100): required = price, rooms, size_sqm, city,
   transaction_type. Deduct for each missing/flagged field.
2. Red flags: missing size, price outlier, rent/sale ambiguous, no phone.
3. Bucket each listing: `ready` (score ≥80, no red flags) /
   `needs_review` (flags present) / `reject` (missing core fields).

## Outputs
- `output/validated-listings.json` - listings + completeness_score, red_flags[],
  bucket.

## Human gate
Show buckets. Agent reviews `needs_review` items in stage 05.

## Pitfalls
| Score threshold too strict | Adjust to 70 if market consistently lacks size data |
| False positive red flags | Allow agent override in stage 05 |
