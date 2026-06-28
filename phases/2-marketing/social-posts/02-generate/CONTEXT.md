# Stage 02 - Generate

Make post image(s) + caption per platform.

## Inputs
- `01-brief/output/brief.json`
- `_config/voice.md`

## Process (MCP + LLM)
1. Per platform, build an image brief from facts.
2. Call Higgsfield MCP `generate_image` with brand/Soul ID preset.
3. LLM writes Hebrew caption (right length, hashtags, brand voice).
4. Write `output/posts.json` - [{platform, image_brief, image_path, caption, status}].

## Outputs
- `output/posts.json`

## Human gate
Show variants. Continue to prediction.

## Audit
Run before writing `output/posts.json`. Revise until all pass.

- [ ] Every caption claim from `brief.json` facts - no invented selling points
- [ ] Caption fits platform character limit (FB 632, IG 2200)
- [ ] Hashtags: 3-5, Hebrew + English mix, relevant
- [ ] Brand voice from `_config/voice.md` - consistent across posts
- [ ] Image brief matches caption topic (same feature highlighted)

## Pitfalls
| Caption claims not in facts | Use only true facts from brief/property |
| MCP outage | Fallback to mock image briefs in `_mock/` |
