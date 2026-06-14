# Codex Is All You Need

中文 | [English](README.md)

`Codex Is All You Need` 是一套公开安全的 V2 Codex plugin-first 预设体系。它不是一个“把某台机器完整复制出去”的私有配置仓库，而是把一套真实生产环境里的经验抽象成 source catalog、可安装插件包、示例素材、管理脚本和只读面板。

一句话：

```text
source catalog -> plugin package -> marketplace install
```

你可以用它做这些事：

1. 安装 Codex Next 插件，把公开 skills 打包成一套可复用工作流能力包。
2. 复制公开示例，搭建自己的本地 agent / skill catalog。
3. 学习如何围绕 plugin-first 工作流设计 Codex agents 和 skills。
4. 在需要时迁移或检查旧的 V1 suite / composition 设置。

## 适合谁

- 想把常用工作流沉淀成 Codex skills 的开发者。
- 想为不同任务域准备不同 custom agents 的团队或个人。
- 想把 Claude Code 风格的 agent / skill 经验迁移到 Codex 的用户。
- 想使用 plugin-first 共享 skills，并只在迁移或本机实验时查看 V1 suite 文档的人。
- 想公开分享 agent / skill 结构，但又不想泄露私有 prompt、路径、模板或真实配置的人。

## 这不是

- 不是 OpenAI 官方 preset 目录规范。
- 不是一键安装完整生产环境的脚本。
- 不是私有 `~/.codex` 或真实业务 skills 的镜像。
- 不是让父目录 `.codex` 自动继承到所有子 git repo 的机制。Codex repo-level discovery 有 project root 边界，详见 [架构说明](docs/architecture.md) 和 [发现边界](docs/discovery-boundaries.md)。

## 仓库结构

```text
dashboard/
  build_dashboard.py              # 只读 dashboard 生成器
  templates/index.html
  examples/config.example.toml

scripts/
  sync_codex_entrypoints.py       # 批量同步 repo-local .codex 入口

docs/
  usage-guide.md                  # 完整双语使用指南
  architecture.md                 # V2 plugin-first 架构
  agent-design.md                 # custom agent 设计
  skill-design.md                 # skill 设计
  agent-skill-map.md              # agent 与 skill 分工
  discovery-boundaries.md         # 脱敏后的 discovery 边界结论
  user-global-agents-example.md   # 公开安全的用户全局 AGENTS.md 示例
  model-catalog-override.md       # Codex 自定义模型 catalog override 教程
  global-git-ignore.md            # 用户级 Git ignore 配置
  v1/                             # legacy suite / composition 文档和迁移说明
  architecture-first-sdlc-flow.md
  claude-to-codex-migration.md
  public-private-strategy.md

plugins/
  codex-next/                      # 可安装的 skills 插件

examples/
  catalog/                        # 脱敏后的公开 agent / skill source catalog
  runtime/                        # runtime AGENTS.md 示例
  suites/                         # V1 suite 示例入口
```

## 当前 V2 模型

```text
source catalog
  存放真实 agent TOML 和 skill folder。
  示例：examples/catalog/dev/agents/dev_python_engineer.toml
       examples/catalog/dev/skills/dev-python-quality/SKILL.md

plugin package
  生产态公开共享 skills 的分发层。
  示例：plugins/codex-next/skills/dev-python-quality/SKILL.md
       .agents/plugins/marketplace.json

marketplace install
  用户安装插件包的入口。
  示例：codex plugin add codex-next@codex-is-all-you-need
```

V1 suite / composition 文档只用于迁移和兼容。只有当某台机器仍通过
`~/.codex/suites` 或 repo-local `.codex/skills` 链接暴露共享 skills 时，才从
[docs/v1/](docs/v1/) 开始看。

V2 的更详细解释见 [docs/usage-guide.md](docs/usage-guide.md) 和
[docs/architecture.md](docs/architecture.md)。

## 3 分钟快速用法

### 1. 查看公开 catalog

```bash
find examples/catalog -maxdepth 3 \( -path '*/agents/*.toml' -o -path '*/skills/*/SKILL.md' \)
```

公开示例包含：

