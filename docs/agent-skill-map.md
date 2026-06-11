# Agent Skill Map / Agent 与 Skill 分工

This is a public-safe map for the example six-pack Codex preset catalog. It is
the detailed reference for which agents and skills are included, what each role
is for, and which skills are recommended by each agent.

这是一个公开安全的六类 Codex 预设分工示例，也是支持 agent / skill 的详细索引：
包含哪些 agent / skill、每个角色负责什么、每个 agent 推荐哪些 skills。

It documents the relationship between agents, recommended skills, and suites without exposing private paths, private workflows, or real machine state.

它只说明 agents、recommended skills 和 suites 的关系，不暴露私有路径、私有工作流或真实本机状态。

## Rules / 规则

```text
Agent
  EN: Role, judgment, boundaries, delegation style.
  CN: 角色、判断边界、分工方式。

Skill
  EN: Reusable workflow, validation gates, scripts, references, assets.
  CN: 可复用工作流、验证门槛、脚本、参考资料和资产。

Suite
  EN: Runtime-visible composition of agents and skills.
  CN: 当前运行目录可见的 agent/skill 组合包。
```

Recommended skills are hints in `developer_instructions`. They are not hard bundles.

`Recommended skills` 是写在 `developer_instructions` 里的提示，不是强制捆绑。

Actual availability is decided by runtime filesystem visibility:

实际可用性由 runtime 文件结构决定：

```text
<runtime>/.codex/agents
<runtime>/.codex/skills
```

## Common Pack / 通用包

| Agent / Entry | Role | Recommended Skills |
|---|---|---|
| `common_task_planner` | Task decomposition, assumptions, validation plan | optional runtime-provided long-text workflow |
| `common_orchestrator` | Cross-domain task coordination, agent lineup, handoffs, validation gates | optional runtime-provided long-text workflow |
| `common_context_summarizer` | Context compression and handoff | optional runtime-provided long-text workflow |
| `common_docs_researcher` | Docs, CLI, config, schema, and source verification | optional runtime-provided long-text workflow |
| `common_quality_reviewer` | Output review and unsupported-claim detection | optional runtime-provided review workflow |
| `common_file_organizer` | Folder organization, manifests, indexes | optional runtime-provided file-indexing workflow |

`common_orchestrator` is a lightweight Codex orchestration preset. It coordinates plans and handoffs; it does not replace the main/default agent as the runtime controller.

## SDLC Manager Pack / SDLC 管理包

| Agent | Role | Recommended Skills |
|---|---|---|
| default Codex Next routing | SDLC control-plane entrypoint before choosing specific SDLC authoring or review workflows | `sdlc-manager`, `sdlc-router` |
| `sdlc_project_researcher` | Existing-project capability mapping, evidence paths, gaps, and downstream SDLC routing | `sdlc-project-research`, `sdlc-requirements-traceability`, `sdlc-readiness-review` |
| `sdlc_requirements_manager` | BRD, URS, PRD, scope baseline, assumptions, success metrics, and requirements package shaping | `sdlc-requirements-workflow`, `sdlc-brd-workflow`, `sdlc-urs-workflow`, `sdlc-prd-workflow`, `sdlc-router` |
| `sdlc_srs_specifier` | Software-facing SRS, requirement IDs, acceptance criteria, NFR hooks, and traceability-ready requirements | `sdlc-srs-workflow`, `sdlc-nfr-spec`, `sdlc-requirements-traceability` |
| `sdlc_solution_spec_manager` | Architecture-first solution package, HLD/LLD/ADR/domain-boundary routing, NFR impact, and SPEC slice organization | `sdlc-solution-spec-workflow`, `sdlc-hld-workflow`, `sdlc-lld-workflow`, `sdlc-domain-boundary-modeling`, `sdlc-modular-monolith-architecture`, `sdlc-architecture-decision-record`, `sdlc-spec-slice-writer`, `sdlc-nfr-spec`, `sdlc-readiness-review` |
| `sdlc_delivery_planner` | Dev handoff and task cards from SRS/NFR/HLD/LLD/ADR/domain-boundary/SPEC/RTM/issue evidence | `sdlc-dev-handoff-planning`, `sdlc-requirements-traceability`, `sdlc-readiness-review` |
| `sdlc_readiness_reviewer` | Readiness review for SDLC materials, direct-dev requests, or handoff packages | `sdlc-readiness-review`, `sdlc-requirements-traceability`, `sdlc-dev-handoff-planning` |
| `sdlc_change_manager` | Baseline, scope, requirement, traceability, and change-control decisions | `sdlc-change-control`, `sdlc-requirements-traceability`, `sdlc-readiness-review` |

