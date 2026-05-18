# Public And Private Strategy / 公开与私有分层

This repository is the public layer. It should teach the system design and provide safe tooling.

本仓库是公开层，用来讲清系统设计并提供安全工具。

## Layer Model / 分层模型

```text
public repository
  EN: Dashboard, docs, sanitized production-derived examples, migration guides.
  CN: 面板、文档、经过脱敏的 production-derived 示例、迁移说明。

private production catalog
  EN: Real agents, real skills, private workflows, local business process.
  CN: 真实 agents、真实 skills、私有工作流、本地业务流程。

local suite aggregation
  EN: Machine-local symlink compositions that choose which agents and skills
      are exposed to each runtime domain.
  CN: 本机 symlink 聚合层，决定每个运行目录暴露哪些 agents / skills。

runtime directories
  EN: Work directories where Codex runs. They expose repo-local `.codex`
      entrypoints by linking to a suite or to a workspace aggregate.
  CN: Codex 实际运行的工作目录，通过 repo-local `.codex` entrypoints
      连接到某个 suite 或工作区聚合层。

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
  product-engineering/
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

Suites are local compositions, not source catalogs.

suite 是本机组合层，不是素材源。

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
```

Each entry inside `agents/` or `skills/` should be a symlink to a source item.

`agents/` 或 `skills/` 中的每个条目应是指向素材项的 symlink。

```text
suite/agents/dev_code_reviewer.toml -> source/dev/agents/dev_code_reviewer.toml
suite/skills/bugfix -> source/dev/skills/bugfix
```

This supports one source item being reused by many suites.

这样一个素材项可以被多个 suite 复用。

## Runtime Rules / 运行目录规则

Runtime directories should link only the exposed entries. A parent workspace
`.codex` is not inherited automatically by child git repositories, so each repo
that should opt in needs local entrypoints:

运行目录只应连接暴露入口。父级工作区 `.codex` 不会被子 git repo 自动继承，
所以每个需要 opt in 的 repo 都需要本地 entrypoints：

```text
<runtime>/.codex/agents -> ~/.codex/suites/<suite>/agents
<runtime>/.codex/skills -> ~/.codex/suites/<suite>/skills

# Or, when a repo must keep real .codex/agents or .codex/skills directories:
<runtime>/.codex/agents/<agent>.toml -> /Users/sky/GitHub/.codex/agents/<agent>.toml
<runtime>/.codex/skills/<skill> -> /Users/sky/GitHub/.codex/skills/<skill>
```

Do not symlink the whole `.codex` folder. Other local files under `.codex` may need to stay runtime-specific.

不要 symlink 整个 `.codex` 文件夹。`.codex` 下的其他本地文件可能需要保留运行目录自己的配置。

For batch setup, use the entrypoint sync helper in dry-run mode first. Choose
`--link-mode directories` for workspace aggregates unless the target repo needs
real entry directories.

批量设置时，先用 entrypoint sync helper 做 dry-run。对 workspace 聚合层优先选择
`--link-mode directories`；只有目标 repo 需要保留真实入口目录时才用逐项模式。

```bash
python3 scripts/sync_codex_entrypoints.py sync \
  --workspace /Users/sky/GitHub \
  --source-root /Users/sky/GitHub/.codex \
  --link-mode directories
```

Apply after reviewing the plan:

确认计划后再 apply：

```bash
python3 scripts/sync_codex_entrypoints.py sync \
  --workspace /Users/sky/GitHub \
  --source-root /Users/sky/GitHub/.codex \
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
  --workspace /Users/sky/GitHub \
  --source-root /Users/sky/GitHub/.codex \
  --link-mode directories
```

The helper updates each target repo's `.git/info/exclude` with `.codex/` and
`.agents/` so machine-local symlink state stays untracked.

这个 helper 会向每个目标 repo 的 `.git/info/exclude` 写入 `.codex/` 和
`.agents/`，让本机 symlink 状态保持未跟踪。

## Project-Specific Overlays / 项目专属叠加

Shared suites are good for broad work domains. Project-specific skills can live in project-local overlays:

共享 suite 适合大任务域。项目专属技能可以放在项目本地叠加层：

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
.codex = shared abstract capability plus repo-local custom agents
.agents = project-specific skill capability
```

Do not expand shared suite skills into `.agents/skills`. That directory is
reserved for user-owned or project-owned overlays. If a repo needs shared
skills beside local `.codex` content, use entry links under `.codex/skills`
instead.

不要把共享 suite skills 展开到 `.agents/skills`。这个目录应保留给用户或项目自有叠加层。
如果某个 repo 需要在本地 `.codex` 内容旁边放共享 skills，应在 `.codex/skills` 下使用
逐项链接。

The dashboard currently focuses on `.codex` suite connections. Project overlay discovery can be added later.

当前面板主要检查 `.codex` 的 suite 连接。项目叠加层发现能力可后续加入。

## Publish Checklist / 发布检查

Before publishing:

发布前检查：

- Run a private-path keyword scan.
- Confirm generated dashboard output is ignored.
- Confirm example configs use placeholder paths only.
- Confirm example agents and skills are public-safe and do not depend on unpublished private skills.
- Confirm docs explain the public/private boundary.
