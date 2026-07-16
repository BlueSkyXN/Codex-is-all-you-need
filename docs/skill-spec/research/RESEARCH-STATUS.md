# Research Status / 调查状态与缺口清单

Last updated: **2026-07-16**

This file tracks how complete the multi-vendor skill-spec research is, what was
already extracted, what can still be investigated from public docs/local samples,
and what is blocked on missing official sources or runtime verification.

本文件标记各平台 skill 规范调查完成度、已落地文档、可继续查清的项、以及当前阻塞点。

## Overall / 总览

| Platform | Confidence | Extract doc | Status |
|---|---:|---|---|
| Agent Skills open standard | High | [agent-skills-open-standard.md](agent-skills-open-standard.md) | Core closed; secondary creation guides still optional |
| Claude Code | High | [claude-code.md](claude-code.md) | Main page closed; some subpages open |
| OpenAI / Codex | Medium-High | [openai-codex.md](openai-codex.md) | Multi-source closed enough for design; authority still migrating |
| OpenClaw | Medium-High | [openclaw.md](openclaw.md) | Main + ClawHub format improved; some subpages open |
| CodeBuddy | Medium | [codebuddy.md](codebuddy.md) | CLI skills page closed; WorkBuddy packaging open |
| Qoder | Medium-Low | [qoder.md](qoder.md) | Partial; path/precedence conflicts unresolved |
| WorkBuddy | Low | _(none yet)_ | No first-party skill package spec found |

**Design-ready now:** open standard + Claude + Codex + OpenClaw core.  
**Not freeze-ready:** WorkBuddy upload package, Qoder conflict rules, full runtime matrix.

---

## What is already clear / 已查清

### Shared core

- Skill = directory + required `SKILL.md`
- Portable minimum frontmatter: `name` + `description`
- Progressive disclosure: metadata → body → resources
- Optional resources: scripts / references-like docs / assets
- Product-private extensions should not become the portable core

### Platform extension styles

| Style | Who | Mechanism |
|---|---|---|
| Sidecar file | Codex | `agents/openai.yaml` |
| Frontmatter runtime fields | Claude, CodeBuddy | `disable-model-invocation`, `allowed-tools`, `context: fork`, … |
| Frontmatter vendor namespace | OpenClaw | `metadata.openclaw` |
| Thin standard only | Qoder (as documented) | mainly `name`/`description` + optional files |
| Package manifests | All distribution layers | `.codex-plugin/plugin.json`, `.claude-plugin/plugin.json`, ClawHub, etc. |

### Local evidence already collected

- Many real `agents/openai.yaml` samples under local Codex skill installs
  - Observed top-level keys only: `interface`, `policy`, `dependencies`
  - In one local curated set (39 files), **zero** set
    `policy.allow_implicit_invocation: false` (all default/implicit-on)
- This repo dual-publishes plugins with both:
  - `.codex-plugin/plugin.json`
  - `.claude-plugin/plugin.json`
- Local system skill-creator contains:
  - `references/openai_yaml.md`
  - `scripts/generate_openai_yaml.py`
  - `scripts/init_skill.py`
  - `scripts/quick_validate.py`
- Machine has OpenClaw / CodeBuddy traces, but **no WorkBuddy skill package sample** was found in the quick local search

---

## Gap board / 缺口看板

Legend:

- `OPEN` — not done
- `PARTIAL` — some sources read, not enough to freeze
- `BLOCKED` — needs external artifact/access we do not currently have
- `DONE` — good enough for design reference

### A. Open standard secondary pages

| ID | Item | Status | Notes / next action |
|---|---|---|---|
| A1 | Specification core | DONE | Captured in `agent-skills-open-standard.md` |
| A2 | Best practices | PARTIAL | Page fetched 2026-07-16; not yet rewritten into extract doc |
| A3 | Optimizing descriptions | OPEN | https://agentskills.io/skill-creation/optimizing-descriptions.md |
| A4 | Using scripts | OPEN | https://agentskills.io/skill-creation/using-scripts.md |
| A5 | Evaluating skills | OPEN | https://agentskills.io/skill-creation/evaluating-skills.md |
| A6 | Client implementation guide | OPEN | useful for “what clients must support” |
| A7 | Client showcase list | OPEN | who claims compatibility |

### B. Claude Code

