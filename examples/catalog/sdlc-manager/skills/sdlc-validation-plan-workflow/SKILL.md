---
name: sdlc-validation-plan-workflow
description: Use to make Validation Plan a first-class SDLC artifact by defining how SRS, NFR, HLD, LLD, ADR, Domain Boundary Map, SPEC, RTM, issue evidence, or dev handoff will be proven correct before dev execution, review, or release.
---

# Validation Plan Workflow

Use this workflow to define how a change will be proven correct before implementation, review, or release.

This is not a missing testing capability. It is an SDLC-manager artifact that makes the validation contract explicit:

```text
Validation Plan defines how correctness will be proven.
dev executes, extends, or reports against that plan.
```

## Use when

- A feature, system change, migration, refactor, bugfix package, or release-bound change needs an explicit validation plan before dev starts.
- SRS, NFR, HLD, LLD, ADR, Domain Boundary Map, SPEC slices, RTM, issue evidence, or dev handoff must be turned into acceptance and evidence expectations.
- The user asks for a validation plan, acceptance test matrix, test plan at the SDLC level, smoke checklist, regression scope, or proof of correctness plan.
- NFRs require measurement, threshold checks, operational proof, or release evidence.
- Architecture, domain ownership, dependency boundaries, permissions, data migration, or public API behavior must be validated rather than assumed.
- A readiness review or handoff has validation gaps that should be authored as an artifact.

## Do not use when

- The task is to run tests, reproduce failures, diagnose logs, or inspect CI output. Use `dev_test_runner` or the relevant dev agent.
- The task is to design repo-specific testing layers, fixtures, coverage, or automation strategy. Use `dev-test-strategy`.
- The task is to implement code, edit tests, or fix test failures. Use the relevant dev skill.
- The task is a release checklist after implementation. Use `dev-release-check` when release execution is the main work.
- The task is a clear, narrow direct-dev bugfix with enough reproduction and validation already stated.

Absence of a formal validation plan is not an automatic stop condition for clear direct-dev tasks.

For lane, ADS, lightweight ID, `local/sdlc`, delivery card, and midstream intake vocabulary, follow `../sdlc-router/references/sdlc-operating-model.md`.

## Inputs

Use the best available sources. Do not require every artifact family.

### SDLC sources

- BRD / URS / PRD
- SRS and acceptance criteria
- NFR matrix
- HLD
- LLD
- ADR
- Domain Boundary Map
- SPEC slices: UI, API, Data, Permission, Admin, Directory, Observability, Release, Integration, or Copy
- Requirements traceability matrix
- Dev handoff or task cards
- Change control record
- Readiness review verdict

### Direct-dev sources

- Issue, bug report, support ticket, or user request
- Reproduction steps
- Failing test
- Expected behavior statement
- Repository evidence or project conventions
- Known validation command
- Existing release or smoke checklist

If inputs are weak, produce a validation seed and mark assumptions instead of inventing requirements.

## Workflow

### 1. Classify validation depth

Choose the smallest sufficient validation depth.

| Depth | Use when | Output |
|---|---|---|
| `seed` | direct-dev or bugfix with clear evidence | source -> expected behavior -> smallest check |
| `feature` | contained feature or behavior change | acceptance matrix, test levels, smoke path |
| `behavior-baseline` | refactor where external behavior should stay stable | characterization checks, smoke paths, regression guard |
| `architecture` | HLD/LLD/ADR/domain/SPEC constraints matter | architecture/domain validation matrix |
| `system` | multi-module, migration, API/data/permission/NFR risk | full validation plan and regression scope |
| `release` | release-bound, compliance, launch, rollback, or operations risk | release validation notes and evidence gate |

Do not force system-level validation on every change.

### 2. Identify proof questions

Answer the questions that apply:

- How will this change be proven correct?
- Which requirements must be accepted?
- Which NFRs must be measured?
- Which architecture or domain boundaries must not be violated?
- Which SPEC slices must be validated?
- Which user, API, data, permission, admin, or operational paths require smoke testing?
- Which existing capabilities require regression coverage?
- What evidence is required before review or release?

### 3. Build acceptance test matrix

Create rows from requirements, issues, SPEC items, or task cards.

```markdown
| ID | Source | Expected outcome | Validation method | Evidence required | Owner | Status |
|---|---|---|---|---|---|---|
```

Recommended ID prefixes:

```text
VAL-AC-001
VAL-NFR-001
VAL-SMOKE-001
VAL-REG-001
VAL-ARCH-001
```

Status values:

```text
planned
ready
blocked
passed
failed
not-run
accepted-gap
```

Do not mark `passed` without execution evidence.

### 4. Define NFR validation methods

For each material NFR, define:

| NFR | Target or threshold | Method | Tool or evidence | Required before |
|---|---|---|---|---|

Examples:

