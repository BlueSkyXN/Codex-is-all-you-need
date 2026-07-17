# WorkBuddy Skills / Experts

## 1. Product and sources

| Item | Value |
|---|---|
| Product | WorkBuddy (desktop agent; shares CodeBuddy packaging DNA) |
| Config root | `$WORKBUDDY_CONFIG_DIR` if set, else `~/.workbuddy` |
| Public package spec | Still **no stable first-party web authoring page** comparable to Claude/Codex |
| First-party local evidence | WorkBuddy.app bundled `builtin-skills/` (verified 2026-07-17) |
| Related product | CodeBuddy CLI docs describe a Claude-like skill surface; WorkBuddy reuses `.codebuddy-plugin` names and often CodeBuddy wording inside creators |
| Extracted | 2026-07-17 from local app package + local install samples |

Primary local sources:

```text
WorkBuddy.app/.../resources/builtin-skills/
  skill-creator/
  expert-manager/
  marketplace-skill-installer/
```

Local user data:

```text
~/.workbuddy/skills/
~/.workbuddy/plugins/marketplaces/
```

> Status note: this extract **unblocks packaging shape** from first-party app assets.
> It is still **not** a public web specification. Prefer treating field rules below as
> product-local evidence until WorkBuddy publishes a stable authoring page.

## 2. What a skill is

WorkBuddy’s bundled `skill-creator` describes skills in classic Agent Skills terms:

- Modular package that extends the agent with specialized workflows, tool integrations,
  domain knowledge, and bundled resources
- Required unit: directory + `SKILL.md`
- Optional resources: `scripts/`, `references/`, `assets/`
- Progressive disclosure:
  1. Metadata (`name` + `description`) always available
  2. `SKILL.md` body when triggered
  3. Bundled resources as needed

WorkBuddy additionally treats **experts (专家包)** as a higher packaging layer:

| Unit | Meaning |
|---|---|
| Skill | Single reusable capability / workflow package |
| Expert plugin | Marketable role package (`expertType: agent` or `team`) that can embed agents + skills |
| Marketplace skill install | Install skills from BuiltinMarket via host tool, not raw HTTP |

## 3. Discovery paths and precedence

### Skills

| Scope | Path (local evidence) | Notes |
|---|---|---|
| User | `~/.workbuddy/skills/<name>/` | Observed live install root |
| Project | `<repo>/.workbuddy/skills/` | Confirmed as product layout in local path survey |
| Plugin / expert | Expert package `skills/` | Declared in `.codebuddy-plugin/plugin.json` |
| Builtin | App `builtin-skills/` | Host-shipped creators and domain skills |

`skill-creator` body text still documents CodeBuddy paths
(`~/.codebuddy/skills/`, `.codebuddy/skills/`). Treat that as **shared template heritage**:
on WorkBuddy the live user root observed is `~/.workbuddy/skills/`.

### Experts / plugins

Expert packages are fixed to:

```text
$WORKBUDDY_CONFIG_DIR/plugins/marketplaces/my-experts/plugins/<expert-name>/
```

Default when unset:

```text
~/.workbuddy/plugins/marketplaces/my-experts/plugins/
```

`expert-manager` refuses generating experts outside that tree so the product can detect them.

Observed marketplaces on this machine also include:

- `codebuddy-plugins-official`
- `cb_teams_marketplace`

## 4. Directory structure

### Skill package

```text
skill-name/
├── SKILL.md                 # required
├── scripts/                 # optional
├── references/              # optional
└── assets/                  # optional
```

Local sample:

```text
~/.workbuddy/skills/feishu-spreadsheet-sheet-float-image/
├── SKILL.md
└── references/float_image_api_reference.md
```

### Expert package (plugin)

From `expert-manager` init/validate/register flow:

