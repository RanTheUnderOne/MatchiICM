# Stage 04 - Approve

Human gate before publish / schedule.

## Inputs
- `03-predict/output/scored-posts.json`

## Process (Human gate)
1. Agent selects + edits final posts (loop back if needed).
2. Write `output/approved-posts.json` + `output/_approval.json`.
3. Publishing API not yet chosen - **🔴 discover** and wire before production.

## Outputs
- `output/approved-posts.json`
- `output/_approval.json`

## Human gate
Mandatory. No auto-posting without approval.

## Pitfalls
| No posting API wired | 🔴 discover and approve a publishing tool before production |
