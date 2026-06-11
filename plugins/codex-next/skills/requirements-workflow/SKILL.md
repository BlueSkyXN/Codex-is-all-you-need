---
name: requirements-workflow
description: Use to turn business, user, and product inputs into a scoped requirements package that may include BRD, URS, PRD, scope baseline, assumptions, success metrics, and handoff inputs.
---

# Requirements Workflow

Use this skill as the main `sdlc-manager` entry point for requirements work.

It coordinates BRD, URS, and PRD material. It does not replace SRS, NFR, SPEC, RTM, or dev handoff skills.

In the lightweight SDLC-ADS model, this skill primarily creates a requirements package as the gate between incubation and delivery. BRD / URS / PRD are incubation tools, not default dev gates. For lane, ADS, ID, and `local/sdlc` vocabulary, follow `../artifact-profile-router/references/sdlc-operating-model.md`.

## Use when

- The user has an idea, product direction, roadmap item, business request, or user problem that is not yet ready for implementation.
- A feature needs clear scope, non-scope, target users, business/user value, success metrics, and acceptance direction.
- Existing materials must be consolidated into a requirements package.
- The task needs a stable scope baseline before SRS, SPEC, or dev handoff.

## Inputs

Gather available inputs:

- Raw idea, meeting notes, roadmap item, user feedback, ticket, stakeholder request, or research notes.
- Existing product docs, business docs, user research, analytics, support tickets, or competitor notes.
- Existing project capability map, if available.
- External Web, GPT5.5Pro, other AI, meeting, or pasted discussion output.
- Constraints: platform, release window, budget, staffing, compliance, privacy, security, target audience.
- Known scope, non-scope, success metrics, and owner decisions.

## Required perspective check

Before writing delivery requirements, diagnose the request from three perspectives:

1. User perspective
   - Who is the target user?
   - What job, scenario, or task are they trying to complete?
   - What do they do today?
   - What pain, cost, risk, or delay exists?
   - How often does the scenario occur?
   - What would make the solution valuable enough to use?

2. Business perspective
   - Why should this be done now?
   - What business outcome or operating result is expected?
   - What success metric or evidence will show progress?
   - What is the cost of not doing it?
   - What trade-off or opportunity cost exists?

3. Delivery perspective
   - What platform, system, module, repo, or workflow is affected?
   - What data, account, permission, integration, or third-party dependency exists?
   - What timeline, release, migration, or rollout constraint matters?
   - What must be proven before dev starts?

## Workflow

1. Normalize source materials.
   - Separate facts, assumptions, decisions, and open questions.
   - Keep source references or evidence notes where available.
   - Do not invent data, users, metrics, competitors, or implementation facts.
   - External AI/web discussion is `[外部建议]` until the user confirms it or repo/local evidence supports it.
   - Long external discussion should land in `local/sdlc/<slug>/01-外部讨论.md`; only normalized `REQ`, `TASK`, and `VAL` items become executable.

2. Decide artifact depth.
   - If depth is unclear, route through `artifact-profile-router`.
   - 快线：do not use this workflow unless scope is unclear; prefer direct-dev or handoff-lite.
   - 增补：produce a short requirements package only when product scope, non-scope, or acceptance is unclear.
   - 规则变更：produce `REQ` items and acceptance direction for permission, billing, data metric, state machine, compliance, privacy, or business-semantic changes.
   - 重建：consume the scope decision table and convert only the first wave into `REQ` items.
   - 从头：produce a lightweight requirements package; do not write BRD/URS/PRD/SRS/RTM all at once.

3. Create a scope baseline.
   - In scope
   - Out of scope
   - Future scope
   - Explicit non-goals
   - Assumptions
   - Constraints
   - Required confirmations

4. Split requirement layers.
   - Business requirements -> `brd-workflow`
   - User requirements -> `urs-workflow`
   - Product requirements -> `prd-workflow`
   - Software requirements -> `srs-workflow`, when the product scope is stable
   - Non-functional requirements -> `nfr-spec`, when quality constraints matter

5. Prepare downstream inputs.
   - Candidate requirement IDs
   - Candidate functional areas
   - Candidate acceptance criteria
   - Candidate SPEC slices
   - Open decisions for owner confirmation

## Output

Return a requirements package with:

1. Requirement summary
2. Evidence and source materials
3. Business goals
4. User roles and scenarios
5. Product scope
6. Non-goals and excluded scope
7. Success metrics
8. Assumptions and open questions
9. Required downstream artifacts
10. Next skill sequence

## Recommended Markdown structure

```markdown
# Requirements Package: <Name>

## 1. Status
- Owner:
- Status: Draft / Review / Baseline / Changed
- Lane:
- Modifier:
- Source materials:

## 2. Executive Summary
-

## 3. Evidence
| Source | Finding | Confidence | Notes |
|---|---|---:|---|

## 3a. External Discussion Intake
| Source | Claim / suggestion | Evidence label | Accepted into |
|---|---|---|---|

## 4. Business Requirements
-

## 5. User Requirements
-

## 6. Product Requirements
-

## 7. Scope Baseline
### In Scope
-

### Out of Scope
-

### Future Scope
-

## 8. Success Metrics
| Metric | Baseline | Target | Measurement | Window |
|---|---|---|---|---|

## 9. Assumptions
| ID | Assumption | Risk if wrong | Confirmation owner |
|---|---|---|---|

## 10. Open Questions
| ID | Question | Required before dev? | Owner |
|---|---|---|---|

## 11. Downstream Artifacts
- SRS:
- NFR:
- SPEC slices:
- Dev handoff:
- RTM:
```

Use lightweight IDs by default:

```text
REQ-001
Q-001
DEC-001
VAL-001
```

Only introduce BRD/URS/PRD/SRS-specific ID chains when the delivery risk actually needs that depth.

## Validation

Check that:

- Why, who, what, and success are clear.
- Scope and non-scope are explicit.
- User scenarios are concrete enough to test.
- Requirements do not jump prematurely into implementation details.
- Open questions are not hidden as assumptions.
- All required downstream materials are named.
- Dev can later consume this package through SRS, SPEC, and handoff.

## Boundaries

- Do not edit code.
- Do not create final HLD, LLD, API, Data, or UI specifications here.
- Do not turn ambiguous ideas directly into implementation tasks.
- Do not write “approved” or “baseline” unless the user or project process has confirmed it.
- Do not overstate evidence. Mark inferred, assumed, and confirmed items separately.
- Do not require this workflow for clear bugfixes, pure refactors, or small direct-dev changes.

## Handoff

After this skill:

- Use `prd-workflow` for formal product requirements.
- Use `srs-workflow` when software-facing requirements are needed.
- Use `nfr-spec` when quality attributes matter.
- Use `spec-slice-writer` when UI/API/Data/Admin/Permission/Directory slices are needed.
- Use `dev-handoff-planning` only after requirements and required specs are stable enough for implementation.
