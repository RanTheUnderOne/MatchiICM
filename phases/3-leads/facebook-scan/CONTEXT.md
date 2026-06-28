# Workflow: Facebook Scan - Group Lead Harvesting

Trigger: "סרוק פייסבוק / חפש לידים בקבוצות / facebook scan".

Scans real-estate Facebook groups for buy/rent intent, extracts structured leads, and dedupes against existing inventory. Reliability = filter spam + dedupe + only real intent.

## Pipeline

| Stage | Action | Execution | Input | Output |
| --- | --- | --- | --- | --- |
| 01-fetch | Pull raw group posts | Script (Apify MCP) | FB groups config | `output/raw-posts.json` + `_run.json` |
| 02-extract | Detect intent, parse rooms/budget/city/phone | LLM + Regex | raw-posts | `output/extracted-leads.json` |
| 03-dedupe | Drop duplicates vs existing leads | MCP | extracted-leads + `list_leads` | `output/deduped-leads.json` |
| 04-approve | Human gate → add to lead inventory | MCP | deduped-leads | `output/approved-leads.json` + `_approval.json` |

## Inputs

- Facebook group URLs/targets (per run config)
- Existing lead inventory via MCP `list_leads` (for dedupe)

## Process

1. **01-fetch** (Script/MCP): `py scripts/mcp_facebook_scan_run.py` - runs Apify Facebook Groups Scraper via MCP. Writes `_run.json` with run_id, source, post_count, fetched_at.
2. **02-extract** (LLM + Regex): Each post fed to LLM - extract intent, rooms, budget, city, timeline, phone. Hebrew regex for phone/price. Drop non-intent posts.
3. **03-dedupe** (MCP): Call `list_leads` - match by phone + text similarity. New leads get `source=facebook`.
4. **04-approve** (MCP/Human): Human approves → MCP `add_new_potential_property` per approved lead.

## Outputs

- `01-fetch/output/_run.json`
- `04-approve/output/approved-leads.json`
- Approved leads committed to CRM via MCP

## Human gate

Stage 04-approve is mandatory. No lead enters inventory without explicit approval.

## Reliability Contract

- 02 only keeps posts with genuine buy/rent intent (spam/ads dropped).
- 03 dedupes against existing leads (phone/name/text similarity).
- Nothing enters the lead list without approval at 04.

## Pitfalls

| Spam posts kept | LLM must classify intent down to "none" and drop |
| Hebrew parsing ambiguous | Budget "2.1" → infer millions for buy (2,100,000) |
| FB rate limits | Apify handles retries; _run.json tracks failures |
