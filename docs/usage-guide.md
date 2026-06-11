# Usage Guide / 使用指南

This guide explains how to use this repository as a pattern for your own Codex
agent / skill preset system.

本文说明如何把本仓库当作模板，搭建你自己的 Codex agent / skill 预设系统。

## 1. Mental Model / 心智模型

The system has three layers.

这套系统分三层。

```text
source catalog
  EN: The source of truth for agent TOML files and skill folders.
  CN: agent TOML 和 skill folder 的事实源。

local suites
  EN: Machine-local symlink compositions that select which source entries are
      exposed together.
  CN: 本机 symlink 组合层，用来选择哪些 source entries 被一起暴露。

runtime entrypoints
  EN: The actual `.codex/agents` and `.codex/skills` entries visible from the
      directory where Codex runs.
  CN: Codex 启动目录实际可见的 `.codex/agents` 和 `.codex/skills`。
```

The core rule is that source entries are reusable, suites are composed views,
and runtime directories only expose entrypoints.

核心规则是：source entries 可复用，suites 是组合视图，runtime directories 只暴露入口。

## 2. What Codex Actually Discovers / Codex 实际发现什么

Repo-level discovery is bounded by the current project root. In practice:

repo-level discovery 受当前 project root 限制。实际规则是：

```text
With a git root:
  Scan only the path chain from git root to current working directory.

有 git root：
  只扫描 git root 到当前工作目录的路径链。

Without a git root:
  Scan only the current working directory.

无 git root：
  只扫描当前工作目录。
```

Important consequences:

重要结论：

- A parent workspace `.codex` is not automatically inherited by child git repos.
- Codex does not recursively scan the whole repository for skills or agents.
- Sibling subtrees are not scanned.
- Nested git repos block outer repo-level discovery.
- Repo-local custom agents belong in `.codex/agents/*.toml`.
- Repo-local skills can be exposed from `.codex/skills/<skill>` or `.agents/skills/<skill>`.

This repository includes a sanitized public summary at
[discovery-boundaries.md](discovery-boundaries.md). Keep machine-specific
matrix logs under ignored `local/` files.

本仓库在 [discovery-boundaries.md](discovery-boundaries.md) 保存脱敏后的公开结论。
包含本机路径和 run ID 的矩阵实验记录应放在被忽略的 `local/` 文件里。

## 3. Quick Start / 快速开始

### Inspect the example catalog / 查看示例目录

```bash
find examples/catalog -maxdepth 3 \
  \( -path '*/agents/*.toml' -o -path '*/skills/*/SKILL.md' \)
```

The catalog is public-safe and sanitized. It mirrors a production-derived shape
without exposing private workflows.

这个 catalog 是公开安全、经过脱敏的示例。它保留生产结构，但不暴露私有工作流。

### Generate the dashboard / 生成面板

```bash
mkdir -p ~/.codex/dashboard
cp dashboard/examples/config.example.toml ~/.codex/dashboard/config.toml

python3 dashboard/build_dashboard.py --config ~/.codex/dashboard/config.toml
open ~/.codex/dashboard/index.html
```

For CI-like checks or terminal-only validation:

用于 CI 风格检查或纯终端验证：

```bash
python3 dashboard/build_dashboard.py \
  --config ~/.codex/dashboard/config.toml \
  --json-only
```

The dashboard is read-only. It reports source entries, suites, runtime
connections, broken symlinks, and status issues.

面板是只读的。它会报告 source entries、suites、runtime 连接、断链和状态问题。

### Sync repo-local entrypoints / 同步 repo-local 入口

If your workspace aggregate is:

如果你的工作区聚合层是：

```text
/path/to/workspace/.codex/agents
/path/to/workspace/.codex/skills
```

then batch-sync entrypoints into child repos. Choose the link mode explicitly;
`directories` is recommended for workspace aggregates.

可以批量同步入口到子 repo。运行时显式选择链接模式；对 workspace 聚合层，建议优先用 `directories`。

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

Recommended directory mode creates:

推荐的目录模式会创建：

```text
<repo>/.codex/agents -> <source-root>/agents
<repo>/.codex/skills -> <source-root>/skills
```

Use `--link-mode entries` when a repo must keep real `.codex/agents` or
`.codex/skills` directories, selectively opt in to a small set of shared
entries, or mix shared entries with local experiments:

当某个 repo 必须保留真实 `.codex/agents` 或 `.codex/skills` 目录时，使用
`--link-mode entries`；它也适合只选择少量共享条目，或把共享条目和本地实验条目
并列的 repo：

```text
<repo>/.codex/agents/<agent>.toml -> <source-root>/agents/<agent>.toml
<repo>/.codex/skills/<skill>      -> <source-root>/skills/<skill>
```

It also writes `.codex/` and `.agents/` into each target repo's
`.git/info/exclude`, so machine-local entrypoint state stays untracked.

