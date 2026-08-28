# Research Status / 调查状态与缺口清单

Last updated: **2026-07-29**（WorkBuddy 5.3.5 bundled scanner / loader / CLI 读取边界复核后）

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
| CodeBuddy | Medium | [codebuddy.md](codebuddy.md) | CLI skills page closed; marketplace package details still thin |
| WorkBuddy | Medium-High | [workbuddy.md](workbuddy.md) | **Unblocked by local app assets** (skill-creator + expert-manager); public web spec still missing |
| Qoder / QoderWork | Medium | [qoder.md](qoder.md) | Public CLI thin + **local QoderWork creators/plugins captured**; precedence still open |
| GitHub Copilot CLI | Medium | [copilot-cli.md](copilot-cli.md) | **New**: local install layout + agents/plugins samples; full official schema open |

**Design-ready now:** open standard + Claude + Codex + OpenClaw core + WorkBuddy skill/expert shape + QoderWork plugin shape.
**Not freeze-ready:** full public SkillHub upload whitepaper, Qoder collision precedence, complete Copilot official plugin schema, full runtime matrix.

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
| Frontmatter runtime fields | Claude, CodeBuddy, some Copilot skills | `disable-model-invocation`, `allowed-tools`, `context: fork`, `user-invocable`, … |
| Frontmatter vendor namespace | OpenClaw | `metadata.openclaw` |
| Product-local frontmatter | WorkBuddy | 5.3.5 scanner reads `allowed-tools` / `disable` / `license` into its local list model and writes `disable` for the local toggle UI; it does **not** read `display_name`, `display-name`, or `disable-model-invocation`. This is scanner/UI evidence, not invocation-runtime enforcement. |
| Bilingual / UI-first naming | QoderWork plugins | Chinese `name` + `name_en` / `description_en` |
| Thin standard only | Qoder public CLI docs | mainly `name`/`description` + optional files |
| Package manifests | Distribution layers | `.codex-plugin/`, `.claude-plugin/`, `.codebuddy-plugin/`, `.qoder-plugin/`, Copilot `plugin.json`, ClawHub, etc. |

### Creation capability styles (local path survey 2026-07-17)

| Style | Who | Mechanism |
|---|---|---|
| Engineering scaffold scripts | Codex, WorkBuddy | init / validate / package / register scripts |
| Conversational creator skills | QoderWork CN | `create-skill`, `plugin-creator`, `create-command` |
| Slash command families + bundled defs | Claude Code, Copilot CLI | `/plugin`, `/agents`; Copilot also ships `definitions/*.agent.yaml` |

### Agent abstraction split

| Family | Who | Abstraction |
|---|---|---|
| Business role packages | WorkBuddy, QoderWork | Expert / 角色套件（plugin）面向业务用户 |
| Developer subagent configs | Codex, Claude Code, Copilot CLI | TOML / markdown / `.agent.yaml` 偏开发者 |

### Sanitized product-shape evidence already collected

- Sanitized `agents/openai.yaml` samples from distributable Codex skill installs
  - Observed top-level keys: `interface`, `policy`, `dependencies`
  - The observed set used default/implicit invocation; that sample is not treated
    as evidence that explicit opt-out is globally uncommon
- This repo dual-publishes plugins with both:
  - `.codex-plugin/plugin.json`
  - `.claude-plugin/plugin.json`
- The system skill-creator exposes sidecar guidance plus generation,
  initialization, and validation helpers
- **WorkBuddy (2026-07-17):**
  - App bundled `skill-creator`, `expert-manager`, `marketplace-skill-installer`
  - User skills root `~/.workbuddy/skills/`; product-local frontmatter exists but is not part of the portable/default definition
  - Expert package fields summarized without copying private templates
  - Manifest dir name `.codebuddy-plugin/`
- **QoderWork CN (2026-07-17):**
  - User skills under `~/.qoderworkcn/skills/`
  - Role plugins under `~/.qoderworkcn/plugins/<localized-role-name>/`
  - `.qoder-plugin/plugin.json` + `.mcp.json` + localized skill names
- **Copilot CLI (2026-07-17):**
  - `~/.copilot/skills/`, `~/.copilot/agents/*.md`
  - `~/.copilot/pkg/darwin-arm64/<version>/definitions/*.agent.yaml`
  - Sanitized `installed-plugins/_direct/plugin.json` shape

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
| B4 | skill-creator / evals format | DONE enough | plugin doctrine + eval/grading/trigger-optimization workflow extracted first-hand 2026-07-31 (local marketplace copy); exact JSON schemas of every eval artifact still not frozen |
| B5 | Settings: `skillOverrides`, listing budgets | PARTIAL | main behaviors captured; exact settings schema page open |
| B6 | Nested monorepo skill qualification | DONE enough | documented on main page |

