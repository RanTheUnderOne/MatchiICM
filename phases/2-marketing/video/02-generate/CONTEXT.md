# Stage 02 - Generate

Generate / animate the shots.

## Inputs
- `01-script/output/script.json`
- agent Soul ID (from agent-profile, for any on-camera shot)

## Process (MCP)
1. Per shot, build a video-generation brief (motion, length, source image).
2. Call Higgsfield `generate_video` for scene shots.
3. Call Higgsfield `motion_control` for camera motion / agent puppeteer.
4. Agent shots always pass the agent soul_id for face consistency.
5. Write `output/clips.json` - [{shot_no, brief, clip_path, soul_id?, status}].

## Outputs
- `output/clips.json`

## Human gate
Show clip plan. Approve before assembly.

## Pitfalls
| Face drift on agent shots | Always pass the agent soul_id |
| MCP outage | Fallback to mock clip briefs in `_mock/` |
