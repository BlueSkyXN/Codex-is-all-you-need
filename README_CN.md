# Codex Is All You Need

中文 | [English](README.md)

`Codex Is All You Need` 是一套 Codex agent / skill 预设体系的公开安全版本。它不是一个“把某台机器完整复制出去”的私有配置仓库，而是把一套真实生产环境里的经验抽象成可学习、可仿照、可检查的目录结构、示例素材、管理脚本和只读面板。

一句话：

```text
source catalog -> local suites -> runtime .codex entrypoints
```

你可以用它做三件事：

1. 学习如何把 Codex agents、skills、suites、runtime entrypoints 分层管理。
2. 复制公开示例，搭建自己的本地 agent / skill catalog。
3. 用 dashboard 和同步脚本检查、部署、维护本机 Codex 预设。

## 适合谁

- 想把常用工作流沉淀成 Codex skills 的开发者。
- 想为不同任务域准备不同 custom agents 的团队或个人。
- 想把 Claude Code 风格的 agent / skill 经验迁移到 Codex 的用户。
- 想用 symlink 管理“一个素材、多套组合、多处 runtime 暴露”的本机环境。
- 想公开分享 agent / skill 结构，但又不想泄露私有 prompt、路径、模板或真实配置的人。

## 这不是

- 不是 OpenAI 官方 preset 目录规范。
- 不是一键安装完整生产环境的脚本。
- 不是私有 `~/.codex` 或真实业务 skills 的镜像。
- 不是让父目录 `.codex` 自动继承到所有子 git repo 的机制。Codex repo-level discovery 有 project root 边界，详见 [架构说明](docs/architecture.md)。

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
  architecture.md                 # source / suite / runtime 架构
  agent-design.md                 # custom agent 设计
  skill-design.md                 # skill 设计
  agent-skill-map.md              # agent 与 skill 分工
  product-engineering-flow.md
  claude-to-codex-migration.md
  public-private-strategy.md

examples/
  catalog/                        # 脱敏后的公开 agent / skill source catalog
  runtime/                        # runtime AGENTS.md 示例
  suites/                         # suite symlink 模式说明

local/
  codex-skill-discovery-matrix.md # 本机 discovery 实验记录
```

## 核心概念

```text
source catalog
  存放真实 agent TOML 和 skill folder。
  示例：examples/catalog/dev/agents/dev_python_engineer.toml
       examples/catalog/dev/skills/python-quality/SKILL.md

