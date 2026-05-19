# Tracking Matrix: {project name}

The management entrypoint for follow-up tracking and reporting. This file links the capability tree / CBS, product structure / PBS, WBS, evidence, blockers, maturity, and next actions.

It is an index, not a replacement for the source artifacts. Keep rows short and traceable.

CSV companion: write the same importable management index to `tables/tracking_matrix.csv`.

## Tracking matrix

| Tracking ID | Capability domain | Function point | Spec candidate | Product module | Work package | Evidence | Status tags | Maturity | Blocker | Next action |
|---|---|---|---|---|---|---|---|---|---|---|
| TRK-001 | CAP-... | FP-... | SPEC-... | `module/path` | WP-... | EVD-... / `path:line` | implemented, blocked | M4 | BLK-... | ... |

## Status legend

- `planned`: stated or inferred need, no spec/code yet.
- `specified`: spec candidate or approved spec exists.
- `implemented`: code exists.
- `runnable`: locally or experimentally runnable.
- `integrated`: connected with peer modules or services.
- `tested`: tests exist and have been run.
- `demoable`: can be shown with sample input and expected output.
- `deployed`: reachable in a real environment.
- `operable`: observable and recoverable.
- `blocked`: linked blocker prevents progress.
- `changed`: target shifted; link to `target-shift-log.md` when present.
- `deprecated`: no longer an active target.

## Reporting hooks

Use this section for later report writers. Do not write completion rates or performance scoring here.

| Report question | Rows to inspect | Notes |
|---|---|---|
| What capabilities exist? | CAP-* rows | Use `capability-map.md` for detail. |
| What can be demonstrated? | rows tagged `demoable` or `runnable` | Verify evidence before reporting. |
| What blocks progress? | rows linked to BLK-* | Use `blocker-list.md` for symptoms and next steps. |
| What should be planned next? | rows with WP-* and next actions | Use `work-breakdown.md` and `next-actions.md`. |
