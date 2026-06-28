# Stage 03 — Portrait

Generate professional portrait(s) using consistent face descriptor.

## Execution Layer
OpenAI — `https://api.openai.com/v1/images/generations` with `$OPENAI_API_KEY`.

## Inputs
- `02-soul-id/output/face-descriptor.json` (face consistency prompt)
- `_config/voice.md` (brand: background, colors, mood)

## Process
1. Build prompt: `face-descriptor` + "professional real-estate headshot,
   clean neutral background, soft professional lighting, business attire".
2. Call OpenAI `generate_image` (GPT Image 1, 1024x1024, HD quality).
3. Save returned image(s) to `output/`.
4. On failure: fallback to placeholder, set `fallback: true`.

## Outputs
- `output/portrait.json` — {image_paths[], prompt_used, status, fallback}.

## Environment
- `OPENAI_API_KEY` — injected by Hermes. Never stored in workspace.

## Human gate
Show portrait(s). Agent picks/approves before the card is assembled.

## Pitfalls
| Background clashes with brand | Use `_config/voice.md` palette in prompt |
| Face drift between portraits | Always include full face-descriptor as prompt prefix |
| API rate limit | GPT Image 1: 1 image/sec. Batch sequentially |
