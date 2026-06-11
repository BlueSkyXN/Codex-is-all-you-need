# Example runtime navigation card / 示例运行目录规则

This directory contains public-safe examples of runtime-level Codex
instructions. Read this card before changing the runtime instruction model or
adding runtime entrypoint examples.
Key files: `AGENTS.md`.

本目录包含可公开的 Codex runtime 级指令示例。修改 runtime 指令模型或新增
runtime entrypoint 示例前，先阅读本卡片。关键文件：`AGENTS.md`。

## Purpose / 用途

This file is also a public-safe example of a runtime `AGENTS.md`.

本文件同时也是一个可公开的 runtime `AGENTS.md` 示例。

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

## Do Not / 禁止

- Do not add real machine paths, private suite names, credentials, or internal
  URLs to this example.
- Do not imply that a parent `.codex` is automatically inherited by every child
  git repository.
- 不要把真实本机路径、私有 suite 名称、凭据或内部 URL 写入本示例。
- 不要暗示父级 `.codex` 会被每个子 git 仓库自动继承。
