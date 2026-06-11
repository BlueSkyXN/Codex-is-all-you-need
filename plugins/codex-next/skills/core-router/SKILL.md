---
name: core-router
description: Use as the Codex Next plugin entrypoint when the user asks to use Codex Next, route a task, choose the smallest SDLC/dev workflow, migrate external discussion into executable work, or coordinate public-safe Codex workflow skills.
---

# Codex Next Router

Codex Next is a workflow router for the skills bundled in this plugin. Use it to
choose the smallest useful path, then continue with the selected skill when the
user wants work completed.

This skill routes. It does not replace the underlying skills.

## Operating Model

For SDLC/ADS work, use:

```text
../sdlc-router/references/sdlc-operating-model.md
```

Core contract:

- Lanes: 快线, 增补, 重构, 重建, 从头.
- Modifiers: 规则变更, 发布.
- ADS: Architecture, Domain, Specification.
- IDs: `REQ`, `TASK`, `VAL`, `ARCH`, `DOM`, `DEC`, `Q`, `ITEM`.
- Dev paths: `direct-read`, `direct-dev`, `handoff-lite`,
  `handoff-full`, `blocked`.

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

## Route Table

| User intent | First skill |
|---|---|
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
