# Function Spec Card: FP-{capability}-{nnn}

One card per critical function point in deep tier. Cards are research drafts — they are not approved PRD specs and must be reviewed before promotion into `functional-spec`.

## Identity

- **ID:** FP-{capability}-{nnn}
- **Name:** ...
- **Capability domain (→ `capability-map.md`):** ...
- **Status tags:** ...
- **Maturity:** M{n}

## Behavior

- **User / actor:** ...
- **Trigger:** ...
- **Preconditions:** ...
- **Inputs:** {field — type — required — validation — source}
- **Processing logic:** {numbered steps; one line each}
- **Outputs:** {what is returned / persisted / emitted}
- **State transitions:** {from → to + guard}
- **Side effects:** {writes, events, external calls}

## Exceptions and edge cases

| Case | Trigger | Expected handling | Evidence (path:line) |
|---|---|---|---|
| ... | invalid input | reject with 422 | `services/api/tasks/routes.py:60` |

## Non-functional requirements (observed or required)

- **Permissions:** ...
- **Logging / audit:** ...
- **Performance:** ...
- **Concurrency / idempotency:** ...

## Evidence

| Type | Path | Notes |
|---|---|---|
| Code | `...` | ... |
| Test | `...` | ... |
| Doc | `...` | ... |

## Gaps and open questions

- {What is missing — spec / test / handling / doc.}
- {What needs owner confirmation.}
- {`[INFERRED]` items used in this card.}
