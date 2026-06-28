# Stage 03 - Analyze (Deterministic)

Compute value estimate. MATH = SCRIPT, not LLM. Reliability core:
same inputs → same numbers, every time, auditable.

## Inputs
- `01-subject/output/subject.json`
- `02-research/output/comps.json` + `_run.json`
- `_config/cma-rules.md` (reference only; logic in script)

## Process (Script)
1. Guard: refuse if `02-research/output/_run.json` missing or stale.
2. Run deterministic engine:
   ```
   py scripts/cma_analyze.py \
     --subject phases/1-exclusivity/cma/01-subject/output/subject.json \
     --comps phases/1-exclusivity/cma/02-research/output/comps.json \
     --out phases/1-exclusivity/cma/03-analyze/output/analysis.json
   ```
   Windows: `py`. macOS/Linux: `python3`.
3. Script applies adjustments, computes price/sqm, value RANGE (low/mid/high),
   price position (above/at/below market), confidence score (0–100).
4. LLM MUST NOT recompute or "round" - read script output as-is.

## Outputs
- `output/analysis.json` - `{estimate_range, price_per_sqm, position, confidence,
  comps_used[], adjustments[]}`.

## Human gate
Show computed range + confidence. Confirm before report.

## Pitfalls
| LLM "fixes" number | Forbidden. Script = source of truth |
| Missing size_sqm | Script errors → fix subject in stage 01 |
