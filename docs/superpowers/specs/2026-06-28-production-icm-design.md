# Production ICM - Design Spec

## Goal
Turn MatchiICM into production-ready ICM that Hermes agent reads and runs.
Pure ICM architecture: `AGENTS.md` + `CONTEXT.md` only.

## Architecture (from Confluence)

Three execution layers in every stage:

| Layer | What | When |
|---|---|---|
| **Script** | Deterministic math (match, score, CMA) | Numbers, rules, calculations |
| **MCP** | Real data access | Properties, leads, CRM, calendar, FB scrape |
| **LLM** | Language (copy, translation, reports) | Text from numbers, Hebrew narrative |

Plus **Adapter** (`mcp_*_run.py`): MCP → engine → MCP. Handles I/O.

## What Changes

### Cut
- `BOT.md` - not ICM. AGENTS.md + CONTEXT.md is enough
- 60+ scaffold CONTEXT.md with no real connections - replace with concise stage files

### Update
- Every stage CONTEXT.md: mock path → real MCP/script path
- AGENTS.md: update trigger table, add production rules
- Root CONTEXT.md: navigation to workflows

### Keep
- `scripts/` - all engines work, no changes
- `_config/` - stable rules, no changes
- `_mock/` - fallback data, keep as backup
- `docs/PROJECT.md` - project doc

## Workflow Status Target

| Workflow | Script | Data Source | Status |
|---|---|---|---|
| cma | `cma_analyze.py` | MCP properties + web research | 🟢 |
| agent-profile | Higgsfield MCP | `generate_image` | 🟢 |
| yad2-import | Apify MCP | Yad2 scraper | 🟢 |
| photo-enhance | Higgsfield | `remove_background`, `generate_image` | 🟢 |
| brochure | `mcp_brochure_run.py` | MCP properties | 🟢 |
| video | Higgsfield | `generate_video` | 🟢 |
| social-posts | Higgsfield | `generate_image` | 🟢 |
| property-page | LLM only | MCP properties | 🟡 |
| facebook-scan | `mcp_facebook_scan_run.py` | Apify FB scraper | 🟢 |
| lead-scoring | `mcp_lead_score_run.py` | MCP leads | 🟢 |
| matching | `mcp_match_run.py` | MCP leads + properties | 🟢 |
| crm-update | `mcp_crm_run.py` | MCP leads | 🟢 |
| contract-sign | LLM + template | `_mock/contract-template.md` | 🟡 |
| scheduling | Google Calendar MCP | `list_events`, `create_event` | 🟢 |
| reminders | Google Calendar + Evolution | `list_events` + WA send | 🟡 |

🟢 = real tool wired, 🟡 = partial/mock fallback

## Verify: Cold Agent Test
Spawn 5 sub-agents (zero context), each runs one phase. Score rubric:
- Navigability: AGENTS.md → workflow → stage resolves? (15%)
- Self-sufficiency: zero guesses? (20%)
- Determinism: math in script? (15%)
- Freshness: `_run.json` guarded? (10%)
- Human gate: stops correctly? (15%)
- Tool wiring: right tool per stage? (10%)
- Source grounding: every fact cites source? (10%)
- Schema contracts: declared? (5%)

Target: ≥8/10 per workflow.
