# Agent Skill Map / Agent 与 Skill 分工

This is a public-safe map for the example five-pack Codex preset catalog.

这是一个公开安全的五类 Codex 预设分工示例。

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
| `common_context_summarizer` | Context compression and handoff | optional runtime-provided long-text workflow |
| `common_docs_researcher` | Docs, CLI, config, schema, and source verification | optional runtime-provided long-text workflow |
| `common_quality_reviewer` | Output review and unsupported-claim detection | optional runtime-provided review workflow |
| `common_file_organizer` | Folder organization, manifests, indexes | optional runtime-provided file-indexing workflow |

## Dev Pack / 开发包

| Agent | Role | Recommended Skills |
|---|---|---|
| `dev_api_designer` | API contract design and review | `api-contract-review`, `fullstack-feature`, `test-strategy` |
| `dev_backend_engineer` | Backend services, APIs, data integrity, auth, queues, observability | `api-contract-review`, `test-strategy`, `security-review`, `performance-diagnosis` |
| `dev_cli_engineer` | CLI flags, config discovery, exit codes, terminal UX | `cli-tooling-workflow`, `test-strategy`, `release-check` |
| `dev_code_mapper` | Read-only codebase mapping before implementation | `repo-onboarding`, `refactor-plan`, `migration-plan` |
| `dev_code_reviewer` | Review diffs, PRs, regressions, test gaps | `pr-review`, `security-review`, `api-contract-review`, `test-strategy` |
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
| `data_sql_analyst` | SQL and metric logic review | `sql-analysis`, `tabular-analysis` |
| `data_script_builder` | Reproducible data scripts and outputs | `tabular-analysis`, `data-cleaning`, `sql-analysis`, `analysis-report` |
| `data_insight_reviewer` | Review analysis claims, charts, and recommendations | `analysis-report`, `tabular-analysis`, `sql-analysis` |

## Office Pack / 办公包

| Agent | Role | Recommended Skills |
|---|---|---|
| `office_weekly_summarizer` | Extract weekly progress, blockers, and missing information | `weekly-report` |
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

github
  common + dev

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
