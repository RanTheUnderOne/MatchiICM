# Stage 04 - Approve

Human gate. Agent reviews the final image set before publish.

## Inputs
- `03-stage/output/staged.json` (full set: edited + staged + pass-through)
- `01-intake/output/photos.json` (original list - for side-by-side before/after)

## Process (Human gate)
1. Assemble the publishable set (originals + edited + staged).
2. Agent approves / requests changes (loop back).
3. Write `output/approved-photos.json` + `output/_approval.json`
   {approved_by, approved_at, count}.

## Outputs
- `output/approved-photos.json`
- `output/_approval.json`

## Human gate
Mandatory. Nothing publishes without approval here.
