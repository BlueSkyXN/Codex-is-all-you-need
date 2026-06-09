# Architecture-first SDLC Manager Flow / 架构先行 SDLC 管理流程

This document defines the public `sdlc-manager` catalog as an Architecture-first, Domain-bounded, Spec-executed SDLC control plane between product or business inputs and repository implementation.

本文档定义公开版 `sdlc-manager` catalog：它位于产品/业务输入和代码实现之间，是 Architecture-first、Domain-bounded、Spec-executed 的 SDLC 控制面。

```text
Architecture defines structure.
Domain boundaries define ownership.
Specifications define execution.
```

```text
架构定义结构。
领域边界定义归属。
规格定义执行。
```

## Boundary / 边界

```text
office
  EN: meeting notes, reports, product planning notes, roadmap framing.
  CN: 会议纪要、报告、产品规划笔记、roadmap 表述。

sdlc-manager
  EN: BRD, URS, PRD, SRS, NFR, HLD, LLD, ADR, domain boundaries,
      SPEC slices, traceability, change control, readiness review, and dev handoff.
  CN: BRD、URS、PRD、SRS、NFR、HLD、LLD、ADR、领域边界、
      SPEC 切片、需求追踪、变更控制、准备度审查和开发交接。

dev
  EN: repository mapping, implementation, tests, code review, security review,
      performance diagnosis, release validation, and direct-dev when the task is clear.
  CN: 仓库映射、实现、测试、代码 review、安全 review、性能诊断、
      发布验证，以及任务清楚时的 direct-dev。
```

`sdlc-manager` does not replace `dev`. It prepares delivery contracts and architecture/spec materials when the work needs them. `dev` consumes those materials when present, but missing SDLC artifacts are a risk signal, not an automatic stop condition for every clear bug fix, issue, or direct user request.

`sdlc-manager` 不替代 `dev`。它在工作需要时准备交付契约、架构材料和规格材料。`dev` 在材料存在时使用这些材料；但缺少 SDLC 材料只是风险信号，不是每个明确 bug fix、issue 或直接用户请求的自动阻断条件。

## Flow / 流程

```text
Idea / source materials / existing repository evidence
-> sdlc_project_researcher when evidence mapping is needed
-> sdlc_requirements_manager for BRD / URS / PRD / scope baseline
-> sdlc_srs_specifier for software-facing SRS
-> sdlc_solution_spec_manager for HLD / LLD / ADR / domain-boundary / SPEC package routing
-> sdlc_delivery_planner for dev handoff and task cards
-> sdlc_readiness_reviewer for proceed / revise / blocked judgment
-> dev catalog when implementation begins
```

Change control stays inside the same control plane:

变更控制仍在同一个控制面内：

```text
baseline / scope / requirements / architecture change
-> sdlc_change_manager
-> traceability impact
-> revised SDLC artifacts or dev handoff
```

## Role Split / 角色拆分

| Phase | Agent | Primary Skills |
|---|---|---|
| Existing-project research | `sdlc_project_researcher` | `project-research`, `requirements-traceability`, `sdlc-readiness-review` |
| Requirements | `sdlc_requirements_manager` | `requirements-workflow`, `brd-workflow`, `urs-workflow`, `prd-workflow`, `artifact-profile-router` |
| Software requirements | `sdlc_srs_specifier` | `srs-workflow`, `nfr-spec`, `requirements-traceability` |
| Architecture and solution package | `sdlc_solution_spec_manager` | `solution-spec-workflow`, `hld-workflow`, `lld-workflow`, `domain-boundary-modeling`, `modular-monolith-architecture`, `architecture-decision-record`, `spec-slice-writer`, `nfr-spec` |
| Delivery planning | `sdlc_delivery_planner` | `dev-handoff-planning`, `requirements-traceability`, `sdlc-readiness-review` |
| Readiness review | `sdlc_readiness_reviewer` | `sdlc-readiness-review`, `requirements-traceability`, `dev-handoff-planning` |
| Change control | `sdlc_change_manager` | `change-control`, `requirements-traceability`, `sdlc-readiness-review` |

## Artifact Depth / 材料深度

Use the smallest sufficient artifact profile. Do not force every task through the full stack.

使用最小充分材料等级。不要强制每个任务都走完整材料栈。

```text
Profile A: Task Delivery
Profile B: Feature Delivery
Profile C: System Delivery
Profile D: Program Delivery
```

Small direct-dev tasks may only need a clear issue, repository evidence, and validation path. Larger or riskier changes may need SRS, NFR, HLD, LLD, ADR, Domain Boundary Map, SPEC slices, RTM, and handoff materials.

小型 direct-dev 任务可能只需要明确 issue、仓库证据和验证路径。更大或风险更高的变更可能需要 SRS、NFR、HLD、LLD、ADR、Domain Boundary Map、SPEC 切片、RTM 和交接材料。

## Suite Guidance / Suite 建议

Recommended local suite shapes:

推荐的本机 suite 形态：

```text
planning
  common + sdlc-manager

github
  common + sdlc-manager + dev

dev-only
  common + dev

nondev-office
  common + office
```

Use `planning` when a directory mainly holds requirements, architecture, specs, taskbooks, or handoff packages. Use `github` when a code workspace needs both SDLC control-plane and repo-aware development capabilities. Use `dev-only` only when planning artifacts are intentionally out of scope.

当目录主要放需求、架构、规格、任务书或交接包时，使用 `planning`。当代码工作区同时需要 SDLC 控制面和 repo-aware 开发能力时，使用 `github`。只有明确不需要规划材料时，才使用 `dev-only`。

## Handoff Standard / 交接标准

Before switching to implementation, the SDLC layer should pass along the relevant constraints rather than just a task title:

切换到实现前，SDLC 层应传递相关约束，而不是只传一个任务标题：

- scope, non-scope, assumptions, and acceptance criteria
- related SRS, NFR, SPEC slices, and RTM rows when present
- architecture constraints from HLD, LLD, ADR, or Domain Boundary Map when present
- domain ownership, allowed dependencies, and forbidden dependencies when relevant
- validation expectations and known blockers

`dev` can still proceed without formal SDLC artifacts when the user request, issue, failing test, or repository evidence is clear enough. In that case it should state assumptions, preserve existing repo boundaries, and report missing artifacts as risk/context rather than an automatic refusal.

没有正式 SDLC 材料时，只要用户请求、issue、失败测试或仓库证据足够清楚，`dev` 仍可继续推进。这时应说明假设，保持现有仓库边界，并把缺失材料报告为风险/上下文缺口，而不是自动拒绝。
