# Work Breakdown Structure (WBS): {project name}

Lists the work packages needed to move capabilities or function points forward. This WBS is for tracking and management. It does not estimate effort, cost, staffing, or schedule.

CSV companion: write work-package rows to `tables/wbs.csv`. In deep tier only, write drilled-down task rows to `tables/task_cards.csv`.

## Work packages

| ID | Work package | Linked capability | Linked function points | Maturity transition | Tracking status | Management unit | Depends on | Blocked by |
|---|---|---|---|---|---|---|---|---|
| WP-001 | ... | CAP-task-management | FP-task-001, FP-task-003 | M5 -> M6 | not-started | yes | WP-000 | BLK-003 |
| WP-002 | ... | CAP-audit | FP-audit-002 | M4 -> M5 | blocked | split-needed | — | BLK-001 |

### Package detail (one block per WP)

#### WP-{id}: {short title}

- **Capability served:** {L1 capability from `capability-map.md`}
- **Function points served:** {FP-... references from `capability-map.md`}
- **Maturity transition:** M{n} → M{n+1}
- **Tracking status:** not-started / in-progress / blocked / done / deprecated
- **Management unit:** yes / split-needed / merge-needed / unknown
- **Scope:** {1-3 sentences. What is in. What is explicitly out.}
- **Definition of done:** {observable signal — "endpoint returns X under Y conditions", not "feature works"}
- **Evidence needed at completion:** {test record / runnable artifact / deployment proof}
- **Dependencies:** {other WPs that must finish first}
- **Open blockers:** {BLK-... references}

(Repeat per package.)

## Drill-down to task cards (deep tier only)

For critical packages that gate the end-to-end chain, expand into task cards. Other packages stay at package level. Detailed delivery sequencing belongs downstream.

### WP-{id} task cards

| Task ID | Task | Owner role | Acceptance signal |
|---|---|---|---|
| WP-{id}-T1 | ... | backend | ... |
| WP-{id}-T2 | ... | frontend | ... |

## Out of scope for this WBS

- Full project task decomposition across all capabilities (→ `delivery-task-planning`)
- Cross-task dependency graph (→ `delivery-task-planning`)
- Test plan generation (→ `delivery-task-planning`)
- Resource assignment and scheduling
- Cost estimation
