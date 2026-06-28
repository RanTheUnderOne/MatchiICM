# Stage 03 - Assemble

Order shots, add captions + brand outro.

## Inputs
- `02-generate/output/clips.json`
- `01-script/output/script.json`
- `_config/voice.md`

## Process (MCP + LLM)
1. Sequence clips per script order.
2. Call Higgsfield MCP `reframe` to convert all clips to 9:16 (reels format).
3. LLM generates Hebrew caption text per shot from script voiceover.
4. Add brand outro card from `_config/voice.md`.
5. Write `output/video-manifest.json` (+ later `reel.mp4`).

## Outputs
- `output/video-manifest.json`

## Human gate
Show the assembly plan. Approve before render/publish.

## Pitfalls
| Wrong aspect ratio | Always `reframe` to 9:16 before assembly |
