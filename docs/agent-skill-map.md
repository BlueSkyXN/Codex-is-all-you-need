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

| Agent | Role | Recommended Skills |
|---|---|---|
| `common_task_planner` | Task decomposition, assumptions, validation plan | optional runtime-provided long-text workflow |
| `common_orchestrator` | Cross-domain task coordination, agent lineup, handoffs, validation gates | optional runtime-provided long-text workflow |
| `common_context_summarizer` | Context compression and handoff | optional runtime-provided long-text workflow |
| `common_docs_researcher` | Docs, CLI, config, schema, and source verification | optional runtime-provided long-text workflow |
| `common_quality_reviewer` | Output review and unsupported-claim detection | optional runtime-provided review workflow |
| `common_file_organizer` | Folder organization, manifests, indexes | optional runtime-provided file-indexing workflow |

`common_orchestrator` is a lightweight Codex orchestration preset. It coordinates plans and handoffs; it does not replace the main/default agent as the runtime controller.

## Product Engineering Pack / 产品工程包

| Agent | Role | Recommended Skills |
|---|---|---|
| `product_engineering_project_researcher` | Existing-project capability mapping with Simplified Chinese artifacts by default: `项目能力摘要.md`, `项目功能能力地图.md`, `项目能力表.csv` | `project-research`, `readiness-review` |
| `product_engineering_requirements_lead` | PRD, scope lock, non-goals, success metrics, and spec handoff | `prd-workflow`, `project-research` |
| `product_engineering_functional_specifier` | Functional behavior, flows, states, fields, permissions, errors, ACs, and traceability | `functional-spec`, `prd-workflow`, `project-research` |
| `product_engineering_technical_bridge` | Engineering bridge drafts, API/data implications, NFRs, test draft, and owner-confirmation questions | `technical-spec-bridge` |
| `product_engineering_delivery_planner` | Implementation plan, task breakdown, dependency graph, validation tasks, and dev handoff | `delivery-task-planning`, `readiness-review`, `project-research` |
| `product_engineering_readiness_reviewer` | Readiness review for PRD, spec, tech bridge, delivery plan, or change-spec handoff | `readiness-review`, `project-research` |
| `product_engineering_change_adapter` | Repository change-spec or OpenSpec-style proposal, design, tasks, and behavior deltas | `change-spec-adapter`, `readiness-review` |

`project-research` is the lightweight upstream entry point when an existing codebase needs an evidence-grounded capability map before PRD, planning, or reporting work. It defaults to Simplified Chinese file names, sections, table headers, statuses, notes, and next steps. Default artifacts are `项目能力摘要.md`, `项目功能能力地图.md`, and `项目能力表.csv`.

`product-engineering` is a planning and engineering-management layer. It should prepare `agent-handoff.md`, `task-breakdown.md`, `review-report.md`, or equivalent change-spec artifacts before `dev` takes over implementation.

`project-research` 是现有代码库进入 PRD、规划或汇报前的轻量上游入口，先形成证据可追溯的项目功能能力地图。默认只产出 `项目能力摘要.md`、`项目功能能力地图.md` 和 `项目能力表.csv`，并默认使用简体中文文件名、中文章节、中文表头、中文状态、中文备注和中文下一步；工作分解、产品结构拆解、成熟度、卡点、规格、任务规划、评分和汇报叙事都属于下游活动。

`product-engineering` 是规划与工程管理层。它应该在 `dev` 接手实现前，准备好 `agent-handoff.md`、`task-breakdown.md`、`review-report.md` 或等价 change-spec 产物。

## Dev Pack / 开发包

