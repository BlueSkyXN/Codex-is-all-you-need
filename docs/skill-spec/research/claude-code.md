# Claude Code Skills

## 1. Product and sources

| Item | Value |
|---|---|
| Product | Claude Code |
| Primary docs | https://code.claude.com/docs/zh-CN/skills |
| Open standard | Declares compatibility with [Agent Skills](https://agentskills.io) |
| Related | Plugins, subagents, hooks, skill-creator plugin, agentskills.io evals |
| Extracted | 2026-07-16 from public Chinese docs page |

Claude Code **extends** Agent Skills with invocation control, subagent execution,
dynamic context injection, permissions, and plugin packaging.

## 2. What a skill is

A skill is a directory with `SKILL.md` instructions that extend Claude’s toolkit.

- Claude may auto-load a skill when relevant
- Users may invoke `/skill-name` directly
- Custom slash commands (`.claude/commands/*.md`) are merged into the skills model;
  skills add supporting files, invocation control, and auto-loading

Create a skill when you repeatedly paste the same procedure, or when `CLAUDE.md`
content has become a multi-step procedure rather than durable project facts.
Unlike `CLAUDE.md`, skill body loads **only when used**.

## 3. Discovery paths and precedence

| Scope | Path | Audience |
|---|---|---|
| Enterprise / managed | Managed settings paths | Org-wide |
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` | All of your projects |
| Project | `.claude/skills/<skill-name>/SKILL.md` | This repo |
| Plugin | `<plugin>/skills/<skill-name>/SKILL.md` | Where plugin is enabled |
| Nested monorepo | Nested `.claude/skills/` under packages | On-demand when editing that subtree |
| Additional dirs | `--add-dir` / `/add-dir` then `.claude/skills/` | Exception: skills load from added dirs |

**Name conflict precedence (same name):**

1. Enterprise overrides personal  
2. Personal overrides project  
3. Any of the above can override a bundled skill of the same name  
4. Plugin skills use `plugin-name:skill-name` namespace (no clash with plain names)  
5. If skill and `.claude/commands/` share a name, **skill wins**

Nested skills with the same basename stay available under qualified names such as
`/apps/web:deploy`.

Live change detection watches personal/project/`--add-dir` skill trees for
`SKILL.md` edits without restart (new top-level skill roots may need restart).
Plugin non-SKILL components may need `/reload-plugins`.

## 4. Directory structure

```text
my-skill/
├── SKILL.md           # required entry
├── template.md        # optional
├── examples/
│   └── sample.md
└── scripts/
    └── validate.sh
```

Docs also show sibling reference files (`reference.md`, `examples.md`) and
`scripts/` helpers. Supporting files are optional.

## 5. `SKILL.md` and frontmatter

Frontmatter is YAML between `---` markers; body is Markdown instructions.

Claude docs state many fields are optional at product level, but the open Agent
Skills standard still treats `name`/`description` as required for portable
skills. Claude recommends `description` so auto-selection works.

### Frontmatter fields (Claude Code)

| Field | Required | Description |
|---|---|---|
| `name` | No (product) | Display name in skill list; defaults to directory name. Usually does **not** change `/` command name except plugin-root `SKILL.md`. |
| `description` | Recommended | What + when. If omitted, first Markdown paragraph may be used. Combined with `when_to_use`, listing text truncated to **1536** chars. |
| `when_to_use` | No | Extra trigger context; appended to listing description; counts toward 1536-char cap |
| `argument-hint` | No | Autocomplete hint for args, e.g. `[issue-number]` |
| `arguments` | No | Named positional args for `$name` substitution |
| `disable-model-invocation` | No | `true` → user-only `/` invoke; not auto-loaded; not preloaded into subagents; default `false` |
| `user-invocable` | No | `false` → hide from `/` menu; default `true` |
| `allowed-tools` | No | Tools usable without prompting while skill active (space-separated or YAML list) |
| `disallowed-tools` | No | Remove tools from pool while skill active |
| `model` | No | Model override for current skill turn |
| `effort` | No | `low` / `medium` / `high` / `xhigh` / `max` |
| `context` | No | `fork` → run in forked subagent |
| `agent` | No | Subagent type when forked (`Explore`, `Plan`, `general-purpose`, custom) |
| `hooks` | No | Skill-lifecycle hooks |
| `paths` | No | Glob(s); auto-activate only when matching files are in play |
| `shell` | No | `bash` (default) or `powershell` for `!` command blocks |

### Command name rules

| Location | `/` command name comes from |
|---|---|
| `~/.claude/skills/<dir>/` or project `.claude/skills/<dir>/` | Directory name |
| Nested conflicting skill | Path-qualified name, e.g. `apps/web:deploy` |
| `.claude/commands/foo.md` | File basename |
| Plugin `skills/<dir>/` | `plugin:dir` |
| Plugin root `SKILL.md` | Frontmatter `name`, else plugin directory name |

### String substitutions

| Token | Meaning |
|---|---|
| `$ARGUMENTS` | All args |
| `$ARGUMENTS[N]` / `$N` | Positional arg |
| `$name` | Named arg from `arguments` |
| `${CLAUDE_SESSION_ID}` | Session id |
| `${CLAUDE_EFFORT}` | Effort level |
| `${CLAUDE_SKILL_DIR}` | Skill directory (plugin skill subdir, not plugin root) |
| `${CLAUDE_PROJECT_DIR}` | Project root (v2.1.196+) |

### Dynamic context injection

`` !`command` `` (and fenced ` ```! ` blocks) run **before** Claude sees the skill
text; stdout replaces the placeholder. Not model-executed tool use.