local suites
  本机组合层。每个 suite 通过 symlink 选择要暴露哪些 agents / skills。
  示例：~/.codex/suites/github/agents/*.toml
       ~/.codex/suites/github/skills/*

runtime entrypoints
  Codex 启动目录实际能发现的 .codex/agents 和 .codex/skills。
  示例：<repo>/.codex/agents/<agent>.toml
       <repo>/.codex/skills/<skill>
```

更详细解释见 [docs/usage-guide.md](docs/usage-guide.md) 和 [docs/architecture.md](docs/architecture.md)。

## 3 分钟快速用法

### 1. 查看公开 catalog

```bash
find examples/catalog -maxdepth 3 \( -path '*/agents/*.toml' -o -path '*/skills/*/SKILL.md' \)
```

公开示例包含：

| Pack | Agents | Skills | 用途 |
|---|---:|---:|---|
| `common` | 6 | 0 | 规划、编排、文档核查、质量复核、上下文压缩、文件整理 |
| `product-engineering` | 6 | 6 | PRD、功能规格、技术桥接、任务拆解、准备度审查 |
| `dev` | 14 | 19 | 代码阅读、实现、测试、review、API、CLI、前端、Python、安全、性能 |
| `data` | 5 | 4 | 数据画像、SQL、清洗、pipeline、分析报告 |
| `office` | 5 | 5 | 会议纪要、周报、项目报告、briefing、PPT 大纲 |
| `research` | 4 | 3 | 材料整理、证据表、去重、综合分析、gap review |

完整分工见 [docs/agent-skill-map.md](docs/agent-skill-map.md)。

### 2. 生成只读 dashboard

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

Dashboard 是只读工具，不会创建、删除或修改 symlink。更多字段说明见 [dashboard/README.md](dashboard/README.md)。

### 3. 批量同步 Git repo 入口

Codex 不会从子 git repo 自动继承父目录 `.codex`。如果你已经有一个聚合好的工作区入口，例如：

```text
/Users/sky/GitHub/.codex/agents
/Users/sky/GitHub/.codex/skills
```

要让 `/Users/sky/GitHub/*` 下的一批 git repo 都可见这套能力，需要在每个 repo 里创建 repo-local entrypoints：

```bash
# dry-run
python3 scripts/sync_codex_entrypoints.py sync \
  --workspace /Users/sky/GitHub \
  --source-root /Users/sky/GitHub/.codex

# apply
python3 scripts/sync_codex_entrypoints.py sync \
  --workspace /Users/sky/GitHub \
  --source-root /Users/sky/GitHub/.codex \
  --apply
```

同步后形态：

```text
<repo>/.codex/agents/<agent>.toml -> /Users/sky/GitHub/.codex/agents/<agent>.toml
<repo>/.codex/skills/<skill>      -> /Users/sky/GitHub/.codex/skills/<skill>
```

更新、清理：

```bash
# 更新并清理陈旧 symlink
python3 scripts/sync_codex_entrypoints.py sync \
  --workspace /Users/sky/GitHub \
  --source-root /Users/sky/GitHub/.codex \
  --prune \
  --apply

# 清理脚本管理的入口
python3 scripts/sync_codex_entrypoints.py clean \
  --workspace /Users/sky/GitHub \
  --source-root /Users/sky/GitHub/.codex \
  --apply
```

脚本只处理指向当前 `--source-root` 的 symlink，不删除真实文件、真实目录或项目自定义 entrypoints。

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
prd-workflow
functional-spec
technical-spec-bridge
delivery-task-planning
readiness-review
change-spec-adapter

repo-onboarding
bugfix
pr-review
test-strategy
python-quality
api-contract-review
frontend-ui-implementation
security-review
performance-diagnosis
release-check
```

完整清单和推荐关系见 [docs/agent-skill-map.md](docs/agent-skill-map.md)，各 pack 的 README 在：

```text
examples/catalog/common/README_CN.md
examples/catalog/product-engineering/README_CN.md
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

Recommended skills: python-quality, test-strategy.

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

注意：custom agent 的 repo-local discovery 路径是 `.codex/agents/*.toml`，不是 `.agents/agents`。

## 如何仿照创建自己的 Skill

最小 skill：

```markdown
---
name: python-quality
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
<source>/dev/skills/python-quality/SKILL.md
```

runtime 可见位置：

```text
<repo>/.codex/skills/python-quality/SKILL.md
```

项目专属 skill 也可以放在：

```text
<repo>/.agents/skills/<project-skill>/SKILL.md
```

## 维护和管理原则

推荐顺序：

```text
1. 先维护 source catalog
2. 再维护 local suites
3. 最后暴露 runtime entrypoints
4. 用 dashboard 和 Codex 可见性验证
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
- suite 里使用 symlink，source catalog 里保存真实文件。
- 私有生产 catalog 和公开示例 catalog 分离。
- 每次改 suite 后跑 `dashboard/build_dashboard.py --json-only`。

## 公开与私有边界

本仓库是公开安全层，只包含：

- dashboard 源码。
- 脱敏后的 agent / skill 示例。
- suite / runtime 管理模式。
- 发现边界实验记录。
- 可复用的 entrypoint 同步脚本。

不应提交：

- 私有 skill 内容。
- 真实 runtime config。
- 真实 dashboard 输出。
- 机器本地 symlink 状态。
- token、账号、内部服务 URL、私有模板。

更多规则见 [docs/public-private-strategy.md](docs/public-private-strategy.md)。
