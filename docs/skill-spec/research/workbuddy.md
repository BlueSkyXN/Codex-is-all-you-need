# WorkBuddy Skills / Experts

## 1. Product and sources

| Item | Value |
|---|---|
| Product | WorkBuddy (desktop agent; shares CodeBuddy packaging DNA) |
| Config root | `$WORKBUDDY_CONFIG_DIR` if set, else `~/.workbuddy` |
| Public package spec | Still **no stable first-party web authoring page** comparable to Claude/Codex |
| First-party local evidence | WorkBuddy.app 5.3.5 bundled `builtin-skills/` and scanner/loader. No separately named CLI payload was found; a scanner comment says its plugin scan mirrors an Agent CLI loader. 5.2.6 field conclusions are retained below only as a historical snapshot. |
| Related product | CodeBuddy CLI docs describe a Claude-like skill surface; WorkBuddy reuses `.codebuddy-plugin` names and often CodeBuddy wording inside creators |
| Extracted | 2026-07-17 from local app package + sanitized local layout samples; 5.2.6 historical snapshot 2026-07-28; 5.3.5 scanner/loader/CLI boundary refreshed 2026-07-29 |

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

Marketplace identifiers vary by installation and are intentionally omitted here;
they are distribution state, not part of the portable skill shape.

## 4. Directory structure

### Skill package

```text
skill-name/
├── SKILL.md                 # required
├── scripts/                 # optional
├── references/              # optional
└── assets/                  # optional
```

Sanitized local shape:

