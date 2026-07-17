# Qoder / QoderWork Skills

## 1. Product and sources

| Item | Value |
|---|---|
| Product | Qoder (IDE + CLI) and QoderWork / QoderWork CN (desktop agent workbench) |
| Overview page | https://docs.qoder.com/extensions/skills |
| CLI deep-dive | https://docs.qoder.com/en/cli/Skills |
| Ecosystem pointers | skills.sh , community skill repos, `/create-skill` |
| Local QoderWork CN root | `~/.qoderworkcn` (parallel non-CN root also seen: `~/.qoderwork`) |
| Extracted | 2026-07-16 public docs; **2026-07-17 local QoderWork CN creators/plugins** |

The overview page is thin; the CLI Skills page supplies the portable authoring
format used below. QoderWork CN adds first-party **conversation creators** and a
**role-plugin** packaging layer that public CLI docs barely cover.

## 2. What a skill is

A skill packages domain expertise into a reusable capability for Qoder IDE/CLI.
Each skill is a folder with required `SKILL.md` (description + instructions +
optional supporting files).

Skills are modular: one skill ≈ one task type.

## 3. Discovery paths and precedence

### Qoder IDE / CLI (public docs)

| Scope | Path | Visibility |
|---|---|---|
| User | `~/.qoder/skills/{skill-name}/SKILL.md` | All projects for that user |
| Project | `.qoder/skills/{skill-name}/SKILL.md` | Current project |

Conflict handling differs slightly across pages:

- Overview-style docs often say **project wins**  
- CLI deep-dive extract noted **user wins** on collision  

Treat collision behavior as **verify on your installed Qoder version** before
relying on it in automation. After manual adds, restart IDE or `/skills reload`
as documented for the surface you use.

### QoderWork / QoderWork CN (local evidence, 2026-07-17)

| Scope | Path | Notes |
|---|---|---|
| User skills | `~/.qoderworkcn/skills/` | Live root; contains `create-skill`, `plugin-creator`, many domain skills |
| Parallel root | `~/.qoderwork/skills/` | Non-CN install mirror (same shape) |
| Plugins (role suites) | `~/.qoderworkcn/plugins/<角色名>/` | e.g. `产品管理/`, `市场营销/`, `data/` |
| Custom plugin staging | `~/.qoderworkcn/plugins-custom/` | Empty/custom staging area |
| Slash commands | `~/.qoderworkcn/commands/` | includes `create-command.md` |

`create-skill` templates paths with `~/{{.DataDirName}}/skills/` (host) or
`/root/{{.DataDirName}}/skills/` (VM/container). On this machine `DataDirName`
resolves to `qoderworkcn`.

## 4. Directory structure

From CLI deep-dive:

```text
{skill-name}/
├── SKILL.md          # required
├── REFERENCE.md      # optional
├── EXAMPLES.md       # optional
├── scripts/          # optional helpers
└── templates/        # optional templates
```

This is compatible in spirit with Agent Skills (`scripts/` + on-demand docs),
though directory names are not forced to `references/` / `assets/`.

## 5. `SKILL.md` and frontmatter

YAML frontmatter + Markdown body.

### Frontmatter (CLI docs / portable core)

| Field | Required | Rules |
|---|---|---|
| `name` | Yes | Unique id; lowercase letters, numbers, hyphens; max **64** chars |
| `description` | Yes | What + when / trigger keywords; max **1024** chars |

Minimal skeleton:

```markdown
---
name: skill-name
description: Brief description of functionality and when to use
---

# Skill Name

## Instructions
Provide clear step-by-step guidance.

## Examples
Show specific usage examples.
```

Overview page does not redefine schema and defers to fuller docs / `/create-skill`.

### QoderWork CN extensions (local plugin skills)

Role-suite skills on this machine commonly add bilingual / UX fields beyond the
portable minimum:

| Field | Role |
|---|---|
| `name` | **May be Chinese** in plugin UI skills (e.g. `PRD生成`, `营销文案`) |
| `description` | Chinese trigger-rich description |
| `name_en` / `description_en` | English mirrors for bilingual packs |
| `displayName` | Optional UI label (seen on some skills) |
| `argument-hint` | Slash/arg autocomplete hint |
| `version` | Present on creator skills themselves (`create-skill`, `plugin-creator`) |
| `description_zh` | Present on creator skills |

This is an important product divergence:

- Public CLI docs emphasize kebab-case English `name`
- QoderWork `plugin-creator` **requires** skill directory name and `SKILL.md`
  `name` to match the **user’s language** for UI display (Chinese for CN users)

Portable multi-runtime packs should still prefer ASCII kebab-case `name` unless
the pack is QoderWork-UI-first.

## 6. Progressive disclosure / loading

CLI docs encourage keeping `SKILL.md` as entrypoint and pointing to extra files
only when needed:

```markdown
For details, see [REFERENCE.md](REFERENCE.md).
For examples, see [EXAMPLES.md](EXAMPLES.md).
Run: python scripts/helper.py input.txt
```

Load lifecycle (CLI):

- New sessions load skills at startup  
- Running CLI may need `/skills reload` after edits  
- List via `/skills` or natural-language “What Skills are available?”  

## 7. Supporting files

Optional:

- `REFERENCE.md`, `EXAMPLES.md` (or similarly named guides)  
- `scripts/` helpers (may need `chmod +x`)  
- `templates/`  

Dependencies can be declared in description or a Requirements section; CLI may
install or request permission.

## 8. Invocation

