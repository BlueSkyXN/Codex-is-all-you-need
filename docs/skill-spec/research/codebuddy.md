# CodeBuddy Code Skills

## 1. Product and sources

| Item | Value |
|---|---|
| Product | CodeBuddy Code (Tencent Cloud coding assistant) |
| Primary docs | https://www.codebuddy.cn/docs/cli/skills |
| Shape affinity | Very close to Claude Code skills UX/fields |
| WorkBuddy note | Site nav mentions WorkBuddy surfaces; **this page does not define a separate WorkBuddy skill API**. Local WorkBuddy evidence is now captured in [workbuddy.md](workbuddy.md) (app-bundled creators + `~/.workbuddy`). |
| Extracted | 2026-07-16 from public CLI skills docs; WorkBuddy cross-link updated 2026-07-17 |

## 2. What a skill is

Skills package domain expertise and workflow templates so the assistant can
handle specialized tasks more reliably. Compared with slash commands:

| | Skills | Slash commands |
|---|---|---|
| Trigger | Model auto-select | User types command |
| Focus | Domain specialist work | Shortcuts / workflows |
| Permissions | Tool allowlists | No special ACL |
| Working dir | Skill base directory supported | Current working directory |
| Visibility | Often transparent | User-initiated |

## 3. Discovery paths and precedence

| Scope | Path |
|---|---|
| Project | `.codebuddy/skills/` |
| User | `~/.codebuddy/skills/` |
| Plugin | Plugin-shipped skills (shown as Plugin skills in `/skills`) |

One directory per skill, each with `SKILL.md`.

Name collisions: **project overrides user**.

`/skills` lists User / Project / Plugin skills and approximate token cost.

## 4. Directory structure

```text
.codebuddy/skills/
├── pdf/SKILL.md
├── data-analysis/SKILL.md
└── code-review/SKILL.md
```

Supporting scripts/assets live under the skill directory and are referenced with
`${CODEBUDDY_SKILL_DIR}` (Claude aliases also accepted).

## 5. `SKILL.md` and frontmatter

Markdown body + optional YAML frontmatter.

```markdown
---
name: pdf
description: PDF 文档处理专家
allowed-tools: Read, Write, Bash, WebFetch
---

You are a PDF specialist...
```

### Frontmatter fields

| Field | Required | Purpose |
|---|---|---|
| `name` | No | Skill id; defaults to directory name |
| `description` | No | Model selection / trigger text |
| `allowed-tools` | No | Tool allowlist (comma-separated in examples; patterns like `Bash(git:*)`) |
| `disable-model-invocation` | No | `true` → manual `/skill-name` only |
| `user-invocable` | No | `false` → hide from `/` menu (default `true`) |
| `context` | No | `fork` → isolated subagent |
| `agent` | No | Subagent type when forked |
| `model` | No | Model override for forked run |
| `hooks` | No | Skill-scoped hooks; **only with `context: fork`** (beta) |

### Placeholders

| Token | Meaning |
|---|---|
| `${CODEBUDDY_SKILL_DIR}` | Absolute directory of this `SKILL.md` |
| `${CODEBUDDY_PLUGIN_ROOT}` | Plugin install root (plugin skills only) |
| `${CODEBUDDY_SESSION_ID}` | Session id |
| `${ENV}` / `${ENV:-default}` | Environment variables |
| Claude aliases | `${CLAUDE_SKILL_DIR}`, `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_SESSION_ID}` accepted |
| `$ARGUMENTS` | Invocation arguments in shell snippets |

Inline shell uses `` !`command` `` (same pipeline family as slash commands).

## 6. Progressive disclosure / loading

The page does **not** formalize the three-stage Agent Skills loading model as
explicitly as Claude/agentskills.io. Closest controls:

- Auto vs manual invocation (`disable-model-invocation`)  
- Menu visibility (`user-invocable`)  
- `/skills` token-size visibility  

In practice, author as if progressive disclosure still matters: short entry
`SKILL.md`, optional supporting files under the skill dir.

## 7. Supporting files

- Scripts/assets under skill directory  
- Hook scripts for fork skills  
- Custom agents under `.codebuddy/agents/` for `context: fork`  
- `@file` references after shell expansion (large files may remain refs)  

## 8. Invocation

1. **Automatic** — model matches task to description/tools/context  
2. **Manual** — `/skill-name` unless hidden  
3. **Slash bridge** — commands can instruct use of a skill  
4. **Inspect** — `/skills`  

Fork mode (`context: fork`):

- New isolated context (no main chat history)  
- Skill body becomes subagent task prompt  
- Agents: `general-purpose` (default), `Explore`, `Plan`, or custom  
- Best for concrete tasks, not pure guideline dumps  

## 9. Packaging and distribution

- Project/user directories for direct authoring  
- Plugin packaging for distribution (`Plugin skills` in `/skills`)  
- Plugin hooks via `hooks/hooks.json` are a separate channel from skill frontmatter hooks  

No separate marketplace upload schema is fully specified on this page.

## 10. Versioning

No dedicated skill version field documented on the skills page. Use git and/or
Agent Skills `metadata.version` if you need portable versioning.

## 11. Limits and constraints

Documented behavioral constraints:

- One skill = one directory + `SKILL.md`  
- `agent` / `model` / frontmatter `hooks` meaningful mainly with `context: fork`  
- Non-fork skills may parse hooks but not register them  
- Project name wins over user name  
- Frontmatter hooks from non-builtin skills require trust setting  

Hard numeric body/description caps are not emphasized on this page; for
portability, use Agent Skills limits (name 64, description 1024).

## 12. Platform-specific extensions

CodeBuddy-specific / Claude-like extensions:

- `allowed-tools` patterns  
- `context: fork` + `agent` + `model`  
- Frontmatter `hooks` with admin trust gate  
- `${CODEBUDDY_*}` placeholders (+ Claude aliases)  
- Inline `` !`command` `` preprocessing  
- Plugin root vs skill dir variables  

### Hooks trust note

Non-builtin skill/agent frontmatter hooks need:

```json
{ "allowUntrustedFrontmatterHooks": true }
```

in user settings, or they are skipped with a warning. Product-bundled skills can
bypass the gate. `Stop` rewrites to `SubagentStop` in fork lifecycle.

## 13. Security

- Prefer narrow `allowed-tools` over open `Bash`  
- Treat frontmatter hooks as potentially executable untrusted code  
- Use PreToolUse path guards in fork review skills  
- Plugin `hooks/hooks.json` is not controlled by the same untrusted-frontmatter flag  

## 14. Authoring practices

1. Write specific descriptions (who/what/when), not vague “handle files”.  
2. Body: capabilities, workflow, tools, edge cases, output shape.  
3. Least-privilege tool allowlists.  
4. Group skills by domain directories if helpful.  
5. `user-invocable: false` for background standards knowledge.  
6. Fork only when isolation helps and the task is concrete.  
7. Debug with `/skills` (load + token view).  
8. Compose with Memory / slash commands / allowlisted MCP tools.

## 15. Extraction notes

- Primary source: https://www.codebuddy.cn/docs/cli/skills  
- Field model is largely Claude-compatible.  
- **WorkBuddy** shares CodeBuddy packaging DNA (`.codebuddy-plugin`, creator text
  still says CodeBuddy paths) but has its own config root (`~/.workbuddy`) and an
  expert-package layer. See [workbuddy.md](workbuddy.md).  
- Progressive disclosure is implied more than specified on the CLI page; WorkBuddy’s
  bundled `skill-creator` states the three-level model explicitly.
