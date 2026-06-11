# Claude To Codex Migration / Claude 到 Codex 迁移

This repository can learn from Claude Code agent and skill libraries, but it should not copy private operational content.

本仓库可以学习 Claude Code agent / skill 库的结构，但不应复制私有生产内容。

## Migration Principle / 迁移原则

```text
Copy the pattern, not the private payload.
复制模式，不复制私有负载。
```

Useful source material:

可学习的来源：

- Role boundaries from legacy subagent Markdown files.
- Trigger examples from public agent libraries.
- Checklists that map to quality gates.
- Skill workflow structures such as inputs, steps, validation, and output format.

Do not migrate directly:

不要直接迁移：

- Claude-only frontmatter such as `tools: Read, Write, Edit`.
- Claude-only context-manager message protocols.
- Long role prose that duplicates general model knowledge.
- Private skills, private examples, private scripts, and real environment paths.

## Agent Conversion / Agent 转换

Claude-style Markdown:

Claude 风格 Markdown：

```markdown
---
name: code-reviewer
description: Use when reviewing code changes...
tools: Read, Write, Edit, Bash, Glob, Grep
model: opus
---

You are a senior code reviewer...
Checklist...
Workflow...
```

Codex-style TOML:

Codex 风格 TOML：

```toml
name = "dev_code_reviewer"
description = "Review code changes for correctness, maintainability, security, tests, and release risk."
nickname_candidates = ["Reviewer"]

developer_instructions = """
You are a pragmatic code reviewer.

Lead with findings. Include file and line references when available.
Check correctness, tests, security, maintainability, and release risk.

Recommended skills: dev-bugfix.
"""
```

Conversion rules:

转换规则：

| Claude Field Or Section | Codex Destination |
|---|---|
| `name` | Keep or rename into domain-prefixed snake_case |
| `description` | Keep the trigger intent, shorten examples |
| `tools` | Usually omit; Codex runtime controls tools |
| `model` | Usually omit; runtime configuration controls model policy |
| Long role body | Compress into `developer_instructions` |
| Workflow details | Move repeated procedures into skills |
| Private examples | Replace with public-safe examples |

## Skill Conversion / Skill 转换

Claude and Codex skills both center on `SKILL.md`, so the migration is mostly editorial.

Claude 和 Codex skills 都以 `SKILL.md` 为中心，因此迁移重点是编辑和脱敏。

Keep:

保留：

- Trigger description.
- Required inputs.
- Step-by-step workflow.
- Validation gates.
- Output format.

Rewrite:

改写：

- Tool-specific commands.
- Absolute paths.
- Internal examples.
- Large background sections.

Split:

拆分：

- Put deterministic helpers into `scripts/`.
- Put large references into `references/`.
- Put reusable templates into `assets/`.

## Domain Mapping / 领域映射

Large Claude agent libraries often have many categories. A compact Codex setup can map them into six packs.

大型 Claude agent 库通常分类很多。紧凑的 Codex 预设可以收敛成六个包。

| Codex Pack | Typical Claude Sources | Codex Purpose |
|---|---|---|
| `common` | meta-orchestration, documentation, review helpers | Planning, context cleanup, quality review |
| `sdlc-manager` | product, requirements, architecture, planning, PM roles | Architecture-first SDLC control, requirements, specs, traceability, handoff |
| `dev` | core development, language specialists, infrastructure, quality/security | Coding, testing, debugging, API/CLI verification |
| `data` | data-ai, database, analytics roles | Tables, DB exports, metrics, reproducible analysis |
| `office` | business-product, project management, writing roles | Reports, status updates, slides, formal documents |
| `research` | research-analysis, market/intelligence roles | Source collection, synthesis, evidence review |

## Migration Workflow / 迁移工作流

1. Inventory source agents and skills.
2. Classify each item into `common`, `sdlc-manager`, `dev`, `data`, `office`, or `research`.
3. Decide whether it should become an agent, a skill, both, or neither.
4. Strip private examples, paths, credentials, and internal process names.
5. Convert agents into short TOML files.
6. Convert reusable procedures into lean `SKILL.md` folders.
7. Add only public-safe examples to this repository.
8. Package public shared skills through Codex Next when they are meant for
   production reuse; keep private production versions in a private catalog.
9. Use local suites only for legacy/local-development composition, custom
   agents, or experiments.

## Decision Table / 决策表

| Source Material | Convert To | Reason |
|---|---|---|
| Role identity and judgment | Agent | It changes how Codex should think and prioritize |
| Repeatable file workflow | Skill | It can be reused across agents and runtimes |
| Long reference material | Skill `references/` | It should be loaded only when needed |
| Deterministic transformation | Skill `scripts/` | It should run reliably instead of being rewritten |
| Private report template | Private skill only | It is operational content, not a public example |
| Huge public agent body | Short agent plus docs | Smaller presets are easier to maintain |

## Validation / 验证

After migration:

迁移后检查：

- Agent TOML parses.
- Skill folders contain `SKILL.md`.
- Public repo has no private paths or sensitive names.
- Codex Next plugin exposes the intended public shared skills when packaging is
  in scope.
- Dashboard can scan the catalog and legacy/local-dev suites without parse errors when suites are in scope.
- Generated local dashboard output stays outside the public repository.
