# Stage 02 — Generate

Make post image(s) + caption per platform.

## Inputs
- `01-brief/output/brief.json`
- `_config/voice.md`

## Process (OpenAI + LLM)
1. Per platform, build an image prompt from facts + brand style.
2. Call OpenAI `generate_image` (GPT Image 1, 1024x1024).
3. LLM writes Hebrew caption (right length, hashtags, brand voice).
4. Write `output/posts.json` — [{platform, image_prompt, image_path, caption, status}].

## Environment
- `OPENAI_API_KEY` — injected by Hermes. Never stored in workspace.

## Outputs
- `output/posts.json`

## Human gate
Show variants. Continue to prediction.

## Audit
Run before writing `output/posts.json`. Revise until all pass.

- [ ] Every caption claim from `brief.json` facts — no invented selling points
- [ ] Caption fits platform character limit (FB 632, IG 2200)
- [ ] Hashtags: 3-5, Hebrew + English mix, relevant
- [ ] Brand voice from `_config/voice.md` — consistent across posts
- [ ] Image prompt matches caption topic (same feature highlighted)

## Pitfalls
| Caption claims not in facts | Use only true facts from brief/property |
| API timeout | Fallback to mock image briefs in `_mock/` |