| Mode | How |
|---|---|
| Automatic | Model matches user intent to skill descriptions |
| Manual | `/skill-name` |
| Discovery | `/` menu / `/skills` |
| Scaffold | `/create-skill`, `/create-skill-ui` |

Skills vs commands (as documented):

| | Skill | Command |
|---|---|---|
| Trigger | Auto or `/skill-name` | Explicit `/command-name` |
| Best for | Domain multi-step expertise | Quick presets |
| Storage | `skills/` | `commands/` |

Internally, skills may map to a special command type sharing a runner.

## 9. Packaging and distribution

### Skills

Ways to obtain skills:

1. `/create-skill <description>` guided scaffold (Qoder) / local `create-skill` skill (QoderWork)  
2. CLI install examples:
   - `npx skills add vercel-labs/agent-browser -a qoder`
   - `npx skills add https://github.com/anthropics/skills --skill skill-creator -a qoder`
3. Hand-authored directories under user/project paths  
4. `/create-skill-ui` for interactive HTML widgets in chat  
5. Bundle many skills into a QoderWork **role plugin** via `plugin-creator`

### QoderWork plugins (role toolkits)

`plugin-creator` (local v1.7.1) defines a plugin as **not** a single skill, but a
role/industry toolkit:

- Skill = one tool (e.g. “draft a contract”)
- Plugin = full toolbox for a role (e.g. “法务助手”)

Observed plugin layout:

```text
~/.qoderworkcn/plugins/产品管理/
├── .qoder-plugin/plugin.json
├── .mcp.json
├── skills/
│   ├── PRD生成/SKILL.md
│   ├── 用户故事拆解/SKILL.md
│   └── ...
├── README.md
├── README_EN.md
└── CONNECTORS.md
```

Observed `plugin.json` fields:

| Field | Example / notes |
|---|---|
| `name` | English kebab-case internal id (`product-management`) |
| `displayName` | User-language UI name (`产品管理`) |
| `displayNameEn` | English display |
| `version` | semver |
| `description` / `descriptionEn` | long bilingual capability blurb |
| `author` | `{name}` |
| `keywords` | Chinese/English search tags |

MCP / connectors are first-class in the creator workflow (market connectors +
user custom connectors), but product copy intentionally hides file-level
`.mcp.json` mechanics from end users.
## 10. Versioning

No first-class version field required. Docs suggest optional version history
sections in Markdown body. For portable packs, use Agent Skills
`metadata.version`.

## 11. Limits and constraints

| Topic | Documented |
|---|---|
| `name` | ≤ 64, kebab-style |
| `description` | ≤ 1024 |
| Name collision | Resolve by scope precedence (verify product version) |
| Other hard limits | Not emphasized (size/count/signing not fully specified on these pages) |

## 12. Platform-specific extensions

Qoder / QoderWork ergonomics:

- `/create-skill` and `/create-skill-ui` (Qoder surfaces)  
- Local conversation creators: `create-skill`, `plugin-creator`, `create-command`  
- `npx skills add … -a qoder` installer path  
- Built-in helpers cited on overview (`/vercel-deploy`, `/create-subagent`, `/canvas`, …)  
- Optional `templates/` directory naming in examples  
- QoderWork plugin manifest dir: **`.qoder-plugin/`**  
- Bilingual skill metadata (`name_en`, `description_en`, `description_zh`)  
- UI-first Chinese skill names inside role plugins  
- Connector/MCP packaging beside skills (`.mcp.json`, `CONNECTORS.md`)  

No Claude-style `context: fork` / OpenClaw `metadata.openclaw` block appears in
the extracted public pages. QoderWork also has **no independent subagent/team
framework** comparable to Claude teams / Codex suites / WorkBuddy experts; “agent”
is approximated by role plugins + skills.

## 13. Security

Pages are light on security policy. Practical baseline still applies:

- Review third-party installed skills before use  
- Treat `scripts/` as executable code  
- Be careful with dependency auto-install prompts  

## 14. Authoring practices

1. One domain per skill.  
2. Specific descriptions with real trigger phrases.  
3. Prefer `/create-skill` if format is unfamiliar, then edit.  
4. Put long material in `REFERENCE.md` / `EXAMPLES.md` / `scripts/`.  
5. Test auto-trigger and edge cases before sharing.  
6. If skill never triggers: check path, YAML syntax, description specificity.  
7. If skills conflict: differentiate trigger terms in descriptions.

## 15. Extraction notes

- Combined from:
  - https://docs.qoder.com/extensions/skills (overview, thinner)
  - https://docs.qoder.com/en/cli/Skills (authoring format)
  - local QoderWork CN creators/plugins under `~/.qoderworkcn` (2026-07-17)
- Some overview vs CLI details (especially name-collision precedence) should be
  re-verified against the installed product if automation depends on it.
- Distinguish surfaces when citing paths:
  - **Qoder IDE/CLI docs** → `~/.qoder` / `.qoder`
  - **QoderWork CN local** → `~/.qoderworkcn` (and optional `~/.qoderwork`)
- Overall portable skill shape is Agent Skills-compatible.
- QoderWork’s distinctive layer is **role plugins + bilingual UI naming + connectors**,
  not a deep frontmatter runtime field set like Claude/CodeBuddy.
- Confidence:
  - Portable `name`/`description` skill core: **High**
  - QoderWork plugin layout / creator doctrine: **High** (local first-party skills)
  - Name-collision precedence across all surfaces: still **Open / runtime needed**
