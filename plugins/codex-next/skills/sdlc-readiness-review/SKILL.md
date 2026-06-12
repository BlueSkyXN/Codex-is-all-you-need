---
name: sdlc-readiness-review
description: Use to assess whether SDLC materials, specs, handoffs, issues, or direct-dev requests are ready, need revision, or are blocked.
---

# SDLC Readiness Review

Use this workflow to judge whether work is ready for the next delivery step.

This is a readiness check, not an enterprise approval board. It should make the next action clear:

```text
ready-for-dev
ready-for-direct-dev
repo-onboarding-first
revise
change-control-needed
blocked
```

SDLC materials improve readiness, but they are not mandatory for every development task. Dev may continue without SDLC materials when the request is narrow, evidence is sufficient, risk is acceptable, and validation is clear.

## Use when

- Requirements, SRS, NFR, SPEC, RTM, or dev handoff must be checked before development.
- A task may proceed directly to dev but the risk needs to be stated.
- Planning artifacts are mixed, incomplete, or possibly stale.
- A change affects baseline, scope, acceptance criteria, or traceability.
- The user asks whether enough detail exists to start implementation.
- A dev agent reports contradiction between artifacts and repository evidence.

## Do not use when

- The request is simple implementation and already clearly ready; route to dev.
- The user asks for code review, test execution, or release publishing.
- The task is to author the missing artifact itself; use the relevant authoring skill.
- The task requires business approval that only the user or organization can provide.

## Inputs

Read available materials:

- artifact profile decision
- BRD, URS, PRD
- SRS
- NFR
- SPEC slices
- dev handoff
- requirements traceability matrix
- change control record
- issue or bug report
- repository evidence
- validation plan
- direct-dev task brief

When no SDLC artifacts exist, inspect the issue/task evidence and decide whether direct dev is acceptable.

## Workflow

### 1. Identify review subject

Classify the review target:

| Subject | Examples |
|---|---|
| requirements readiness | BRD, URS, PRD, scope baseline |
| software spec readiness | SRS, NFR, SPEC slices |
| handoff readiness | dev handoff, task cards, validation plan |
| traceability readiness | RTM or traceability seed |
| change readiness | change request, baseline update |
| direct-dev readiness | issue, bug report, user request, clear local task |

State the delivery profile and risk level if known.

### 2. Check source authority

Determine which source controls the work:

| Source | Status | Controls scope? | Notes |
|---|---|---:|---|

Possible statuses:

```text
draft
review-ready
baseline
change-pending
superseded
unknown
issue-only
repo-evidence-only
```

If sources conflict, do not choose silently. Report the conflict and recommend a resolution path.

### 3. Check scope and non-scope

A ready item must identify:

- what must be delivered
- what must not be delivered
- what is deferred
- what assumptions exist
- what would count as scope expansion

For direct-dev work, this may be expressed as:

```text
Implement only the requested issue or observed failure.
Do not refactor unrelated architecture.
Do not change public behavior outside the stated path.
```

### 4. Check software-facing completeness

For SDLC-backed work, check:

| Area | Question |
|---|---|
| SRS | Are functional requirements numbered and testable? |
| NFR | Are quality constraints measurable or explicitly not applicable? |
| SPEC | Are UI/API/Data/Permission/Admin/Directory needs covered where relevant? |
| Handoff | Are task cards executable? |
| RTM | Can requirements trace to tasks and validation? |
| Change | Is baseline change controlled? |

For direct-dev work, check:

| Area | Question |
|---|---|
| issue clarity | Is the requested change understandable? |
| affected area | Is there a plausible repo area to inspect? |
| validation | Is there a smallest relevant check? |
| risk | Is risk acceptable without formal SDLC artifacts? |
| fallback | Can dev report blocker if repo evidence contradicts the request? |

### 5. Check acceptance and validation

Ready work must have at least one validation path.

Acceptable validation sources:

- acceptance criteria
- reproduction steps
- failing test
- expected behavior statement
- unit/integration/e2e/manual smoke command
- NFR measurement
- release smoke condition

Do not require a full test plan for every direct-dev task. Require enough validation for the risk.

### 6. Check traceability level

Use the appropriate traceability depth:

| Situation | Required traceability |
|---|---|
| direct-dev small task | source -> task -> validation seed |
| feature delivery | SRS/SPEC -> task -> validation |
| system delivery | source -> SRS/NFR/SPEC -> task -> test |
| program or compliance delivery | full RTM plus change and release evidence |

If traceability is absent but the task is safe for direct dev, mark it as an accepted direct-dev gap rather than blocking.

### 7. Decide readiness verdict

Use one verdict only:

| Verdict | Meaning |
|---|---|
| `ready-for-dev` | SDLC-backed package is sufficient for dev execution |
| `ready-for-direct-dev` | Formal SDLC materials are absent or unnecessary, but the task can proceed safely |
| `repo-onboarding-first` | Dev can proceed after read-only repo mapping |
| `revise` | Materials need revision before dev should start |
| `change-control-needed` | Scope or baseline change requires change-control first |
| `blocked` | Critical missing information or contradiction prevents safe execution |

Avoid vague results such as “mostly okay.”

### 8. Provide next action

The review must end with a concrete route:

```text
Next skill:
Next agent:
Required artifact or task:
Risk if skipped:
```

## Output

Return a readiness review:

```markdown
# SDLC Readiness Review: <Subject>

## 1. Review Subject
## 2. Source Authority
## 3. Scope and Non-scope Check
## 4. Completeness Check
## 5. Validation Check
## 6. Traceability Check
## 7. Risks and Gaps
## 8. Verdict
## 9. Next Action
```

Use this verdict block:

```text
Verdict: ready-for-dev | ready-for-direct-dev | repo-onboarding-first | revise | change-control-needed | blocked
Reason:
Required before next step:
Can proceed without:
Must not skip:
Next agent / skill:
```

The `Can proceed without` line is important. It prevents the process from treating optional SDLC artifacts as mandatory blockers.

## Validation

Before returning the verdict, check:

- The verdict matches the evidence.
- Required and optional gaps are separated.
- Direct-dev readiness is allowed when scope and validation are sufficient.
- Missing SDLC artifacts are not automatically treated as blockers.
- High-risk gaps are clearly marked.
- Change-control needs are called out when baseline or scope changes.
- The next action names an agent or skill, not only a general recommendation.

## Boundaries

- Do not approve business strategy, legal acceptance, security exception, or production release.
- Do not write replacement artifacts inside the review unless asked.
- Do not block safe dev work solely because BRD, URS, PRD, SRS, or RTM is absent.
- Do not claim tests passed or validation succeeded without evidence.
- Do not let readiness review become project management overhead.
- Do not let dev own SDLC artifacts; dev may report implementation blockers and contradictions.

## Handoff

Route by verdict:

| Verdict | Route |
|---|---|
| `ready-for-dev` | `sdlc-dev-handoff-planning` or dev implementation skill |
| `ready-for-direct-dev` | dev skill such as `dev-bugfix`, `dev-repo-onboarding`, or `dev-spec-driven-implementation` |
| `repo-onboarding-first` | `dev-repo-onboarding` |
| `revise` | relevant authoring skill: `sdlc-srs-workflow`, `sdlc-nfr-spec`, `sdlc-spec-slice-writer`, `sdlc-requirements-workflow` |
| `change-control-needed` | `sdlc-change-control` |
| `blocked` | ask for required owner decision, missing input, or conflict resolution |
