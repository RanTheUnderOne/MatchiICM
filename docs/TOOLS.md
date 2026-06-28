# MatchiICM - Per-Stage Tool Map

What every stage needs: mock (now), real (later), tool status, what action triggers the tool.
**Mock shape = contract.** Replace mock read line → real adapter outputs same shape → stage logic unchanged.

Legend:
- 🟢 **Live** - MCP/API available, can wire immediately
- 🟡 **Chosen** - tool identified, not yet wired
- 🔴 **Discover** - tool NOT chosen, needs web-research → present → approve → wire
- ⚪ **Deterministic script** - runs locally, no external tool
- ➖ **LLM only** - no external tool needed (copywriting, assembly, parsing)

---

## Phase 1 - Exclusivity (בלעדיות)

### cma (5 stages)
| Stage | Action | Mock tool (now) | Real tool (later) | Tool status | What the tool does |
| --- | --- | --- | --- | --- | --- |
| 01-subject | Identify subject property | Read `_mock/properties.json` | **Supabase** REST / MCP `search_real_estate_properties` | 🟡 | Look up property by address/id |
| 02-research | Gather comps + neighborhood stats | Read `_research/*.md` cache | **nadlan.gov.il** CARMAN API (sold transactions) + **Yad2/Madlan** via Apify scrape | 🟡 | Fetch sold prices last 18mo + active listings + trend |
| 03-analyze | Deterministic CMA math | `py scripts/cma_analyze.py` | same script | ⚪ built+tested | Adjust comp prices to subject → value range + position + confidence |
| 04-report | Narrative report in Hebrew | LLM | LLM + `_config/voice.md` | ➖ | Write the report from the 03 numbers |
| 05-approve | Human gate | - | - | ➖ | Agent reviews, edits, sends |

### agent-profile (5 stages)
| Stage | Action | Mock tool (now) | Real tool (later) | Tool status | What the tool does |
| --- | --- | --- | --- | --- | --- |
| 01-intake | Collect agent details | Read `_mock/agent.json` | **Supabase** / onboarding questionnaire | 🟡 | Load agent name, phone, license, photo_refs |
| 02-soul-id | Train consistent identity | Write mock brief | **Higgsfield** `show_characters(action:train)` + `generate_image` | 🟢 | Upload 5-20 agent photos → train Soul ID → returns `soul_id` |
| 03-portrait | Professional headshot | Write mock descriptor | **Higgsfield** `generate_image` (headshot preset + `soul_id`) | 🟢 | Generate headshot(s) with locked face |
| 04-profile-card | Branded card assembly | LLM | LLM + `_config/voice.md` (brand palette) | ➖ | Assemble card: photo + name + title + contact |
| 05-approve | Human gate | - | - | ➖ | Agent picks/approves portrait + card |

### yad2-import (5 stages)
| Stage | Action | Mock tool (now) | Real tool (later) | Tool status | What the tool does |
| --- | --- | --- | --- | --- | --- |
| 01-fetch | Pull raw listings | Read `_mock/yad2-raw.json` | **Apify** Yad2 scraper actor / Yad2 native API | 🟡 | Scrape active listings → raw JSON |
| 02-structure | Normalize messy Hebrew text → clean fields | LLM | LLM + parsing rules | ➖ | Parse "2.75 מיליון"→2,750,000, "קומה 3 מתוך 5"→floor, sale vs rent |
| 03-enrich | Add price/sqm, neighborhood context | Read `_research/*.md` | **Madlan** / **nadlan.gov.il** via Apify | 🟡 | Enrich with neighborhood avg price/sqm, distances |
| 04-validate | Red flags + completeness score | LLM | LLM + checks | ➖ | Flag missing size, suspicious price |
| 05-approve | Human gate → inventory | - | **Supabase** upsert (approved only) | 🟡 | Write approved listings to inventory |

---

## Phase 2 - Marketing (שיווק)

