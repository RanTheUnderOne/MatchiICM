# Stage 02 - Send

Send the draft for digital signature.

## Inputs
- `01-prepare/output/draft-contract.md`
- recipient (owner) contact

## Process
1. Present draft + recipient to agent for approval.
2. Write `output/send-request.json` - {recipients, doc_path, envelope_id, status:"pending-provider"}.
3. 🔴 Signature provider NOT chosen. Discovery + approval needed before real send.

## Options (discover+approve)
| Provider | Region | Notes |
| --- | --- | --- |
| Hatima | IL | Israeli e-signature, local compliance |
| DocuSign | Global | Industry standard, paid tiers |
| SignNow | Global | Lower cost, basic features |

## Outputs
- `output/send-request.json` - {recipients, doc_path, envelope_id, status:"pending-provider"}.

## Human gate
Approve provider choice + recipients before a real send.
