# Architecture / 架构说明

This repository is now in the V2 plugin-first state. The production model is
the installable Codex Next plugin, backed by a public-safe source catalog and a
checked-in marketplace entry.

本仓库现在处于 V2 plugin-first 状态。生产模型是可安装的 Codex Next 插件，
由公开安全的 source catalog 和仓库内 marketplace entry 支撑。

V2 production path:

V2 生产路径：

```text
source catalog / 素材目录
  -> plugin package / 插件包
  -> marketplace install / marketplace 安装
```

V1 suite/composition remains only as a legacy compatibility model for migration,
explicit local-development experiments, or custom-agent exposure. It is not the
default production architecture. See [V1 Suite Composition](v1/suite-composition.md)
and [V1 To V2 Migration](v1/suite-to-plugin-migration.md).

V1 suite / composition 只作为迁移、明确 local-development 实验或 custom-agent
暴露的 legacy 兼容模型保留。它不是默认生产架构。见
[V1 Suite Composition](v1/suite-composition.md) 和
[V1 To V2 Migration](v1/suite-to-plugin-migration.md)。

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
V1 legacy/local-dev symlink target. Each child repo still needs repo-local
entrypoints under its own `.codex` if it opts into that compatibility path.

这意味着 `/path/to/workspace/.codex` 这样的工作区聚合层只是 V1 legacy/local-dev
symlink target。若某个子 repo 选择这条兼容路径，仍需要在自己的 `.codex` 下创建
repo-local entrypoints。

## Public And Private Sources / 公开与私有素材

The dashboard supports configurable private roots. When a skill resolves under a private root, the generated local dashboard marks it as private. This is useful when a public repository provides tooling, while production machines compose public and private sources locally.

面板支持配置 private roots。当某个 skill 的最终解析路径落在 private root 下时，本地生成的 dashboard 会把它标记为 private。这适合“公开仓库提供工具，本机生产环境同时组合公开和私有素材”的模式。

Generated files can contain private paths and private skill names. Keep them outside the public repository.

生成文件可能包含私有路径和私有 skill 名称，应放在公开仓库外。

## Overlay Direction / 叠加层方向

Production shared skills should come from the installed plugin. Runtime
`.codex/agents` remains the custom-agent discovery path, and `.codex/skills`
is a V1 legacy/local-dev path for suite exposure or project-specific experiments.

生产态共享 skills 应来自已安装插件。runtime 的 `.codex/agents` 仍是 custom
agent 发现路径，`.codex/skills` 是 V1 legacy/local-dev 的 suite 暴露或项目实验路径。

Project-level `.agents/skills` overlays can be reserved for project-specific
skills. Custom agents, however, are discovered from `.codex/agents/*.toml`;
`.agents/agents` is not a custom agent discovery path.

可以把项目级 `.agents/skills` 预留给项目专属 skill。但 custom agent 的有效
发现路径是 `.codex/agents/*.toml`；`.agents/agents` 不是 custom agent
discovery path。

Do not expand shared plugin or V1 suite skills into `.agents/skills`; keep that
namespace available for user or project-defined skills.

不要把共享 plugin 或 V1 suite skills 展开到 `.agents/skills`；这个命名空间应留给用户或项目自定义 skills。

## Related Design Docs / 相关设计文档

- [Agent Design / Agent 设计](agent-design.md)
- [Agent Skill Map / Agent 与 Skill 分工](agent-skill-map.md)
- [Skill Design / Skill 设计](skill-design.md)
- [Skill Spec / Skill 开发规范](skill-spec/SPEC.md)
- [Skill platform research / 平台调研](skill-spec/research/README.md)
- [SDLC Manager Flow / SDLC 管理流程](architecture-first-sdlc-flow.md)
- [Claude To Codex Migration / Claude 到 Codex 迁移](claude-to-codex-migration.md)
- [Public And Private Strategy / 公开与私有分层](public-private-strategy.md)

## Example Assets / 示例资产

The `examples/` directory contains a sanitized production-derived source
catalog, a V1 suite fixture pointer, and a sample runtime `AGENTS.md`.

`examples/` 目录包含从真实生产设计抽取并脱敏后的 source catalog、V1 suite 示例入口
和一个示例 runtime `AGENTS.md`。

They are documentation fixtures and public templates, not a complete production preset system.

它们是文档示例和公开模板，不是完整生产预设系统。