## 6. Progressive disclosure / loading

1. Skill **names/descriptions** enter context so Claude knows what exists  
2. Full `SKILL.md` loads on invoke  
3. Supporting files load when referenced/needed  

Lifecycle notes:

- Rendered skill content stays in the session after invoke  
- Re-invoke with identical rendered content may only note “already loaded”  
- On auto-compact, recent skill invocations are reattached with budgets  
  (per-skill keep front portion; combined reattach budget documented as 25k tokens)  
- Description listing budget scales with model context (default about 1%); per-entry
  description+when_to_use cap **1536** chars  

Guidance: keep `SKILL.md` under **500 lines**.

## 7. Supporting files

From `SKILL.md`, link what each file is and when to read it:

```markdown
- For API details, see [reference.md](reference.md)
- For examples, see [examples.md](examples.md)
```

Scripts are executed, not necessarily fully loaded as prose.

Optional eval assets (via skill-creator workflow): `evals/evals.json`, grading
outputs, benchmarks.

## 8. Invocation

| Mode | How |
|---|---|
| Automatic | Model matches user request to description |
| Manual | `/skill-name` and optional args |
| Stacked | Multiple `/skills` in one message (version-dependent limits) |
| Forked | `context: fork` runs skill as subagent task prompt |
| Visibility override | `settings.skillOverrides`: `on` / `name-only` / `user-invocable-only` / `off` |

Invocation matrix:

| Frontmatter | User `/` | Model auto | Description always listed? |
|---|---|---|---|
| default | yes | yes | yes |
| `disable-model-invocation: true` | yes | no | no |
| `user-invocable: false` | no | yes | yes |

## 9. Packaging and distribution

- Commit project skills under `.claude/skills/`
- Ship via Claude **plugins** (`skills/` inside plugin)
- Org-wide via managed settings
- Skill folder may include `.claude-plugin/plugin.json` to behave as a mini-plugin

## 10. Versioning

No first-class skill semver field in the Claude skills page. Practical options:

- Git history of the skill directory
- Optional `metadata.version` from Agent Skills open standard
- Plugin package version if distributed as a plugin

## 11. Limits and constraints

| Topic | Documented guidance / limit |
|---|---|
| `SKILL.md` length | Keep under **500 lines** |
| Description listing entry | `description` + `when_to_use` truncated to **1536** chars |
| Listing budget | ~1% of model context by default; configurable |
| Compact reattach | Front 5000 tokens per skill; 25000 combined budget (as documented) |
| Open standard name/description | Still apply for portable skills (64 / 1024) |

## 12. Platform-specific extensions

Claude-specific power features:

- `disable-model-invocation` / `user-invocable`
- `allowed-tools` / `disallowed-tools`
- `context: fork` + `agent`
- `!` dynamic shell injection
- `paths` gated activation
- `hooks`, `model`, `effort`
- `skillOverrides` in settings
- Bundled skills (`/doctor`, `/code-review`, `/verify`, …)
- skill-creator evaluation loop

## 13. Security

- Project skills with `allowed-tools` take effect after workspace trust acceptance  
- Review project skills before trust; they can grant broad tool access  
- Permission rules can allow/deny `Skill` tool or named skills  
- `disableSkillShellExecution` can block `!` command expansion from untrusted sources  
- Treat third-party/plugin skills as code

## 14. Authoring practices

1. Put trigger keywords in `description` (and `when_to_use` if needed).  
2. Write actions, not essays; body stays in session after load.  
3. Split detail into supporting files; stay under 500 lines.  
4. Use `disable-model-invocation: true` for side-effect workflows (deploy/commit).  
5. Use `user-invocable: false` for background knowledge that is not a user command.  
6. Reference scripts with `${CLAUDE_SKILL_DIR}`.  
7. Measure trigger quality and output quality separately (skill-creator / evals).  
8. Fix “never triggers” by improving description keywords; fix “over-triggers” by
   narrowing description or disabling model invocation.

## 15. Extraction notes

- Primary source: https://code.claude.com/docs/zh-CN/skills  
- Page is detailed; this note compresses tables and rules for comparison.  
- Subpages (plugins reference, hooks, best practices, agentskills eval format)
  were not fully re-ingested here—follow upstream links for those subsystems.
