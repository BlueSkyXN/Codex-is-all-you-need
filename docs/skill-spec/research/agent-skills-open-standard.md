# Agent Skills Open Standard

## 1. Product and sources

| Item | Value |
|---|---|
| Product | Agent Skills (open specification) |
| Home | https://agentskills.io |
| Spec URL | https://agentskills.io/specification |
| Role | Shared interchange format for skill directories across tools |
| Extracted | 2026-07-16 from public specification page |

This is the **common baseline** that Claude Code, OpenAI Skills, OpenClaw, and
many other tools declare compatibility with.

## 2. What a skill is

A skill is a **directory** containing, at minimum, a `SKILL.md` file with:

1. YAML frontmatter (metadata)
2. Markdown body (instructions)

Optional supporting files and directories may sit beside `SKILL.md`.

## 3. Discovery paths and precedence

The open specification defines the **package shape**, not a universal install
path. Product docs define where skills are discovered (user home, project root,
plugin, hosted registry).

## 4. Directory structure

```text
skill-name/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation loaded on demand
├── assets/           # Optional: templates, images, static resources
└── ...               # Any additional files or directories
```

## 5. `SKILL.md` and frontmatter

`SKILL.md` must start with YAML frontmatter, then Markdown body.

### Required / optional fields

| Field | Required | Constraints |
|---|---|---|
| `name` | Yes | Max **64** chars. Lowercase `a-z`, digits, hyphens only. Must not start/end with `-`. Must not contain `--`. **Must match parent directory name**. |
| `description` | Yes | Max **1024** chars. Non-empty. What it does **and** when to use it. |
| `license` | No | License name or reference to a bundled license file. |
| `compatibility` | No | Max **500** chars. Environment requirements (product, packages, network, etc.). |
| `metadata` | No | Arbitrary string key → string value map for extra properties. Prefer reasonably unique keys. |
| `allowed-tools` | No | Space-separated pre-approved tools. **Experimental**; support varies. |

### Minimal example

```markdown
---
name: skill-name
description: A description of what this skill does and when to use it.
---
```

### Example with optional fields

```markdown
---
name: pdf-processing
description: Extract PDF text, fill forms, merge files. Use when handling PDFs.
license: Apache-2.0
metadata:
  author: example-org
  version: "1.0"
---
```

### Body

No fixed body schema. Recommended content:

- Step-by-step instructions
- Input/output examples
- Edge cases

The agent loads the **entire** `SKILL.md` when the skill activates. Split long
content into referenced files.

## 6. Progressive disclosure / loading

Designed progressive loading:

1. **Metadata (~100 tokens)** — `name` + `description` for all skills at startup
2. **Instructions (< 5000 tokens recommended)** — full `SKILL.md` body on activation
3. **Resources (as needed)** — `scripts/`, `references/`, `assets/` only when required

Guidance:

- Keep main `SKILL.md` under **500 lines**
- Move detailed reference material to separate files

## 7. Supporting files

| Path | Purpose | Notes |
|---|---|---|
| `scripts/` | Executable helpers | Self-contained or clearly documented deps; good errors |
| `references/` | On-demand docs | Keep files focused; smaller = less context |
| `assets/` | Templates, images, data files | Static resources |

### File references

- Use **relative paths from the skill root**
- Keep references **one level deep** from `SKILL.md`
- Avoid deep nested reference chains

```markdown
See [the reference guide](references/REFERENCE.md) for details.
Run: scripts/extract.py
```

## 8. Invocation

The open spec does not mandate slash commands or auto-trigger UX. Products
typically:

- Match user intent to `description`
- Or expose an explicit `/skill-name` command

## 9. Packaging and distribution

The spec defines the on-disk skill package. Distribution (git, marketplace, zip
upload, plugin) is product-specific.

Validation reference library mentioned by the spec:

```bash
skills-ref validate ./my-skill
```

## 10. Versioning

No mandatory version field. Optional practice via:

```yaml
metadata:
  version: "1.0"
```

Product platforms may add their own package/version registries on top.

## 11. Limits and constraints

| Constraint | Value |
|---|---|
| `name` length | ≤ 64 |
| `name` charset | `[a-z0-9]+(?:-[a-z0-9]+)*` style rules (no leading/trailing/consecutive hyphens) |
| `name` vs directory | Must match |
| `description` length | ≤ 1024 |
| `compatibility` length | ≤ 500 if present |
| Body length guidance | < 500 lines recommended |
| Body token guidance | < 5000 tokens recommended |

## 12. Platform-specific extensions

Use `metadata` for non-standard properties. Clients should ignore unknown keys
they do not understand. Products often add top-level runtime fields beyond the
open set; those are **extensions**, not part of the core interchange minimum.

## 13. Security

Not heavily normative in the core page, but practical implications:

- Skills can include executable `scripts/`
- Treat third-party skills as untrusted code/instructions
- Validate with `skills-ref` before publish/install where available

## 14. Authoring practices

1. Write `description` with both **capability** and **trigger keywords**.
2. Keep `SKILL.md` short; progressive-disclose detail.
3. Prefer relative, one-level-deep links to references/scripts.
4. Put product-only data under unique `metadata` keys.
5. Validate with `skills-ref` when shipping.

## 15. Extraction notes

- Source: https://agentskills.io/specification
- This note is a structured extract, not a fork of the standard.
- Numeric limits above are from the open spec and are the best shared baseline
  for multi-platform authoring.