```text
<expert-name>/
├── .codebuddy-plugin/
│   └── plugin.json          # required manifest
├── agents/
│   └── <agent-name>.md      # agent or team-lead / members
├── skills/                  # optional skill dirs
├── avatars/                 # required for marketplace display
└── ...
```

## 5. `SKILL.md` and frontmatter

Portable core (from `skill-creator`):

| Field | Required | Notes |
|---|---|---|
| `name` | Yes | Skill id / discovery |
| `description` | Yes | What + when; third-person preferred |

WorkBuddy-specific / product-local:

| Field | Required | Notes |
|---|---|---|
| `agent_created` | Required for agent-managed lifecycle | `true` so `skill_manage` can later modify/delete |
| `allowed-tools` | Optional | Seen on builtin skills (may be empty/list/special host tools) |
| `disable` | Optional | Builtin creators use `disable: false` |
| `license` | Optional | e.g. pointer to `LICENSE.txt` |

Local user skill sample frontmatter:

```yaml
---
name: feishu-spreadsheet-sheet-float-image
description: This skill should be used when the task involves ...
agent_created: true
---
```

Marketplace installer builtin uses host-gated tools:

```yaml
allowed-tools: workbuddy_marketplace_skill
```

## 6. Progressive disclosure / loading

`skill-creator` explicitly documents the three-level model:

1. Metadata always in context (~100 words)
2. Body on trigger (<5k words guidance)
3. Resources on demand (scripts may run without full read)

Authoring rules:

- Keep only essential procedure in `SKILL.md`
- Put detailed schemas/docs in `references/`
- Put output templates/binaries in `assets/`
- Avoid duplicating the same content in body and references

## 7. Supporting files

| Dir / file | Role |
|---|---|
| `scripts/` | Deterministic helpers (Python/Bash/etc.) |
| `references/` | On-demand docs (API, schema, policy) |
| `assets/` | Output templates / icons / boilerplate |
| `scripts/init_skill.py` | Scaffold skill tree (bundled creator) |
| `scripts/package_skill.py` | Validate + zip skill for distribution |

Expert-manager scripts:

| Script | Role |
|---|---|
| `init_expert.py` | Scaffold expert dir (`--type agent|team`) |
| `validate_expert.py` | Compliance check |
| `register_expert.py` | Write marketplace registration |
| `package_expert.py` | Package for submission |
| `batch_create.py` | Serial multi-expert helper |

## 8. Invocation

Skills:

- Model auto-selection from description
- Slash / skill-id style invoke for installed skills
- Marketplace one-shot install via `marketplace-skill-installer` →
  host tool `workbuddy_marketplace_skill` (`search` / `install`)

Experts:

- Not a separate “agent-creator skill”
- Created/operated by `expert-manager`
- Agent-type expert = single specialist
- Team-type expert = lead + members + SOP

## 9. Packaging and distribution

### Skill distribution

1. Local authoring under user/project skills roots  
2. `package_skill.py` → zip after validation  
3. BuiltinMarket install through host tool (no user-constructed HTTP/auth)  
4. Editing marketplace-installed skills must mark local meta `userModified: true`
   so auto-update does not silently overwrite

### Expert distribution

Lifecycle enforced by `expert-manager`:

```text
collect info → init_expert.py → fill files → avatar →
validate_expert.py → register_expert.py → package_expert.py
```

Manifest directory name is **`.codebuddy-plugin/`** (not `.workbuddy-plugin/`).

## 10. Versioning

- Expert `plugin.json` uses semantic `version`
- Marketplace skill results expose `version` / `installedVersion` / `updateAvailable`
- Skill-level portable versioning is not emphasized beyond package/marketplace metadata;
  for portable packs still prefer Agent Skills `metadata.version`

## 11. Limits and constraints

Documented / observed product constraints:

- Skill = one directory + `SKILL.md`
- Expert must live under fixed `my-experts/plugins` path
- Expert identity fields are sticky and must not be casually renamed:
  - `plugin.json` `name`
  - `agentName`
  - expert directory name
  - `agents/*.md` filenames (`agentName` = basename)
