# OpenAI / Codex Skills

## 1. Product and sources

OpenAI skill material is **split across surfaces**. The API tools page alone is
**not** a complete authoring guide for Codex.

| Surface | URL | What it covers well | What it under-specifies |
|---|---|---|---|
| API Skills guide | https://developers.openai.com/api/docs/guides/tools-skills | Hosted/local/inline attach, upload limits, artifact versions | Codex discovery paths, authoring style, `agents/openai.yaml`, plugins |
| Codex build skills | https://learn.chatgpt.com/docs/build-skills | Local discovery, progressive disclosure budgets, create flows, `agents/openai.yaml` | Hosted API zip limits |
| Codex build plugins | https://learn.chatgpt.com/docs/build-plugins | Skill-only plugin layout, marketplace packaging | Deep body-writing craft |
| skill-creator (system skill) | https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md | Authoring craft, freedom levels, init/validate scripts, what not to ship | Product install UX |
| Open standard | https://agentskills.io/specification | Portable field limits and progressive disclosure | Product packaging |
| Example repos | `openai/skills` (deprecated pointer), prefer `openai/plugins` | Examples / migration pointer | Treat deprecated repo as historical |

**Extracted:** 2026-07-16 from the sources above.

> Important: the `openai/skills` README states the repository is **deprecated**
> for current Codex skill/plugin examples in favor of
> [openai/plugins](https://github.com/openai/plugins) and the Build plugins
> guide. The bundled `.system/skill-creator` content remains a useful authoring
> doctrine extract even when the repo status is deprecated.

## 2. What a skill is

A skill is a folder of instructions plus optional scripts/resources that makes a
task-specific workflow repeatable for Codex / agents.

Skills can provide:

1. Multi-step domain workflows  
2. Tool / file-format / API integration guidance  
3. Domain or company knowledge the model does not reliably “just know”  
4. Bundled scripts, references, and assets  

In Codex product language:

- **Skill** = authoring unit for a reusable workflow  
- **Plugin** = distribution unit that can package one or more skills (and optional
  MCP/app/hooks)

In API language:

- **Skill** = versioned file bundle with `SKILL.md`, attached to a shell
  environment as hosted reference, local path, or inline zip

## 3. Discovery paths and precedence

### Codex local discovery (product docs)

| Scope | Location | Use |
|---|---|---|
| REPO | `$CWD/.agents/skills` | Skills for current working folder |
| REPO | `$CWD/../.agents/skills` | Parent-folder shared skills (nested repos) |
| REPO | `$REPO_ROOT/.agents/skills` | Repo-root skills |
| USER | `$HOME/.agents/skills` | Personal skills across repos |
| ADMIN | `/etc/codex/skills` | Machine-wide / automation defaults |
| SYSTEM | Bundled with Codex | Built-ins such as skill-creator / plan |

Notes from product docs:

- For repos, Codex scans `.agents/skills` from CWD up toward repo root  
- Same `name` does **not** merge; both may appear in selectors  
- Symlinked skill folders are supported  
- Local folders are for authoring/discovery; broader distribution prefers plugins  

Enable/disable without deleting (`~/.codex/config.toml`):

```toml
[[skills.config]]
path = "/path/to/skill/SKILL.md"
enabled = false
```

Restart Codex after config changes.

### API attachment model (not path discovery)

| Mode | Attachment |
|---|---|
| Hosted shell | `skill_reference` + `skill_id` (+ version) |
| Local shell | `{name, description, path}` |
| Inline | base64 zip skill source |
| Curated | first-party ids (e.g. `openai-spreadsheets`) |

## 4. Directory structure

### Portable / Codex authoring shape

```text
skill-name/
├── SKILL.md                 # required
├── agents/                  # recommended for Codex UI / policy
│   └── openai.yaml
├── scripts/                 # optional executable helpers
├── references/              # optional on-demand docs
└── assets/                  # optional output templates/resources
```

skill-creator also stresses:

- Folder name = skill name  
- Do **not** ship human-process clutter as skill content:
  `README`, installation guides, changelogs, setup/testing essays intended for
  humans rather than the agent runtime  

### Skill-only plugin shape (distribution)

```text
my-plugin/
├── .codex-plugin/plugin.json    # required manifest
└── skills/
    └── hello/
        └── SKILL.md
```

Manifest example:

```json
{
  "name": "my-first-plugin",
  "version": "1.0.0",
  "description": "Reusable greeting workflow",
  "skills": "./skills/"
}
```

Only the manifest lives under `.codex-plugin/`. Skills stay at plugin-root
`skills/`.

## 5. `SKILL.md` and frontmatter

### Minimum (Codex + API + open standard)

```markdown
---
name: skill-name
description: Explain exactly when this skill should and should not trigger.
---

Skill instructions for Codex to follow.
```

| Field | Role |
|---|---|
| `name` | Identity; kebab-case; align with directory |
| `description` | **Selection metadata**: what + when (+ when not). Implicit trigger depends on this |

Open standard constraints still apply for portable packs:

- `name` ≤ 64, lowercase/digits/hyphens, no leading/trailing/consecutive `-`  
- `description` ≤ 1024  

### skill-creator doctrine on frontmatter

- For authored skills, treat frontmatter as **`name` + `description` first**  
- Triggering/selection is driven by those fields; a “When to Use” section only in
  the body does **not** help discovery  
- Put all trigger conditions in `description`  
- Optional open-standard fields (`license`, `compatibility`, `metadata`,
  experimental `allowed-tools`) remain available for portability  

### Optional Codex UI / policy sidecar: `agents/openai.yaml`

This is the main **Codex-specific reinforcement** beyond plain Agent Skills.

Path:

```text
skill-name/
├── SKILL.md
└── agents/
    └── openai.yaml
```

Purpose (from skill-creator reference):

> `agents/openai.yaml` is an extended, product-specific config intended for the
> **machine/harness** to read, **not the agent**. Other product-specific config
> can also live in the `agents/` folder.

It does **not** replace `SKILL.md`. Trigger matching still comes from
`SKILL.md` `name`/`description`. `openai.yaml` adds:

1. UI presentation (ChatGPT desktop / skill chips)
2. Invocation policy (implicit vs explicit-only)
3. Declared tool/MCP dependencies

#### Full example

```yaml
interface:
  display_name: "Optional user-facing name"
  short_description: "Optional user-facing description"
  icon_small: "./assets/small-400px.png"
  icon_large: "./assets/large-logo.svg"
  brand_color: "#3B82F6"
  default_prompt: "Use $skill-name-here to draft a concise weekly status update."

dependencies:
  tools:
    - type: "mcp"
      value: "github"
      description: "GitHub MCP server"
      transport: "streamable_http"
      url: "https://api.githubcopilot.com/mcp/"

policy:
  allow_implicit_invocation: true
```

#### Field map

| Path | Meaning | Constraints / notes |
|---|---|---|
| `interface.display_name` | Human title in UI lists/chips | Quote strings |
| `interface.short_description` | Short UI blurb | **25–64 chars** (skill-creator validates) |
| `interface.icon_small` | Small icon path | Prefer `./assets/...` |
| `interface.icon_large` | Large logo path | Prefer `./assets/...` |
| `interface.brand_color` | UI accent hex | e.g. `"#3B82F6"` |
| `interface.default_prompt` | Default prompt inserted on invoke | Should explicitly mention `$skill-name` |
| `policy.allow_implicit_invocation` | Implicit auto-select allowed? | Default `true`. `false` = not injected into model context by default; still callable via `$skill` |
| `dependencies.tools[].type` | Dependency category | Currently only `"mcp"` |
| `dependencies.tools[].value` | Tool/server id | e.g. `"figma"`, `"linear"` |
| `dependencies.tools[].description` | Human explanation | |
| `dependencies.tools[].transport` | MCP transport | e.g. `"streamable_http"` |
| `dependencies.tools[].url` | MCP server URL | |

Observed top-level keys in real installed skills: only
`interface` / `policy` / `dependencies`.

#### Relation to Claude-style controls

| Goal | Codex (`openai.yaml`) | Claude Code (`SKILL.md`) |
|---|---|---|
| Block model auto-trigger | `policy.allow_implicit_invocation: false` | `disable-model-invocation: true` |
| UI display name | `interface.display_name` | mostly directory / `name` |
| Default invoke prompt | `interface.default_prompt` | `$ARGUMENTS` / body patterns |
| Declare MCP need | `dependencies.tools` | usually separate MCP config |

#### Generator

System skill-creator ships:

```bash
# conceptual; path depends on local Codex install
python3 .../skill-creator/scripts/generate_openai_yaml.py <skill_dir> \
  --interface display_name="PDF Skill" \
  --interface short_description="Create, edit, and review PDFs"
```

Without `agents/openai.yaml`, the skill still works; policy defaults to allowing
implicit invocation.

## 6. Progressive disclosure / loading

Shared three-level model (open standard + skill-creator + Codex docs):

1. **Metadata** — `name` + `description` (+ path) always available for selection  
2. **`SKILL.md` body** — loaded when skill is selected/triggered  
3. **Bundled resources** — scripts/references/assets on demand  

Codex product budget for the **initial skills list**:

- At most **~2% of the model context window**, or  
- **8,000 characters** if window unknown  
- With many skills: descriptions shortened first; some skills may be omitted with warning  
- Budget applies to the listing only; selected skills still load full instructions  

skill-creator size guidance:

- Body ideally **under ~500 lines** / **&lt; ~5k words**  
- Metadata roughly ~100 words  

API loading note: skill instructions are treated as **user-prompt input**, not
system prompt, when attached through the Skills/shell environment path.

## 7. Supporting files

| Path | Purpose | Authoring rules (skill-creator) |
|---|---|---|
| `scripts/` | Deterministic / fragile / repeated operations | Prefer real tested scripts; token-efficient; may run without loading full prose |
| `references/` | Schemas, policies, long API docs | Load on demand; no duplication with body; TOC if file &gt;100 lines; one level deep from `SKILL.md`; if huge (&gt;10k words), add grep/entry hints in body |
| `assets/` | Templates, logos, boilerplate outputs | Output resources, not instruction dumps |
| `agents/openai.yaml` | UI/policy/tool deps | Codex presentation sidecar |

Freedom-level framing (skill-creator):

| Freedom | When | Form |
|---|---|---|
| High | Many valid approaches | Short prose instructions |
| Medium | Preferred pattern | Parameterized scripts / pseudocode |
| Low | Sequence must be exact | Fixed scripts |

## 8. Invocation

### Codex product

| Mode | How |
|---|---|
| Explicit | Mention skill in prompt; CLI/IDE `/skills` or `$skill` |
| Implicit | Codex may select when task matches `description` |
| Policy gate | `allow_implicit_invocation: false` forces explicit only |

Create flows:

- `$skill-creator` / built-in creator  
- Record & Replay style capture  
- Manual folder + `SKILL.md`  
- `$skill-installer` for curated/local installs  

### API environments

Model chooses after metadata injection; callers can force use with explicit
prompting (“use the `<skill name>` skill”).

## 9. Packaging and distribution

| Path | Use |
|---|---|
| Local/repo `.agents/skills` | Fast iteration, repo-scoped |
| Plugin (`skills/` + `.codex-plugin/plugin.json`) | Shareable installable package |
| Marketplace entry | Local/personal/public distribution |
| API `POST /v1/skills` | Hosted artifact for Responses/container workflows |
| Inline base64 zip | One-off container attach |

API upload limits (hosted artifacts):

| Limit | Value |
|---|---|
| Max zip | 50 MB |
| Max files per version | 500 |
| Max uncompressed file | 25 MB |
| `SKILL.md` count | exactly one (`SKILL.md` / `skill.md`) |

## 10. Versioning

Two different version layers:

| Layer | Where | Meaning |
|---|---|---|
| Behavior / content version | optional `metadata.version` in `SKILL.md` | Portable skill revision semantics |
| Plugin package version | `.codex-plugin/plugin.json` `version` | Installable package SemVer |
| Hosted API skill version | integer / `latest` / `default_version` | Uploaded artifact revisions |

Do not conflate them.

## 11. Limits and constraints

| Topic | Source | Rule / guidance |
|---|---|---|
| name/description lengths | Agent Skills | 64 / 1024 |
| Body length | skill-creator / open standard | ~500 lines guidance |
| Skills list budget | Codex product | ~2% context or 8k chars |
| Hosted zip/files | API guide | 50MB / 500 files / 25MB file |
| Frontmatter minimum | all | `name` + `description` |
| Trigger text location | skill-creator | keep in description, not only body |
| Human clutter files | skill-creator | avoid shipping README/process docs as skill payload |

## 12. Platform-specific extensions

Codex / OpenAI-specific beyond bare Agent Skills:

- `agents/openai.yaml` UI + `allow_implicit_invocation` policy  
- Plugin packaging (`.codex-plugin/plugin.json`, marketplaces)  
- Local multi-root `.agents/skills` discovery  
- `$skill-creator`, `$skill-installer`, plugin-creator flows  
- Hosted `skill_id` version registry for API  
- System skills under Codex install / historical `.system` packs  

## 13. Security

From API + general skill practice:

- Treat skills as privileged instructions/code  
- Inspect third-party skills before enable/install  
- Prefer developer-selected skills mapped to bounded workflows  
- Gate write/high-impact actions  
- Hosted container mounts are lifecycle-bound  
- Use local shell/path mode when execution must stay on your machine  
- Do not embed secrets in `SKILL.md`  

## 14. Authoring practices

Synthesized from **skill-creator + Codex build-skills** (stronger than API page alone):

1. **Concise is key** — context is shared with system prompt, history, other skill
   metadata, and the user request. Add only what the model lacks.  
2. Write `description` with clear include **and exclude** triggers; front-load
   keywords in case listings are truncated.  
3. Keep body imperative, step-oriented, with explicit inputs/outputs.  
4. Prefer instructions first; add scripts only for determinism/tooling.  
5. Progressive-disclose: short `SKILL.md`, long detail in `references/`.  
6. One skill = one job.  
7. Test real prompts against description for implicit trigger quality.  
8. Validate with tooling when available (`quick_validate.py` in skill-creator pack).  
9. Iterate from real friction after use, not from abstract completeness.  
10. Distribute reusable work as a plugin once local skill stabilizes.

### skill-creator process (ordered)

1. Understand with concrete examples / sample utterances  
2. Plan reusable scripts/refs/assets  
3. Initialize (`init_skill.py` or creator flow)  
4. Edit resources + `SKILL.md`  
5. Validate  
6. Use → observe misses → revise  

## 15. Extraction notes

### Why the API page felt incomplete

Your suspicion is correct.  
https://developers.openai.com/api/docs/guides/tools-skills is primarily an
**attachment/runtime API** document. The deeper **authoring doctrine** lives in:

1. Codex product docs (`learn.chatgpt.com/docs/build-skills`)  
2. Plugin packaging docs (`learn.chatgpt.com/docs/build-plugins`)  
3. The system `skill-creator` skill (historically in `openai/skills`, now with
   migration pressure toward `openai/plugins`)

### What skill-creator adds beyond the API page

- Freedom-level design (high/medium/low specificity)  
- Hard guidance that trigger text belongs in description only  
- Explicit progressive-disclosure budgets and ~500-line body target  
- `agents/openai.yaml` as recommended sidecar  
- Ban on human-oriented clutter files inside skill packages  
- init/validate script workflow and iteration loop  
- Concrete resource roles for scripts vs references vs assets  

### What Codex product docs add

- Concrete `.agents/skills` discovery roots  
- Skills-list context budget (~2% / 8k chars)  
- `$skill-creator` / `$skill-installer` / enable config  
- Plugin-first distribution path  

### Residual gaps

- Exact current location of skill-creator after `openai/skills` deprecation should
  be re-checked against the latest Codex install / `openai/plugins`  
- Numeric listing budgets and API upload limits can change; re-fetch before
  treating as hard compliance gates  
- This repo’s own public skill contract remains
  [skill-design.md](../skill-design.md) +
  [skill-versioning.md](../skill-versioning.md); this note is comparative research
