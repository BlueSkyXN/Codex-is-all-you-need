# Codex Is All You Need

Public-safe tooling for Codex preset catalogs, local suite inspection, and a read-only bilingual dashboard.

这是一个面向公开分享的 Codex 预设工具仓库，用于展示 agent / skill catalog、local suite 检查逻辑，以及只读双语面板。

This repository is intentionally not a complete copy of any private production setup. It contains public-safe tooling, design docs, and a sanitized production-derived example catalog. Private skills, runtime paths, generated scan results, and machine-specific symlink state should stay outside this repository.

本仓库不是任何私有生产环境的完整拷贝，只放可公开的工具、设计文档和经过脱敏的 production-derived 示例目录。私有 skills、真实 runtime 路径、生成的扫描结果和本机 symlink 状态都应留在仓库外。

## Repository Layout / 仓库结构

```text
dashboard/
  build_dashboard.py
  templates/index.html
  examples/config.example.toml

docs/
  architecture.md
  agent-design.md
  agent-skill-map.md
  skill-design.md
  claude-to-codex-migration.md
  public-private-strategy.md

examples/
  catalog/
    common/
    dev/
    data/
    office/
    research/
  runtime/
    AGENTS.md
  suites/
```

## What This Repo Contains / 本仓库包含什么

```text
Dashboard / 面板
  EN: A read-only static dashboard generator for catalog, suite, and runtime
      connection inspection.
  CN: 只读静态面板生成器，用于查看素材、组合包和运行目录连接状态。

Design guides / 设计文档
  EN: Public-safe rules for designing Codex agents, skills, and suite overlays.
  CN: 面向公开分享的 Codex agents、skills 和 suite 叠加设计规则。

Migration notes / 迁移说明
  EN: How to learn from Claude Code style agents and skills without copying
      private operational content.
  CN: 如何从 Claude Code 风格的 agents / skills 中学习结构，而不复制私有生产内容。

Examples / 示例
  EN: Sanitized production-derived agents, skills, and suite layout examples.
  CN: 从真实生产设计抽取并脱敏后的 agents、skills 和 suite 目录示例。
```

## Dashboard / 预设面板

The dashboard scans a configurable Codex preset environment:

面板会扫描一个可配置的 Codex preset 环境：

```text
source catalog -> local suites -> runtime .codex/agents and .codex/skills
```

It is read-only. It does not create, delete, or modify symlinks.

它是只读工具，不会创建、删除或修改 symlink。

Typical local usage:

典型本地用法：

```bash
python3 dashboard/build_dashboard.py --config ~/.codex/dashboard/config.toml
open ~/.codex/dashboard/index.html
```

Use `dashboard/examples/config.example.toml` as the starting point for a local config. Do not commit real runtime configs or generated dashboard output.

可以从 `dashboard/examples/config.example.toml` 开始写本机配置。不要提交真实 runtime config 或生成的 dashboard output。

The generated HTML supports Chinese and English through a `中文 / EN` switch.

生成的 HTML 面板支持中文和英文，可通过 `中文 / EN` 切换。

See [dashboard/README.md](dashboard/README.md) for setup, config fields, status meanings, and troubleshooting.

更多安装、配置字段、状态含义和排障说明见 [dashboard/README.md](dashboard/README.md)。

## Design Guides / 设计文档

- [Architecture / 架构说明](docs/architecture.md)
- [Agent Design / Agent 设计](docs/agent-design.md)
- [Agent Skill Map / Agent 与 Skill 分工](docs/agent-skill-map.md)
- [Skill Design / Skill 设计](docs/skill-design.md)
- [Claude To Codex Migration / Claude 到 Codex 迁移](docs/claude-to-codex-migration.md)
- [Public And Private Strategy / 公开与私有分层](docs/public-private-strategy.md)

## Examples / 示例

The files under `examples/` are public-safe templates derived from a real production preset design. They are not intended to be installed as-is into a real machine without review.

`examples/` 下的文件是从真实生产 preset 设计抽取后的可公开模板，不应在未经审查的情况下直接安装到真实机器。

```text
examples/catalog/
  common/       5 agents, 0 public skills
  dev/         12 agents, 17 public skills
  data/         4 agents, 4 public skills
  office/       4 agents, 5 public skills
  research/     4 agents, 3 public skills

examples/runtime/
  AGENTS.md

examples/suites/
  README.md
```

The public catalog intentionally excludes private symlinked skills and any generated local dashboard state.

公开示例目录刻意排除了私有 symlink skills 和任何本机生成的 dashboard 状态。
