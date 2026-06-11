# Architecture / 架构说明

The repository now has a plugin-first production model, with the dashboard still
describing the legacy/local-development suite model.

本仓库现在采用 plugin-first 的生产模型；dashboard 仍用于说明 legacy/local-dev
suite 模型。

Production path:

生产路径：

```text
source catalog / 素材目录
  -> plugin package / 插件包
  -> marketplace install / marketplace 安装
```

Legacy/local-development path:

legacy/local-dev 路径：

```text
source catalog / 素材目录
  EN: Groups such as common, sdlc-manager, dev, data, office, and research.
      Each group can contain agents/*.toml and skills/<skill-name>/SKILL.md.
  CN: common、sdlc-manager、dev、data、office、research 等分组。
      每个分组可以包含 agents/*.toml 和 skills/<skill-name>/SKILL.md。

local suites / 本机组合包
  EN: Legacy or local-development symlink compositions such as user, github,
      nondev-data, nondev-all, and all. Suites are not new sources; they are
      composed views over source entries.
  CN: legacy 或 local-dev symlink 组合层，例如 user、github、nondev-data、
      nondev-all、all。suite 不是新的素材源，而是对 source entries 的组合视图。

runtime directories / 运行目录
  EN: Actual working directories whose repo-local .codex/agents and
      legacy .codex/skills entries can expose a shared aggregate or suite.
  CN: 实际工作目录，其中 repo-local .codex/agents 和 .codex/skills
      可以暴露共享聚合层或 suite。
```

For plugin-first production, install the plugin and keep shared skills out of
repo-local suite symlinks. Runtime entrypoints should point to suites only for
legacy/local-dev composition, custom agent exposure, or project-specific
experiments.

plugin-first 生产态应安装插件，并避免通过 repo-local suite symlink 暴露共享
skills。只有 legacy/local-dev 组合、custom agent 暴露或项目实验才应让 runtime
entrypoints 指向 suites 或已经聚合好的工作区 `.codex`：

```text
<runtime>/.codex/agents -> <suites-root>/<suite>/agents
<runtime>/.codex/skills -> <suites-root>/<suite>/skills

# Or, when a repo must keep real entry directories:
<runtime>/.codex/agents/<agent>.toml -> <workspace>/.codex/agents/<agent>.toml
<runtime>/.codex/skills/<skill> -> <workspace>/.codex/skills/<skill>
```

For legacy/local-dev workspace aggregates, directory links let suite updates
flow through automatically. Entry-by-entry links are useful only when a repo
must keep real `.codex/agents` or `.codex/skills` directories, selectively opt
in to a small set of shared entries, or mix shared entries with local
experiments.

对 legacy/local-dev workspace 聚合层，目录级链接可以让 suite 更新自动传导。逐项链接
只适合需要保留真实 `.codex/agents` 或 `.codex/skills` 目录、选择性 opt in
少量共享条目，或把共享条目和本地实验条目并列的 repo。

Do not symlink the whole `.codex` directory. Runtime directories may need their own `.codex/config.toml`, hooks, or other local files.

不要 symlink 整个 `.codex` 目录。runtime directories 可能需要保留自己的 `.codex/config.toml`、hooks 或其他本地文件。

## Discovery Boundary / 发现边界

Repo-level discovery is bounded by the current project root. With a git root,
Codex discovers repo skills and custom agents only along the path from the git
root to the current working directory. Without a git root, discovery is limited
to the current working directory. A parent workspace such as `/path/to/workspace`
is not inherited by child git repositories automatically.

repo-level discovery 受当前 project root 限制。有 git root 时，Codex 只在
git root 到当前工作目录的路径链上发现 repo skills 和 custom agents。没有 git
root 时，只看当前工作目录。像 `/path/to/workspace` 这样的父级工作区不会被子
git repo 自动继承。

This means a workspace aggregate such as `/path/to/workspace/.codex` is only a
legacy/local-dev symlink target. Each child repo still needs repo-local
entrypoints under its own `.codex` if it opts into that path.

这意味着 `/path/to/workspace/.codex` 这样的工作区聚合层只是 legacy/local-dev
symlink target。若某个子 repo 选择这条路径，仍需要在自己的 `.codex` 下创建
repo-local entrypoints。

## Public And Private Sources / 公开与私有素材

The dashboard supports configurable private roots. When a skill resolves under a private root, the generated local dashboard marks it as private. This is useful when a public repository provides tooling, while production machines compose public and private sources locally.

面板支持配置 private roots。当某个 skill 的最终解析路径落在 private root 下时，本地生成的 dashboard 会把它标记为 private。这适合“公开仓库提供工具，本机生产环境同时组合公开和私有素材”的模式。

Generated files can contain private paths and private skill names. Keep them outside the public repository.

生成文件可能包含私有路径和私有 skill 名称，应放在公开仓库外。

## Overlay Direction / 叠加层方向

Production shared skills should come from the installed plugin. Runtime
`.codex/agents` remains the custom-agent discovery path, and `.codex/skills`
is a legacy/local-dev path for suite exposure or project-specific experiments.

生产态共享 skills 应来自已安装插件。runtime 的 `.codex/agents` 仍是 custom
agent 发现路径，`.codex/skills` 是 legacy/local-dev 的 suite 暴露或项目实验路径。

Project-level `.agents/skills` overlays can be reserved for project-specific
skills. Custom agents, however, are discovered from `.codex/agents/*.toml`;
`.agents/agents` is not a custom agent discovery path.

可以把项目级 `.agents/skills` 预留给项目专属 skill。但 custom agent 的有效
发现路径是 `.codex/agents/*.toml`；`.agents/agents` 不是 custom agent
discovery path。

Do not expand shared plugin or suite skills into `.agents/skills`; keep that
namespace available for user or project-defined skills.

不要把共享 plugin 或 suite skills 展开到 `.agents/skills`；这个命名空间应留给用户或项目自定义 skills。

## Related Design Docs / 相关设计文档

- [Agent Design / Agent 设计](agent-design.md)
- [Agent Skill Map / Agent 与 Skill 分工](agent-skill-map.md)
- [Skill Design / Skill 设计](skill-design.md)
- [SDLC Manager Flow / SDLC 管理流程](architecture-first-sdlc-flow.md)
- [Claude To Codex Migration / Claude 到 Codex 迁移](claude-to-codex-migration.md)
- [Public And Private Strategy / 公开与私有分层](public-private-strategy.md)

## Example Assets / 示例资产

The `examples/` directory contains a sanitized production-derived source
catalog, legacy/local-dev suite notes, and a sample runtime `AGENTS.md`.

`examples/` 目录包含从真实生产设计抽取并脱敏后的 source catalog、legacy/local-dev
suite 说明和一个示例 runtime `AGENTS.md`。

They are documentation fixtures and public templates, not a complete production preset system.

它们是文档示例和公开模板，不是完整生产预设系统。
