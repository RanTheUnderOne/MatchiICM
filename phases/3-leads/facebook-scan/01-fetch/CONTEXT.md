# Stage 01 - Fetch

Pull raw group posts from Facebook Groups via Apify MCP scraper.

## Inputs

- Facebook group URLs (configured per run)
- Fallback: `_mock/fb-groups-raw.json` (when MCP unavailable)

## Process

1. (Script/MCP) Run `py scripts/mcp_facebook_scan_run.py` - invokes Apify Facebook Groups Scraper via MCP endpoint `https://prod-mcp.nadlanai.org/mcp`.
2. MCP returns raw post data as JSON array.
3. Fallback path: if MCP call fails, load `_mock/fb-groups-raw.json`.
4. Write `output/raw-posts.json` (full raw data).
5. Write `output/_run.json` `{run_id, source, post_count, fetched_at, mock_fallback}`.

## Outputs

- `output/raw-posts.json`
- `output/_run.json`

## Human gate

Review post count + group sources. Confirm before extraction.

## Pitfalls

| Apify MCP timeout | Fallback to mock; log warning |
| FB auth / rate limit | Apify actor manages credentials; retry in _run.json |
