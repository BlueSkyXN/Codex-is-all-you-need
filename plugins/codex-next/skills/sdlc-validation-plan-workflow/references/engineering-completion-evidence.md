# Engineering Completion Evidence

Use this reference to select the evidence layers needed for a validation plan.
It is a repository workflow heuristic, not a claim that every task must satisfy
one universal lifecycle checklist.

## Completion dimensions

| Dimension | Proof question | Typical evidence |
|---|---|---|
| Requirement | Is the expected behavior observable and satisfied? | acceptance criteria, scenario, demo |
| Architecture | Are ownership and dependency boundaries preserved? | boundary check, ADR conformance review |
| Code | Is the implementation scoped, understandable, and statically sound? | review, lint, typecheck |
| API | Are compatibility, errors, and idempotency explicit? | contract test, request/response evidence |
| Data | Are ownership, migration, transaction, and recovery behavior safe? | migration rehearsal, integrity check |
| Test | Are critical behavior and failure paths exercised? | targeted test output, regression evidence |
| Build | Is the artifact reproducible and tied to the intended source? | build output, artifact record, source revision |
| Release | Are rollout and rollback or forward recovery executable? | release record, rollout/rollback rehearsal |
| Runtime | Are health, logs, metrics, and business smoke behavior observable? | runtime readback, monitoring evidence, smoke result |
| Documentation | Are usage and durable decisions updated where needed? | documentation diff, ADR or runbook update |

## Applicability

Select the smallest set of dimensions that can prove the affected behavior and
risk. For every dimension included in the plan, set `Applicability` to one of:

- `required`: evidence is needed for the current acceptance or release decision;
- `not-applicable`: the dimension was plausibly relevant but is excluded for a
  stated reason;
- `deferred`: evidence is intentionally postponed, with an owner, risk, and
  follow-up or exit condition.

At `seed` depth, include only dimensions plausibly affected by the narrow
change; do not expand a small bugfix into a ten-row lifecycle matrix. At broader
depths, review every affected layer and make exclusions visible when they could
otherwise be mistaken for completed proof.

`Applicability` is not a second validation status. Continue to use only:

```text
planned
ready
blocked
passed
failed
not-run
accepted-gap
```

For `not-applicable`, normally use `not-run` and record the exclusion reason in
the method or evidence field. For `deferred`, use the existing status that
matches reality, such as `planned`, `blocked`, `not-run`, or `accepted-gap`.
Never mark a dimension `passed` without execution evidence for that dimension.

## Depth defaults

- `seed`: select the minimum requirement, behavior, and regression proof needed
  for the reported bug or direct-dev change.
- `feature`: select dimensions affected by the feature's interfaces, data,
  behavior, and user path.
- `behavior-baseline`: prove the behavior that must remain stable and the
  structural risks introduced by the refactor.
- `architecture`: select dimensions affected by ownership, dependency, data,
  interface, or NFR decisions.
- `system`: assess every affected application, integration, data, build,
  runtime, and operational layer; mark genuine exclusions rather than assuming
  them complete.
- `release`: always assess build, release, runtime, and rollback or forward
  recovery, in addition to the product and risk dimensions affected by the
  release.

## Evidence boundaries

Evidence is layer-specific. Record the source revision, environment, target,
and result when they matter to the proof question.

- Unit tests do not prove integration, release, runtime, or business behavior
  that they did not exercise.
- A merged pull request proves repository history, not artifact, deployment, or
  runtime state.
- An artifact proves a build output exists, not that the target runtime uses it.
- A `RUNNING` status proves a process state, not health, version identity, or a
  successful business smoke path.

Do not require every layer merely because evidence could exist. Do not use one
local green signal to silently stand in for a different required layer.
