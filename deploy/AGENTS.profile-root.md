# MatchiICM — Smart Router

You are a general-purpose agent. The folder `workspace/MatchiICM/`
contains a dedicated real-estate agent workspace.

## Context Detection
If the user talks about real estate (properties, leads, agents, matches,
sales, rent, pricing, reports, CMA, brochure, photos, video, contract,
scheduling, showings, reminders, listings, Yad2, Facebook scan, scoring)
→ navigate to `workspace/MatchiICM/`, read `AGENTS.md` + `CONTEXT.md`.
All work happens from there. Hebrew keywords: נדל"ן, דירה, נכס, ליד,
מחיר, השכרה, מכירה, ברושור, חוזה, פגישה, שיווק, בלעדיות.

Any other topic → behave normally. Do not load the workspace.

## Rules
1. Decide by content, not exact keywords. Hebrew + English.
2. Once inside the workspace, follow the ICM rules in its AGENTS.md.
3. Do not load workspace files for casual conversation.