`sdlc-manager` is the bundled SDLC entrypoint skill and the Architecture-first SDLC control plane: architecture defines structure, domain boundaries define ownership, and specifications define execution. It owns requirements, architecture/design artifacts, domain boundaries, SPEC slices, traceability, readiness, change control, and dev handoff.

`sdlc-project-research` is the lightweight upstream entry point when an existing codebase needs an evidence-grounded capability map before BRD/URS/PRD, SRS/SPEC, traceability, handoff, or reporting work. It defaults to Simplified Chinese file names, sections, table headers, statuses, notes, and next steps. Default artifacts are `项目能力摘要.md`, `项目功能能力地图.md`, and `项目能力表.csv`.

`sdlc-solution-spec-workflow` coordinates a solution package; it should not replace dedicated `sdlc-hld-workflow`, `sdlc-lld-workflow`, `sdlc-domain-boundary-modeling`, `sdlc-modular-monolith-architecture`, or `sdlc-architecture-decision-record` workflows.

`sdlc-manager` 是插件内的 SDLC 入口 skill，也是架构先行的 SDLC 控制面：架构定义结构，领域边界定义归属，规格定义执行。它负责需求、架构/设计材料、领域边界、SPEC 切片、需求追踪、准备度、变更控制和开发交接。

`sdlc-project-research` 是现有代码库进入 BRD/URS/PRD、SRS/SPEC、traceability、handoff 或汇报前的轻量上游入口，先形成证据可追溯的项目功能能力地图。默认只产出 `项目能力摘要.md`、`项目功能能力地图.md` 和 `项目能力表.csv`，并默认使用简体中文文件名、中文章节、中文表头、中文状态、中文备注和中文下一步。

`sdlc-solution-spec-workflow` 负责协调 solution package；它不替代专项的 `sdlc-hld-workflow`、`sdlc-lld-workflow`、`sdlc-domain-boundary-modeling`、`sdlc-modular-monolith-architecture` 或 `sdlc-architecture-decision-record`。

## Dev Pack / 开发包

| Agent | Role | Recommended Skills |
|---|---|---|
| `dev_api_designer` | API contract design and review | `dev-api-contract-review`, `dev-fullstack-feature`, `dev-test-strategy` |
| `dev_architect_reviewer` | Architecture, service boundaries, technology choices, migration paths, reliability, and evolution risk review | `dev-migration-plan`, `dev-refactor-plan`, `dev-api-contract-review`, `dev-security-review`, `dev-performance-diagnosis`, `dev-test-strategy` |
| `dev_backend_engineer` | Backend services, APIs, data integrity, auth, queues, observability | `dev-spec-driven-implementation`, `dev-api-contract-review`, `dev-test-strategy`, `dev-security-review`, `dev-performance-diagnosis` |
| `dev_cli_engineer` | CLI flags, config discovery, exit codes, terminal UX | `dev-spec-driven-implementation`, `dev-cli-tooling-workflow`, `dev-test-strategy`, `dev-release-check` |
| `dev_code_mapper` | Read-only codebase mapping before implementation | `dev-repo-onboarding`, `dev-refactor-plan`, `dev-migration-plan` |
| `dev_code_reviewer` | Review diffs, PRs, regressions, test gaps | `dev-pr-review`, `dev-security-review`, `dev-api-contract-review`, `dev-test-strategy` |
| `dev_docs_engineer` | Developer docs, API/CLI docs, guides, README structure, and docs-as-code workflows | `dev-repo-onboarding`, `dev-api-contract-review`, `dev-cli-tooling-workflow`, `dev-release-check` |
| `dev_docs_researcher` | API, SDK, CLI, config, version behavior verification | `dev-api-contract-review`, `dev-dependency-upgrade`, `dev-release-check` |
| `dev_frontend_engineer` | UI components, state, routing, accessibility, browser validation | `dev-spec-driven-implementation`, `dev-frontend-ui-implementation`, `dev-test-strategy`, `dev-performance-diagnosis` |
| `dev_implementer` | Scoped implementation, bug fixes, tests, targeted refactors | `dev-spec-driven-implementation`, `dev-bugfix`, `dev-fullstack-feature`, `dev-refactor-plan`, `dev-test-strategy`, `dev-api-contract-review`, `dev-dependency-upgrade` |
| `dev_performance_engineer` | Measured performance diagnosis and optimization | `dev-performance-diagnosis`, `dev-build-optimization`, `dev-test-strategy` |
| `dev_python_engineer` | Python scripts, APIs, CLIs, packaging, typing, pytest | `dev-spec-driven-implementation`, `dev-python-quality`, `dev-test-strategy`, `dev-performance-diagnosis`, `dev-dependency-upgrade` |
| `dev_security_reviewer` | Read-only security review | `dev-security-review`, `dev-dependency-upgrade`, `dev-pr-review` |
| `dev_test_runner` | Test execution, failure reproduction, log diagnosis | `dev-bugfix`, `dev-test-strategy`, `dev-performance-diagnosis` |

