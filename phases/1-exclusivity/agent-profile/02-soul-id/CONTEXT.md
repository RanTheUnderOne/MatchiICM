# Stage 02 — Reference Images

Collect reference photos for consistent agent portraits. No training needed —
OpenAI prompt consistency replaces Soul ID.

## Execution Layer
Human → OpenAI `generate_image` (GPT Image 1).

## Inputs
- `01-intake/output/agent.json` (photo_refs, name, brand)

## Process
1. Validate photo_refs (5-10 well-lit, varied angles recommended).
2. Build a consistent face descriptor from reference photos — note key features:
   face shape, hair color/style, eye color, skin tone, age range.
3. Save descriptor to `output/` — stage 03 uses it as prompt prefix.
4. No MCP call in this stage. Just extract + validate.

## Outputs
- `output/face-descriptor.json` — {features: {...}, photos_used: N, status}.

## Human gate
Show the descriptor. Confirm before generating portraits.

## Pitfalls
| < 5 photos | Descriptor may be weak — warn agent |
| Multiple people in photos | Flag ambiguity |