### photo-enhance (4 stages)
| Stage | Action | Mock tool (now) | Real tool (later) | Tool status | What the tool does |
| --- | --- | --- | --- | --- | --- |
| 01-intake | Collect source photos | Read `_mock/photos.json` | **Supabase** storage / agent upload widget | 🟡 | Load photos for the property + flagged issues |
| 02-declutter | Remove clutter + relight | Write mock briefs | **Higgsfield** `remove_background` + `generate_image` (inpaint) | 🟢 | Remove furniture/clutter/personal items + correct lighting |
| 03-stage | Virtual furniture for empty rooms | Write mock staging briefs | **Higgsfield** `generate_image` (staging preset) | 🟢 | Furnish empty rooms, brand palette from `voice.md` |
| 04-approve | Human gate | - | - | ➖ | Agent approves publishable set |

### brochure (4 stages)
| Stage | Action | Mock tool (now) | Real tool (later) | Tool status | What the tool does |
| --- | --- | --- | --- | --- | --- |
| 01-gather | Collect property facts + best photos | Read `_mock/properties.json` + `_mock/photos.json` + `_mock/agent.json` | **Supabase** (property + agent + photos) | 🟡 | Load facts + select 3-5 best photos |
| 02-copy | Write HE + EN copy | LLM | LLM + `_config/voice.md` | ➖ | Headline + highlights + blurb, both languages |
| 03-layout | Assemble one-pager | LLM → markdown | LLM → PDF render | ➖ | Place copy + photos + contact in branded template |
| 04-approve | Human gate | - | - | ➖ | Export approved |

### video (4 stages)
| Stage | Action | Mock tool (now) | Real tool (later) | Tool status | What the tool does |
| --- | --- | --- | --- | --- | --- |
| 01-script | Write shot-by-shot script | LLM | LLM + `_config/voice.md` | ➖ | 5-8 shots: hook, exterior, rooms, standout, agent outro |
| 02-generate | Generate/animate each shot | Write mock briefs | **Higgsfield** `generate_video` + `motion_control` (agent shots: `soul_id`) | 🟢 | Generate video clips per shot from stills / script |
| 03-assemble | Sequence clips + captions + outro | Write mock manifest | Video editor/render + `reframe` for 9:16 | 🟢 reframe / 🔴 editor | Stitch clips, add captions, brand outro card |
| 04-approve | Human gate | - | - | ➖ | Approve before publish |

### social-posts (4 stages)
| Stage | Action | Mock tool (now) | Real tool (later) | Tool status | What the tool does |
| --- | --- | --- | --- | --- | --- |
| 01-brief | Pick subject + angle + platforms | Read `_mock/properties.json` + `_mock/agent.json` | **Supabase** (property + agent) | 🟡 | Choose property/agent + angle + FB/IG |
| 02-generate | Make post image(s) + caption | Write mock briefs | **Higgsfield** `generate_image` (brand/Soul ID preset) + LLM caption | 🟢 | Generate image + write caption (right length/hashtags) |
| 03-predict | Score predicted performance | Write mock scores | **Higgsfield** `virality_predictor` | 🟢 | Score hook strength, retention risk, predicted engagement |
| 04-approve | Human gate → publish | - | **Posting API** (FB/IG) - 🔴 discover+approve | 🔴 | Publish posts to social platforms |

### property-page (4 stages)
| Stage | Action | Mock tool (now) | Real tool (later) | Tool status | What the tool does |
| --- | --- | --- | --- | --- | --- |
| 01-content | Assemble page content | Read `_mock/properties.json` + reuse approved photos/copy from other workflows | **Supabase** (property + photos + copy) | 🟡 | Collect facts, sections, photos, contact |
| 02-build | Generate public page | LLM → markdown/HTML | Deploy to hosting → get URL - 🔴 discover+approve | 🔴 | Render RTL-branded page, publish, return URL |
| 03-chat | Build grounded Q&A for page chat | LLM → fact sheet | Chat widget/API with grounded-only rule | 🔴 | Turn facts into allowed Q&A; unknown → defer to agent |
| 04-approve | Human gate | - | - | ➖ | Approve page + chat boundary before public |

---

## Phase 3 - Leads (לידים)

### facebook-scan (4 stages)
| Stage | Action | Mock tool (now) | Real tool (later) | Tool status | What the tool does |
| --- | --- | --- | --- | --- | --- |
| 01-fetch | Pull raw group posts | Read `_mock/fb-groups-raw.json` | **FB source** - Apify FB group scraper OR Graph API - 🔴 discover+approve | 🔴 | Scrape groups for posts containing buy/rent intent |
| 02-extract | Detect intent + parse fields | LLM | LLM + parsing rules | ➖ | Classify intent, parse rooms/budget/city/timeline from free text |
| 03-dedupe | Remove spam + duplicates | Read `_mock/leads.json` (existing inventory) | **Supabase** leads table | 🟡 | Match by name+text similarity against existing leads |
| 04-approve | Human gate → inventory | - | **Supabase** upsert | 🟡 | Write approved new leads to inventory |

