# Codex Preset Dashboard / Codex 预设面板

Read-only dashboard for Codex agent and skill preset systems.

这是一个只读面板，用来查看 Codex agent / skill 预设系统的素材、组合包和运行目录连接状态。

It is meant for humans first: open one HTML file and quickly see which preset packages exist, what each package exposes, and whether runtime folders are connected correctly.

它主要是给人看的：打开一个 HTML 文件，就能快速看到有哪些 preset packages、每个 package 暴露了哪些 agents / skills，以及 runtime folders 是否正确连接。

## Quick Start / 快速开始

From the repository root:

在仓库根目录执行：

```bash
python3 dashboard/build_dashboard.py --config ~/.codex/dashboard/config.toml
open ~/.codex/dashboard/index.html
```

Or from this directory:

也可以在 `dashboard/` 目录执行：

```bash
python3 build_dashboard.py --config ~/.codex/dashboard/config.toml
open ~/.codex/dashboard/index.html
```

The command generates a local JSON state file and a static HTML dashboard.

这个命令会生成本地 JSON 状态文件和一个静态 HTML 面板。

## First-Time Setup / 首次配置

Create a local config outside the repository:

在仓库外创建本机配置：

```bash
mkdir -p ~/.codex/dashboard
cp dashboard/examples/config.example.toml ~/.codex/dashboard/config.toml
```

Then edit:

然后编辑：

```text
~/.codex/dashboard/config.toml
```

The config file is local machine state. Do not commit it.

这个配置属于本机状态，不要提交到公开仓库。

## UI Language / 界面语言

The generated dashboard supports Chinese and English. Use the `中文 / EN` switch in the top-right corner.

生成后的面板支持中文和英文，可以通过右上角的 `中文 / EN` 切换。

The selected language is stored in browser `localStorage` when available. If storage is unavailable under `file://`, the switch still works for the current page session.

语言偏好会在可用时保存到浏览器 `localStorage`。如果某些 `file://` 预览环境禁用了 storage，当前页面内切换仍然可用。

## Config Fields / 配置字段

Minimal config:

最小配置示例：

```toml
[source]
name = "local production"
codex_root = "/path/to/your/codex/source"
suites_root = "/Users/example/.codex/suites"

[output]
dir = "/Users/example/.codex/dashboard"
state_file = "preset-state.json"
html_file = "index.html"

[[runtimes]]
name = "github-dev"
path = "/Users/example/GitHub"
expected_suite = "github"
```

Important fields:

关键字段：

```text
source.codex_root
  EN: Production source catalog. It should contain groups such as common, dev,
      data, office, and research.
  CN: 生产素材目录。通常包含 common、dev、data、office、research 等分组。

source.suites_root
  EN: Local suite aggregation directory. Each suite contains agents/ and skills/.
  CN: 本机 suite 聚合目录。每个 suite 里包含 agents/ 和 skills/。

source.private_roots
  EN: Optional roots that should be marked private when a skill resolves under them.
  CN: 可选。skill 最终路径落在这些目录下时，会标记为 private。

source.public_roots
  EN: Optional roots that should be marked public.
  CN: 可选。路径落在这些目录下时，会标记为 public。

output.dir
  EN: Output directory for preset-state.json and index.html.
  CN: preset-state.json 和 index.html 的输出目录。

runtimes
  EN: Runtime folders to inspect. Each runtime is expected to expose:
      <runtime>/.codex/agents -> <suites_root>/<expected_suite>/agents
      <runtime>/.codex/skills -> <suites_root>/<expected_suite>/skills
  CN: 需要检查的运行目录。每个 runtime 预期暴露：
      <runtime>/.codex/agents -> <suites_root>/<expected_suite>/agents
      <runtime>/.codex/skills -> <suites_root>/<expected_suite>/skills
```

Use this example as a starting point:

可以从这个示例开始：

```text
dashboard/examples/config.example.toml
```

## What It Scans / 扫描内容

```text
source catalog / 素材目录:
  <codex_root>/<group>/agents/*.toml
  <codex_root>/<group>/skills/<skill-name>/SKILL.md

local suites / 本机组合包:
  <suites_root>/<suite>/agents/*
  <suites_root>/<suite>/skills/*

runtime folders / 运行目录:
  <runtime>/.codex/agents
  <runtime>/.codex/skills
```

The scanner follows symlink targets and reports broken links.

扫描器会解析 symlink 的最终目标，并报告断链。

## Dashboard Sections / 面板区域

