# Stage 01 - Script

Write a short shot-by-shot script.

## Inputs
- MCP `get_property_full_details` (property facts)
- `_config/voice.md`

## Process (LLM)
1. Wipe stale output.
2. 5-8 shots: hook, exterior, key rooms, standout feature, agent outro/CTA.
3. Short Hebrew voiceover line per shot.
4. LLM generates script following brand voice from `_config/voice.md`.
5. Write `output/script.json` + `output/_run.json`.

## Outputs
- `output/script.json` - [{shot_no, scene, vo_he, seconds}].
- `output/_run.json`

## Audit
Run before writing `output/script.json`. Revise until all pass.

- [ ] 5-8 shots: hook + exterior + rooms + standout + outro
- [ ] Every shot has: scene description, VO line (Hebrew), duration (seconds)
- [ ] VO total under 60 seconds
- [ ] No invented property features - all from MCP data
- [ ] CTA clear: "לצפייה התקשרו" or equivalent

## Human gate
Show the script. Approve before generating shots.
