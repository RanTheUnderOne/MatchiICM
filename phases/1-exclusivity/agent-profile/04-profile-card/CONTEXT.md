# Stage 04 - Profile Card

Assemble the branded agent profile card.

## Execution Layer
LLM - OpenAI with brand instructions from `_config/voice.md`.

## Inputs
- `01-intake/output/agent.json`
- `03-portrait/output/portrait.json`
- `_config/voice.md` (brand colors, logo, contact-line rules)

## Process
1. Lay out: portrait, name + title, agency, areas served, specialty,
   years experience, languages, tagline, contact (phone/email).
2. Apply brand: colors #1B4965 / #62B6CB, logo watermark, RTL.
3. Output card content as markdown (rendered to image/PDF downstream).

## Outputs
- `output/profile-card.md` - the card content + layout notes.

## Human gate
Reviewed in stage 05.

## Pitfalls
| Missing portrait image | Render card with text placeholder - note for agent |
| Wrong language direction | Enforce RTL for Hebrew names/addresses |
