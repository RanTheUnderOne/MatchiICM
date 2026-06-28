# Stage 03 - Layout

Assemble the one-pager as a museum-quality PDF.

## Inputs
- `02-copy/output/copy.json`
- `01-gather/output/brochure-data.json`
- `_config/voice.md`

## Process (Script)
1. Run `py scripts/mcp_brochure_run.py --property-id <id>`.
2. Script renders headline, photos, highlights, blurb, contact line into an RTL-aware HTML template.
3. Playwright renders HTML to museum-quality PDF.
4. Write `output/brochure.pdf` + `output/_run.json`.

## Outputs
- `output/brochure.pdf`

## Human gate
Show the assembled page. Approve before export.

## Pitfalls
| Playwright not installed | Run `npx playwright install chromium` |
