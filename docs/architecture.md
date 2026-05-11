# Architecture / 架构说明

The dashboard follows a three-layer model.

这个 dashboard 使用三层模型。

```text
source catalog / 素材目录
  EN: Groups such as common, dev, data, office, and research.
      Each group can contain agents/*.toml and skills/<skill-name>/SKILL.md.
  CN: common、dev、data、office、research 等分组。
      每个分组可以包含 agents/*.toml 和 skills/<skill-name>/SKILL.md。

local suites / 本机组合包
  EN: Machine-local symlink compositions such as user, github, nondev-data,
      and nondev-all. Suites are not new sources; they are composed views over
      source entries.
  CN: 本机上的 symlink 组合层，例如 user、github、nondev-data、nondev-all。
      suite 不是新的素材源，而是对 source entries 的组合视图。

runtime directories / 运行目录
  EN: Actual working directories whose .codex/agents and .codex/skills entries
      point to a suite.
  CN: 实际工作目录，其中 .codex/agents 和 .codex/skills 指向某个 suite。
```

Only these runtime entries should point to suites:

只有下面两个 runtime entries 应该指向 suites：

```text
<runtime>/.codex/agents -> <suites-root>/<suite>/agents
<runtime>/.codex/skills -> <suites-root>/<suite>/skills
```

Do not symlink the whole `.codex` directory. Runtime directories may need their own `.codex/config.toml`, hooks, or other local files.

不要 symlink 整个 `.codex` 目录。runtime directories 可能需要保留自己的 `.codex/config.toml`、hooks 或其他本地文件。

## Public And Private Sources / 公开与私有素材

The dashboard supports configurable private roots. When a skill resolves under a private root, the generated local dashboard marks it as private. This is useful when a public repository provides tooling, while production machines compose public and private sources locally.

面板支持配置 private roots。当某个 skill 的最终解析路径落在 private root 下时，本地生成的 dashboard 会把它标记为 private。这适合“公开仓库提供工具，本机生产环境同时组合公开和私有素材”的模式。

Generated files can contain private paths and private skill names. Keep them outside the public repository.

生成文件可能包含私有路径和私有 skill 名称，应放在公开仓库外。

## Overlay Direction / 叠加层方向

Runtime `.codex/agents` and `.codex/skills` are for shared suite exposure.

runtime 的 `.codex/agents` 和 `.codex/skills` 用于暴露共享 suite。

Project-level `.agents/skills` overlays can be added later for project-specific skills. The dashboard currently records this as a limitation rather than treating it as complete runtime discovery.

后续可以用项目级 `.agents/skills` 做项目专属 skill 叠加。当前 dashboard 把这件事列为限制，不把自己声明成完整的 runtime discovery。

## Related Design Docs / 相关设计文档

- [Agent Design / Agent 设计](agent-design.md)
- [Agent Skill Map / Agent 与 Skill 分工](agent-skill-map.md)
- [Skill Design / Skill 设计](skill-design.md)
- [Claude To Codex Migration / Claude 到 Codex 迁移](claude-to-codex-migration.md)
- [Public And Private Strategy / 公开与私有分层](public-private-strategy.md)

## Example Assets / 示例资产

The `examples/` directory contains a sanitized production-derived source catalog, suite notes, and a sample runtime `AGENTS.md`.

`examples/` 目录包含从真实生产设计抽取并脱敏后的 source catalog、suite 说明和一个示例 runtime `AGENTS.md`。

They are documentation fixtures and public templates, not a complete production preset system.

它们是文档示例和公开模板，不是完整生产预设系统。
