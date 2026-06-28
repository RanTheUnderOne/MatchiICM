# MatchiICM - Project Documentation

Rebuild of the Matchi real-estate product (matchi.co.il) as a library of
ICM workflows that run on a Hermes agent. The chat stays in Hermes/WhatsApp.
Each Matchi feature becomes a deterministic ICM pipeline triggered mid-chat.

## Goal

Feed this repo to Hermes → it reads `AGENTS.md` → during a normal WhatsApp
conversation it detects intent (e.g. "תכין ברושור") → starts the matching ICM
workflow → runs stages → returns result in chat. One agent, many workflows.

## The Three Layers (ICM)

| Layer | Here | Answers |
| --- | --- | --- |
| Map | `AGENTS.md` + `CONTEXT.md` | Where am I? Which workflow? |
| Rooms | `phases/*/<workflow>/<stage>/CONTEXT.md` | What do I do at this stage? |
| Tools | `_config/`, `_mock/` | What rules / data do I use? |

## Build Strategy

1. **Mock first.** Every stage that would call MCP/Supabase/Evolution/Yad2
   reads from `_mock/` instead. Prove the workflow logic + control flow.
2. **Verify control.** Run each workflow against mock data, confirm stage
   handoffs, freshness guards, and human gates behave correctly.
3. **Connect one-by-one.** Once a workflow is proven, swap its mock read for
   the real API call. Only the data-source line changes; stage logic stays.

## Source → Target Mapping (Matchi feature → ICM workflow)

| Matchi Phase | Feature | ICM Workflow | Real API (later) |
| --- | --- | --- | --- |
| 1 Exclusivity | CMA report | `1-exclusivity/cma` | market data + Yad2 |
| 1 Exclusivity | Agent profile + portrait | `1-exclusivity/agent-profile` | image gen |
| 1 Exclusivity | Yad2 auto-import | `1-exclusivity/yad2-import` | Yad2 scrape |
| 2 Marketing | Furniture removal / staging | `2-marketing/photo-enhance` | image AI |
| 2 Marketing | Brochure HE/EN | `2-marketing/brochure` | doc gen |
| 2 Marketing | Property video | `2-marketing/video` | video gen |
| 2 Marketing | Social posts | `2-marketing/social-posts` | post APIs |
| 2 Marketing | Public property page + chat | `2-marketing/property-page` | hosting + chat |
| 3 Leads | Facebook group scan | `3-leads/facebook-scan` | FB scrape |
| 3 Leads | Lead scoring | `3-leads/lead-scoring` | Supabase |
| 3 Leads | Lead↔property matching | `3-leads/matching` | match engine |
| 3 Leads | CRM kanban update | `3-leads/crm-update` | Supabase |
| 4 Closing | Digital signature | `4-closing/contract-sign` | Hatima AI |
| 4 Closing | Scheduling | `4-closing/scheduling` | calendar |
| 4 Closing | Reminders | `4-closing/reminders` | Evolution (WA) |

## Status Log

| Date | Change |
| --- | --- |
| 2026-06-26 | Folder tree, root AGENTS.md/CONTEXT.md, project doc created. Phase 1 in build (mock). Phases 2-4 scaffold. |
| 2026-06-26 | Reliability research (Higgsfield, nadlan.gov.il). Added `_research/` cache layer + reliability patterns. Phase 1 fully built (mock): cma (5 stages + deterministic `scripts/cma_analyze.py`, tested), agent-profile (5 stages, Soul ID), yad2-import (5 stages). |
| 2026-06-26 | Confluence doc system (parent 47087617 + 5 child pages). `docs/INTEGRATIONS.md` (Apify/API plan). **Cold context-free subagent test: 8.5/10** - a zero-context agent ran the full cma pipeline from AGENTS.md alone, stopped at human gate, same result. Fixed 5 gaps it found: (1) `python`→`py` on Windows, (2) `_run.json` owner-stage contradiction, (3) `_run.json` schema drift, (4) `renovated` now explicit in `_mock/properties.json` + stage-01, (5) `comps.json` schema declared in 02-research. Re-verified engine. |
| 2026-06-27 | **Phases 2-4 scaffold built (mock).** 12 workflows × 4 stages = 60 stage `CONTEXT.md` + 12 workflow `CONTEXT.md`, each with a mock→real swap table + reliability contract + human gates. New mock data: `_mock/photos.json`, `fb-groups-raw.json`, `leads.json`, `calendar.json`, `contract-template.md`. Full **Swap Map** added to `docs/INTEGRATIONS.md`. Not run, not wired - structure + mock only. |
| 2026-06-27 | **Built + tested 2 deterministic scripts** (Phase 3 cores, copy `cma_analyze.py` pattern): `scripts/lead_score.py` (reads `_config/lead-rules.md` → scored + buckets; mock: L-4=95,L-1=87,L-2=82,L-3=75 all hot) and `scripts/match.py` (reads `_config/match-rules.md` → 20 pairs, 6 scored/14 blocked; L-2→P-1004 rental + L-3→P-1005 חדרה now resolve). Stages 02-score/02-match CONTEXT flipped from "by hand" → run the script. Phase 3 scoring/matching now deterministic + reproducible, not LLM-guessed. |
| 2026-06-27 | **Parallel cold e2e tests (3 agents, Phases 2/3/4).** Each agent ran all workflows context-free, wrote output, graded gaps. Scores: photo-enhance 6, brochure 8, video 5, social-posts 8, property-page 9, facebook-scan 7, lead-scoring 4, matching 5, crm-update 6, contract-sign 4, scheduling 8, reminders 6. **Fixed all gaps:** (1) photo-enhance 02→03 handoff (empty rooms now pass through with `needs_staging`), (2) brochure + property-page: added `agent.json` as declared input, (3) video: `soul_id` added to `_mock/agent.json`, (4) social-posts: clarified WA not in scope, (5) created `_config/lead-rules.md` + `match-rules.md` + `crm-rules.md` (deterministic rules were missing - biggest gap), (6) added rental property P-1004 + חדרה property P-1005 to `_mock/properties.json`, (7) added `owner` + `exclusivity_months` + `fee_pct` + `license` to mock so contract-sign fills all placeholders, (8) fixed `agent_id` A-1→A-01 in calendar, (9) moved S-1 showing to within 24h, (10) denormalized lead contact into showing, (11) added `_mock/crm-requests.json` + `scheduling-request.json` fixtures, (12) created 60 per-stage `output/` dirs (were missing). |