### lead-scoring (4 stages)
| Stage | Action | Mock tool (now) | Real tool (later) | Tool status | What the tool does |
| --- | --- | --- | --- | --- | --- |
| 01-load | Load leads | Read `_mock/leads.json` | **Supabase** leads table | 🟡 | Load full lead set |
| 02-score | Deterministic 0-100 per lead | `py scripts/lead_score.py` | same script | ⚪ built+tested | Score by timeline+budget+intent+recency+stage, explainable |
| 03-bucket | Hot/warm/cold by thresholds | `scripts/lead_score.py` outputs buckets inline | same | ⚪ | Thresholds from `_config/lead-rules.md`: ≥70 hot, 40-69 warm, <40 cold |
| 04-approve | Human gate → prioritized list | - | - | ➖ | Agent reviews priorities |

### matching (4 stages)
| Stage | Action | Mock tool (now) | Real tool (later) | Tool status | What the tool does |
| --- | --- | --- | --- | --- | --- |
| 01-load | Load leads + properties | Read `_mock/leads.json` + `_mock/properties.json` | **Supabase** (leads + properties) | 🟡 | Build `{"leads":[...], "properties":[...]}` for match engine |
| 02-match | Deterministic fit score per pair | `py scripts/match.py` | same script | ⚪ built+tested | Hard constraints + soft factors → fit 0-100 per (lead, property) |
| 03-rank | Top 3 matches per lead + per property | `scripts/match.py` outputs ranked inline | same | ⚪ | Top-by-lead + top-by-property, tie-break lower price |
| 04-approve | Human gate → outreach suggestions | - | - | ➖ | Agent approves which matches to act on |

### crm-update (4 stages)
| Stage | Action | Mock tool (now) | Real tool (later) | Tool status | What the tool does |
| --- | --- | --- | --- | --- | --- |
| 01-load | Load current lead states | Read `_mock/leads.json` | **Supabase** leads table | 🟡 | Load leads with current `stage` |
| 02-transition | Validate legal stage moves | Read `_mock/crm-requests.json` (fixture) + `_config/crm-rules.md` | Chat intent (Hermes parses "שנה סטטוס L-1 ל-contact") | ➖ | Check adjacency matrix, reject illegal jumps |
| 03-write | Apply transitions + audit log | Write mock files | **Supabase** update leads + insert audit table | 🟡 | Atomically update stage + append audit row |
| 04-approve | Human gate | - | - | ➖ | Confirm before CRM write |

---

## Phase 4 - Closing (סגירה)

### contract-sign (4 stages)
| Stage | Action | Mock tool (now) | Real tool (later) | Tool status | What the tool does |
| --- | --- | --- | --- | --- | --- |
| 01-prepare | Fill template with deal facts | Read `_mock/contract-template.md` + `_mock/properties.json` + `_mock/agent.json` | Legal-approved template + **Supabase** (deal record) | 🟡 | Fill {{placeholders}} from property.owner + agent; flag blanks |
| 02-send | Send for digital signature | Write mock send request | **Signature provider** - 🔴 discover+approve (Hatima / DocuSign / SignNow) | 🔴 | Send draft to recipient(s) via provider's API |
| 03-track | Track signature status | Write mock status | Same provider's poll/webhook API | 🔴 | Poll status: pending / signed / declined |
| 04-confirm | Human confirm + archive | - | - | ➖ | Agent confirms completion, archives signed doc |

### scheduling (4 stages)
| Stage | Action | Mock tool (now) | Real tool (later) | Tool status | What the tool does |
| --- | --- | --- | --- | --- | --- |
| 01-request | Capture meeting request | Read `_mock/scheduling-request.json` (fixture) + `_mock/leads.json` | Chat intent (Hermes parses "קבע צפייה") | ➖ | Resolve lead + property + window + duration |
| 02-slots | Compute free slots | Read `_mock/calendar.json` → subtract busy from window | **Google Calendar MCP** `list_events` + `suggest_time` | 🟢 | Query busy blocks → propose free slots |
| 03-book | Tentatively book chosen slot | Write mock booking | **Google Calendar MCP** `create_event` | 🟢 | Re-check free → create event with attendees |
| 04-confirm | Human + invitee confirm | - | **Google Calendar MCP** send invites + track RSVP | 🟢 | Confirm and notify invitee |

