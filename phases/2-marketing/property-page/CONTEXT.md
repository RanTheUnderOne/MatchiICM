# Workflow: Property Page - Public Listing Page + Chat

Trigger: "תכין דף נכס / עמוד נכס ציבורי / landing page לנכס".

Builds a public property page with an embedded chat that answers buyer questions
from the property facts. Reliability = the chat answers ONLY from grounded facts.

## Pipeline
| Stage | Action | Execution |
| --- | --- | --- |
| 01-content | Assemble page content (facts, photos, copy) | MCP `get_property_full_details`. Reuse approved photos/copy from other workflows |
| 02-build | Generate the page (RTL-branded HTML) | LLM -> RTL HTML. Hosting target 🔴 discover |
| 03-chat | Build a grounded Q&A knowledge file for the page chat | LLM -> grounded Q&A from property facts. Unknown -> defer to agent |
| 04-approve | Human gate -> publish | Human gate |

## Reliability Contract
- 03 chat answers strictly from the property fact sheet; unknown -> "I'll check
  with the agent", never invents.
- Reuses brochure copy + approved photos when available (no duplicate writing).
- Brand from `_config/voice.md`.

## MCP & Tools
- Production MCP: `https://prod-mcp.nadlanai.org/mcp`
- Data MCP: `get_property_full_details` for property facts

## Freshness
01 writes `01-content/output/_run.json` {run_id, source, fetched_at, counts}.
