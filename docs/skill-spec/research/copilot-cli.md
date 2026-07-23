# GitHub Copilot CLI Skills / Plugins / Agents

## 1. Product and sources

| Item | Value |
|---|---|
| Product | GitHub Copilot CLI (`copilot`) |
| User config root | `~/.copilot` (not `.copilotcli`) |
| Binary sample | `/opt/homebrew/bin/copilot` |
| Local package root | `~/.copilot/pkg/darwin-arm64/<version>/` |
| Extracted | 2026-07-17 from a versioned local install + sanitized user-layout observations |
| Public docs | Product docs exist for cloud-agent customization; local CLI packaging is partly inferred from install layout |

This extract covers **local CLI extensibility paths** observed on disk:

- Skills
- Plugins
- Agents (user markdown + bundled YAML definitions)

It does **not** fully freeze every public schema page; treat YAML/JSON field lists as
observed-product evidence.

## 2. What a skill / plugin / agent is

| Unit | Meaning in Copilot CLI |
|---|---|
| Skill | Agent Skills-shaped directory with `SKILL.md` (workflow/domain package) |
| Plugin | Installable extension package (`plugin.json`) that can ship commands/hooks/skills/agents |
| Agent | Specialized subagent definition (user `.md` and/or bundled `.agent.yaml`) |

Conceptual split is closer to Claude/Codex developer tooling than WorkBuddy/QoderWork’s
“专家 / 角色套件” business packaging.

## 3. Discovery paths and precedence

| Scope | Path | Notes |
|---|---|---|
| User skills | `~/.copilot/skills/<name>/` | Live user skills root |
| User agents | `~/.copilot/agents/*.md` | Markdown agent defs with YAML frontmatter |
| User plugins | `~/.copilot/plugins/` | Local plugin checkouts / projects |
| Installed plugins | `~/.copilot/installed-plugins/` | Includes `_direct/` installs |
| Bundled skills | `~/.copilot/pkg/.../builtin-skills/` | Versioned with CLI package |
| Bundled agents | `~/.copilot/pkg/.../definitions/*.agent.yaml` | First-party subagents |
| Repo / shared discovery (interop) | `.agents/skills`, `.claude/skills`, `.github/skills` | Copilot participates in multi-root skill discovery in the broader ecosystem; exact precedence needs runtime matrix |

Creation UX (product commands, from path survey):

- `/plugin` scaffolds plugin packages
- `/agents` scaffolds agent definitions

## 4. Directory structure

### Skill

```text
~/.copilot/skills/<skill-name>/
├── SKILL.md
└── ... optional resources
```

A sanitized layout survey confirmed that public/bundled and user-authored packs
can coexist under this root; installation-specific identifiers are omitted.

### Plugin

Observed direct-install shape:

```text
installed-plugins/_direct/
├── plugin.json
├── hooks.json
├── commands/            # if declared
├── scripts/
└── ...
```

Sanitized user-plugin workspace shape:

```text
~/.copilot/plugins/<plugin-name>/
```

### Agent

Two coexisting formats:

```text
# User-authored markdown agents
~/.copilot/agents/<agent-name>.md
...

# Bundled YAML agents (versioned package)
~/.copilot/pkg/darwin-arm64/<ver>/definitions/
  <bundled-agent>.agent.yaml
```

## 5. `SKILL.md` and frontmatter

Copilot skills follow the Agent Skills core:

```yaml
---
name: failure-recovery
description: "Use when a task has failed repeatedly and needs structured recovery."
---
```

Bundled skill sample also uses Claude-like invocation control:

```yaml
---
name: customize-cloud-agent
description: >-
  Skill for customizing the Copilot cloud agent ...
user-invocable: false
---
```

Implications for portable authors:

- Keep `name` + `description` as the portable minimum
- Claude-style fields such as `user-invocable` may appear and should remain optional adapters
- No Copilot-only sidecar equivalent to Codex `agents/openai.yaml` was required in local samples

## 6. Progressive disclosure / loading

No separate first-party progressive-disclosure doctrine file was extracted from the CLI
package in this pass. Practical model still matches Agent Skills:

1. Metadata for discovery
2. Body when selected
3. Optional resources/scripts as needed

Bundled `customize-cloud-agent` is a long instructional skill about cloud environment
setup (GitHub Actions `copilot-setup-steps.yml`), i.e. docs-as-skill rather than a tiny
router skill.

## 7. Supporting files

| Area | Observed |
|---|---|
| Skill resources | Optional files beside `SKILL.md` (same family as other Agent Skills clients) |
| Plugin hooks | `hooks.json` + scripts |
| Plugin commands | Directory referenced by `plugin.json` `commands` |
| Agent prompts | Inline in markdown body or YAML `prompt` / `promptParts` |

## 8. Invocation

