---
name: sdlc-router
description: Use to route SDLC/ADS work by scenario lane and choose the smallest sufficient materials for 重建、重构、增补、从头开发、bugfix、规则变更、发布、local/sdlc、交付卡、handoff, or direct-dev.
---

# Artifact Profile Router

Use this skill when a request may need SDLC/ADS materials but the smallest safe path is unclear.

This skill only routes. It does not write BRD, URS, PRD, SRS, NFR, HLD, LLD, ADR, SPEC, RTM, handoff, or implementation content.

For the canonical vocabulary, local state layout, ID contract, and lightweight templates, read `references/sdlc-operating-model.md`.

## Use When

- The user asks whether a task needs formal SDLC materials or can go directly to dev.
- The work may affect product scope, architecture, domain ownership, data ownership, API contracts, permissions, compliance, security, privacy, release, rollback, or validation evidence.
- Existing materials are mixed, incomplete, stale, or not clearly connected to implementation.
- New information appears during implementation and needs to be classified as same-scope, side-path, conflicting, or urgent.
- A task mentions 重建、重构、增补、从头开发、bugfix、规则变更、发布、`local/sdlc`, 交付卡, `handoff`, or `direct-dev`.
- The user brings a plan from Web, GPT5.5Pro, another AI, a pasted discussion, or an external research session and wants to make it usable in the SDLC/dev flow.

Do not use this skill for simple read-only explanation when no delivery decision is needed. Use `direct-read` / `dev-repo-onboarding` style exploration instead.

## Inputs

Read what is available:

- User request, issue, bug report, support ticket, meeting note, roadmap item, or business brief.
- External discussion notes, pasted AI output, web research summary, or proposal draft.
- Existing repo evidence, tests, logs, current implementation, and known validation commands.
- Existing SDLC/ADS materials: BRD, URS, PRD, SRS, NFR, HLD, LLD, ADR, Domain Boundary Map, SPEC, Validation Plan, RTM, design docs, or architecture notes.
- Existing local state, when present:
  - `local/sdlc/_资产.md`
  - `local/sdlc/架构.md`
  - `local/sdlc/领域.md`
  - current `local/sdlc/<slug>/00-状态.md`
- Delivery constraints: deadline, target release, risk tolerance, stakeholders, platform, release or rollback needs.

If inputs are missing, route using the evidence available and mark assumptions explicitly. Missing SDLC material is a risk signal, not a global stop condition.

## Routing Workflow

### 1. Classify the lane

- `none`: read-only explanation, codebase onboarding, fact check, or research with no delivery decision.
- `快线`: bugfix, small repair, config, copy, clear issue, or localized task.
- `增补`: clear new feature, small module, contained behavior change, or implementation-facing addition.
- `重构`: external behavior should stay basically unchanged while structure, dependencies, modules, or implementation change.
- `重建`: old system/module replacement, rewrite, migration, or capability re-mapping.
- `从头`: greenfield project, new subsystem, or no meaningful existing baseline.

Modifiers:

- `规则变更`: permissions, billing, data metrics, state machine, compliance, privacy, business semantics, domain ownership, or data ownership changes.
- `发布`: release, rollback, launch evidence, support burden, or rollout risk changes.

### 2. Classify midstream intake when applicable

Only output `Intake` when new information arrives during an active implementation:

- `同范围补充`: append to current `TASK` / `VAL`.
- `旁路小修`: use fast-lane `direct-dev`; record only if it affects current state.
- `冲突变更`: update current state, record `Q` / `DEC`, and decide whether ADS/spec must change.
- `紧急修复`: fix first through fast lane, validate minimally, then record impact.

Do not restart SDLC by default for midstream intake.

### 2a. Classify external proposal intake when applicable

When the source is Web, GPT5.5Pro, another AI, pasted chat, or an external proposal:

- Treat it as reference input, not executable truth.
- If short, summarize it into current `00-状态.md`.
- If long, route it to `local/sdlc/<slug>/01-外部讨论.md`.
- Convert only accepted pieces into `REQ`, `TASK`, and `VAL`.
- Label evidence as `[用户确认]`, `[外部建议]`, `[代码证据]`, `[local材料]`, `[推断]`, or `[未验证]`.