### C. OpenAI / Codex

| ID | Item | Status | Notes / next action |
|---|---|---|---|
| C1 | API tools-skills attach model | DONE | hosted/local/inline + limits |
| C2 | Codex build-skills product page | DONE | discovery paths, budgets, create flows |
| C3 | `agents/openai.yaml` | DONE | fields + local samples + generator |
| C4 | Plugin packaging | DONE enough | skill-only plugin layout captured |
| C5 | skill-creator doctrine | DONE | progressive disclosure, freedom levels, validate flow; validation-integrity / forward-testing discipline re-extracted first-hand 2026-07-31 from local system install |
| C6 | Current canonical location after `openai/skills` deprecation | DONE enough | ships as local system skill `skills/.system/skill-creator` (verified 2026-07-31); `openai/plugins` remains the public repo pointer |
| C7 | Whether `allow_implicit_invocation: false` is common in first-party skills | PARTIAL | sanitized observed set used defaults; sample is not representative enough to freeze prevalence |
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
| E4 | Relation to WorkBuddy | DONE enough for design | Local WorkBuddy extract shows shared `.codebuddy-plugin` DNA + separate `~/.workbuddy` root; see G* |

### F. Qoder / QoderWork

| ID | Item | Status | Notes / next action |
|---|---|---|---|
| F1 | Extensions overview skills page | DONE enough | thin |
| F2 | CLI skills deep page | PARTIAL | earlier fetch worked for `/en/cli/Skills`; later alternate path 404 |
| F3 | Project vs user name collision precedence | OPEN | docs conflict; needs runtime test |
| F4 | Newer CLI skills URL variants | OPEN | search found `/cli/using-qodercli/skills` (404 on one fetch) — re-resolve live IA |
| F5 | Security/versioning/package limits | OPEN | not documented on pages read |
| F6 | QoderWork creator skills + role plugins | DONE enough | local `create-skill` / `plugin-creator` / plugin samples captured in `qoder.md` |
| F7 | Whether Chinese `name` is accepted outside QoderWork UI plugins | OPEN | portable guidance: prefer kebab-case ASCII |

### G. WorkBuddy

| ID | Item | Status | Notes / next action |
|---|---|---|---|
| G1 | First-party skill authoring shape | DONE enough | app-bundled creator + sanitized user-layout observation |
| G2 | SkillHub / BuiltinMarket upload package format | PARTIAL | installer + package_skill flow known; still no public whitepaper |
| G3 | Expert vs skill relationship | DONE enough | `expert-manager` + plugin-json/agent-md/team specs |
| G4 | Compatibility with CodeBuddy / Agent Skills | DONE enough for design | shared progressive disclosure + `.codebuddy-plugin`; live root `~/.workbuddy` |
| G5 | Project skill path precedence vs CodeBuddy template paths | PARTIAL | creator text still says `~/.codebuddy`; live survey uses `~/.workbuddy` |

### I. GitHub Copilot CLI

| ID | Item | Status | Notes / next action |
|---|---|---|---|
| I1 | User skill / agent / plugin paths | DONE enough | sanitized install layout captured in `copilot-cli.md` |
| I2 | Bundled `.agent.yaml` schema | DONE enough for observed keys | richer than user markdown agents |
| I3 | Official public plugin schema page | OPEN | currently inferred from samples + path survey |
| I4 | Skill discovery precedence across `.agents`/`.claude`/`.github`/user roots | OPEN | needs runtime matrix |
| I5 | Whether Claude dual-manifest install remains green on latest CLI | PARTIAL | previously verified on v1.0.62; re-check on current package |
| I6 | First-party authoring doctrine / skill-creator | DONE (negative result) | 1.0.61 / 1.0.64-1 / 1.0.75 builtin-skills contain only `customize-cloud-agent`; no creator, no doctrine (2026-07-31) |

### H. Cross-cutting verification (not docs)