| Mode | How |
|---|---|
| Skill auto | Model matches descriptions |
| Skill manual | Product skill/slash surfaces (where enabled) |
| Agent | `/agents` management + runtime subagent dispatch |
| Plugin | Install/enable plugin, then use its commands/hooks/skills |

Bundled agents are task-specialized subagents, typically orchestrated by the main
agent; their installation-specific identifiers are omitted here.

## 9. Packaging and distribution

### Plugin manifest (`plugin.json`) observed fields

From `installed-plugins/_direct/plugin.json`:

| Field | Example / role |
|---|---|
| `name` | `example-plugin` |
| `description` | one-line summary |
| `version` | semver |
| `author` | `{name}` |
| `license` | e.g. MIT |
| `keywords` | search tags |
| `category` | e.g. `productivity` |
| `commands` | path, e.g. `commands/` |
| `hooks` | path, e.g. `hooks.json` |

Path-survey notes also indicate plugin spec support for `skills`, `agents`,
`extensions` in broader packaging (not all present in the observed sample).

### Marketplace interop note

Cross-ecosystem experiments in this repo’s history show Copilot CLI can consume
Claude-style marketplace/plugin manifests in practice (`.claude-plugin/`), while also
understanding Codex-like `.agents` roots. Treat dual-manifest publishing as an
**interop strategy**, not proof that every Copilot release only has one canonical
manifest directory.

## 10. Versioning

- CLI package version appears in `~/.copilot/pkg/darwin-arm64/<version>/`
- Plugin `version` is semver in `plugin.json`
- Skill-level version field not required in local samples; portable packs may still use
  Agent Skills `metadata.version`

## 11. Limits and constraints

Documented hard caps were not fully extracted from local package schemas in this pass.
Practical constraints observed:

- Skills are directory packages centered on `SKILL.md`
- User agents are markdown files under `~/.copilot/agents/`
- Bundled agents use a richer YAML schema and ship inside versioned CLI packages
- Plugin installs can be direct (`installed-plugins/_direct`) or marketplace-mediated

For portable limits, fall back to Agent Skills (`name` ≤ 64, `description` ≤ 1024).

## 12. Platform-specific extensions

### User agent markdown frontmatter (sanitized observed shape)

```yaml
---
name: example-reviewer
description: "Use this agent when a structured review is required."
tools: Read, Write, Edit, Bash, Glob, Grep
model: example-model
---
```

Notes:

- `tools` may be declared on user agents (contrast WorkBuddy expert agent MD, which forbids `tools`)
- `model` can pin a model alias
- Body is freeform operating instructions (Chinese/English both observed)

### Bundled `.agent.yaml` (observed keys)

From a sanitized `definitions/<bundled-agent>.agent.yaml` shape:

| Key | Role |
|---|---|
| `name` | id |
| `displayName` | UI label |
| `description` | when/what |
| `model` | concrete model id |
| `tools` | allowlist (supports `github/...` MCP short names, local tools) |
| `promptParts` | flags: safety / tool instructions / parallel tool calling / custom agent instructions |
| `prompt` | full system/task prompt with `{{cwd}}` templating |

This YAML format is **Copilot-package-native** and richer than plain user markdown agents.

### Skill frontmatter adapters

- Claude-like `user-invocable` observed on bundled skill
- No mandatory Copilot-only sidecar found for ordinary skills

## 13. Security

- Review third-party skills/plugins before install
- Plugin hooks/scripts are executable automation surfaces
- Bundled research agents intentionally constrain GitHub search rate behavior in prompt text
- Cloud-agent customization skill documents environment/firewall setup outside local CLI

## 14. Authoring practices

1. Write portable skills as Agent Skills directories; they drop into `~/.copilot/skills/`.
2. Use Claude-compatible optional fields only when needed (`user-invocable`, etc.).
3. Prefer markdown agents under `~/.copilot/agents/` for simple custom specialists.
4. Use plugin packages when shipping commands/hooks together with skills/agents.
5. Do not assume user-agent `tools:` syntax is portable to WorkBuddy/Claude/Codex without adaptation.
6. For multi-ecosystem distribution, dual thin manifests + shared `skills/` remains the practical pattern.

## 15. Extraction notes

- Source of truth for this pass is **local CLI install layout**, not a complete public packaging whitepaper.
- Copilot CLI is clearly in the “developer subagent + plugin” family with Claude/Codex, not the “业务专家包” family with WorkBuddy/QoderWork.
- Confidence:
  - Skill path + Agent Skills shape: **High**
  - User agent markdown fields: **High** (multiple samples)
  - Bundled `.agent.yaml` richness: **High** (package definitions)
  - Complete official plugin schema / precedence matrix: **Medium / open**
  - Cross-runtime marketplace behavior: **Medium** (prior interop experiments + local manifests)