## Reliability Patterns (applied to every workflow)

1. **Source grounding** - every fact cites where it came from (nadlan.gov.il / yad2 / madlan).
2. **`_research/` cache** - fetch real data once, store dated markdown, reuse. The "research once" model.
3. **Deterministic core** - math lives in a script (`cma_analyze.py`), not the LLM. Reproducible.
4. **Confidence + range** - never false precision. CMA reports a range + High/Medium/Low band.
5. **Self-verify before gate** - agent checks its numbers trace to a source before the human sees it.
6. **Higgsfield = real tool** - Soul ID locks one agent face across all visuals.
7. **Human gate every stage** - EU AI Act oversight + quality boundary.

## Higgsfield Mapping (real later, MCP already available)

| Use | Higgsfield capability | MCP tool |
| --- | --- | --- |
| Agent portrait (consistent face) | Soul ID / AI Headshot | `generate_image` |
| Furniture removal / staging | AI Product Photography, remove_background, outpaint | `generate_image`, `remove_background`, `outpaint_image` |
| Property video | 30+ models (Veo/Kling/Sora) | `generate_video`, `motion_control` |
| Social posts | 60+ style presets | `generate_image` |
| Post performance | virality_predictor | `virality_predictor` |

## Conventions

- Plain text / markdown only. Git = deploy. Folder = agent.
- Stage outputs are git-ignored runtime artifacts - never committed.
- Human gate after every stage. No autonomous binding decisions.
- Decompose each feature into atomic actions → one action ≈ one stage.

## Integrations (planned, not connected)

Real sources (Yad2, Madlan, nadlan.gov.il, other portals) will connect later via
**Apify actors** or **native APIs**. All mock now. Method map: `docs/INTEGRATIONS.md`.
Key rule: the mock data SHAPE is the contract - real adapters conform to it, so
stage logic never changes when we swap mock → real.

## Documentation System (Confluence - NP space)

Mirror of this project. Parent folder under the ICM hub. Keep both in sync:
after each work session, append a dated entry to the **Build Log** (Confluence)
and update the status log below.

| Page | ID | Purpose |
| --- | --- | --- |
| MatchiICM (parent) | 47087617 | Overview, status, links |
| Build Log (Reproducible) | 47120385 | Append-only session log + reproduce steps |
| Architecture & Decisions | 47153153 | Layers, structure, decisions |
| Phase 1 - Exclusivity | 47185921 | Workflows, stages, demo results |
| Reliability Patterns & Higgsfield | 47218689 | Credibility patterns + tool mapping |
| Integrations (Planned) | 47022082 | Apify/API connection plan + discovery rule |
| Per-Stage Tool Map | TBD | Every stage → tool → status (🟢live/🟡chosen/🔴discover/⚪script/➖LLM) |
| ICM Factory - Loop-Coding Protocol | 47448066 | Claude Code loop for manufacturing ICMs |

**Update protocol (every session):**
1. Append `## YYYY-MM-DD · Session N` to Build Log (47120385): Goal · Actions · Verify · Result · Gotchas.
2. Update the relevant phase page if a workflow changed.
3. Update the parent status table if a phase status changed.

## References

- ICM on Hermes: Confluence page 43253761
- OKF + ICM + Hermes: Confluence page 44564507
- ICM for Real Estate (capabilities/ROI): Confluence page 42860545
- POC repo: github.com/RanTheUnderOne/RealEstateICM
- ICM paper: arXiv:2603.16021
