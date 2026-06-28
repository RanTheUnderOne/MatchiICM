# Stage 02 - Copy

Write Hebrew + English brochure copy.

## Inputs
- `01-gather/output/brochure-data.json`
- `_config/voice.md` (brand voice)

## Process (LLM)
1. Headline + 3-5 highlight bullets + short blurb - in Hebrew.
2. Mirror the same in English (no new facts, no drift).
3. Use ONLY facts from 01. Flag anything missing instead of inventing.
4. LLM generates copy using brand voice from `_config/voice.md`.

## Outputs
- `output/copy.json` - {he:{headline,bullets[],blurb}, en:{...}}.

## Human gate
Show both languages side by side. Approve before layout.

## Audit
Run before writing `output/copy.json`. Revise until all pass.

- [ ] Every fact traceable to `brochure-data.json` - no invented amenities
- [ ] HE and EN say exactly same claims (cross-read both)
- [ ] Headline is one line, punchy, no clichés
- [ ] Bullets are facts, not adjectives
- [ ] Brand voice matches `_config/voice.md` tone
- [ ] Agent contact line from `_mock/agent.json` included

## Pitfalls
| Invented amenity | Only use facts from 01 |
| HE/EN drift | Both languages = same claims |
