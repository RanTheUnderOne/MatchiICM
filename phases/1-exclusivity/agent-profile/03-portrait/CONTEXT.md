# Stage 03 - Portrait

Generate the professional portrait(s) using the locked identity.

## Execution Layer
MCP - Higgsfield `generate_image` with soul_id.

## Inputs
- `02-soul-id/output/soul-id.json` (soul_id)
- `_config/voice.md` (brand: background, colors)

## Process
1. Build portrait generation parameters: professional real-estate headshot,
   clean neutral or branded background, soft professional lighting, business
   attire.
2. Call Higgsfield `generate_image` with the `soul_id` + headshot preset.
3. Save returned image(s) to `output/`. Set `fallback: true` if MCP
   unavailable.

## Outputs
- `output/portrait.json` - {soul_id, image_paths[], status, fallback}.

## Human gate
Show portrait(s). Agent picks/approves before the card is assembled.

## Pitfalls
| Background clashes with brand | Use `_config/voice.md` colors |
| Face drift | Always pass soul_id - never generate without it |
| MCP timeout / failure | Fall back - stage 04 uses placeholder if no image |