它也会把 `.codex/` 和 `.agents/` 写入每个目标 repo 的 `.git/info/exclude`，避免本机入口状态污染 Git。

For cross-repository personal defaults, keep user-level rules in
`~/.config/git/ignore`; see [Global Git Ignore Profile](global-git-ignore.md).

跨仓库个人默认规则应放在 `~/.config/git/ignore`；见
[Global Git Ignore Profile](global-git-ignore.md)。

Do not deploy shared suites into `.agents/skills`; keep `.agents/skills` for
project-only skills.

不要把共享 suite 部署到 `.agents/skills`；`.agents/skills` 应留给项目专属 skills。

## 4. Sync, Update, Prune, Clean / 创建、更新、裁剪、清理

The script supports two actions: `sync` and `clean`, and two link modes:
`directories` and `entries`.

脚本支持两个动作：`sync` 和 `clean`，以及两种链接模式：`directories` 和
`entries`。

```bash
# Create missing entrypoints and update changed symlink targets.
# 创建缺失入口，并更新目标变化的 symlink。
python3 scripts/sync_codex_entrypoints.py sync \
  --workspace /path/to/workspace \
  --source-root /path/to/workspace/.codex \
  --link-mode directories \
  --apply

# Also remove stale symlinks that still point into the selected source root.
# 同时删除仍指向当前 source root、但已经不在聚合层中的陈旧 symlink。
python3 scripts/sync_codex_entrypoints.py sync \
  --workspace /path/to/workspace \
  --source-root /path/to/workspace/.codex \
  --link-mode entries \
  --prune \
  --apply

# Remove managed entrypoints.
# 清理脚本管理的入口。
python3 scripts/sync_codex_entrypoints.py clean \
  --workspace /path/to/workspace \
  --source-root /path/to/workspace/.codex \
  --link-mode directories \
  --apply
```

For a narrower run:

缩小范围：

```bash
python3 scripts/sync_codex_entrypoints.py sync --link-mode directories --repo XDB
python3 scripts/sync_codex_entrypoints.py sync --link-mode directories --include 'CPA-*'
python3 scripts/sync_codex_entrypoints.py sync --link-mode directories --exclude 'Archive-*'
```

Safety rules:

安全规则：

- Default mode is dry-run.
- `--link-mode` is explicit so the caller chooses directory links or individual entry links.
- Non-symlink conflicts are reported, not overwritten.
- Directory mode may replace old managed entry directories when every child is a symlink into the selected source directory.
- Real directories with local content are reported as conflicts, not overwritten.
- `clean` removes only symlinks that point into the selected `--source-root`.
- `clean` does not delete real files, real directories, or project-specific entrypoints.

## 5. Supported Packs / 支持的能力包

| Pack | Agents | Skills | Best For |
|---|---:|---:|---|
| `common` | 6 | 2 | Planning, orchestration, context summaries, docs verification, quality review |
| `sdlc-manager` | 7 | 20 | Architecture-first SDLC control: requirements, SRS/NFR, HLD/LLD, ADR, domain boundaries, SPEC, handoff |
| `dev` | 14 | 20 | SDLC-aware and direct-dev implementation, testing, API, CLI, frontend, Python, security, performance |
| `data` | 5 | 4 | Data profiling, SQL, cleaning, pipelines, reports |
| `office` | 5 | 5 | Meeting minutes, weekly reports, project reports, briefing notes, slide outlines |
| `research` | 4 | 3 | Source deduplication, evidence mapping, synthesis, gap review |

Detailed role and skill relationships are documented in
[agent-skill-map.md](agent-skill-map.md).

详细 agent / skill 分工见 [agent-skill-map.md](agent-skill-map.md)。

## 6. Agent Pattern / Agent 仿照模板

Agents are TOML files. They define a role, activation description, sandbox
preference, and role-specific instructions.

Agent 是 TOML 文件，用来定义角色、触发描述、sandbox 偏好和角色说明。

```toml
name = "dev_python_engineer"
description = "Use for Python code, scripts, APIs, CLIs, pytest, typing, packaging, and Python performance work."

sandbox_mode = "workspace-write"

nickname_candidates = ["Python"]

developer_instructions = """
You implement Python software using the project's actual conventions.

Recommended skills: python-quality, test-strategy.

Do:
- Inspect project config, tests, and style tools first.
- Keep changes scoped.
- Run targeted checks when available.

Do not:
- Add heavy dependencies without evidence.
- Rewrite style to a different framework without approval.

Return:
1. Scope
2. Changes
3. Checks run
4. Remaining risk
"""
```

Recommended source location:

推荐 source 位置：

```text
<source-catalog>/dev/agents/dev_python_engineer.toml
```

Runtime-visible location:

runtime 可见位置：

```text
<repo>/.codex/agents/dev_python_engineer.toml
```

## 7. Skill Pattern / Skill 仿照模板

Skills are folders. `SKILL.md` is the entrypoint, and extra files such as
`scripts/`, `references/`, `examples/`, and `assets/` should stay inside the same
folder.