| ID | Item | Status | Notes / next action |
|---|---|---|---|
| H1 | Same minimal skill installed on 5+ runtimes | OPEN | discovery/trigger/explicit invoke matrix (now includes WorkBuddy/QoderWork/Copilot more clearly) |
| H2 | Whether unknown frontmatter is ignored or rejected | OPEN | critical for strict-superset strategy |
| H3 | Whether `agents/openai.yaml` is ignored harmlessly outside Codex | OPEN | expected yes; verify |
| H4 | Whether `metadata.openclaw` is ignored harmlessly outside OpenClaw | OPEN | expected yes; verify |
| H5 | Dual Claude+Codex plugin manifests interoperability | PARTIAL | this repo already ships dual manifests; formal matrix not run |
| H6 | Whether WorkBuddy product-local top-level fields / QoderWork Chinese `name` break other clients | OPEN | do not assume ignore/soft-fail; verify |

---

## Newly gathered facts this pass / 本轮补充到的事实

### Authoring doctrine first-hand comparison (2026-07-31)

- 本地一手提取三家创作方法论并写入平台文档与 [comparison.md](comparison.md) 第 5 节：
  - Codex system skill-creator（`~/.codex` 安装树）：简洁经济学、自由度三档校准、
    "Protect Validation Integrity" 与 forward-testing 反污染纪律。
  - Claude 官方 skill-creator plugin（claude-plugins-official 本地副本）：
    with-skill vs baseline 双跑 eval loop、反 ALWAYS/NEVER、反过拟合、
    description 触发优化（60/40 train/test）、盲评。
  - Copilot CLI 1.0.61 / 1.0.64-1 / 1.0.75：builtin-skills 均仅
    `customize-cloud-agent`，**无任何 authoring doctrine**（格式采用者）。
- 交集结论「约束强度匹配风险 + 实证迭代」已作为工程实践依据进入 SPEC 0.3
  （核心原则 6/7、6.3 内容设计建议、第 8 章评测增补）。

### Terminology / SKILL.md / directory matrix (2026-07-17)

- 新增横表文档：[comparison.md](comparison.md)
- 开放标准复核（live spec）：
  - Skill = folder + required `SKILL.md`
  - `name`/`description` required with hard limits；`name` must match directory
  - optional dirs: `scripts/` `references/` `assets/` + explicit `...`
  - progressive disclosure: metadata → body → resources
- 名词分层：Skill（本体）/ Plugin（分发）/ Agent（角色）/ Expert|Team（WorkBuddy 上架壳）
- `name` 最大冲突：开放标准 kebab-case vs QoderWork UI 中文 name
- Codex 调用策略在 sidecar，不在 frontmatter；Claude 家族在 frontmatter

### Source path overview (local, 2026-07-17)

Primary input: sanitized local path survey across WorkBuddy / QoderWork CN / Codex / Claude Code / Copilot CLI creation roots, summarized in the checked-in platform extracts below.

### WorkBuddy (local first-party assets)

- Bundled creators:
  - `skill-creator` (Agent Skills progressive disclosure; creator prose mentions `agent_created`, but scaffold/validator do not enforce it)
  - `expert-manager` (agent/team experts, init/validate/register/package)
  - `marketplace-skill-installer` (host tool `workbuddy_marketplace_skill`)
- Skill package shape: `SKILL.md` + optional `scripts/` `references/` `assets/`
- **Current 5.3.5 bundled inventory** (18 top-level Skills): `license` 3, `allowed-tools` 10 (8 empty, 2 non-empty), bare `disable: false` 3, `disable-model-invocation: true` 6, and Skill-level `display_name` / `display-name` 0.
- **Current 5.3.5 scanner/loader boundary:** its local Skill-list projection reads `allowed-tools` (normalizes a non-empty comma-separated string or array to `allowedTools`), `disable`, and `license`; the local toggle action writes `disable` back to `SKILL.md`. The same scanner projection has no reader for `display_name`, `display-name`, or `disable-model-invocation`. No separately named CLI payload was found in this app package; the scanner source only says that its plugin scan mirrors an Agent CLI loader. The inspected bundled code does not prove that `allowedTools`, `disable`, or `license` constrain an invocation runtime.
- **Historical 5.2.6 snapshot (2026-07-28):** this research previously recorded scanner/UI handling for `display_name` with a `display-name` fallback and documented manual-only behavior for `disable-model-invocation`. Keep that record version-scoped; do not use it as a current 5.3.5 authoring recommendation without an invocation test.
- Live user skill root: `~/.workbuddy/skills/`
- Expert fixed root: `$WORKBUDDY_CONFIG_DIR/plugins/marketplaces/my-experts/plugins/`
- Manifest dir: `.codebuddy-plugin/plugin.json`
- Expert display contracts: bilingual fields, 3 tags, 3 quick prompts, categoryId
- Agent MD forbids frontmatter `tools` (system assigns tools)

