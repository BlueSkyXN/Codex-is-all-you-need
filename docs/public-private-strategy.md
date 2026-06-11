# Public And Private Strategy / 公开与私有分层

This repository is the public layer. It should teach the system design and provide safe tooling.

本仓库是公开层，用来讲清系统设计并提供安全工具。

## Layer Model / 分层模型

```text
public repository
  EN: Dashboard, docs, sanitized production-derived examples, plugin package,
      marketplace metadata, migration guides.
  CN: 面板、文档、经过脱敏的 production-derived 示例、插件包、marketplace metadata、
      迁移说明。

plugin distribution
  EN: Codex Next packages public-safe shared skills and is installed through
      the repository marketplace.
  CN: Codex Next 打包公开安全的共享 skills，并通过仓库 marketplace 安装。

private production catalog
  EN: Real agents, real skills, private workflows, local business process.
  CN: 真实 agents、真实 skills、私有工作流、本地业务流程。

legacy/local-dev suite aggregation
  EN: Legacy or local-development symlink compositions for custom agents,
      experiments, or machines that have not migrated to plugins.
  CN: legacy 或 local-dev symlink 聚合层，用于 custom agents、实验，或尚未迁移到
      plugin 的机器。

runtime directories
  EN: Work directories where Codex runs. They expose repo-local `.codex`
      entrypoints only when a local suite/custom-agent path is intentionally used.
  CN: Codex 实际运行的工作目录，通过 repo-local `.codex` entrypoints
      有意使用本地 suite/custom-agent 路径时才暴露入口。

project overlays
  EN: Optional `.agents/skills` folders for project-specific skill extras.
      Project-specific custom agents still belong in `.codex/agents/*.toml`.
  CN: 可选的 `.agents/skills`，用于项目专属 skill 补充。项目专属
      custom agent 仍应放在 `.codex/agents/*.toml`。
```

## Public Repository Rules / 公开仓库规则

The public repository may include:

公开仓库可以包含：

- Dashboard source code.
- Codex Next plugin package and marketplace metadata.
- Public-safe docs.
- Sanitized public-safe agents and skills.
- Production-derived examples after private content has been removed.
- Example config with placeholder paths.
- Migration guides and architecture diagrams.

The public repository must not include:

公开仓库不应包含：

- Real production paths.
- Private skill content.
- Unpublished private skill names that only make sense in a local catalog.
- Generated dashboard state from a real machine.
- Private business templates.
- Credentials, tokens, account names, or internal service URLs.

## Private Catalog Rules / 私有素材规则

The private catalog can hold the complete production set:

私有素材库可以保存完整生产集：

```text
codex/
  common/
    agents/
    skills/
  sdlc-manager/
    agents/
    skills/
  dev/
    agents/
    skills/
  data/
    agents/
    skills/
  office/
    agents/
    skills/
  research/
    agents/
    skills/
```

Private skills may point to private templates, scripts, and examples. Keep them out of the public repository until they are deliberately sanitized.

私有 skills 可以引用私有模板、脚本和示例。除非已经明确脱敏，否则不要放入公开仓库。

## Suite Rules / Suite 规则

Suites are local compositions, not source catalogs. They are legacy or
local-development infrastructure after shared production skills move into the
Codex Next plugin.

suite 是本机组合层，不是素材源。在共享生产 skills 迁移到 Codex Next 插件后，
它们属于 legacy 或 local-dev 基础设施。

```text
~/.codex/suites/
  user/
    agents/
    skills/
  planning/
    agents/
    skills/
  github/
    agents/
    skills/
  nondev-all/
    agents/
    skills/
  all/
    agents/
    skills/
```

Each entry inside `agents/` or `skills/` should be a symlink to a source item.

`agents/` 或 `skills/` 中的每个条目应是指向素材项的 symlink。

```text
suite/agents/dev_code_reviewer.toml -> source/dev/agents/dev_code_reviewer.toml
suite/skills/dev-bugfix -> source/dev/skills/dev-bugfix
```

This supports one source item being reused by many suites.

这样一个素材项可以被多个 suite 复用。

## Runtime Rules / 运行目录规则

Production shared skills should come from the installed plugin. Runtime
directories should link exposed entries only for legacy suite setups,
local-development experiments, or project-specific custom agents. A parent
workspace `.codex` is not inherited automatically by child git repositories, so
each repo that should opt in to this local path needs local entrypoints:

生产态共享 skills 应来自已安装插件。运行目录只有在 legacy suite 设置、local-dev
实验或项目专属 custom agents 场景下才应连接暴露入口。父级工作区 `.codex`
不会被子 git repo 自动继承，所以每个需要 opt in 本地路径的 repo 都需要本地
entrypoints：

```text
<runtime>/.codex/agents -> ~/.codex/suites/<suite>/agents
<runtime>/.codex/skills -> ~/.codex/suites/<suite>/skills

# Or, when a repo must keep real .codex/agents or .codex/skills directories:
<runtime>/.codex/agents/<agent>.toml -> /path/to/workspace/.codex/agents/<agent>.toml
<runtime>/.codex/skills/<skill> -> /path/to/workspace/.codex/skills/<skill>
```

Do not symlink the whole `.codex` folder. Other local files under `.codex` may need to stay runtime-specific.

不要 symlink 整个 `.codex` 文件夹。`.codex` 下的其他本地文件可能需要保留运行目录自己的配置。

For legacy/local-dev batch setup, use the entrypoint sync helper in dry-run mode
first. Choose `--link-mode directories` for workspace aggregates unless the
target repo needs real entry directories.

legacy/local-dev 批量设置时，先用 entrypoint sync helper 做 dry-run。对 workspace
聚合层优先选择 `--link-mode directories`；只有目标 repo 需要保留真实入口目录时才用
逐项模式。

```bash
python3 scripts/sync_codex_entrypoints.py sync \
  --workspace /path/to/workspace \
  --source-root /path/to/workspace/.codex \
  --link-mode directories
```

Apply after reviewing the plan:

确认计划后再 apply：

```bash
python3 scripts/sync_codex_entrypoints.py sync \
  --workspace /path/to/workspace \
  --source-root /path/to/workspace/.codex \
  --link-mode directories \
  --apply
```

Use `--link-mode entries --prune` with `sync` to remove stale individual symlinks
that still point into the same aggregate but no longer exist there.

需要清理仍指向同一聚合层、但聚合层已不存在的逐项 symlink 时，使用
`--link-mode entries --prune`。

Clean managed entrypoints with:

清理脚本管理的 entrypoints：

```bash
python3 scripts/sync_codex_entrypoints.py clean \
  --workspace /path/to/workspace \
  --source-root /path/to/workspace/.codex \
  --link-mode directories
```

The helper updates each target repo's `.git/info/exclude` with `.codex/` and
`.agents/` so machine-local symlink state stays untracked.

这个 helper 会向每个目标 repo 的 `.git/info/exclude` 写入 `.codex/` 和
`.agents/`，让本机 symlink 状态保持未跟踪。

For user-level defaults across repositories, use Git's XDG ignore path
`~/.config/git/ignore`; see [Global Git Ignore Profile](global-git-ignore.md).

跨仓库的用户级默认规则应使用 Git 的 XDG ignore 路径
`~/.config/git/ignore`；见 [Global Git Ignore Profile](global-git-ignore.md)。

## Project-Specific Overlays / 项目专属叠加

Plugin-installed skills are the shared production layer. Legacy/local-dev
suites can still serve broad work domains, and project-specific skills can live
in project-local overlays:

插件安装的 skills 是共享生产层。legacy/local-dev suites 仍可服务大任务域，
项目专属技能可以放在项目本地叠加层：

```text
<project>/
  .codex/
    agents/
      shared_agent.toml -> workspace aggregate
      project_agent.toml
    skills/
      shared-skill -> workspace aggregate
  .agents/
    skills/
      project-only-skill/
        SKILL.md
```

This gives two layers:

这形成两层：

```text
.codex = legacy/local-dev shared capability plus repo-local custom agents
.agents = project-specific skill capability
```

Do not expand shared plugin or suite skills into `.agents/skills`. That directory is
reserved for user-owned or project-owned overlays. If a repo needs shared
suite skills beside local `.codex` content, use entry links under
`.codex/skills` instead. For production shared skills, install the plugin.

不要把共享 plugin 或 suite skills 展开到 `.agents/skills`。这个目录应保留给用户或项目自有叠加层。
如果某个 repo 需要在本地 `.codex` 内容旁边放共享 suite skills，应在 `.codex/skills`
下使用逐项链接。生产态共享 skills 应安装插件。

The dashboard currently focuses on `.codex` suite connections for
legacy/local-dev setups. Project overlay discovery can be added later.

当前面板主要检查 legacy/local-dev 设置中的 `.codex` suite 连接。项目叠加层发现能力可后续加入。

## Publish Checklist / 发布检查

Before publishing:

发布前检查：

- Run a private-path keyword scan.
- Confirm generated dashboard output is ignored.
- Confirm example configs use placeholder paths only.
- Confirm example agents and skills are public-safe and do not depend on unpublished private skills.
- Confirm plugin package and marketplace metadata contain only public-safe skill content.
- Confirm docs explain the public/private boundary.
