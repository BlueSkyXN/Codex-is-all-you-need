# OpenClaw Skills

## 1. Product and sources

| Item | Value |
|---|---|
| Product | OpenClaw |
| Primary docs | https://docs.openclaw.ai/tools/skills |
| Open standard | Follows [AgentSkills](https://agentskills.io) |
| Registry | ClawHub (https://clawhub.ai) |
| Extracted | 2026-07-16 from public tools/skills docs |

OpenClaw uses the standard skill folder model, then adds **gating**,
**allowlists**, **ClawHub install**, **node-hosted skills**, and session
snapshots via `metadata.openclaw`.

## 2. What a skill is

A skill is a markdown instruction package that teaches an agent how and when to
use tools. Each skill is a directory with `SKILL.md` (YAML frontmatter + body).

OpenClaw loads bundled skills and local overrides, then filters eligibility by
environment, config, and binary presence.

## 3. Discovery paths and precedence

Highest precedence wins on name collision:

| Priority | Source | Path |
|---|---|---|
| 1 | Workspace | `<workspace>/skills` |
| 2 | Project agent | `<workspace>/.agents/skills` |
| 3 | Personal agent | `~/.agents/skills` |
| 4 | Managed/local | `~/.openclaw/skills` |
| 5 | Bundled | shipped with install |
| 6 | Extra / plugins | `skills.load.extraDirs` + plugin skill dirs |

Notes:

- Discovery finds `SKILL.md` up to **6 levels** under a root  
- Folder nesting is organizational; identity comes from frontmatter `name` (or directory name)  
- Codex CLI `$CODEX_HOME/skills` is **not** an OpenClaw root (migrate via `openclaw migrate …`)  
- Connected node skills can appear from the node’s skill dir; collisions may get node-prefixed names  

Visibility (who can see a skill) is separate from precedence and can be narrowed
by agent allowlists (`agents.defaults.skills`, `agents.list[].skills`).

## 4. Directory structure

Standard skill directory with `SKILL.md` at the skill root. Agent Skills-style
optional resources apply. Body may use `{baseDir}` for the skill folder path.

ClawHub installs may carry origin metadata such as `.clawhub/origin.json`.

## 5. `SKILL.md` and frontmatter

Minimum required (product docs): `name` and `description`.

```markdown
---
name: image-lab
description: Generate or edit images via a provider-backed image workflow
---

When the user asks to generate an image, use the `image_generate` tool...
```

Parsing notes:

- YAML first; fallback single-line-only parser  
- Nested `metadata` may be flattened/re-parsed as JSON5  

### Common optional fields

| Field | Default | Purpose |
|---|---|---|
| `homepage` | — | Website link in UI |
| `user-invocable` | `true` | Expose as slash command |
| `disable-model-invocation` | `false` | Keep body out of normal prompt; slash may still work |
| `command-dispatch` | — | `"tool"` bypasses model and dispatches a tool |
| `command-tool` | — | Tool name for tool dispatch |
| `command-arg-mode` | `raw` | Raw arg forwarding mode |

### `metadata.openclaw` gating extensions

Skills without `metadata.openclaw` are generally eligible unless disabled.

| Key | Purpose |
|---|---|
| `always` | Skip other gates when true |
| `emoji` | UI emoji |
| `homepage` | UI website |
| `os` | `darwin` / `linux` / `win32` filter |
| `requires.bins` | All binaries must be on `PATH` |
| `requires.anyBins` | At least one binary on `PATH` |
| `requires.env` | Required env vars |
| `requires.config` | Truthy `openclaw.json` paths |
| `primaryEnv` | Env key tied to `skills.entries.<name>.apiKey` |
| `install` | Installer specs for UI bootstrap |
| `skillKey` | Config key override under `skills.entries` |

Legacy `metadata.clawdbot` may still be accepted when `openclaw` is absent; new
skills should use `openclaw`.

## 6. Progressive disclosure / loading

- Eligible skills compile into a compact XML `<available_skills>`-style prompt block  
- Base overhead only when ≥1 skill is eligible  
- Per skill roughly ~97 chars + name/description/location lengths before tokenization effects  
- If over `skills.limits.maxSkillsPromptChars`, identities are preserved first; descriptions may be shortened/omitted  
- `disable-model-invocation: true` withholds body from normal prompt (slash-only style path)  
- Eligibility snapshot at session start; refresh on watcher / node / allowlist changes  

## 7. Supporting files

- Standard optional scripts/docs/assets under the skill directory  
- Use `{baseDir}` for portable relative references  
- Node-hosted skill binaries/resources execute on the node (`exec host=node …`)  
- Config overrides in `~/.openclaw/openclaw.json` under `skills.entries`:
  `enabled`, `apiKey`, `env`, `config`, plus bundled allowlisting controls  

## 8. Invocation

| Mode | Behavior |
|---|---|
| Model prompt list | Eligible skills summarized into system prompt block |
| Slash command | When `user-invocable` is true |
| Tool dispatch | `command-dispatch: tool` routes slash to a tool without model mediation |
| Agent allowlist | Restricts which skills are visible/buildable for an agent |

## 9. Packaging and distribution

ClawHub / CLI oriented:

```bash
openclaw skills install @owner/<slug>
openclaw skills install git:owner/repo@ref
openclaw skills install ./path --as my-tool
openclaw skills install ... --global    # shared managed dir
openclaw skills update --all
openclaw skills verify @owner/<slug>
```

Also:

- Plugin skill directories via `openclaw.plugin.json`  
- Skill Workshop for agent-drafted proposals with human apply  
- Private uploaded archives gated off by default  

## 10. Versioning

- No dedicated skill semver field emphasized on the skills page  
- ClawHub origin metadata can record registry/version identity  
- Prompt compaction may retain a version token under budget pressure  

Prefer Agent Skills `metadata.version` in-file if you need portable behavior
versioning.

## 11. Limits and constraints

| Topic | Rule |
|---|---|
| Discovery depth | Up to 6 levels under a skill root |
| Prompt budget | `skills.limits.maxSkillsPromptChars` (short descriptions recommended) |
| Allowlists | Empty agent list = no skills; non-empty replaces defaults (no merge) |
| Bin checks | Host `PATH`; sandboxes need bins inside container too |
| Symlinks | Realpath must stay in trusted roots unless allowlisted |
| Snapshots | Sticky for session unless refresh triggers |

## 12. Platform-specific extensions

OpenClaw-heavy surface area:

- `metadata.openclaw` eligibility gates and installers  
- Multi-root precedence including `.agents/skills` and `~/.openclaw/skills`  
- ClawHub install/verify/update  
- Node-hosted remote skills  
- Session skill snapshots + watcher hot refresh  
- `command-dispatch` tool short-circuit  

## 13. Security

Docs treat third-party skills as untrusted code:

- Read before enable; prefer sandbox for risky tools  
- Path containment for workspace/project/extra roots  
- Optional `security.installPolicy` (fail closed) before installs  
- Secrets via `skills.entries.*.env` / `apiKey` on host turn only—not in SKILL.md  
- Verify ClawHub packages; scanning integrations mentioned in ecosystem docs  

## 14. Authoring practices

1. Always set clear short `name` + compact `description`.  
2. Declare real gates (`requires.bins` / `env` / `os` / `config`).  
3. Prefer `metadata.openclaw` over legacy keys.  
4. Use `{baseDir}` for local file references.  
5. Place skills by intended visibility (workspace vs managed global vs plugin).  
6. Use `disable-model-invocation` for slash-only workflows.  
7. Never embed secrets in skill text.  
8. Keep descriptions short to survive prompt budgets.  
9. Human-review workshop proposals and third-party installs.

## 15. Extraction notes

- Primary source: https://docs.openclaw.ai/tools/skills  
- Strong on load gating and distribution; lighter on body-authoring templates.  
- Align frontmatter minimum with Agent Skills open standard for portability.

### Follow-up sources already identified

| Page | URL | Captured? |
|---|---|---|
| ClawHub skill format | https://docs.openclaw.ai/clawhub/skill-format | Partial (2026-07-16): publish limits, metadata schema, install kinds, MIT-0 policy |
| Creating skills | https://docs.openclaw.ai/tools/creating-skills | Partial: authoring workflow; description “under 160 chars” is product guidance, not open-standard max |
| Skills config | https://docs.openclaw.ai/tools/skills-config | Open |
| macOS skills UI | https://docs.openclaw.ai/platforms/mac/skills | Open |
| CLI skills | https://docs.openclaw.ai/cli/skills | Open |

ClawHub publish constraints worth remembering:

- text-based files only
- bundle ≤ **50MB**
- embedding text: `SKILL.md` + up to ~40 non-`.md` files
- install kinds include `brew` / `node` / `go` / `uv` (download appears on other pages)
- published skills under MIT-0 policy on ClawHub

See [RESEARCH-STATUS.md](RESEARCH-STATUS.md) for the full gap board.
