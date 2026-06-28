# Stage 02 - Transition

Parse intent and validate stage transitions against adjacency rules.

## Inputs

- `01-load/output/current.json`
- (LLM) User chat request - e.g. "שנה סטטוס L-1 ל-contact", "העבר ליד 3 לסטטוס qualified"
- `_config/crm-rules.md` (allowed transitions adjacency matrix)

## Process

1. (LLM) Parse chat intent → extract lead_id + target stage from Hebrew/English text.
   - e.g. "שנה סטטוס L-1 ל-contact" → `{lead_id: "L-1", to: "contacted"}`
2. (LLM) Validate target stage exists in CRM vocabulary.
3. Look up current stage from `current.json` for the identified lead.
4. Check adjacency matrix in `_config/crm-rules.md`: is `current_stage → target_stage` allowed?
5. Reject illegal jumps (e.g. new -> won) with a reason.
6. Build transitions array.

## Outputs

- `output/transitions.json` `[{lead_id, from, to, legal, reason?}]`

## Human gate

Show proposed changes + any rejected transitions. Confirm before write.

## Pitfalls

| Illegal stage jump | Validate against allowed transitions; reject with reason |
| LLM misparses lead_id | Require exact lead ID prefix (L-NNN); reject ambiguous |
| Multiple leads requested | Parse each independently; batch into transitions.json |
