# Stage 01 - Fetch

Pull raw listings from Yad2 via Apify MCP scraper.

## Execution Layer
Script / MCP - Apify MCP Yad2 scraper actor.

## Inputs
- Search parameters: city, neighborhood, transaction_type (sale/rent),
  max listings, optional filters (rooms, price range).

## Process
1. Wipe stale output: `rm -f output/*.json`.
2. Call Apify MCP Yad2 scraper actor with search parameters.
3. Collect raw listings from the actor's dataset output.
4. If MCP unavailable, fall back to local `_mock/yad2-raw.json` with
   `fallback: true` flag.
5. Write `output/raw-listings.json` + `output/_run.json`
   {run_id, source, listing_count, fetched_at, fallback}.

## Outputs
- `output/raw-listings.json`
- `output/_run.json`

## Human gate
Show how many listings pulled. Confirm before structuring.

## Pitfalls
| Scraper returns stale data | Check fetched_at - discard if > 24h old |
| Apify MCP timeout | Fall back to mock data; set fallback flag |
| Rate limiting | Respect Apify rate limits - add delay between runs |