| Pack | Agents | Skills | 用途 |
|---|---:|---:|---|
| `common` | 6 | 2 | 规划、编排、文档核查、质量复核、上下文压缩、文件整理 |
| `sdlc-manager` | 7 | 21 | 架构先行 SDLC 控制：BRD/URS/PRD、SRS/NFR、HLD/LLD、ADR、领域边界、SPEC、交接 |
| `dev` | 14 | 20 | 代码阅读、实现、测试、review、API、CLI、前端、Python、安全、性能 |
| `data` | 5 | 4 | 数据画像、SQL、清洗、pipeline、分析报告 |
| `office` | 5 | 5 | 会议纪要、周报、项目报告、briefing、PPT 大纲 |
| `research` | 4 | 3 | 材料整理、证据表、去重、综合分析、gap review |

完整分工见 [docs/agent-skill-map.md](docs/agent-skill-map.md)。

### 2. 安装 Codex Next

Codex Next 把公开安全的 skills 打包成一个可安装插件。它不打包
`.codex/agents` custom agent TOML，也不打包 V1 本机 suite symlink。插件内包含
`core-router` 入口 skill，用来把任务路由到最小充分的内置工作流。

插件源码：

```text
plugins/codex-next
```

仓库 marketplace：

```text
.agents/plugins/marketplace.json
```

从 GitHub marketplace source 安装：

```bash
codex plugin marketplace add https://github.com/BlueSkyXN/Codex-is-all-you-need.git
```

本地开发时，也可以把当前 checkout 的仓库根目录添加为 marketplace：

```bash
codex plugin marketplace add /path/to/Codex-is-all-you-need
```

确认 Codex 能看到未安装的 marketplace 条目。使用 JSON 输出时必须加
`--available`；否则 `codex plugin list --json` 只显示已安装插件，容易误判为
marketplace 为空。

```bash
codex plugin marketplace list --json
codex plugin list --marketplace codex-is-all-you-need --available --json
```

然后从这个 marketplace 安装插件：

```bash
codex plugin add codex-next@codex-is-all-you-need
```

安装后可以调用 `$codex-next:core-router`，或直接要求 Codex 使用 Codex Next 处理任务。

如果你要把已有 V1 机器从 suite-based runtime entrypoints 迁移到 Codex Next，见
[V1 To V2 Migration](docs/v1/suite-to-plugin-migration.md)。

### 3. 生成只读 dashboard

首次配置：

```bash
mkdir -p ~/.codex/dashboard
cp dashboard/examples/config.example.toml ~/.codex/dashboard/config.toml
```

编辑本机配置：

```text
~/.codex/dashboard/config.toml
```

生成面板：

```bash
python3 dashboard/build_dashboard.py --config ~/.codex/dashboard/config.toml
open ~/.codex/dashboard/index.html
```

只验证 JSON：

```bash
python3 dashboard/build_dashboard.py \
  --config ~/.codex/dashboard/config.toml \
  --json-only
```

Dashboard 是只读工具。在 V2 中主要用于 source catalog 检查；如果配置了 V1
兼容路径，它仍可报告 V1 legacy/local-dev suite 可见性。它不会创建、删除或修改
symlink。更多字段说明见 [dashboard/README.md](dashboard/README.md)。

### 4. 可选 V1 兼容：同步 legacy/local-dev Git repo 入口

生产态共享 skills 应来自已安装的 Codex Next 插件。这个 helper 只用于 V1 legacy suite
设置、local-dev 实验，或项目专属 custom agent 暴露。旧 suite 模型见
[V1 Suite Composition](docs/v1/suite-composition.md)。

Codex 不会从子 git repo 自动继承父目录 `.codex`。如果你已经有一个聚合好的工作区入口，例如：

```text
/path/to/workspace/.codex/agents
/path/to/workspace/.codex/skills
```

要让 `/path/to/workspace/*` 下的一批 git repo 都可见这套能力，需要在每个 repo 里创建 repo-local entrypoints。运行时显式选择链接模式；对 workspace 聚合层，建议优先用 `directories`：

