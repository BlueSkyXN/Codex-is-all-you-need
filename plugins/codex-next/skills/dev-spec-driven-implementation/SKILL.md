---
name: dev-spec-driven-implementation
description: Use to implement scoped code changes from specs, handoff, issues, bugs, or direct requests with validation and blocker reporting.
metadata:
  version: "0.4"
  updated: "2026-06-12"
---

# Spec-driven Implementation

## SDLC artifact policy

Use SDLC artifacts when they are present, but do not require them for every development task.

Authoritative SDLC inputs may include:

- SRS
- NFR matrix
- HLD
- LLD
- ADR
- Domain Boundary Map
- UI, API, Data, Admin, Permission, Directory, Observability, or Release SPEC
- dev handoff
- validation plan, acceptance test matrix, smoke checklist, regression scope, or evidence expectations
- requirements traceability matrix
- acceptance criteria
- change-control record

When these artifacts exist, treat them as delivery inputs. Keep the implementation inside the allowed scope, preserve forbidden scope, preserve architecture and domain boundaries, and report contradictions with repository evidence.

When these artifacts are absent, continue from the best available direct input when it is sufficient: user request, issue, bug report, reproduction steps, failing test, local diff, repository evidence, or explicit user instruction. Missing SDLC artifacts are a risk signal, not an automatic stop condition.

Do not make `dev` own, approve, or rewrite SDLC-manager artifacts unless the user explicitly asks for that. Dev may report blockers, contradictions, implementation evidence, and suggested follow-up artifacts.

When present, read the lightweight SDLC-ADS state before implementation:

- `local/sdlc/_资产.md`
- `local/sdlc/架构.md`
- `local/sdlc/领域.md`
- current `local/sdlc/<slug>/00-状态.md`
- current `local/sdlc/<slug>/01-外部讨论.md`, only as reference input

These files are context and constraints, not universal gates. If they are absent and the task is clear, proceed through direct-dev.

External Web/GPT/AI discussion is not executable by itself. Implement only the parts that are normalized into a direct user instruction, delivery card, `REQ`, `TASK`, `VAL`, or explicit user-confirmed scope.

## Use when

- A dev agent must implement from SRS, NFR, HLD, LLD, ADR, Domain Boundary Map, SPEC, Validation Plan, dev handoff, RTM, or acceptance criteria.
- A task card has already been produced by `sdlc-dev-handoff-planning`.
- The user asks to implement a feature, fix, refactor, migration, API change, UI change, or release-bound change.
- No SDLC artifacts exist, but the request or issue is clear enough to start from direct-dev mode.

## Do not use when

- The user is asking to create BRD, URS, PRD, SRS, NFR, SPEC, traceability, or change-control materials. Use `sdlc-manager` skills.
- The repository area is unknown and the task is risky. Start with `dev-repo-onboarding`.
- The requested change is unsafe, unbounded, or impossible to validate.

## Inputs

Prefer inputs in this order:

1. Current user instruction and repository evidence.
2. Dev handoff, delivery card, or task card.
3. `local/sdlc` state and durable ADS constraints.
4. External discussion only after it has been tagged and normalized.
5. Validation Plan, acceptance test matrix, smoke checklist, regression scope, or evidence expectations.
6. SRS / NFR / HLD / LLD / ADR / Domain Boundary Map / SPEC / RTM / acceptance criteria.
7. Issue, bug report, reproduction steps, failing test, local diff, or explicit instruction.
8. Repository map, command list, test plan, CI config, or previous implementation notes.

## Workflow

1. Classify the entry path.

   | Path | Use when | Behavior |
   |---|---|---|
   | SDLC-backed | SRS/SPEC/handoff exists | Treat artifacts as source-of-truth delivery inputs. |
   | Partial-artifact | Some materials exist but gaps remain | Use available materials and mark gaps. |
   | Direct-dev | No SDLC material exists but request is clear | Proceed from issue/request/repo evidence. |
   | Repo-onboarding-first | Scope or repo area is unclear | Run `dev-repo-onboarding` first. |
   | Blocked | Contradictory, unsafe, unbounded, or untestable | Stop and report blocker. |

