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
  EN: Work directories where Codex runs. They expose `.codex/agents` and
      `.codex/skills` by linking to a suite.
  CN: Codex 实际运行的工作目录，通过 `.codex/agents` 和 `.codex/skills`
      连接到某个 suite。

project overlays
  EN: Optional `.agents/skills` folders for project-specific extras.
  CN: 可选的 `.agents/skills`，用于项目专属补充。
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

Runtime directories should link only the exposed entries:

运行目录只应连接暴露入口：

```text
<runtime>/.codex/agents -> ~/.codex/suites/<suite>/agents
<runtime>/.codex/skills -> ~/.codex/suites/<suite>/skills
```

Do not symlink the whole `.codex` folder. Other local files under `.codex` may need to stay runtime-specific.

不要 symlink 整个 `.codex` 文件夹。`.codex` 下的其他本地文件可能需要保留运行目录自己的配置。

## Project-Specific Overlays / 项目专属叠加

Shared suites are good for broad work domains. Project-specific skills can live in project-local overlays:

共享 suite 适合大任务域。项目专属技能可以放在项目本地叠加层：

```text
<project>/
  .codex/
    agents -> suite agents
    skills -> suite skills
  .agents/
    skills/
      project-only-skill/
        SKILL.md
```

This gives two layers:

这形成两层：

```text
.codex = shared abstract capability
.agents = project-specific capability
```

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
