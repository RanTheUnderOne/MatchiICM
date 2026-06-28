# Stage 01 - Intake

Collect the agent's details and photo references.

## Execution Layer
Script - loads from onboarding questionnaire / local config.

## Inputs
- User message + onboarding questionnaire (or local `_config/agent.json`).

## Process
1. Load agent record: full_name, title, agency, areas, specialty, years,
   phone, email, languages, tagline, photo_refs.
2. Check photo_refs exist (≥1, ideally 10–20 for good Soul ID). If too few,
   note it - Soul ID quality depends on photo count/variety.
3. Write normalized record to `output/`.

## Outputs
- `output/agent.json` - normalized agent record.

## Human gate
Confirm details are correct before generating visuals.

## Pitfalls
| Missing photo_refs | Soul ID cannot train - ask agent to upload at least 5 photos |
| Poor photo quality | Blurry / dark photos reduce Soul ID quality - warn and request better |