| ID | Item | Status | Notes / next action |
|---|---|---|---|
| B1 | Main skills page | DONE | `claude-code.md` |
| B2 | Plugins reference (skills packaging) | OPEN | linked from skills page |
| B3 | Hooks in skills/agents | PARTIAL | fields known; full schema not extracted |
| B4 | skill-creator / evals format | PARTIAL | known exists; eval file schema not fully captured |
| B5 | Settings: `skillOverrides`, listing budgets | PARTIAL | main behaviors captured; exact settings schema page open |
| B6 | Nested monorepo skill qualification | DONE enough | documented on main page |

### C. OpenAI / Codex

| ID | Item | Status | Notes / next action |
|---|---|---|---|
| C1 | API tools-skills attach model | DONE | hosted/local/inline + limits |
| C2 | Codex build-skills product page | DONE | discovery paths, budgets, create flows |
| C3 | `agents/openai.yaml` | DONE | fields + local samples + generator |
| C4 | Plugin packaging | DONE enough | skill-only plugin layout captured |
| C5 | skill-creator doctrine | DONE enough | progressive disclosure, freedom levels, validate flow |
| C6 | Current canonical location after `openai/skills` deprecation | PARTIAL | README points to `openai/plugins`; re-check live install path periodically |
| C7 | Whether `allow_implicit_invocation: false` is common in first-party skills | PARTIAL | local curated sample set showed 0/39 false |
| C8 | Exact schema validation for openai.yaml beyond skill-creator notes | OPEN | no formal JSON schema found yet |

### D. OpenClaw

