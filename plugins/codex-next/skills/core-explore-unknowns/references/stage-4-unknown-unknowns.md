# Stage 4 - Unknown Unknowns: Hunt the Landmines

This stage searches for risks that did not show up as questions. Inspect the
area the task will touch and turn hidden constraints into explicit map entries.

## Procedure

1. State the coverage: files, docs, configs, or data paths inspected.
2. Look for:
   - silent failure modes, stale derived data, permissive filters, escaping
     issues, and wrong defaults;
   - conventions enforced by code but not documented;
   - abandoned attempts or reverted changes near the same behavior;
   - inherited issues that the requested change would expose or depend on.
3. Report each finding with evidence, impact, and what it changes about the
   plan. Put the highest-risk findings first.
4. If a finding requires a decision, treat it like a stage-2 question with a
   recommendation. If it only needs awareness, mark it as a sharp edge.

**Done when** the relevant surface has been swept and every hidden risk is
classified as decided, OPEN, or sharp edge.