### reminders (4 stages)
| Stage | Action | Mock tool (now) | Real tool (later) | Tool status | What the tool does |
| --- | --- | --- | --- | --- | --- |
| 01-load | Find upcoming events needing reminder | Read `_mock/calendar.json` → select `reminder_sent=false` in window | **Google Calendar MCP** `list_events` | 🟢 | Query showings in next 24h where reminder not yet sent |
| 02-compose | Write reminder message (HE) | LLM | LLM + `_config/voice.md` | ➖ | Per event: time, address, agent contact, reschedule option |
| 03-send | Send via WhatsApp | Write mock send-log | **Evolution API** (WhatsApp message) | 🟡 | Send text to lead's phone via WA |
| 04-confirm | Human gate + mark reminded | - | **Google Calendar MCP** `update_event` (set `reminder_sent` extended property) or update in store | 🟢 | Mark `reminder_sent=true`, prevent double-remind |

---

## Summary by Tool

| Tool | Where needed | Status | Action required |
| --- | --- | --- | --- |
| **Higgsfield MCP** (image/video/virality) | agent-profile, photo-enhance, video, social-posts (7 stages) | 🟢 Live | **Can wire now** - replace mock briefs with real `generate_image`/`generate_video`/`motion_control`/`remove_background`/`virality_predictor` calls |
| **Google Calendar MCP** | scheduling, reminders (5 stages) | 🟢 Live | **Can wire now** - replace `_mock/calendar.json` reads with `list_events`/`create_event`/`suggest_time` |
| **Supabase** | Properties + leads + agents + photos + CRM + audit (across all phases, ~15 stages) | 🟡 Chosen | Set up tables matching mock shapes. Swap read/write lines. Largest single swap. |
| **3 Deterministic Scripts** (`cma_analyze`, `lead_score`, `match`) | cma, lead-scoring, matching (3 stages) | ⚪ Built | **Done.** No swap needed - same scripts in mock and real. |
| **Apify** (Yad2/Madlan/nadlan.gov.il) | yad2-import, cma (3 stages) | 🟡 Chosen | Wrap each actor in an adapter → same JSON shape as `_mock/yad2-raw.json` and `_research/*.md` |
| **Evolution API** (WhatsApp) | reminders/03-send | 🟡 Chosen | WhatsApp message API. Integration endpoint + auth TBD. |
| **FB Source** (scraper / Graph API) | facebook-scan/01-fetch | 🔴 Discover | Research: Apify FB actor vs Meta Graph API. Compare: cost, ToS risk, auth complexity. Present to user. |
| **Signature Provider** | contract-sign/02-send, 03-track | 🔴 Discover | Research: Hatima (IL) vs DocuSign vs SignNow. Compare: IL legal compliance, API quality, pricing. Present |
| **Posting API** (FB/IG) | social-posts/04-approve | 🔴 Discover | Research: Meta Graph API posting vs Buffer/Hootsuite API. Compare: auth, rate limits, platform coverage. |
| **Page Host** | property-page/02-build | 🔴 Discover | Research: Vercel/Netlify deploy API vs Supabase hosting vs generic S3+CDN. |
| **LLM only** (no tool) | Copy, layout, parsing, assembly (~10 stages) | ➖ | No external tool. Hermes LLM does the work directly from `_config/voice.md` + stage inputs. |

## First Tools to Wire (recommended order)
1. **Higgsfield** (live) - creates actual portraits, edited photos, videos, virality scores. Visual proof the pipeline is real.
2. **Google Calendar** (live) - actual scheduling + reminders with real events.
3. **Supabase** - connects everything to a real database, the backbone swap.
4. **Apify** - real market data flowing into CMA + Yad2 import.
5. **Evolution API** - real WhatsApp sends.
6. **Discover 4 tools** (FB source, signature, posting API, page host) - research → present → approve → wire.
