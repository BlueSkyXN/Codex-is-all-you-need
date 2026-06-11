# Suite Examples / Suite 示例

Suites are legacy or local-development symlink compositions. This directory
documents the pattern without creating real symlinks. For production shared
skills, prefer the Codex Next plugin instead of runtime suite links.

suite 是 legacy 或 local-dev symlink 组合层。本目录只说明模式，不创建真实 symlink。
生产态共享 skills 优先使用 Codex Next 插件，而不是 runtime suite links。

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

  nondev-all/
    agents/
      common_task_planner.toml -> <source>/common/agents/common_task_planner.toml
      data_profile_analyst.toml -> <source>/data/agents/data_profile_analyst.toml
      office_report_writer.toml -> <source>/office/agents/office_report_writer.toml
      research_synthesis_writer.toml -> <source>/research/agents/research_synthesis_writer.toml
    skills/
      data-tabular-analysis -> <source>/data/skills/data-tabular-analysis
      office-weekly-report -> <source>/office/skills/office-weekly-report
      research-synthesis -> <source>/research/skills/research-synthesis

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

Only link exposed runtime entrypoints when this legacy/local-dev path is
intended. Production shared skills should come from an installed plugin. A
parent workspace `.codex` is a useful aggregate target, but child git
repositories do not inherit it automatically.

只有明确使用 legacy/local-dev 路径时才连接暴露的 runtime entrypoints。生产态共享
skills 应来自已安装插件。父级工作区 `.codex` 可以作为聚合 target，但子 git repo
不会自动继承它。

```text
<runtime>/.codex/agents -> ~/.codex/suites/<suite>/agents
<runtime>/.codex/skills -> ~/.codex/suites/<suite>/skills

# Or, when a repo must keep real entry directories:
<runtime>/.codex/agents/<agent>.toml -> /path/to/workspace/.codex/agents/<agent>.toml
<runtime>/.codex/skills/<skill> -> /path/to/workspace/.codex/skills/<skill>
```

Do not link the entire `.codex` folder.

不要连接整个 `.codex` 文件夹。

## One Source, Many Suites / 一个素材，多套组合

Because each entry is a symlink, one source agent or skill can appear in many suites.

由于每个条目都是 symlink，一个素材 agent 或 skill 可以出现在多个 suite 中。

```text
common_task_planner.toml
  -> user/agents/common_task_planner.toml
  -> github/agents/common_task_planner.toml
  -> nondev-all/agents/common_task_planner.toml
  -> all/agents/common_task_planner.toml
```

For skills, the symlink points to the skill folder:

skill 的 symlink 指向整个 skill 文件夹：

```text
office-weekly-report -> <source>/office/skills/office-weekly-report
```

This keeps `SKILL.md`, `scripts/`, `references/`, and `assets/` together.

这样可以保持 `SKILL.md`、`scripts/`、`references/` 和 `assets/` 一起移动。