## Data Pack / 数据包

| Agent | Role | Recommended Skills |
|---|---|---|
| `data_profile_analyst` | Dataset profiling, schema, grain, missingness, anomalies | `data-tabular-analysis`, `data-cleaning` |
| `data_pipeline_engineer` | Reproducible ETL/ELT, data quality checks, orchestration, and data monitoring | `data-cleaning`, `data-sql-analysis`, `data-tabular-analysis`, `data-analysis-report` |
| `data_sql_analyst` | SQL and metric logic review | `data-sql-analysis`, `data-tabular-analysis` |
| `data_script_builder` | Reproducible data scripts and outputs | `data-tabular-analysis`, `data-cleaning`, `data-sql-analysis`, `data-analysis-report` |
| `data_insight_reviewer` | Review analysis claims, charts, and recommendations | `data-analysis-report`, `data-tabular-analysis`, `data-sql-analysis` |

## Office Pack / 办公包

| Agent | Role | Recommended Skills |
|---|---|---|
| `office_weekly_summarizer` | Extract weekly progress, blockers, and missing information | `office-weekly-report` |
| `office_product_planner` | Product planning, PRD drafting, requirement consolidation, roadmap framing, and success metrics | `office-briefing-note`, `office-project-report`, `office-weekly-report` |
| `office_report_writer` | Draft reports, status updates, briefings, and management summaries | `office-weekly-report`, `office-project-report`, `office-briefing-note` |
| `office_meeting_summarizer` | Meeting minutes, decisions, owners, deadlines | `office-meeting-summary` |
| `office_slide_planner` | Deck storyline, slide outline, speaker notes | `office-ppt-outline` |

## Research Pack / 研究包

| Agent | Role | Recommended Skills |
|---|---|---|
| `research_material_processor` | Inventory, classify, and deduplicate collected materials | `research-source-dedup`, `research-evidence-table` |
| `research_evidence_mapper` | Claim/evidence/source mapping | `research-evidence-table`, `research-source-dedup` |
| `research_gap_finder` | Find gaps, conflicts, weak assumptions, and follow-up questions | `research-evidence-table`, `research-synthesis` |
| `research_synthesis_writer` | Draft research briefs and synthesis notes | `research-synthesis`, `research-evidence-table`, `office-briefing-note` |

## Suite Examples / Suite 示例

```text
user
  common

planning
  common + sdlc-manager

github
  common + sdlc-manager + dev

nondev-data
  common + data

nondev-office
  common + office

nondev-research
  common + research

nondev-all
  common + data + office + research

all
  common + sdlc-manager + dev + data + office + research
```

Runtime links should expose only:

runtime 只应暴露：

```text
<runtime>/.codex/agents -> <suite>/agents
<runtime>/.codex/skills -> <suite>/skills
```

Do not symlink an entire `.codex` folder.

不要 symlink 整个 `.codex` 文件夹。
