# Workflow: Video — Short Property Reel

Trigger: "תכין סרטון / וידאו לנכס / property video".

**🔴 BLOCKED.** No video generation API available. Script writing + storyboard
only. Video generation waits for Sora API or equivalent.

## Pipeline
| Stage | Action | Execution |
| --- | --- | --- |
| 01-script | Write short shot-by-shot script + voiceover | LLM + `_config/voice.md`. 5-8 shots: hook, exterior, rooms, standout, outro |
| 02-generate | 🔴 Blocked — no video model | Would use `generate_video` when available |
| 03-assemble | 🔴 Blocked — no video model | Would assemble shots + captions |
| 04-approve | Human gate | Review script only |

## Reliability Contract
- Script only. No video output until video API wired.
- Shots reflect real rooms, not invented spaces.
- Brand outro + palette from `_config/voice.md`.

## Freshness
01 writes `01-script/output/_run.json` {run_id, source, fetched_at, counts}.
