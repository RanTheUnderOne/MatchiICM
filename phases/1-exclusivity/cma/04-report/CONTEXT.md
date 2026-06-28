# Stage 04 - Report

Turn deterministic analysis into client-facing CMA report. LLM writes
narrative ONLY - copies numbers from analysis.json verbatim.

## Inputs
- `03-analyze/output/analysis.json` (authoritative numbers)
- `01-subject/output/subject.json` (property details)
- `02-research/output/comps.json` (comp sources for citations)
- `_config/voice.md` (tone, brand, formatting)

## Process (LLM)
1. Read analysis.json. Use range, position, confidence as-is.
2. Self-verify before writing: every number must match analysis.json.
   Every comp cited must carry its source. Untraceable number → don't write it.
3. Compose report in `_config/voice.md` style:
   - Subject summary
   - Estimated value RANGE (low/mid/high) - never single figure
   - Asking vs market position
   - Comparable table with sources
   - Confidence band + one-line explanation
   - Recommendation (1-2 lines)

## Outputs
- `output/cma-report.md` - final Hebrew report.

## Human gate
Agent reviews + edits report. Nothing sent before stage 05 approval.

## Audit
Run before writing `output/cma-report.md`. Revise until all pass.

- [ ] Every number in report matches `analysis.json` - cross-check 100%
- [ ] Every comp cited carries source (nadlan.gov.il / yad2 / madlan)
- [ ] Value presented as RANGE (low–mid–high), never single figure
- [ ] Confidence band stated (High/Medium/Low) with one-line reason
- [ ] No invented amenities, facts, or market claims
- [ ] Hebrew is natural, not translated-from-English

## Pitfalls
| Number not in analysis.json | Hallucination - don't write it |
| Comp without source | Drop it or label "unverified" |
| Single price stated | Forbidden - always a range |