Skill 是目录。`SKILL.md` 是入口，`scripts/`、`references/`、`examples/`、
`assets/` 等附属文件应留在同一个目录内。

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

Recommended source location:

推荐 source 位置：

```text
<source-catalog>/dev/skills/python-quality/SKILL.md
```

Runtime-visible location:

runtime 可见位置：

```text
<repo>/.codex/skills/python-quality/SKILL.md
```

Project-only overlay:

项目专属叠加：

```text
<repo>/.agents/skills/project-only-skill/SKILL.md
```

## 8. Building A Suite / 组合一个 Suite

A suite is a directory with symlink entries:

suite 是一个包含 symlink entries 的目录：

```bash
mkdir -p ~/.codex/suites/demo-dev/agents
mkdir -p ~/.codex/suites/demo-dev/skills

ln -sfn "$PWD/examples/catalog/common/agents/common_task_planner.toml" \
  ~/.codex/suites/demo-dev/agents/common_task_planner.toml

ln -sfn "$PWD/examples/catalog/dev/agents/dev_python_engineer.toml" \
  ~/.codex/suites/demo-dev/agents/dev_python_engineer.toml

ln -sfn "$PWD/examples/catalog/dev/skills/python-quality" \
  ~/.codex/suites/demo-dev/skills/python-quality
```

An `all` suite can be built with the same pattern by linking every source group
into one suite. Use it only for explicit full-capability runtimes; smaller
domain suites are easier to reason about.

`all` suite 可以用同样模式把所有 source group 链接进同一个 suite。它只适合明确
需要全能力的 runtime；更小的任务域 suite 更容易维护和审查。

Expose the suite to a runtime:

暴露到 runtime：

```bash
mkdir -p /tmp/codex-demo/.codex
ln -sfn ~/.codex/suites/demo-dev/agents /tmp/codex-demo/.codex/agents
ln -sfn ~/.codex/suites/demo-dev/skills /tmp/codex-demo/.codex/skills
```

Do not symlink the whole `.codex` directory. A runtime may need its own
`.codex/config.toml`, hooks, or local files.

不要 symlink 整个 `.codex` 目录。runtime 可能需要自己的 `.codex/config.toml`、
hooks 或本地文件。

## 9. Maintenance Checklist / 维护检查清单

Before changing presets:

改预设前：

```text
1. Confirm the source catalog is the source of truth.
2. Confirm agent TOML files parse.
3. Confirm each skill folder has SKILL.md.
4. Confirm suite symlinks point to the intended source entries.
5. Confirm runtime entrypoints are repo-local or user-global as intended.
6. Run the dashboard in json-only mode.
7. Use Codex prompt-input or a real Codex run for visibility validation when needed.
```

Helpful commands:

常用命令：

```bash
python3 dashboard/build_dashboard.py --config ~/.codex/dashboard/config.toml --json-only
find -L ~/.codex/suites -type l -print
git diff --check
python3 scripts/sync_codex_entrypoints.py sync --workspace /path/to/workspace --source-root /path/to/workspace/.codex --link-mode directories
```

## 10. Common Mistakes / 常见错误

```text
Mistake:
  Put one .codex under a parent workspace and expect child git repos to inherit it.
Fix:
  Sync repo-local .codex entrypoints into each child repo.

错误：
  在父级工作区放一个 .codex，然后期待所有子 git repo 自动继承。
修正：
  给每个子 repo 同步 repo-local .codex entrypoints。
```

```text
Mistake:
  Put custom agents under .agents.
Fix:
  Put repo-local custom agents under .codex/agents/*.toml.

错误：
  把 custom agents 放到 .agents。
修正：
  repo-local custom agents 应放到 .codex/agents/*.toml。
```

```text
Mistake:
  Link only SKILL.md.
Fix:
  Link the whole skill folder so scripts, references, examples, and assets work.

错误：
  只链接 SKILL.md。
修正：
  链接整个 skill folder，保证 scripts、references、examples、assets 可用。
```

```text
Mistake:
  Commit generated dashboard output or machine-local symlink state.
Fix:
  Keep output under ~/.codex/dashboard and ignore .codex/.agents runtime state.

错误：
  提交生成的 dashboard output 或本机 symlink 状态。
修正：
  输出放到 ~/.codex/dashboard，并忽略 .codex/.agents runtime state。
```

## 11. Public / Private Boundary / 公开与私有边界

This public repository may include:

本公开仓库可以包含：

- Sanitized examples.
- Architecture and design docs.
- Dashboard source code.
- Public-safe maintenance scripts.
- Discovery experiment notes after private data is removed.

It must not include:

不应包含：

- Private skill content.
- Real runtime config.
- Generated machine-local dashboard output.
- Credentials, tokens, account names, or internal URLs.
- Private business templates.

See [public-private-strategy.md](public-private-strategy.md).

详见 [public-private-strategy.md](public-private-strategy.md)。