```bash
# dry-run
python3 scripts/sync_codex_entrypoints.py sync \
  --workspace /path/to/workspace \
  --source-root /path/to/workspace/.codex \
  --link-mode directories

# apply
python3 scripts/sync_codex_entrypoints.py sync \
  --workspace /path/to/workspace \
  --source-root /path/to/workspace/.codex \
  --link-mode directories \
  --apply
```

推荐的目录模式同步后形态：

```text
<repo>/.codex/agents -> /path/to/workspace/.codex/agents
<repo>/.codex/skills -> /path/to/workspace/.codex/skills
```

只有当某个 repo 必须保留真实 `.codex/agents` 或 `.codex/skills` 目录、只选择少量共享条目，或需要把共享条目和本地实验条目并列时，才选择 `--link-mode entries`：

```text
<repo>/.codex/agents/<agent>.toml -> /path/to/workspace/.codex/agents/<agent>.toml
<repo>/.codex/skills/<skill>      -> /path/to/workspace/.codex/skills/<skill>
```

更新、清理示例：

```bash
# 目录模式会通过目录 symlink 自动跟随源目录更新
python3 scripts/sync_codex_entrypoints.py sync \
  --workspace /path/to/workspace \
  --source-root /path/to/workspace/.codex \
  --link-mode directories \
  --apply

# 逐项模式可以额外清理陈旧 symlink
python3 scripts/sync_codex_entrypoints.py sync \
  --workspace /path/to/workspace \
  --source-root /path/to/workspace/.codex \
  --link-mode entries \
  --prune \
  --apply

# 清理脚本管理的入口
python3 scripts/sync_codex_entrypoints.py clean \
  --workspace /path/to/workspace \
  --source-root /path/to/workspace/.codex \
  --link-mode directories \
  --apply
```

脚本只处理指向当前 `--source-root` 的 symlink，不删除真实文件、真实目录或项目自定义 entrypoints。如果真实目录里有本地内容，目录模式会报告 conflict，而不是直接替换。

`.agents/skills` 应保留给项目专属 skills。不要把共享 plugin 或 V1 suite skills 部署到这里。
生产态共享 skills 应安装插件；V1 legacy/local-dev suite 可见性才通过 `.codex/skills`
的目录级或逐项链接实现。

## 支持的 Agents 和 Skills

公开 catalog 是按任务域分组的。最常用的是：

```text
common
  common_task_planner
  common_orchestrator
  common_context_summarizer
  common_docs_researcher
  common_quality_reviewer
  common_file_organizer

sdlc-manager
  sdlc_project_researcher
  sdlc_requirements_manager
  sdlc_srs_specifier
  sdlc_solution_spec_manager
  sdlc_delivery_planner
  sdlc_readiness_reviewer
  sdlc_change_manager

dev
  dev_code_mapper
  dev_implementer
  dev_code_reviewer
  dev_python_engineer
  dev_backend_engineer
  dev_frontend_engineer
  dev_api_designer
  dev_test_runner
  dev_security_reviewer
  dev_performance_engineer
  dev_cli_engineer
  dev_docs_engineer
  dev_docs_researcher
  dev_architect_reviewer
```

常用 skills：

```text
sdlc-prd-workflow
sdlc-manager
sdlc-project-research
sdlc-srs-workflow
sdlc-nfr-spec
sdlc-hld-workflow
sdlc-lld-workflow
sdlc-domain-boundary-modeling
sdlc-architecture-decision-record
sdlc-solution-spec-workflow
sdlc-spec-slice-writer
sdlc-dev-handoff-planning
sdlc-requirements-traceability
sdlc-readiness-review
sdlc-change-control

dev-repo-onboarding
dev-spec-driven-implementation
dev-bugfix
dev-pr-review
dev-test-strategy
dev-python-quality
dev-api-contract-review
dev-frontend-ui-implementation
dev-security-review
dev-performance-diagnosis
dev-release-check
```

完整清单和推荐关系见 [docs/agent-skill-map.md](docs/agent-skill-map.md)，各 pack 的 README 在：

