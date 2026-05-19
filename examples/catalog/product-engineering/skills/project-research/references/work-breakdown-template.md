# Work Breakdown (WBS-lite): {project name}

Lists the work needed to move each capability to its next maturity level. Default granularity is **work package (1-3 person-weeks)**. This is not a full project WBS — full task decomposition, sequencing, and validation expectations belong to `delivery-task-planning`.

## Work packages

| ID | Work package | Serves capability (→ `capability-map.md`) | Maturity transition | Scope (1 line) | Depends on | Blocked by (→ `blocker-list.md`) | Est. size |
|---|---|---|---|---|---|---|---|
| WP-001 | ... | task-management | M5 → M6 | wire task service into notification bus | WP-000 | BLK-003 | 2 person-weeks |
| WP-002 | ... | audit | M4 → M5 | get local Docker compose stack to start cleanly | — | BLK-001 | 1 person-week |

### Package detail (one block per WP)

#### WP-{id}: {short title}

- **Capability served:** {L1 capability from `capability-map.md`}
- **Maturity transition:** M{n} → M{n+1}
- **Scope:** {1-3 sentences. What is in. What is explicitly out.}
- **Definition of done:** {observable signal — "endpoint returns X under Y conditions", not "feature works"}
- **Evidence needed at completion:** {test record / runnable artifact / deployment proof}
- **Dependencies:** {other WPs that must finish first}
- **Open blockers:** {BLK-... references}
- **Est. size:** {person-weeks}

(Repeat per package.)

## Drill-down to task cards (deep tier only)

For the top 3-5 critical packages that gate the end-to-end chain, expand into task cards. Other packages stay at package level. Full WBS belongs downstream.

### WP-{id} task cards

| Task ID | Task | Owner role | Est. effort | Acceptance signal |
|---|---|---|---|---|
| WP-{id}-T1 | ... | backend | 1 day | ... |
| WP-{id}-T2 | ... | frontend | 0.5 day | ... |

## Out of scope for this WBS

- Full project task decomposition across all capabilities (→ `delivery-task-planning`)
- Cross-task dependency graph (→ `delivery-task-planning`)
- Test plan generation (→ `delivery-task-planning`)
- Resource assignment and scheduling (project management tool)
- Cost estimation (out of scope for this skill entirely; see `methodology.md` §8.4)