2. Read repository instructions.

   - `AGENTS.md`
   - README and docs index
   - package/project metadata
   - build and test config
   - relevant source files
   - existing tests

3. Map source requirements to implementation units.

   For SDLC-backed work, link changes to requirement IDs, SPEC IDs, task IDs, or RTM rows.

   For direct-dev work, create temporary source labels in the report:

   ```text
   REQ-001 or DIRECT-REQ-001
   TASK-001
   VAL-001
   ```

4. Define the smallest safe scope.

   Identify:

   - files or modules likely affected
   - public contracts involved
   - data or migration risk
   - auth, permission, privacy, security, or release risk
   - tests or checks to run first
   - validation plan evidence to produce, if present
   - forbidden scope

5. Implement incrementally.

   - Prefer existing conventions.
   - Keep changes targeted.
   - Avoid unrelated refactors.
   - Preserve public contracts unless the task explicitly changes them.
   - Add or update tests when behavior changes.
   - Do not weaken tests to pass.

6. Validate.

   - Run the smallest relevant check first.
   - Follow Validation Plan evidence expectations when present.
   - Broaden checks only when the change or failure requires it.
   - Capture exact commands, status, and important output.
   - Separate failures caused by the change from pre-existing failures.

7. Report blockers or contradictions.

   Use this format:

   ```text
  Source / task ID:
  Contradiction or blocker:
  Repository evidence:
  Impact:
   Suggested next owner:
   Suggested resolution:
   ```

8. Handle midstream intake.

   If new information appears while implementing, classify it before editing further:

   | Type | Behavior |
   |---|---|
   | 同范围补充 | Merge into current task and validation. |
   | 旁路小修 | Treat as fast-lane direct-dev if independently validatable. |
   | 冲突变更 | Stop or reduce scope; report `Q` / contradiction with repository evidence. |
   | 紧急修复 | Fix minimally, validate, and report impact. |

   Dev does not silently update SDLC baselines. Escalate when scope, Architecture, Domain, business semantics, release risk, or validation baseline changes.

## Validation

Before final response, verify:

- Scope remained inside the task or handoff.
- Required behavior or direct request was addressed.
- Tests/checks were run or explicitly marked not run with reason.
- Validation Plan evidence expectations were satisfied or explicitly reported as not run / blocked.
- SDLC contradictions were reported rather than silently resolved.
- No SDLC artifacts were rewritten unless explicitly requested.

## Output

Return:

1. Entry path: SDLC-backed / partial-artifact / direct-dev / repo-onboarding-first / blocked
2. Source inputs used
3. Scope and files changed
4. Implementation summary
5. Validation commands and results
6. Requirement / task / test traceability, if available
7. Blockers, contradictions, or remaining risks

## Boundaries

- Do not invent missing requirements.
- Do not implement raw external AI/web suggestions without user confirmation or normalized `REQ` / `TASK` / `VAL`.
- Do not expand scope because the repository exposes adjacent code.
- Do not treat absent SDLC artifacts as automatic refusal.
- Do not treat absence of a formal Validation Plan as automatic refusal for clear direct-dev tasks.
- Do not claim release readiness unless release checks were actually performed.

## Handoff

- Use `dev-test-strategy` for validation design or test gap review.
- Use `sdlc-validation-plan-workflow` when the pre-implementation proof-of-correctness artifact itself is missing or needs SDLC-manager ownership.
- Use `dev-pr-review` for diff review before merge.
- Use `dev-security-review` or `dev-performance-diagnosis` when NFRs require it.
- Use `dev-release-check` when the change is release-bound.
- Return to `sdlc-manager` only when artifacts need ownership-level update, baseline change, traceability update, or change control.
