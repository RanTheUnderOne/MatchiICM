# Stage 05 - Approve (Human Gate)

## Execution Layer
Human - agent reviews and approves the final card.

## Inputs
- `03-portrait/output/portrait.json`
- `04-profile-card/output/profile-card.md`

## Process
1. Present portrait + card to the agent.
2. Approve / edit / regenerate a stage.
3. On approval - mark ready to publish.

## Outputs
- `output/approved-profile.md`
- `output/_approval.json` - {approved_by, approved_at, approved_portrait, approved_card}.

## Rule
No publish without agent approval.