```text
examples/catalog/common/README_CN.md
examples/catalog/sdlc-manager/README_CN.md
examples/catalog/dev/README_CN.md
examples/catalog/data/README_CN.md
examples/catalog/office/README_CN.md
examples/catalog/research/README_CN.md
```

## 如何仿照创建自己的 Agent

最小 custom agent：

```toml
name = "dev_python_engineer"
description = "Use for Python code, scripts, APIs, CLIs, pytest, typing, packaging, and Python performance work."

sandbox_mode = "workspace-write"

developer_instructions = """
You implement Python software using the project's actual conventions.

Recommended skills: dev-python-quality, dev-test-strategy.

Do:
- Inspect project config and tests first.
- Keep changes scoped and validated.

Return:
1. Scope
2. Changes
3. Checks run
4. Remaining risk
"""
```

放置位置：

```text
<source>/dev/agents/dev_python_engineer.toml
```

runtime 可见位置：

```text
<repo>/.codex/agents/dev_python_engineer.toml
```

注意：custom agent 的 repo-local discovery 路径是 `.codex/agents/*.toml`，
不是 `.agents/agents`。Codex Next 不打包这些 custom agent TOML 文件。

## 如何仿照创建自己的 Skill

最小 skill：

```markdown
---
name: dev-python-quality
description: Use for Python implementation, modernization, typing, packaging, pytest, ruff/mypy checks, and maintainability work.
---

# Python quality workflow

Use this workflow when Python code, packaging, tests, scripts, or modernization are the main task.

## Steps

1. Read project conventions.
2. Define the Python change.
3. Implement idiomatically.
4. Validate with the smallest relevant checks.
5. Report compatibility notes and remaining risk.
```

放置位置：

```text
<source>/dev/skills/dev-python-quality/SKILL.md
```

runtime 可见位置：

```text
<repo>/.codex/skills/dev-python-quality/SKILL.md
```

生产态共享 skills 应使用已安装的 `codex-next` 插件。上面的 repo-local
`.codex/skills` 路径用于 V1 legacy、local-dev 或项目专属暴露。

项目专属 skill 也可以放在：

```text
<repo>/.agents/skills/<project-skill>/SKILL.md
```

## 维护和管理原则

推荐顺序：

```text
1. 先维护 source catalog
2. 保持 plugins/codex-next 这个 packaged skill surface 同步
3. V1 local suites 不进入默认生产路径
4. runtime entrypoints 只用于迁移、custom agents 或项目专属 overlay
5. 用 plugin、dashboard 和 Codex 可见性验证
```

不要：

- 不要 symlink 整个 `.codex` 目录。
- 不要把私有素材提交到公开仓库。
- 不要假设父目录 `.codex` 会被所有子 repo 自动继承。
- 不要只链接 `SKILL.md` 文件；skill 应该按整个 folder 链接。
- 不要用 `config.toml` 当作 agent / skill 的 cwd 路由表。

建议：

- 所有批量脚本先 dry-run。
- `.codex/` 和 `.agents/` 作为本机 entrypoint state 加入 ignore。
- 跨仓库个人 ignore 规则放在 `~/.config/git/ignore`；见
  [Global Git Ignore Profile](docs/global-git-ignore.md)。
- 保持 plugin 打包的公开 skills 和 source catalog 对齐。
- V1 suite symlink 只用于迁移或明确的 local-development 设置。
- 私有生产 catalog 和公开示例 catalog 分离。
- 每次改 suite 后跑 `dashboard/build_dashboard.py --json-only`；每次改 plugin package 后使用
  Codex plugin list 命令验证。

## 公开与私有边界

本仓库是公开安全层，只包含：

- dashboard 源码。
- 脱敏后的 agent / skill 示例。
- Codex Next plugin package 和 marketplace metadata。
- V1 legacy suite / runtime 管理模式。
- 脱敏后的 discovery 边界结论。
- 可复用的 entrypoint 同步脚本。

不应提交：

- 私有 skill 内容。
- 真实 runtime config。
- 真实 dashboard 输出。
- 机器本地 symlink 状态。
- token、账号、内部服务 URL、私有模板。

更多规则见 [docs/public-private-strategy.md](docs/public-private-strategy.md)。