- performance: benchmark, load check, query plan, bundle size, latency log
- reliability: retry/fallback test, failure injection, restore check
- security/privacy: permission test, audit log check, secret scan, data minimization review
- accessibility: keyboard path, screen reader labels, contrast check
- observability: log, metric, trace, alert, dashboard evidence
- compatibility: migration rehearsal, API version check, feature flag rollback

If an NFR cannot be measured now, record the accepted gap and owner.

### 5. Define architecture and domain validation

When HLD, LLD, ADR, Domain Boundary Map, modular-monolith rules, or Directory SPEC exist, include:

| Constraint | Source | What must hold | Validation method | Evidence |
|---|---|---|---|---|

Check for:

- allowed and forbidden dependencies
- data ownership and migration boundaries
- API/control flow constraints
- transaction and error-handling boundaries
- trust, auth, permission, privacy, and audit boundaries
- module layout and public/internal interface rules

This prevents dev from proving only behavior while breaking structure or ownership.

### 6. Define smoke and regression scope

List:

```text
Manual smoke paths:
Automated checks:
Regression areas:
Out-of-scope checks:
Release evidence:
```

Tie each check to a source requirement, issue, SPEC, task, or accepted risk.

### 6a. Define refactor behavior baseline

For the `重构` lane, define how unchanged external behavior will be proven before dev changes structure:

```text
Behavior to preserve:
Representative paths:
Existing tests or smoke commands:
Characterization checks to add or run:
Known accepted gaps:
Stop condition:
```

Do not ask for BRD/PRD just because the work is large. For pure refactor, the product target is usually unchanged behavior plus safer structure.

### 7. Define evidence expectations

Specify what dev should report:

- command names and exit status
- important test output
- screenshots or browser checks when UI behavior matters
- API request/response samples when contracts matter
- migration dry-run or data verification when data changes
- NFR measurement result
- manual smoke result
- known failures and whether they are pre-existing

Evidence expectations should be precise enough for review, but not so heavy that small changes become process-bound.

### 8. Mark direct-dev fallback

When formal SDLC materials are absent but the task is clear, produce a small validation seed:

```markdown
# Validation Seed: <Change Name>

| Source | Expected behavior | Smallest relevant check | Evidence expected | Risk |
|---|---|---|---|---|
```

State why direct-dev may continue:

```text
Proceed path: direct-dev
Reason: clear issue / reproduction / target behavior / validation command
Risk:
Required safeguard:
```

## Output

Return or write one of these artifacts.

### Behavior Baseline

```markdown
# Behavior Baseline: <Change Name>

## 1. Preserved Behavior
## 2. Representative Paths
## 3. Existing Checks
## 4. Characterization Checks
## 5. Regression Scope
## 6. Accepted Gaps
## 7. Stop Conditions
```

### Validation Plan

```markdown
# Validation Plan: <Change Name>

## 1. Scope
## 2. Source Artifacts
## 3. Validation Depth
## 4. Acceptance Test Matrix
## 5. NFR Validation Matrix
## 6. Architecture and Domain Validation
## 7. Smoke Checklist
## 8. Regression Scope
## 9. Evidence Expectations
## 10. Gaps and Risks
## 11. Handoff Notes
```

### Acceptance Test Matrix

```markdown
# Acceptance Test Matrix: <Change Name>

| ID | Source | Expected outcome | Validation method | Evidence required | Owner | Status |
|---|---|---|---|---|---|---|
```

### Validation Seed

```markdown
# Validation Seed: <Change Name>

| Source | Expected behavior | Smallest relevant check | Evidence expected | Risk |
|---|---|---|---|---|
```

## Validation

Before returning the plan, check:

- Each P0/P1 requirement, issue criterion, or task has a validation method or accepted gap.
- NFRs have methods, not only labels.
- Architecture/domain constraints have validation where they affect implementation.
- Smoke and regression scope are explicit.
- Evidence expectations are reviewable.
- Direct-dev remains allowed when the task is clear and bounded.
- Pure refactor has a behavior baseline before structural changes proceed.
- The plan does not claim tests passed before dev executes them.

## Boundaries

- Do not run tests.
- Do not edit code.
- Do not modify tests.
- Do not fix test failures.
- Do not replace `dev-test-strategy`.
- Do not replace `dev_test_runner`.
- Do not replace `dev-release-check`.
- Do not block clear direct-dev tasks solely because a formal validation plan is absent.

## Handoff

Route downstream:

| Need | Next step |
|---|---|
| dev execution | `sdlc-dev-handoff-planning` or `dev-spec-driven-implementation` |
| repo-specific test strategy | `dev-test-strategy` |
| test execution or failure diagnosis | `dev_test_runner` |
| traceability update | `sdlc-requirements-traceability` |
| readiness decision | `sdlc-readiness-review` |
| release validation execution | `dev-release-check` |
| missing SRS/NFR/SPEC/HLD/LLD/ADR/domain source | relevant `sdlc-manager` authoring skill |