If the external proposal conflicts with repository evidence, route as `冲突变更` or `blocked`.

### 3. Make the ADS quick judgment

- `A / Architecture`: does it affect architecture, module/runtime boundaries, dependency direction, deployment, migration, or durable technical decisions?
- `D / Domain`: does it affect domain ownership, business rules, data ownership, permissions, metrics, privacy, compliance, or forbidden dependencies?
- `S / Specification`: are scope, non-scope, acceptance, and validation clear enough for implementation?

Use ADS as a judgment frame, not as a requirement to write A/D/S documents every time.

### 4. Choose the dev path

- `direct-read`: no delivery decision; explain, inspect, map, or verify facts.
- `direct-dev`: clear, local, reversible or low-risk, and independently verifiable.
- `handoff-lite`: scope is clear but cross-session, cross-agent, or task/validation handoff is useful.
- `handoff-full`: architecture/domain impact, rule change, rebuild, greenfield, multi-wave delivery, release risk, or validation ambiguity requires durable materials.
- `blocked`: user decision is required for business tradeoff, compatibility, risk acceptance, irreversible operation, or spec contradiction.

### 5. Choose the smallest sufficient materials

Default material budgets:

- `none`: no `local/sdlc` material.
- `快线`: 0 files; optional delivery card only when state must survive across sessions.
- `增补`: existing ADS state plus `handoff-lite` or `20-规格.md` only if needed.
- `重构`: as-built, to-be, behavior baseline, and migration handoff.
- `重建`: capability map, scope decision table, first-wave spec, first-wave handoff.
- `从头`: lightweight requirements package, initial architecture/domain, first-wave spec, first-wave handoff.

BRD, URS, PRD, SRS, full RTM, and full change-control are not default gates for bugfix, clear small feature, pure refactor, or direct-dev.

Escalate only when scope, Architecture, Domain, business semantics, release risk, or validation baseline changes.

## Next Skill Routing

Use the smallest next step:

- Read-only repo exploration: `dev-repo-onboarding`
- Bugfix or urgent repair: `dev-bugfix`
- Direct implementation from clear input: `dev-spec-driven-implementation`
- Requirements package or Product Pack: `sdlc-requirements-workflow`, `sdlc-prd-workflow`, `sdlc-brd-workflow`, `sdlc-urs-workflow`
- Software requirements or NFR: `sdlc-srs-workflow`, `sdlc-nfr-spec`
- Architecture or domain impact: `sdlc-hld-workflow`, `sdlc-domain-boundary-modeling`, `sdlc-architecture-decision-record`, `sdlc-modular-monolith-architecture`
- Detailed design or implementation-facing slices: `sdlc-lld-workflow`, `sdlc-solution-spec-workflow`, `sdlc-spec-slice-writer`
- Handoff: `sdlc-dev-handoff-planning`
- Validation plan: `sdlc-validation-plan-workflow`
- Traceability or change control: `sdlc-requirements-traceability`, `sdlc-change-control`
- Readiness check: `sdlc-readiness-review`
- Refactor or migration planning: `dev-refactor-plan`, `dev-migration-plan`
- Release readiness: `dev-release-check`

## Output

Return this compact block:

```markdown
## Routing Result

- Lane: none / 快线 / 增补 / 重构 / 重建 / 从头
- Modifier: none / 规则变更 / 发布
- Intake: none / 同范围补充 / 旁路小修 / 冲突变更 / 紧急修复
- ADS:
  - A:
  - D:
  - S:
- Dev path: direct-read / direct-dev / handoff-lite / handoff-full / blocked

## Required

Now:
-

Before dev:
-

## Not needed

-

## Next skill

-
```

Omit `Intake` when the request is not midstream.

## Boundaries

- Do not inflate artifact needs to imitate a heavy process.
- Do not weaken artifact needs when implementation would otherwise guess scope, ownership, validation, or release risk.
- Do not make Validation Plan, RTM, PRD, or SRS universal blockers for clear, narrow, verifiable direct-dev tasks.
- Do not let dev rewrite SDLC baseline silently; dev reports contradictions with repository evidence, and the controlling thread decides whether to update state, spec, architecture, or domain materials.
