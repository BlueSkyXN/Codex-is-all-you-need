# Example Runtime Instructions / 示例运行目录规则

This file is a public-safe example of a runtime `AGENTS.md`.

这是一个可公开的 runtime `AGENTS.md` 示例。

## Communication / 沟通

- Use Chinese for user-facing explanations when the user writes Chinese.
- Keep code, commands, file paths, API names, and config keys in English.
- State verification gaps explicitly.

## Work Rules / 工作规则

- Inspect real files before changing behavior.
- Prefer existing project conventions over new abstractions.
- Keep edits scoped to the requested task.
- Do not overwrite user changes.
- Validate with the smallest meaningful command, test, or render check.

## Preset Model / 预设模型

```text
.codex/agents = shared runtime-visible roles
.codex/skills = shared runtime-visible workflows
.agents/skills = optional project-specific overlays
```

Agents may recommend skills, but filesystem visibility decides what Codex can actually use.

agent 可以推荐 skill，但实际是否可用由文件结构决定。