### QoderWork CN (local creators/plugins)

- Creators: `create-skill`, `plugin-creator`, `create-command`
- Plugin = role toolbox; Skill = single tool inside it
- Plugin layout: `.qoder-plugin/plugin.json` + `.mcp.json` + `skills/` + README/CONNECTORS
- UI-first Chinese skill directory/`name` inside plugins; `plugin.json.name` stays English kebab-case
- No independent subagent/team framework; role plugin approximates “agent”

### Copilot CLI (sanitized local install layout)

- Roots: `~/.copilot/skills`, `~/.copilot/agents`, `~/.copilot/plugins`, `installed-plugins/`
- Bundled agents: `definitions/*.agent.yaml` with `tools`, `model`, `promptParts`, `prompt`
- User agents: markdown + frontmatter (`name`, `description`, `tools`, `model`)
- Skills are Agent Skills-shaped; bundled skill uses `user-invocable: false`
- Plugin sample fields: `name`, `description`, `version`, `author`, `license`, `keywords`, `category`, `commands`, `hooks`

### Creation-style taxonomy (cross-tool)

1. Scripted engineering scaffolds (Codex / WorkBuddy)
2. Conversational creator skills (QoderWork)
3. Slash command families + bundled definitions (Claude / Copilot)

---

## Recommended investigation order / 建议继续调查顺序

Not urgent freeze; when continuing, do this order for highest value:

1. **A2–A5** open-standard creation/eval guides
   → improves portable authoring doctrine without product politics
2. **H1/H2/H6** minimal skill + unknown frontmatter smoke across Claude/Codex/Copilot/WorkBuddy/QoderWork
   → turns packaging hypotheses into compatibility claims
3. **I3/I4** Copilot official plugin schema + discovery precedence
4. **D4–D7** OpenClaw config/CLI/security pages
5. **C6/C8** Codex current canonical skill-creator/plugin examples / openai.yaml schema
6. **B2–B4** Claude plugin/hooks/eval details
7. **F3** Qoder precedence runtime test
8. **G2** WorkBuddy public SkillHub whitepaper only if/when published

---

## Working rules while incomplete / 未完成前的使用原则

1. Design portable skills against **Agent Skills open standard**.
2. Treat product fields as **adapters**:
   - Codex → `agents/openai.yaml`
   - Claude/CodeBuddy/Copilot-ish → frontmatter runtime fields
   - OpenClaw → `metadata.openclaw`
   - WorkBuddy → default to portable core. In 5.3.5, `allowed-tools` / `disable` / `license` have local scanner/UI evidence only; do not add `display_name`, `display-name`, or `disable-model-invocation` without a version-matched consumer test
   - QoderWork → bilingual UI fields + `.qoder-plugin` role suites
3. Do not put WorkBuddy expert marketplace cosmetics or QoderWork Chinese UI names into the portable core.
4. Do not claim cross-runtime behavior that has not been smoke-tested (H1–H6).
5. Do not infer invocation semantics from observed vendor frontmatter or scanner/UI code: in WorkBuddy 5.3.5, `allowed-tools`, `disable`, and `license` are projected by the local scanner, while `display_name`, `display-name`, and `disable-model-invocation` are not. The 5.2.6 display-name/manual-only record is historical, not a current guarantee.
6. When docs conflict (Qoder precedence, OpenClaw description length guidance, WorkBuddy creator text saying `~/.codebuddy`), mark as **unresolved** instead of picking silently.

---

## File map / 文件地图

```text
docs/skill-spec/research/
  README.md
  RESEARCH-STATUS.md          ← this file
  comparison.md               ← terminology / SKILL.md / dirs matrix
  agent-skills-open-standard.md
  claude-code.md
  openai-codex.md
  openclaw.md
  codebuddy.md
  workbuddy.md                ← added 2026-07-17
  qoder.md                    ← expanded with QoderWork local evidence
  copilot-cli.md              ← added 2026-07-17

规范正文（勿与调研混淆）：
docs/skill-spec/SPEC.md
```

Optional future files (not created yet):

```text
platform-extensions.md        # deeper sidecar/frontmatter-only deep dive (comparison.md already covers matrix)
compatibility-matrix.md       # runtime smoke results
creation-paths.md             # optional distilled create-path matrix from local survey
```

Added this pass:

```text
comparison.md                 # terminology + SKILL.md + directory structure cross-vendor matrix
```