- Marketplace display fields are tightly shaped:
  - `displayDescription.zh` about 40–50 chars
  - `tags` fixed **3**
  - `quickPrompts` fixed **3** (first = `defaultInitPrompt`)
- Agent MD frontmatter must **not** declare `tools`
  (tool ACL is system-assigned)

## 12. Platform-specific extensions

### Skill layer

- `agent_created: true` lifecycle flag
- Host tool allowlists such as `workbuddy_marketplace_skill`
- CodeBuddy-compatible resource layout and progressive disclosure doctrine

### Expert / plugin layer (`.codebuddy-plugin/plugin.json`)

Core identity:

| Field | Notes |
|---|---|
| `name` | kebab-case id / namespace |
| `version` | semver |
| `description` | English one-line |
| `expertType` | `agent` or `team` |
| `agentName` | primary agent basename (business-meaningful, not generic `team-lead`) |
| `agents` | path list to agent MD files |
| `skills` | optional skill dir path list |

Marketplace display:

| Field | Notes |
|---|---|
| `displayName` | `{en, zh}` |
| `profession` | `{en, zh}`; team must match display name |
| `displayDescription` | `{en, zh}` |
| `avatar` | relative path |
| `categoryId` | industry category id |
| `defaultInitPrompt` | `{en, zh}` |
| `tags` | exactly 3 bilingual tags |
| `quickPrompts` | exactly 3 bilingual prompts |
| `plugin` | equals `name` |
| `members` / `teamInfo` | team-only |

### Agent MD (inside expert)

Required frontmatter pattern:

```yaml
---
name: {matches filename, business-meaningful}
description: {English trigger description}
displayName:
  en: "..."
  zh: "..."
profession:
  en: "..."
  zh: "..."
maxTurns: 50
---
```

Optional:

```yaml
skills: [skill-name]
```

Body templates differ for ordinary agent / member vs team lead; members must return
results to lead via messaging conventions.

## 13. Security

- Marketplace installer forbids hand-built HTTP and token handling; host tool only
- Expert validate/register before use
- Treat bundled scripts as executable code
- Do not put tool ACL in agent frontmatter; system assigns tools
- Prefer least-privilege skill tool lists when product supports them

## 14. Authoring practices

1. Author portable skill core as Agent Skills (`name`/`description` + lean body + resources).  
2. On WorkBuddy, set `agent_created: true` if the skill should remain agent-manageable.  
3. Use `skill-creator` for skills; use `expert-manager` when the unit is a marketable role/team.  
4. Keep expert generation inside the fixed `my-experts/plugins` root.  
5. Fill bilingual display fields carefully; they are product UX contracts, not optional polish.  
6. After editing marketplace-installed skills, mark `userModified: true`.  
7. Do not assume WorkBuddy upload/SkillHub rules from community posts alone — prefer
   app-bundled validators/scripts when packaging.

## 15. Extraction notes

- Unblocked primarily by **local first-party app assets**, not a public docs page.
- Strong CodeBuddy heritage:
  - `.codebuddy-plugin`
  - creator text still says CodeBuddy / `~/.codebuddy`
  - official marketplace samples live under WorkBuddy’s plugin marketplaces
- Live user skill root observed: `~/.workbuddy/skills/`
- Expert abstraction is the product’s answer to “agent/team creation”
- Portable skill authors can ignore expert marketplace cosmetics; adapter authors cannot

### Confidence

| Area | Confidence |
|---|---|
| Skill package shape (`SKILL.md` + resources) | High |
| `agent_created` requirement | High (creator + local sample) |
| Expert plugin schema | High (bundled `plugin-json-spec.md` + scripts) |
| Exact project-path precedence vs CodeBuddy paths | Medium (path survey + mixed template text) |
| Public SkillHub upload schema | Still open / not first-party web-documented here |
