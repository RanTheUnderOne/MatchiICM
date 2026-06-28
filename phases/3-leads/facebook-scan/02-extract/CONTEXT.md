# Stage 02 - Extract

Detect buy/rent intent and parse structured lead fields from Hebrew free text.

## Inputs

- `01-fetch/output/raw-posts.json`

## Process

1. (LLM) Per post: classify intent (buy / rent / none).
2. (LLM) Parse rooms, budget, city, neighborhood, timeline, phone from free text.
   - e.g. "3 חדרים בהדר עד 1.6 מיליון" → rooms 3, city חיפה, budget 1600000.
3. (Regex) Post-process LLM output: extract phone numbers (`05X-XXXXXXX`), validate price format.
4. Drop posts with no real intent (spam, ads, links).

## Outputs

- `output/extracted-leads.json` `[{post_id, name, intent, rooms, budget, city, neighborhood, timeline, phone, raw}]`

## Human gate

Review extracted leads + dropped count. Confirm before dedupe.

## Pitfalls

| Spam/ads kept | Drop loan ads, links, non-intent posts |
| "2.1" budget | Infer millions for buy ("2.1" → 2,100,000) |
| LLM hallucinates fields | Cross-check with regex for phone/price; flag low-confidence |
| Hebrew nicknames | Keep as-is; dedupe handles similarity |
