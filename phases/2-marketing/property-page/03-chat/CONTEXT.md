# Stage 03 - Chat

Build the grounded Q&A knowledge for the page's chat.

## Inputs
- `01-content/output/page-content.json`

## Process (LLM)
1. LLM turns property facts into a structured Q&A / fact-sheet the chat is allowed to answer from.
2. Rule: answer ONLY from these facts; unknown -> defer to agent ("I'll check with the agent"), never invent.
3. Write `output/chat-kb.json` - {facts[], allowed_answers, fallback}.

## Outputs
- `output/chat-kb.json`

## Human gate
Review the fact boundary. Approve before publish.

## Pitfalls
| Chat invents answers | Hard rule: grounded-only + fallback to agent |
