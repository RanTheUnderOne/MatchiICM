# MatchiICM - Integrations (Planned, NOT connected yet)

Records HOW each data source will be connected in the future. **Right now
everything is mock** (`_mock/`, `_research/`). Nothing below is wired. This is
the target map so when we connect sources one-by-one, the method is decided.

## Swap Map - "replace WHAT with WHAT to make it live"
One row per data source. To go live: open the named stage's `CONTEXT.md`, find
its "Process (MOCK now)" step, and replace ONLY the mock read line with the real
call. The mock SHAPE is the contract - the real adapter must output the same shape.

### Phase 1 - Exclusivity
| Mock file (now) | Replace with (real later) | Stage(s) that read it |
| --- | --- | --- |
| `_mock/yad2-raw.json` | **Apify** Yad2 scraper actor / Yad2 native API | yad2-import/01-fetch |
| `_research/*.md` (comps) | nadlan.gov.il API + yad2 + madlan (Apify/scrape) | cma/02-research, yad2-import/03-enrich |
| `_mock/properties.json` | Supabase REST / platform MCP | cma/01-subject, brochure, video, property-page, matching |
| `_mock/agent.json` | onboarding questionnaire / Supabase | agent-profile/01-intake, social, brochure, contract |
| mock briefs | Higgsfield MCP (**already live**) | agent-profile 02-soul-id / 03-portrait |

### Phase 2 - Marketing
| Mock file (now) | Replace with (real later) | Stage(s) that read it |
| --- | --- | --- |
| `_mock/photos.json` | agent upload / property storage (Supabase) | photo-enhance/01-intake, brochure/01-gather |
| mock edit/staging briefs | Higgsfield `remove_background`, `generate_image`, `outpaint_image` (**live**) | photo-enhance/02-declutter, 03-stage |
| mock video briefs | Higgsfield `generate_video`, `motion_control`, `reframe` (**live**) | video/02-generate, 03-assemble |
| mock post score | Higgsfield `virality_predictor` (**live**) | social-posts/03-predict |
| n/a (publish) | **posting API** (FB/IG/X) - NOT chosen, discover+approve | social-posts/04-approve |
| n/a (page host) | hosting/deploy target - NOT chosen, discover+approve | property-page/02-build |

### Phase 3 - Leads
| Mock file (now) | Replace with (real later) | Stage(s) that read it |
| --- | --- | --- |
| `_mock/fb-groups-raw.json` | **Apify** FB group scraper / Graph API - discover+approve | facebook-scan/01-fetch |
| `_mock/leads.json` | Supabase leads table / platform MCP | facebook-scan/03-dedupe, lead-scoring, matching, crm-update, scheduling |
| `scripts/lead_score.py` (**built + tested**) | already deterministic - no swap needed | lead-scoring/02-score |
| `scripts/match.py` (**built + tested**) | already deterministic - no swap needed | matching/02-match |
| mock CRM write | Supabase update + audit table | crm-update/03-write |

### Phase 4 - Closing
| Mock file (now) | Replace with (real later) | Stage(s) that read it |
| --- | --- | --- |
| `_mock/contract-template.md` | legal-approved template | contract-sign/01-prepare |
| mock send/track | **digital-signature provider** (Hatima/DocuSign-class) - NOT chosen, discover+approve | contract-sign/02-send, 03-track |
| `_mock/calendar.json` | Google Calendar MCP (`create_event`/`list_events`/`suggest_time`) | scheduling/02-slots, 03-book, reminders/01-load |
| mock send-log | Evolution API (WhatsApp) | reminders/03-send |

### Deterministic scripts (no LLM math) - all BUILT + tested
| Script | Status | Used by |
| --- | --- | --- |
| `scripts/cma_analyze.py` | ✅ built + tested | cma/03-analyze |
| `scripts/lead_score.py` | ✅ built + tested (L-4=95,L-1=87,L-2=82,L-3=75) | lead-scoring/02-score |
| `scripts/match.py` | ✅ built + tested (6 scored, 14 blocked on mock) | matching/02-match |

### Tools NOT chosen yet (require Capability-Driven Discovery - see below)
- Social posting API (Phase 2 social-posts publish)
- Page hosting/deploy (Phase 2 property-page)
- Facebook group source - Apify actor vs Graph API (Phase 3 facebook-scan)
- Digital-signature provider (Phase 4 contract-sign)

## Connection Pattern (when we wire each one)
1. The stage's `CONTEXT.md` already names the source as "mock now → real later".
2. To connect: replace ONLY the data-source read line with the real call
   (Apify run + fetch dataset, or native API GET). Stage logic stays unchanged.
3. Cache the result into `_research/<area>.md` (dated) so we "research once".
4. Re-run the workflow against real data; confirm same control flow.
5. Log the connection in the Build Log (Confluence 47120385) + flip status here.

## Apify Notes (for later)
- Each portal = one Apify actor run → produces a dataset → fetch as JSON.
- Wrap each actor in a tiny adapter that outputs the SAME shape the mock used
  (e.g. yad2 adapter → same fields as `_mock/yad2-raw.json`). Mock shape is the
  contract; the adapter conforms to it. That keeps stages untouched.

## Capability-Driven Tool Discovery (factory rule)
Tools (Higgsfield/Apify/META/...) are examples, not a fixed list. When a stage
needs a capability and no tool is available:
1. Web-research candidate tools/APIs.
2. Present options + tradeoffs (cost, fit, auth, risk) to the human.
3. On approval → wire it and record it in this table. Never adopt silently.
(See Confluence: ICM Factory protocol, page 47448066.)

## Status
| Source | Connected? |
| --- | --- |
| Everything | ❌ mock - by design, until logic proven |
| Higgsfield MCP | available, not yet wired into stages |
| Google Calendar MCP | available, not yet wired (Phase 4 scheduling/reminders) |
| Phases 2-4 | scaffold + mock built (12 workflows, 4 stages each). Not run, not wired. |
