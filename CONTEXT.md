# MatchiICM - Navigation

Phases → workflows. Each workflow = self-contained ICM pipeline (stages 01..0N + output/).
Run only workflow a trigger points to.

## Phase 1 - Exclusivity
| Workflow | Produces | Engine |
|---|---|---|
| cma | Comparative Market Analysis (asking vs market) | Script `cma_analyze.py` + MCP properties |
| agent-profile | Branded agent profile card + portrait | OpenAI GPT Image 1 (`$OPENAI_API_KEY` env) |
| yad2-import | Structured property list from Yad2 | Apify MCP (Yad2 scraper) |

## Phase 2 - Marketing
| Workflow | Produces | Engine |
|---|---|---|
| photo-enhance | Staged/enhanced property images | OpenAI GPT Image 1 (edit + inpaint) |
| brochure | Museum-quality PDF brochure HE/EN | Script `mcp_brochure_run.py` + Playwright |
| video | Property video script + clips | 🔴 Blocked — no video API. Script only |
| social-posts | FB/IG post pack with virality scores | OpenAI GPT Image 1 + LLM virality estimate |
| property-page | Public property page content + chat FAQ | LLM + MCP property data |

## Phase 3 - Leads
| Workflow | Produces | Engine |
|---|---|---|
| facebook-scan | Buyer leads from FB groups | Script `mcp_facebook_scan_run.py` + Apify MCP |
| lead-scoring | Scored + bucketed leads (hot/warm/cold) | Script `mcp_lead_score_run.py` (engine: `lead_score.py`) |
| matching | Lead↔property match pairs + ranks | Script `mcp_match_run.py` (engine: `match.py`) |
| crm-update | CRM kanban state transitions + audit | Script `mcp_crm_run.py` (rules: `_config/crm-rules.md`) |

## Phase 4 - Closing
| Workflow | Produces | Engine |
|---|---|---|
| contract-sign | Contract package + signature request | LLM + template. 🟡 mock fallback |
| scheduling | Showing/meeting booked | Google Calendar MCP |
| reminders | Confirmation + reminder messages | Google Calendar MCP. Send: 🟡 fallback to log |

## Conventions
- Stage = numbered folder `0X-name/` with `CONTEXT.md` + `output/`.
- Each stage declares execution layer: Script / MCP / LLM.
- Human gate after each stage. Agent reports, waits for approval.
- `_run.json` freshness stamp in data-fetch stage; downstream stages guard on it.
- Scripts live in `scripts/`. Config in `_config/`. Fallback data in `_mock/`.
