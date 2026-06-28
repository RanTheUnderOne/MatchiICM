# Stage 03 - Track

Track signature status.

## Inputs
- `02-send/output/send-request.json`

## Process
1. 🔴 Signature provider not yet chosen. Mock status for now.
2. Write `output/signature-status.json` - {envelope_id, status, signed_by[], updated_at}.
3. Real later: poll provider API or receive webhook per chosen provider.

## Outputs
- `output/signature-status.json`.

## Human gate
Show current status. Continue when signed.