```text
Overview metrics / 总览指标
  Group count, agent count, skill count, suite count, runtime count, issue count.
  分组数、agent 数、skill 数、suite 数、runtime 数、issue 数。

Suites / 组合包
  Each suite package and the agents/skills it exposes.
  每个 suite package 暴露的 agents / skills。

Agents / 角色
  Agent name, source group, reasoning effort, nickname, suite usage, and skill hints.
  Agent 名称、来源分组、推理强度、别名、suite 使用情况和 skill 提示。

Skills / 技能
  Skill name, source group, scope, final resolved path, and suite usage.
  Skill 名称、来源分组、范围、最终解析路径和 suite 使用情况。

Runtime / 运行目录
  Whether each runtime is connected, missing, partially connected, occupied, or wrong-target.
  每个 runtime 是已连接、缺失、部分连接、已占用，还是指向错误目标。

Issues / 问题
  Warnings and errors found during the scan.
  扫描过程中发现的 warning 和 error。
```

## Status Meaning / 状态含义

```text
connected / 已连接
  .codex/agents and .codex/skills both point to the expected suite.
  .codex/agents 和 .codex/skills 都指向预期 suite。

missing / 缺失
  Runtime does not currently expose agents/skills at the checked location.
  runtime 在检查位置没有暴露 agents / skills。

partial / 部分连接
  Only one of agents/skills points to the expected suite.
  agents / skills 只有一项指向预期 suite。

occupied / 已占用
  agents or skills exists as a real directory/file instead of the expected symlink.
  agents 或 skills 是真实目录/文件，而不是预期 symlink。

wrong-target / 目标错误
  agents or skills is a symlink, but not to the expected suite.
  agents 或 skills 是 symlink，但没有指向预期 suite。
```

## JSON-Only Mode / 仅生成 JSON

Use this when another tool or script only needs the machine-readable state:

当其他工具或脚本只需要机器可读状态时使用：

```bash
python3 dashboard/build_dashboard.py \
  --config ~/.codex/dashboard/config.toml \
  --json-only
```

## Output / 输出

By default, output should be written outside the repository:

默认输出应写到仓库外：

```text
~/.codex/dashboard/preset-state.json
~/.codex/dashboard/index.html
```

These generated files may contain private paths and should not be committed.

这些生成文件可能包含私有路径，不应提交。

## Safety Guarantees / 安全边界

The dashboard is read-only.

该面板是只读工具。

It does not:

它不会：

```text
create symlinks / 创建 symlink
delete symlinks / 删除 symlink
modify .codex / 修改 .codex
modify .agents / 修改 .agents
edit agent TOML / 修改 agent TOML
edit SKILL.md / 修改 SKILL.md
write generated state into the repository unless the config explicitly asks for it
除非配置显式要求，否则不会把生成状态写进仓库
```

## Current Limitations / 当前限制

The current version focuses on source catalogs, local suites, and runtime `.codex/agents` plus `.codex/skills` connections.

当前版本主要覆盖 source catalog、本机 suites，以及 runtime 的 `.codex/agents` 和 `.codex/skills` 连接状态。

Project-level `.agents/skills` overlays are a planned next step. Until that is implemented, the dashboard should not be treated as a complete view of every skill Codex can discover inside an individual project folder.

项目级 `.agents/skills` 叠加层是后续计划。在实现之前，不应把 dashboard 视为单个项目目录内所有 Codex 可发现 skill 的完整视图。

## Related Docs / 相关文档

- [Architecture / 架构说明](../docs/architecture.md)
- [Agent Design / Agent 设计](../docs/agent-design.md)
- [Agent Skill Map / Agent 与 Skill 分工](../docs/agent-skill-map.md)
- [Skill Design / Skill 设计](../docs/skill-design.md)
- [Public And Private Strategy / 公开与私有分层](../docs/public-private-strategy.md)

项目级 `.agents/skills` 叠加层是后续计划。在实现之前，不应把该面板视为某个具体项目里 Codex 可发现 skill 的完整视图。

## Troubleshooting / 排障

If the dashboard is empty:

如果面板为空：

```bash
python3 dashboard/build_dashboard.py --config ~/.codex/dashboard/config.toml
```

Check that `source.codex_root` and `source.suites_root` exist.

检查 `source.codex_root` 和 `source.suites_root` 是否存在。

If a skill is marked private:

如果某个 skill 被标记为 private：

```text
Its final resolved path is under one of source.private_roots.
它的最终解析路径落在 source.private_roots 的某个目录下。
```

If a runtime is `occupied`:

如果某个 runtime 是 `occupied`：

```text
Inspect <runtime>/.codex/agents and <runtime>/.codex/skills before changing anything.
修改前先检查 <runtime>/.codex/agents 和 <runtime>/.codex/skills。
```
