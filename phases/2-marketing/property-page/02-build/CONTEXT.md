# Stage 02 - Build

Generate the public page.

## Inputs
- `01-content/output/page-content.json`
- `_config/voice.md`

## Process (LLM)
1. LLM renders a single responsive HTML page (RTL-aware), brand palette from `_config/voice.md`.
2. Write `output/page.html`.
3. Hosting target not yet chosen - **🔴 discover** and wire before production.

## Outputs
- `output/page.html`

## Human gate
Show the page. Approve before chat wiring.

## Audit
Run before writing `output/page.html`. Revise until all pass.

- [ ] RTL layout renders correctly (Hebrew text right-aligned)
- [ ] Brand colors from `_config/voice.md` applied
- [ ] All facts from `page-content.json` - no invented claims
- [ ] Responsive: readable on mobile (320px) and desktop
- [ ] Agent contact visible without scrolling
- [ ] No broken image references

## Pitfalls
| No hosting target | 🔴 discover and wire hosting before production |
