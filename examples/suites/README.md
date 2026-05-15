# Suite Examples / Suite 示例

Suites are local symlink compositions. This directory documents the pattern without creating real symlinks.

suite 是本机 symlink 组合层。本目录只说明模式，不创建真实 symlink。

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
      bugfix -> <source>/dev/skills/bugfix

  planning/
    agents/
      common_task_planner.toml -> <source>/common/agents/common_task_planner.toml
      product_engineering_requirements_lead.toml -> <source>/product-engineering/agents/product_engineering_requirements_lead.toml
      product_engineering_delivery_planner.toml -> <source>/product-engineering/agents/product_engineering_delivery_planner.toml
    skills/
      prd-workflow -> <source>/product-engineering/skills/prd-workflow
      delivery-task-planning -> <source>/product-engineering/skills/delivery-task-planning

  nondev-all/
    agents/
      common_task_planner.toml -> <source>/common/agents/common_task_planner.toml
      data_profile_analyst.toml -> <source>/data/agents/data_profile_analyst.toml
      office_report_writer.toml -> <source>/office/agents/office_report_writer.toml
      research_synthesis_writer.toml -> <source>/research/agents/research_synthesis_writer.toml
    skills/
      tabular-analysis -> <source>/data/skills/tabular-analysis
      weekly-report -> <source>/office/skills/weekly-report
      research-synthesis -> <source>/research/skills/research-synthesis
```

## Runtime Links / 运行目录连接

Only link the two exposed directories:

只连接两个暴露目录：

```text
<runtime>/.codex/agents -> ~/.codex/suites/<suite>/agents
<runtime>/.codex/skills -> ~/.codex/suites/<suite>/skills
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
```

For skills, the symlink points to the skill folder:

skill 的 symlink 指向整个 skill 文件夹：

```text
weekly-report -> <source>/office/skills/weekly-report
```

This keeps `SKILL.md`, `scripts/`, `references/`, and `assets/` together.

这样可以保持 `SKILL.md`、`scripts/`、`references/` 和 `assets/` 一起移动。
