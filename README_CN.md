# Codex Is All You Need

中文 | [English](README.md)

这是一个面向公开分享的 Codex 预设工具仓库，用于展示 agent / skill catalog、本机 suite 检查逻辑，以及只读双语面板。

本仓库不是任何私有生产环境的完整拷贝，只放可公开的工具、设计文档和经过脱敏的 production-derived 示例目录。私有 skills、真实 runtime 路径、生成的扫描结果和本机 symlink 状态都应留在仓库外。

## 仓库结构

```text
dashboard/
  build_dashboard.py
  templates/index.html
  examples/config.example.toml

scripts/
  sync_codex_entrypoints.py

docs/
  architecture.md
  agent-design.md
  agent-skill-map.md
  skill-design.md
  product-engineering-flow.md
  claude-to-codex-migration.md
  public-private-strategy.md

examples/
  catalog/
    common/
    product-engineering/
    dev/
    data/
    office/
    research/
  runtime/
    AGENTS.md
  suites/
```

## 本仓库包含什么

```text
面板
  只读静态面板生成器，用于查看素材、组合包和运行目录连接状态。

设计文档
  面向公开分享的 Codex agents、skills 和 suite 叠加设计规则。

迁移说明
  如何从 Claude Code 风格的 agents / skills 中学习结构，而不复制私有生产内容。

示例
  从真实生产设计抽取并脱敏后的 agents、skills 和 suite 目录示例。
```

## 预设面板

面板会扫描一个可配置的 Codex preset 环境：

```text
source catalog -> local suites -> runtime .codex/agents and .codex/skills
```

它是只读工具，不会创建、删除或修改 symlink。

典型本地用法：

```bash
python3 dashboard/build_dashboard.py --config ~/.codex/dashboard/config.toml
open ~/.codex/dashboard/index.html
```

可以从 `dashboard/examples/config.example.toml` 开始写本机配置。不要提交真实 runtime config 或生成的 dashboard output。

生成的 HTML 面板支持中文和英文，可通过 `中文 / EN` 切换。

更多安装、配置字段、状态含义和排障说明见 [dashboard/README.md](dashboard/README.md)。

## Repo 入口同步

Codex repo-level discovery 不会从子 git repo 自动继承父目录的 `.codex`。如果希望
`/Users/sky/GitHub/*` 下的一批 repo 共享已经聚合好的 GitHub runtime，可以把每个 repo
自己的 `.codex/agents` 和 `.codex/skills` 入口同步为 symlink：

```bash
python3 scripts/sync_codex_entrypoints.py sync \
  --workspace /Users/sky/GitHub \
  --source-root /Users/sky/GitHub/.codex
```

`sync` 会创建缺失入口，也会更新目标发生变化的 symlink。默认是 dry-run；确认输出后再写入：

```bash
python3 scripts/sync_codex_entrypoints.py sync \
  --workspace /Users/sky/GitHub \
  --source-root /Users/sky/GitHub/.codex \
  --apply
```

如果还要移除仍指向当前 `--source-root`、但已经不在聚合层里的陈旧 symlink，加 `--prune`。

后续如果要清理脚本管理的入口，用 `clean`。它只删除指向当前 `--source-root` 的 symlink：

```bash
python3 scripts/sync_codex_entrypoints.py clean \
  --workspace /Users/sky/GitHub \
  --source-root /Users/sky/GitHub/.codex
```

脚本只创建 repo-local `.codex` 下的入口，不会 symlink 整个 `.codex` 目录，也不会写入 `.agents`。
`.agents/skills` 可以留给项目专属 skill；custom agent 的有效 repo-local 路径仍是
`.codex/agents/*.toml`。

## 设计文档

- [架构说明](docs/architecture.md)
- [Agent 设计](docs/agent-design.md)
- [Agent 与 Skill 分工](docs/agent-skill-map.md)
- [Skill 设计](docs/skill-design.md)
- [Product Engineering Flow](docs/product-engineering-flow.md)
- [Claude 到 Codex 迁移](docs/claude-to-codex-migration.md)
- [公开与私有分层](docs/public-private-strategy.md)

## 示例

`examples/` 下的文件是从真实生产 preset 设计抽取后的可公开模板，不应在未经审查的情况下直接安装到真实机器。

```text
examples/catalog/
  common/                 6 agents, 0 public skills
  product-engineering/    6 agents, 6 public skills
  dev/                   14 agents, 19 public skills
  data/                   5 agents, 4 public skills
  office/                 5 agents, 5 public skills
  research/               4 agents, 3 public skills

examples/runtime/
  AGENTS.md

examples/suites/
  README.md
```

公开示例目录刻意排除了私有 symlink skills 和任何本机生成的 dashboard 状态。
