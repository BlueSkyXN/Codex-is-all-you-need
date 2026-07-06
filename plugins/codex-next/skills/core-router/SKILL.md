---
name: core-router
description: Use as Codex Next plugin entrypoint to route SDLC/dev/data/office/research tasks, choose the smallest workflow, or normalize external discussion into executable work.
---

# Codex Next Router

Codex Next is a workflow router for the skills bundled in this plugin. Use it to
choose the smallest useful path, then continue with the selected skill when the
user wants work completed.

This skill routes. It does not replace the underlying skills.

## Operating Model

For SDLC/ADS lane, artifact, ID, and dev-path definitions, use the single
source of truth:

```text
../sdlc-router/references/sdlc-operating-model.md
```

Read it when lane, ADS, ID, or intake classification matters. Do not restate the
contract here.

## Codex Next Flow Map

- Direct-dev line: direct request -> relevant dev skill -> smallest validation
  -> review or release check when risk requires it.
- SDLC line: project research -> requirements/SRS/NFR -> architecture/domain ->
  spec slice or handoff -> implementation -> validation/readiness.
- Bug line: feedback loop -> reproduce/minimise -> hypothesis/probe -> fix ->
  regression -> refactor or architecture recommendation if the seam is poor.
- Context line: `core-goal-run` executes an existing local goal plan. For session
  compaction or fork handoff, write the smallest durable handoff note needed by
  the next run; do not turn it into an SDLC artifact unless the task needs that.
- Skill-quality line: authoring discipline -> surface check -> `core-skill-eval`
  for major behavior changes.

## Workflow

1. Identify the user intent.
   - Read-only explanation or fact check.
   - Direct implementation, bugfix, review, or validation.
   - Requirements, architecture, domain, spec, handoff, or release work.
   - Data, office, research, or prompt-evaluation work.
   - External Web/GPT/AI discussion that must be normalized before execution.

2. Choose the smallest route.
   - If the request is SDLC/ADS, `local/sdlc`, handoff, architecture,
     requirements, specification, validation, or external proposal intake work,
     use `sdlc-manager`.
   - If the request only needs lane, ADS, or minimum-material classification,
     use `sdlc-router`.
   - If the request is clear and local, route to the relevant dev skill.
   - If the user asks to produce an artifact, route directly to that artifact
     skill.
   - If the user asks to implement, continue past routing and perform the work
     with the selected skill.

3. Keep source boundaries clear.
   - External AI or web discussion is reference input until user-confirmed or
     supported by repository/local evidence.
   - External/private skill libraries are not the runtime source of truth for this plugin.
   - `.codex/agents/*.toml` custom agents are not bundled by this plugin.
   - Plugin skills are workflow instructions; they do not automatically install
     MCP servers, apps/connectors, hooks, or custom agents.
   - Draft or experimental notes are not packaged until a corresponding skill
     directory exists under this plugin's `skills/` surface.

## Route Table

| User intent | First skill |
|---|---|
| Stress-test or interrogate an ambiguous plan/design | `core-grilling` |
| Evaluate a skill rewrite with golden cases | `core-skill-eval` |
| SDLC/ADS work, `local/sdlc`, handoff, or external proposal intake | `sdlc-manager` |
| Need only lane, ADS, or minimum artifact decision | `sdlc-router` |
| Existing repo capability map | `sdlc-project-research` |
| Requirements package | `sdlc-requirements-workflow` |
| SRS or software-facing requirements | `sdlc-srs-workflow` |
| NFRs or measurable quality constraints | `sdlc-nfr-spec` |
| Architecture impact | `sdlc-hld-workflow` |
| Domain ownership or dependency boundaries | `sdlc-domain-boundary-modeling` |
| Solution/spec package coordination | `sdlc-solution-spec-workflow` |
| Implementation-facing slices | `sdlc-spec-slice-writer` |
| Dev handoff | `sdlc-dev-handoff-planning` |
| Validation plan or behavior baseline | `sdlc-validation-plan-workflow` |
| Traceability | `sdlc-requirements-traceability` |
| Change control | `sdlc-change-control` |
| Clear implementation | `dev-spec-driven-implementation` or the relevant dev skill |
| Bugfix | `dev-bugfix` |
| PR or diff review | `dev-pr-review` |
| Security review | `dev-security-review` |
| Test planning or validation strategy | `dev-test-strategy` |
| Release readiness | `dev-release-check` |
| Data cleaning or tabular analysis | `data-cleaning`, `data-tabular-analysis`, or `data-sql-analysis` |
| Office writing | `office-meeting-summary`, `office-weekly-report`, `office-project-report`, `office-briefing-note`, or `office-ppt-outline` |
| Research synthesis | `research-synthesis`, `research-source-dedup`, or `research-evidence-table` |

## Manual or Expensive Helpers

Some workflows are intentionally expensive or human-started. Prefer explicit
user confirmation before running them at scale:

- `core-skill-eval` - use golden cases and blind runs before shipping major
  skill behavior rewrites.
- `core-goal-run` - resume or execute an existing local goal plan, without
  rewriting the plan unless asked.
- Surface governance - run `scripts/check_codex_next_surface.py` after changing
  this plugin's skills or manifests.

## Output

When routing only, return:

```markdown
## Codex Next Route

- Intent:
- Lane:
- Modifier:
- ADS:
  - A:
  - D:
  - S:
- Dev path:
- First skill:
- Next action:
```

When the user asks to solve or implement, do not stop after this block. Continue
with the selected skill and report the actual result.

## Boundaries

- Do not inflate a clear direct-dev task into a full SDLC package.
- Do not skip needed artifacts when scope, Architecture, Domain, release risk,
  or validation is unclear.
- Do not treat plugin installation as proof that custom agents are available.
- Do not claim MCP, Apps, or Hooks are bundled unless this plugin manifest
  actually declares them.