```text
~/.workbuddy/skills/example-workflow/
├── SKILL.md
└── references/example-api.md
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
| `description` | Yes | What the Skill handles and the applicable event/task context; third-person is preferred by the bundled creator |

Additional fields observed in WorkBuddy. The following are strictly versioned;
the 5.3.5 scanner/UI facts do not establish invocation-runtime behavior.

| Field | Required | Notes |
|---|---|---|
| `display_name` / `display-name` | No current scanner support found | The 5.3.5 local Skill scanner's explicit field projection does not read either spelling. The 5.2.6 `display_name`-first / `display-name`-fallback observation is retained below as historical evidence, not a current authoring rule. Neither spelling replaces `name` or `description`. |
| `allowed-tools` | Optional scanner/UI metadata | In 5.3.5, a non-empty comma-separated value or YAML array is normalized to the local list object's `allowedTools`; empty and absent both produce no value. The inspected app bundle does not prove that invocation enforces it as a tool allowlist. |
| `disable-model-invocation` | Bundled sample only in 5.3.5 | Six current builtins retain `true`, but the 5.3.5 scanner has no explicit reader. The 5.2.6 manual-only claim is historical and requires a version-matched invocation test before reuse. |
| `disable` | Local scanner and management UI | 5.3.5 reads the boolean into its local list object and its local toggle flow writes the field back to `SKILL.md`. This proves local management state, not that a running model/invocation runtime excludes the Skill. |
| `license` | Local scanner/UI metadata | 5.3.5 reads a text value into its local list object. It has no invocation-runtime semantics established by the inspected code. |
| `agent_created` | Observed lifecycle marker, not a portable/default field | Bundled prose associates `true` with later SkillManage maintenance, but `init_skill.py` does not generate it and `quick_validate.py` does not validate it. Keep it out of the portable definition. |

Sanitized field shape from the current bundled `skill-creator` frontmatter:

```yaml
---
name: skill-creator
description: Guide for creating effective skills and reusable workflow resources.
license: Complete terms in LICENSE.txt
allowed-tools:
disable: false
---
```

This example proves field presence only. In 5.3.5, empty `allowed-tools:` is
not projected as a local list value; `disable` and `license` are projected for
the scanner/UI. None of those observations proves an invocation-runtime policy.

Marketplace installer builtin uses host-gated tools:

```yaml
allowed-tools: workbuddy_marketplace_skill
```

### Versioned inventory and evidence boundary

**Current 5.3.5 bundle:** 18 top-level builtin Skills; `license` appears on 3,
`allowed-tools` on 10 (8 empty, 2 non-empty), bare `disable: false` on 3, and
`disable-model-invocation: true` on 6. Neither `display_name` nor `display-name`
appears. The bundled local scanner explicitly projects `allowed-tools`, `disable`,
and `license`, and the local toggle flow persists `disable`; it does not project
or otherwise explicitly consume `display_name`, `display-name`, or
`disable-model-invocation`.

**Historical 5.2.6 snapshot (recorded 2026-07-28):** the prior bundle was
observed to use `display_name` first with a `display-name` fallback for a Skill
UI value and documented `disable-model-invocation` as manual-only. This is not a
current 5.3.5 recommendation and is not evidence of today's invocation behavior.

The app-asar inspection separates two layers: local filesystem scanner/list/toggle
code versus the runtime that decides which Skill a model may invoke. It establishes
the former only. No separately named CLI payload was found in the package; a
scanner comment referring to an Agent CLI loader is not executable CLI evidence.
No bundled, version-matched invocation test was run, so do not treat
`allowed-tools`, `disable`, `license`, or the historical 5.2.6 fields as
execution-policy guarantees.

Do not add `display_name` / `display-name` to a new WorkBuddy Skill by default.
Do not copy the Expert/Plugin camelCase `displayName` object into a Skill: that is
a different packaging layer.

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

- Bundled Skill text describes model auto-selection from description and slash /
  skill-id-style invocation for installed Skills.
- Marketplace one-shot install via `marketplace-skill-installer` →
  host tool `workbuddy_marketplace_skill` (`search` / `install`)

The current 5.3.5 scanner/list code is not itself the invocation runtime. It
does not explicitly read `disable-model-invocation`, `display_name`, or
`display-name`; therefore this extract does not assert their current effect on
auto-selection, Skill-tool invocation, or slash invocation.

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

- Scanner/UI metadata: `allowed-tools`, `disable`, and `license` (5.3.5)
- Bundled, but not scanner-consumed: `disable-model-invocation: true` (5.3.5)
- Historical-only 5.2.6 scanner/UI spelling: `display_name` with `display-name`
  fallback
- An observed `agent_created` lifecycle marker whose creator prose, scaffold, and validator are not synchronized; it is not part of the portable/default definition
- CodeBuddy-compatible resource layout and progressive disclosure doctrine

### Expert / plugin layer (`.codebuddy-plugin/plugin.json`)

The camelCase `displayName` fields below belong to Expert/Plugin and Agent MD
presentation contracts. They are distinct from the WorkBuddy Skill frontmatter
string `display_name` described above.

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
- Do not treat `allowed-tools` as a security boundary until a version-matched
  invocation test proves enforcement. In 5.3.5 it is scanner/UI metadata and an
  empty value is absent from the local list projection.
- Use the local `disable` control only as a WorkBuddy management-state mechanism;
  its actual invocation effect remains unverified. Do not rely on
  `disable-model-invocation` without a current consumer test.

## 14. Authoring practices

1. Author portable skill core as Agent Skills (`name`/`description` + lean body + resources).
2. For packages authored under this repository's SPEC, keep `description` as a single line describing capability and applicable event/task context; do not define it as a list of guessed user phrases. This is repository guidance, not a claimed WorkBuddy runtime hard limit.
3. Do not add observed product-local fields by default. In particular, do not add
   `display_name`, `display-name`, `allowed-tools`, or
   `disable-model-invocation` on the strength of the historical 5.2.6 record;
   do not rely on `disable` as an execution control.
4. Use `skill-creator` for skills; use `expert-manager` when the unit is a marketable role/team.
5. Keep expert generation inside the fixed `my-experts/plugins` root.
6. Fill bilingual display fields carefully; they are product UX contracts, not optional polish.
7. After editing marketplace-installed skills, mark `userModified: true`.
8. Do not assume WorkBuddy upload/SkillHub rules from community posts alone — prefer
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
| 5.3.5 scanner/UI read/write behavior (`allowed-tools` / `disable` / `license`) | High for the inspected bundled local scanner and toggle flow |
| 5.3.5 `display_name` / `display-name` / `disable-model-invocation` scanner handling | High: no explicit scanner reader found; this is not proof about every remote or future consumer |
| Invocation semantics for all five fields | Unverified; no version-matched live invocation matrix was run |
| 5.2.6 `display_name` fallback and manual-only claim | Historical snapshot only; do not generalize to 5.3.5 |
| `agent_created` lifecycle intent | Medium (creator prose conflicts with scaffold and validator) |
| Expert plugin schema | High (bundled `plugin-json-spec.md` + scripts) |
| Exact project-path precedence vs CodeBuddy paths | Medium (path survey + mixed template text) |
| Public SkillHub upload schema | Still open / not first-party web-documented here |
