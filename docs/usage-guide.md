# Usage Guide / 使用指南

This guide explains the current V2 plugin-first model for using this repository
as a pattern for your own Codex agent / skill preset system.

本文说明本仓库当前 V2 plugin-first 模型，以及如何把它当作模板搭建自己的
Codex agent / skill 预设系统。

## 1. Mental Model / 心智模型

The current repository state is V2. The production path is plugin-first.

本仓库当前状态是 V2。生产路径是 plugin-first。

```text
source catalog
  EN: The source of truth for public-safe skill folders and agent examples.
  CN: 公开安全 skill folder 和 agent 示例的事实源。

plugin package
  EN: `plugins/codex-next`, the packaged shared-skill surface.
  CN: `plugins/codex-next`，打包后的共享 skill surface。

marketplace install
  EN: `.agents/plugins/marketplace.json` exposes the checked-in plugin.
  CN: `.agents/plugins/marketplace.json` 暴露仓库内插件。
```

The old suite/composition model is V1. It remains documented only for migration,
compatibility, and local-development experiments:
[v1/](v1/).

旧的 suite / composition 模型属于 V1。它只为迁移、兼容和 local-development
实验保留文档：[v1/](v1/)。

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
- Production shared skills should come from installed plugins.
- Repo-local skills can be exposed from V1 legacy `.codex/skills/<skill>` or project-specific `.agents/skills/<skill>`.

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

### Install Codex Next / 安装 Codex Next

Codex Next is the production path for shared public skills from this repository.

Codex Next 是本仓库公开共享 skills 的生产路径。

```bash
codex plugin marketplace add https://github.com/BlueSkyXN/Codex-is-all-you-need.git
codex plugin list --marketplace codex-is-all-you-need --available --json
codex plugin add codex-next@codex-is-all-you-need
```

After installation, start with `$codex-next:core-router` or ask Codex to use
Codex Next for the task.

安装后可以从 `$codex-next:core-router` 开始，或直接要求 Codex 使用 Codex Next。

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

The dashboard is read-only. In V2 it reports source entries. When V1
compatibility paths are configured, it can also report V1 legacy/local-dev suites,
runtime connections, broken symlinks, and status issues.

面板是只读的。在 V2 中它报告 source entries；如果配置了 V1 兼容路径，也可以报告
V1 legacy/local-dev suites、runtime 连接、断链和状态问题。

### Optional V1 compatibility: sync legacy/local-dev repo-local entrypoints / 可选 V1 兼容：同步 legacy/local-dev repo-local 入口

Use this only for V1 legacy suite setups, local-development experiments, or
project-specific custom agent exposure. Production shared skills should come
from the installed plugin.

只有 V1 legacy suite 设置、local-dev 实验或项目专属 custom agent 暴露才需要使用这里。
生产态共享 skills 应来自已安装插件。

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

Do not deploy shared plugin or V1 suite skills into `.agents/skills`; keep
`.agents/skills` for project-only skills.

不要把共享 plugin 或 V1 suite skills 部署到 `.agents/skills`；`.agents/skills` 应留给项目专属 skills。

## 4. V1 Compatibility Sync, Update, Prune, Clean / V1 兼容：创建、更新、裁剪、清理

For V1 legacy/local-dev entrypoint management, the script supports two actions:
`sync` and `clean`, and two link modes: `directories` and `entries`.

对于 V1 legacy/local-dev entrypoint 管理，脚本支持两个动作：`sync` 和 `clean`，
以及两种链接模式：`directories` 和 `entries`。

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
| `sdlc-manager` | 7 | 21 | Architecture-first SDLC control: requirements, SRS/NFR, HLD/LLD, ADR, domain boundaries, SPEC, handoff |
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

Recommended skills: dev-python-quality, dev-test-strategy.

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

Recommended source location:

推荐 source 位置：

```text
<source-catalog>/dev/skills/dev-python-quality/SKILL.md
```

Plugin-installed production availability:

plugin 安装后的生产态可用性：

```text
$codex-next:dev-python-quality
```

V1 legacy/local-dev runtime-visible location:

V1 legacy/local-dev runtime 可见位置：

```text
<repo>/.codex/skills/dev-python-quality/SKILL.md
```

Project-only overlay:

项目专属叠加：

```text
<repo>/.agents/skills/project-only-skill/SKILL.md
```

## 8. V1 Legacy Suite Docs / V1 Legacy Suite 文档

The suite/composition tutorial has moved out of the V2 usage path. Use it only
for migration, explicit local-development experiments, or legacy custom-agent
exposure.

suite / composition 教程已经移出 V2 使用路径。只有迁移、明确的 local-development
实验或 legacy custom-agent 暴露才需要使用。

- [V1 Suite Composition](v1/suite-composition.md)
- [V1 To V2 Migration](v1/suite-to-plugin-migration.md)

## 9. Maintenance Checklist / 维护检查清单

Before changing presets:

改预设前：

```text
1. Confirm the source catalog is the source of truth.
2. Confirm agent TOML files parse.
3. Confirm each skill folder has SKILL.md.
4. Confirm plugin package contents align with intended public skills.
5. Confirm V1 suite symlinks only exist for migration or explicit local-dev needs.
6. Confirm runtime entrypoints are repo-local or user-global as intended.
7. Run the dashboard in json-only mode when V1 suites are involved.
8. Use Codex plugin list, prompt-input, or a real Codex run for visibility validation when needed.
```

Helpful commands:

常用命令：

```bash
codex plugin list --marketplace codex-is-all-you-need --available --json
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
  Install the plugin for shared skills, or sync repo-local .codex entrypoints only for V1 legacy/local-dev suites.

错误：
  在父级工作区放一个 .codex，然后期待所有子 git repo 自动继承。
修正：
  共享 skills 安装插件；只有 V1 legacy/local-dev suites 才给每个子 repo 同步 repo-local .codex entrypoints。
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
