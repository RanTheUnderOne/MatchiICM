# Stage 04 - Confirm

Human confirm + archive the signed doc.

## Inputs
- `03-track/output/signature-status.json`

## Process
1. Agent confirms completion - all parties have signed.
2. Archive signed document (copy to `output/signed-contract.md` or designated archive path).
3. Write `output/_approval.json` {confirmed_by, at, archived_path}.

## Outputs
- `output/_approval.json`

## Human gate
Mandatory. Agent reviews signed doc before archiving. Not legal advice - final doc is the agent's responsibility.
