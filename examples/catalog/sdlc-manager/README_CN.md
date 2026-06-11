# SDLC Manager Catalog / SDLC 管理目录

`SDLC Manager` 是软件交付的 Architecture-first SDLC 控制面，负责 BRD、URS、PRD、NFR、SRS、HLD、LLD、ADR、领域边界、SPEC、需求追踪、变更控制、准备度检查和开发交接。

```text
架构定义结构。
领域边界定义归属。
规格定义执行。
```

## 边界

```text
sdlc-manager
  负责：交付契约、需求、架构/设计材料、领域边界、规格、追踪、准备度、开发交接

dev
  负责：仓库映射、实现、测试、review、发布验证
```

`SDLC Manager` 不替代 `dev`。

`dev` 有 SDLC 材料时使用这些材料；没有正式 SDLC 材料时，只要任务足够清楚，也可以继续走 direct-dev。

## Agents

```text
sdlc_project_researcher
sdlc_requirements_manager
sdlc_srs_specifier
sdlc_solution_spec_manager
sdlc_delivery_planner
sdlc_readiness_reviewer
sdlc_change_manager
```

## Skills

```text
sdlc-project-research
sdlc-router
sdlc-requirements-workflow
sdlc-brd-workflow
sdlc-urs-workflow
sdlc-prd-workflow
sdlc-nfr-spec
sdlc-srs-workflow
sdlc-hld-workflow
sdlc-lld-workflow
sdlc-domain-boundary-modeling
sdlc-modular-monolith-architecture
sdlc-architecture-decision-record
sdlc-solution-spec-workflow
sdlc-spec-slice-writer
sdlc-dev-handoff-planning
sdlc-requirements-traceability
sdlc-readiness-review
sdlc-change-control
```

## 车道与材料深度

```text
快线: dev-bugfix、小修、小配置、小文案、明确 issue
增补: 清楚的新功能、小模块或局部行为变化
重构: 外部行为基本不变的结构调整
重建: 替换、重写、迁移或能力重新映射
从头: greenfield 项目或全新子系统
```

用 ADS 判断 Architecture、Domain、Specification 影响，选择最小充分材料。
车道不是所有 dev 工作的全局门槛。

## 开发交接

推荐路径：

```text
requirements package / NFR / SPEC / RTM / Dev Handoff
HLD / LLD / ADR / Domain Boundary Map when relevant
-> dev repo onboarding
-> implementation
-> validation
-> review
-> release check when needed
```

允许的 direct-dev 路径：

```text
issue / bug report / user request / repo evidence
-> dev repo onboarding or direct implementation
-> validation
-> review
```
