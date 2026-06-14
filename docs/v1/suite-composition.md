# V1 Suite Composition / V1 Suite 组合

This page preserves the old suite/composition model for legacy migration and
local-development compatibility. It is not the current production model.

本页保留旧的 suite / composition 模型，用于历史迁移和 local-development 兼容。
它不是当前生产模型。

For V2 usage, install the Codex Next plugin and start from the plugin surface:

V2 使用方式应安装 Codex Next 插件，并从插件 surface 开始：

```text
source catalog -> plugin package -> marketplace install
```

## Example Layout / 示例结构

```text
~/.codex/suites/
  user/
    agents/
      common_task_planner.toml -> <source>/common/agents/common_task_planner.toml
    skills/

  github/
    agents/
      common_task_planner.toml -> <source>/common/agents/common_task_planner.toml
      dev_code_reviewer.toml -> <source>/dev/agents/dev_code_reviewer.toml
    skills/
      dev-bugfix -> <source>/dev/skills/dev-bugfix

  planning/
    agents/
      common_task_planner.toml -> <source>/common/agents/common_task_planner.toml
      sdlc_requirements_manager.toml -> <source>/sdlc-manager/agents/sdlc_requirements_manager.toml
      sdlc_delivery_planner.toml -> <source>/sdlc-manager/agents/sdlc_delivery_planner.toml
    skills/
      sdlc-prd-workflow -> <source>/sdlc-manager/skills/sdlc-prd-workflow
      sdlc-dev-handoff-planning -> <source>/sdlc-manager/skills/sdlc-dev-handoff-planning

  all/
    agents/
      common_task_planner.toml -> <source>/common/agents/common_task_planner.toml
      sdlc_requirements_manager.toml -> <source>/sdlc-manager/agents/sdlc_requirements_manager.toml
      dev_code_reviewer.toml -> <source>/dev/agents/dev_code_reviewer.toml
      data_profile_analyst.toml -> <source>/data/agents/data_profile_analyst.toml
      office_report_writer.toml -> <source>/office/agents/office_report_writer.toml
      research_synthesis_writer.toml -> <source>/research/agents/research_synthesis_writer.toml
    skills/
      sdlc-prd-workflow -> <source>/sdlc-manager/skills/sdlc-prd-workflow
      dev-bugfix -> <source>/dev/skills/dev-bugfix
      data-tabular-analysis -> <source>/data/skills/data-tabular-analysis
      office-weekly-report -> <source>/office/skills/office-weekly-report
      research-synthesis -> <source>/research/skills/research-synthesis
```

## Runtime Links / 运行目录连接

Only link runtime entrypoints when this V1 compatibility path is intentional.
Production shared skills should come from an installed plugin.

只有明确使用 V1 兼容路径时才连接 runtime entrypoints。生产态共享 skills
应来自已安装插件。

```text
<runtime>/.codex/agents -> ~/.codex/suites/<suite>/agents
<runtime>/.codex/skills -> ~/.codex/suites/<suite>/skills

# Or, when a repo must keep real entry directories:
<runtime>/.codex/agents/<agent>.toml -> /path/to/workspace/.codex/agents/<agent>.toml
<runtime>/.codex/skills/<skill> -> /path/to/workspace/.codex/skills/<skill>
```

Do not link the entire `.codex` folder. A runtime may need its own
`.codex/config.toml`, hooks, or local files.

不要连接整个 `.codex` 文件夹。runtime 可能需要自己的 `.codex/config.toml`、
hooks 或本地文件。

## One Source, Many Suites / 一个素材，多套组合

Because each entry is a symlink, one source agent or skill can appear in many
suites. This was useful in V1 when runtime-visible filesystem entrypoints were
the main composition mechanism.

由于每个条目都是 symlink，一个 source agent 或 skill 可以出现在多个 suites 中。
这在 V1 中有用，因为当时 runtime-visible filesystem entrypoints 是主要组合机制。

```text
common_task_planner.toml
  -> user/agents/common_task_planner.toml
  -> github/agents/common_task_planner.toml
  -> all/agents/common_task_planner.toml
```

For skills, the symlink points to the whole skill folder, not only `SKILL.md`,
so `scripts/`, `references/`, `examples/`, and `assets/` stay available.

skill 的 symlink 应指向整个 skill folder，而不是只指向 `SKILL.md`，这样
`scripts/`、`references/`、`examples/`、`assets/` 才能一起可用。

## Migration / 迁移

If an existing machine still depends on this model, use
[V1 To V2 Migration](suite-to-plugin-migration.md) to archive runtime
links and verify that plugin-provided skills remain available.