| Agent | Role | Recommended Skills |
|---|---|---|
| `dev_api_designer` | API contract design and review | `api-contract-review`, `fullstack-feature`, `test-strategy` |
| `dev_architect_reviewer` | Architecture, service boundaries, technology choices, migration paths, reliability, and evolution risk review | `migration-plan`, `refactor-plan`, `api-contract-review`, `security-review`, `performance-diagnosis`, `test-strategy` |
| `dev_backend_engineer` | Backend services, APIs, data integrity, auth, queues, observability | `api-contract-review`, `test-strategy`, `security-review`, `performance-diagnosis` |
| `dev_cli_engineer` | CLI flags, config discovery, exit codes, terminal UX | `cli-tooling-workflow`, `test-strategy`, `release-check` |
| `dev_code_mapper` | Read-only codebase mapping before implementation | `repo-onboarding`, `refactor-plan`, `migration-plan` |
| `dev_code_reviewer` | Review diffs, PRs, regressions, test gaps | `pr-review`, `security-review`, `api-contract-review`, `test-strategy` |
| `dev_docs_engineer` | Developer docs, API/CLI docs, guides, README structure, and docs-as-code workflows | `repo-onboarding`, `api-contract-review`, `cli-tooling-workflow`, `release-check` |
| `dev_docs_researcher` | API, SDK, CLI, config, version behavior verification | `api-contract-review`, `dependency-upgrade`, `release-check` |
| `dev_frontend_engineer` | UI components, state, routing, accessibility, browser validation | `frontend-ui-implementation`, `test-strategy`, `performance-diagnosis` |
| `dev_implementer` | Scoped implementation, bug fixes, tests, targeted refactors | `bugfix`, `fullstack-feature`, `refactor-plan`, `test-strategy`, `api-contract-review`, `dependency-upgrade` |
| `dev_performance_engineer` | Measured performance diagnosis and optimization | `performance-diagnosis`, `build-optimization`, `test-strategy` |
| `dev_python_engineer` | Python scripts, APIs, CLIs, packaging, typing, pytest | `python-quality`, `test-strategy`, `performance-diagnosis`, `dependency-upgrade` |
| `dev_security_reviewer` | Read-only security review | `security-review`, `dependency-upgrade`, `pr-review` |
| `dev_test_runner` | Test execution, failure reproduction, log diagnosis | `bugfix`, `test-strategy`, `performance-diagnosis` |

## Data Pack / 数据包

| Agent | Role | Recommended Skills |
|---|---|---|
| `data_profile_analyst` | Dataset profiling, schema, grain, missingness, anomalies | `tabular-analysis`, `data-cleaning` |
| `data_pipeline_engineer` | Reproducible ETL/ELT, data quality checks, orchestration, and data monitoring | `data-cleaning`, `sql-analysis`, `tabular-analysis`, `analysis-report` |
| `data_sql_analyst` | SQL and metric logic review | `sql-analysis`, `tabular-analysis` |
| `data_script_builder` | Reproducible data scripts and outputs | `tabular-analysis`, `data-cleaning`, `sql-analysis`, `analysis-report` |
| `data_insight_reviewer` | Review analysis claims, charts, and recommendations | `analysis-report`, `tabular-analysis`, `sql-analysis` |

## Office Pack / 办公包

| Agent | Role | Recommended Skills |
|---|---|---|
| `office_weekly_summarizer` | Extract weekly progress, blockers, and missing information | `weekly-report` |
| `office_product_planner` | Product planning, PRD drafting, requirement consolidation, roadmap framing, and success metrics | `briefing-note`, `project-report`, `weekly-report` |
| `office_report_writer` | Draft reports, status updates, briefings, and management summaries | `weekly-report`, `project-report`, `briefing-note` |
| `office_meeting_summarizer` | Meeting minutes, decisions, owners, deadlines | `meeting-summary` |
| `office_slide_planner` | Deck storyline, slide outline, speaker notes | `ppt-outline` |

## Research Pack / 研究包

| Agent | Role | Recommended Skills |
|---|---|---|
| `research_material_processor` | Inventory, classify, and deduplicate collected materials | `source-dedup`, `evidence-table` |
| `research_evidence_mapper` | Claim/evidence/source mapping | `evidence-table`, `source-dedup` |
| `research_gap_finder` | Find gaps, conflicts, weak assumptions, and follow-up questions | `evidence-table`, `research-synthesis` |
| `research_synthesis_writer` | Draft research briefs and synthesis notes | `research-synthesis`, `evidence-table`, `briefing-note` |

## Suite Examples / Suite 示例

```text
user
  common

planning
  common + product-engineering

github
  common + product-engineering + dev

nondev-data
  common + data

nondev-office
  common + office

nondev-research
  common + research

nondev-all
  common + data + office + research
```

Runtime links should expose only:

runtime 只应暴露：

```text
<runtime>/.codex/agents -> <suite>/agents
<runtime>/.codex/skills -> <suite>/skills
```

Do not symlink an entire `.codex` folder.

不要 symlink 整个 `.codex` 文件夹。
