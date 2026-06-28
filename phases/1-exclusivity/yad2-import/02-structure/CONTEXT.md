# Stage 02 - Structure

Normalize messy listing text into clean structured fields.

## Execution Layer
LLM - OpenAI with structured parsing prompts.

## Inputs
- `01-fetch/output/raw-listings.json`

## Process - parsing rules
1. **price**: strip ₪/שח/commas/"מיליון". "1,450,000 ₪" → 1450000;
   "2.75 מיליון" → 2750000; "3900 שח לחודש" → 3900.
2. **transaction_type**: rent if price < 20,000 or text has להשכרה/לחודש;
   else sale. Flag if ambiguous.
3. **rooms**: numeric. "4" → 4, "3.5" → 3.5.
4. **size_sqm**: extract number from "95 מ\"ר"; empty → null (flag).
5. **floor / total_floors**: "קומה 3 מתוך 5" → 3/5; "8/8" → 8/8;
   "קרקע" → 0.
6. **city / neighborhood**: split location string.
7. **features**: map to balcony/parking/elevator/renovated booleans from
   מרפסת/חניה/מעלית/משופצת.

## Outputs
- `output/structured-listings.json` - clean property objects + a `parse_flags`
  list per listing (what was uncertain).

## Human gate
Show structured results + any parse flags. Confirm before enrich.

## Pitfalls
| "מיליון" not expanded | 2.75 ≠ 2,750,000 - expand it |
| rent vs sale wrong | Check magnitude AND keywords |
| empty size | Don't guess - flag null |