| ID | Item | Status | Notes / next action |
|---|---|---|---|
| D1 | Main skills tools page | DONE | discovery, gating, slash/tool dispatch |
| D2 | ClawHub skill-format | PARTIAL→improved | [skill-format](https://docs.openclaw.ai/clawhub/skill-format): publish limits, metadata schema, install kinds |
| D3 | Creating skills page | PARTIAL | [creating-skills](https://docs.openclaw.ai/tools/creating-skills) fetched; description “under 160 chars” conflicts with open standard 1024 — mark as product UI guidance vs portable max |
| D4 | Skills config (`skills.entries`) | OPEN | https://docs.openclaw.ai/tools/skills-config |
| D5 | macOS skills install UI behavior | OPEN | https://docs.openclaw.ai/platforms/mac/skills |
| D6 | CLI `openclaw skills *` full flag set | OPEN | https://docs.openclaw.ai/cli/skills |
| D7 | Security installPolicy details | OPEN | referenced, not fully extracted |
| D8 | Local OpenClaw workspace skill samples | PARTIAL | machine has OpenClaw installs; not systematically inventoried |

### E. CodeBuddy

| ID | Item | Status | Notes / next action |
|---|---|---|---|
| E1 | CLI skills page | DONE | Claude-like frontmatter captured |
| E2 | Plugin marketplace package format | OPEN | not fully specified on skills page |
| E3 | Hooks trust model details | PARTIAL | known gate `allowUntrustedFrontmatterHooks` |
| E4 | Relation to WorkBuddy | BLOCKED/PARTIAL | nav only on CodeBuddy page; no first-party joint package spec found |

### F. Qoder

| ID | Item | Status | Notes / next action |
|---|---|---|---|
| F1 | Extensions overview skills page | DONE enough | thin |
| F2 | CLI skills deep page | PARTIAL | earlier fetch worked for `/en/cli/Skills`; later alternate path 404 |
| F3 | Project vs user name collision precedence | OPEN | docs conflict; needs runtime test |
| F4 | Newer CLI skills URL variants | OPEN | search found `/cli/using-qodercli/skills` (404 on one fetch) — re-resolve live IA |
| F5 | Security/versioning/package limits | OPEN | not documented on pages read |

### G. WorkBuddy (adjacent, high product relevance)

| ID | Item | Status | Notes / next action |
|---|---|---|---|
| G1 | First-party skill authoring spec | BLOCKED | no stable official package spec page found in search |
| G2 | SkillHub upload package format | BLOCKED | community articles only; need official doc or exported package |
| G3 | “专家/Expert” vs skill relationship | PARTIAL | product marketing/community materials; not normative |
| G4 | Compatibility with CodeBuddy / Agent Skills | PARTIAL | community claims SKILL.md-shaped; not verified |

### H. Cross-cutting verification (not docs)

| ID | Item | Status | Notes / next action |
|---|---|---|---|
| H1 | Same minimal skill installed on 5 runtimes | OPEN | discovery/trigger/explicit invoke matrix |
| H2 | Whether unknown frontmatter is ignored or rejected | OPEN | critical for strict-superset strategy |
| H3 | Whether `agents/openai.yaml` is ignored harmlessly outside Codex | OPEN | expected yes; verify |
| H4 | Whether `metadata.openclaw` is ignored harmlessly outside OpenClaw | OPEN | expected yes; verify |
| H5 | Dual Claude+Codex plugin manifests interoperability | PARTIAL | this repo already ships dual manifests; formal matrix not run |

---

## Newly gathered facts this pass / 本轮补充到的事实

### OpenClaw / ClawHub skill-format (public docs)

Source: [ClawHub skill format](https://docs.openclaw.ai/clawhub/skill-format)

- Required: skill folder + `SKILL.md` (`skill.md` / legacy `skills.md` accepted)
- Publish accepts **text-based files only**
- Bundle size limit: **50MB**
- Embedding text: `SKILL.md` + up to ~40 non-`.md` files (best-effort)
- `metadata.openclaw` supports requires/install/os/emoji/homepage/primaryEnv/envVars/…
- Install kinds documented: `brew`, `node`, `go`, `uv` (download appears in other OpenClaw pages)
- Published skills license policy on ClawHub: **MIT-0**, no paid skills
- Local install metadata: `.clawhub/origin.json`; workdir lock `.clawhub/lock.json`

### OpenClaw creating-skills notes

Source: [Creating skills](https://docs.openclaw.ai/tools/creating-skills)

- Product guidance may say description “under 160 characters” for discovery UI
- Portable Agent Skills max remains **1024**
- Treat 160 as **product recommendation**, not open-standard hard limit
- Emphasizes concise instructions and safety around `exec`

### Agent Skills secondary docs map

Source index: https://agentskills.io/llms.txt

- Spec
- Quickstart
- Best practices
- Optimizing descriptions
- Using scripts
- Evaluating skills
- Client implementation / showcase

Best-practices themes already confirmed: real expertise grounding, context thrift, progressive disclosure, calibrate control, gotchas, templates, validation loops, bundle scripts when repeated.

### WorkBuddy

- Public web search did **not** yield a stable first-party package specification comparable to Claude/Codex/OpenClaw docs
- Community/secondary articles describe SKILL.md-shaped skills and SkillHub install/import
- Status remains **blocked on official source or a real exported package**

### Qoder

- Additional candidate URLs appeared in search (`/cli/using-qodercli/skills`, rules/config hierarchy)
- At least one candidate path 404’d on fetch
- Precedence conflict (user vs project) still unresolved without runtime test

---

## Recommended investigation order / 建议继续调查顺序

Not urgent freeze; when continuing, do this order for highest value:

1. **A2–A5** open-standard creation/eval guides  
   → improves portable authoring doctrine without product politics  
2. **D2–D6** OpenClaw format/config/CLI pages  
   → closest “Codex-like ecosystem” with public docs  
3. **C6/C8** Codex current canonical skill-creator/plugin examples  
   → keep openai.yaml guidance current  
4. **B2–B4** Claude plugin/hooks/eval details  
   → needed if dual Claude+Codex packaging is a hard requirement  
5. **F3 + H1** Qoder precedence + 5-runtime smoke matrix  
   → turns docs into verified compatibility claims  
6. **G1/G2** WorkBuddy only when an official doc or real package is available  

---

## Working rules while incomplete / 未完成前的使用原则

1. Design portable skills against **Agent Skills open standard**.  
2. Treat product fields as **adapters**:
   - Codex → `agents/openai.yaml`
   - Claude/CodeBuddy → frontmatter runtime fields
   - OpenClaw → `metadata.openclaw`
3. Do not freeze WorkBuddy-specific packaging rules yet.  
4. Do not claim cross-runtime behavior that has not been smoke-tested (H1–H4).  
5. When docs conflict (Qoder precedence, OpenClaw description length guidance), mark as **unresolved** instead of picking silently.

---

## File map / 文件地图

```text
docs/skill-spec/research/
  README.md
  RESEARCH-STATUS.md          ← this file
  agent-skills-open-standard.md
  claude-code.md
  openai-codex.md
  openclaw.md
  codebuddy.md
  qoder.md

规范正文（勿与调研混淆）：
docs/skill-spec/SPEC.md
```

Optional future files (not created yet):

```text
comparison.md                 # cross-vendor matrix
platform-extensions.md        # sidecar/frontmatter extension map
workbuddy.md                  # only after official source exists
compatibility-matrix.md       # runtime smoke results
```
