# MatchiICM - Production Manifest

Built: 2026-06-28. ICM architecture. Hermes-ready.

## Architecture

```
MatchiICM/
├── AGENTS.md           ← Brain: trigger table, rules, execution layers
├── CONTEXT.md          ← Navigation: phases → workflows
├── MANIFEST.md         ← This file: production status
├── scripts/            ← Deterministic engines + MCP adapters
│   ├── mcp_client.py           JSON-RPC 2.0 client (prod-mcp.nadlanai.org)
│   ├── match.py                Pure match engine (deterministic)
│   ├── lead_score.py           Pure scoring engine (deterministic)
│   ├── cma_analyze.py          CMA math engine (deterministic)
│   ├── render_brochure_v3.py   Museum brochure HTML+PDF
│   ├── mcp_match_run.py        MCP → match → MCP adapter
│   ├── mcp_lead_score_run.py   MCP → score → MCP adapter
│   ├── mcp_crm_run.py          MCP → CRM rules → MCP adapter
│   ├── mcp_brochure_run.py     MCP → brochure → PDF adapter
│   ├── mcp_facebook_scan_run.py Apify → extract → MCP adapter
│   ├── icm_pipeline.py         Master orchestrator
│   └── cold_test.py            Structure verification
├── _config/            ← Stable rules (read-only)
│   ├── voice.md                Brand voice + tone
│   ├── cma-rules.md            CMA formulas + comp selection
│   ├── crm-rules.md            CRM state adjacency matrix
│   ├── lead-rules.md           Scoring thresholds
│   └── match-rules.md          Hard constraints + soft factors
├── _mock/              ← Fallback data (MCP unreachable only)
├── _research/          ← Cached market data
├── phases/             ← 15 ICM workflows (AGENTS.md → trigger → workflow)
│   ├── 1-exclusivity/  ← cma, agent-profile, yad2-import
│   ├── 2-marketing/    ← photo-enhance, brochure, video, social-posts, property-page
│   ├── 3-leads/        ← facebook-scan, lead-scoring, matching, crm-update
│   └── 4-closing/      ← contract-sign, scheduling, reminders
└── docs/               ← Project docs + Confluence references
```

## Execution Layers (every stage declares one)

| Layer | When | Example |
|---|---|---|
| **Script** | Math, calculations, PDF rendering | `py scripts/cma_analyze.py` |
| **MCP** | Data access, image/video gen, calendar | `search_real_estate_properties` |
| **LLM** | Language: Hebrew copy, reports, parsing | Narrative from numbers |
| **Human** | Gate before send/write/publish | Stage 0N-approve |

## Workflow Status

### Phase 1 - Exclusivity 🟢
| Workflow | Data | Engine | Status |
|---|---|---|---|
| cma | MCP `search_real_estate_properties` | Script `cma_analyze.py` | 🟢 Proven 9/10 cold-test |
| agent-profile | Higgsfield MCP | `generate_image` + Soul ID | 🟢 Higgsfield live |
| yad2-import | Apify MCP | Yad2 scraper → MCP `add_new_potential_property` | 🟢 Apify live |

### Phase 2 - Marketing 🟢
| Workflow | Data | Engine | Status |
|---|---|---|---|
| photo-enhance | MCP `get_property_full_details` | Higgsfield `remove_background` + `generate_image` | 🟢 |
| brochure | MCP properties | Script `mcp_brochure_run.py` (Playwright PDF) | 🟢 Pipeline verified |
| video | MCP properties | Higgsfield `generate_video` + `motion_control` | 🟢 |
| social-posts | MCP properties | Higgsfield `generate_image` + `virality_predictor` | 🟢 (publish 🔴 discover) |
| property-page | MCP properties | LLM RTL HTML | 🟡 (hosting 🔴 discover) |

### Phase 3 - Leads 🟢
| Workflow | Data | Engine | Status |
|---|---|---|---|
| facebook-scan | Apify MCP FB scraper | Script `mcp_facebook_scan_run.py` | 🟢 Pipeline verified |
| lead-scoring | MCP `list_leads` | Script `mcp_lead_score_run.py` (engine: `lead_score.py`) | 🟢 Pipeline verified |
| matching | MCP leads + properties | Script `mcp_match_run.py` (engine: `match.py`) | 🟢 Pipeline verified |
| crm-update | MCP `list_leads` | Script `mcp_crm_run.py` (rules: `crm-rules.md`) | 🟢 Pipeline verified |

### Phase 4 - Closing 🟡
| Workflow | Data | Engine | Status |
|---|---|---|---|
| contract-sign | MCP properties + template | LLM fill | 🟡 (signature provider 🔴 discover) |
| scheduling | Google Calendar MCP | `list_events` + `create_event` + `suggest_time` | 🟢 Calendar MCP live |
| reminders | Google Calendar MCP | `list_events` + compose. Send: 🟡 fallback to log | 🟡 (send not yet wired) |

## MCP Endpoints

| Endpoint | Status | Tools |
|---|---|---|
| `https://prod-mcp.nadlanai.org/mcp` | 🟢 Live | search_real_estate_properties, get_property_full_details, list_leads, add_new_potential_property, get_lead_statistics_summary |
| Higgsfield MCP | 🟢 Live | generate_image, generate_video, motion_control, remove_background, virality_predictor, reframe |
| Apify MCP | 🟢 Live | FB group scraper, Yad2 scraper |
| Google Calendar MCP | 🟢 Live | list_events, create_event, update_event, suggest_time |

## 🔴 Discover Queue (tools not yet chosen)

| Capability | Needed by | Options |
|---|---|---|
| Digital signature (IL) | contract-sign | Hatima, DocuSign, SignNow |
| Social posting API | social-posts publish | Meta Graph API, Buffer |
| Page hosting | property-page | Vercel, Netlify, S3+CDN |

## Quick Start

```bash
cd MatchiICM
pip install playwright pypdf
playwright install chromium

# Dry-run all pipeline stages (no DB writes)
py scripts/icm_pipeline.py

# Run specific stage
py scripts/mcp_match_run.py

# Write to production DB
py scripts/icm_pipeline.py --write

# Render brochure for property #2
py scripts/mcp_brochure_run.py --property-id 2

# Scan Facebook groups (needs APIFY_TOKEN)
py scripts/mcp_facebook_scan_run.py --fb-group-url "https://www.facebook.com/groups/..."
```

## Requirements

- Python 3.11+
- MCP endpoint reachable: `https://prod-mcp.nadlanai.org/mcp`
- User ID: `nadlanai.solutions@gmail.com`
- Playwright + Chromium (for brochure PDF)
- Apify token (for FB/Yad2 scrape)
