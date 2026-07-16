# Qoder Skills

## 1. Product and sources

| Item | Value |
|---|---|
| Product | Qoder (IDE + CLI) |
| Overview page | https://docs.qoder.com/extensions/skills |
| CLI deep-dive | https://docs.qoder.com/en/cli/Skills |
| Ecosystem pointers | skills.sh , community skill repos, `/create-skill` |
| Extracted | 2026-07-16 from public docs |

The overview page is thin; the CLI Skills page supplies the practical authoring
format used below.

## 2. What a skill is

A skill packages domain expertise into a reusable capability for Qoder IDE/CLI.
Each skill is a folder with required `SKILL.md` (description + instructions +
optional supporting files).

Skills are modular: one skill ≈ one task type.

## 3. Discovery paths and precedence

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

### Frontmatter (CLI docs)

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

Ways to obtain skills:

1. `/create-skill <description>` guided scaffold  
2. CLI install examples:
   - `npx skills add vercel-labs/agent-browser -a qoder`
   - `npx skills add https://github.com/anthropics/skills --skill skill-creator -a qoder`
3. Hand-authored directories under user/project paths  
4. `/create-skill-ui` for interactive HTML widgets in chat  

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

Qoder-specific ergonomics:

- `/create-skill` and `/create-skill-ui`  
- `npx skills add … -a qoder` installer path  
- Built-in helpers cited on overview (`/vercel-deploy`, `/create-subagent`, `/canvas`, …)  
- Optional `templates/` directory naming in examples  

No Claude-style `context: fork` / OpenClaw `metadata.openclaw` block appears in
the extracted pages.

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
- Some overview vs CLI details (especially name-collision precedence) should be
  re-verified against the installed product if automation depends on it.  
- Overall shape is Agent Skills-compatible with a smaller extension surface than
  Claude/OpenClaw/CodeBuddy.
