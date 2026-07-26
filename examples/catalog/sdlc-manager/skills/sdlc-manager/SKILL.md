---
name: sdlc-manager
description: Use only when the user explicitly invokes this skill to plan and route a multi-artifact SDLC/ADS workstream without automatically invoking downstream skills.
metadata:
  version: "1.1"
  updated: "2026-07-26"
---

# SDLC Manager

Use this skill as the explicit SDLC coordination entrypoint inside Codex Next.
It recommends which workflow the user should invoke next, while keeping lane,
ADS, and minimum-material classification in the dedicated router workflow.

This skill coordinates. It does not replace the authoring skills.

## Operating Model

For canonical lane, ADS, dev path, ID, `local/sdlc`, delivery card, and
midstream-intake vocabulary, follow
`../sdlc-router/references/sdlc-operating-model.md`.

## Workflow

1. Identify whether this is SDLC work.
   - Requirements, BRD, URS, PRD, SRS, NFR, architecture, HLD, LLD, ADR,
     domain boundaries, SPEC, validation, traceability, readiness, handoff,
     change control, `local/sdlc`, or release-risk planning are SDLC work.
   - Clear implementation, bugfix, test execution, PR review, or release checks
     with no SDLC uncertainty should route to the relevant `dev-*` skill.

2. Recommend the smallest next step.
   - If the only need is lane, ADS, dev path, or minimum-material classification,
     recommend `$codex-next:sdlc-router` and stop.
   - If a concrete artifact should be written or updated, recommend the
     smallest authoring skill below.
   - If implementation is already ready, recommend
     `dev-spec-driven-implementation` or the relevant `dev-*` skill.
   - If the recommendation is an explicit-control skill, return its exact
     `$codex-next:<skill-name>` command and stop for the user to invoke it.
   - Do not invoke, imitate, or begin the recommended workflow. Explicit
     authorization for this manager does not transfer to another skill.

3. Treat external proposals as reference input.
   - Web, GPT, other-AI, pasted chat, or research outputs are not executable
     truth until accepted by the user or supported by repository/local evidence.
   - Summarize short external input in the routing response.
   - For long external input, recommend an optional discussion artifact but do
     not create it. Accepted pieces become `REQ`, `TASK`, or `VAL` through the
     recommended authoring skill, not through this manager.

## Route Table

| Need | Next skill |
|---|---|
| Lane, ADS, dev path, or minimum materials | `$codex-next:sdlc-router` |
| Existing repo capability map | `sdlc-project-research` |
| Requirements package | `$codex-next:sdlc-requirements-workflow` |
| Business, user, or product incubation | `sdlc-brd-workflow`, `sdlc-urs-workflow`, or `sdlc-prd-workflow` |
| Software requirements | `sdlc-srs-workflow` |
| Measurable quality constraints | `sdlc-nfr-spec` |
| Architecture or high-level design | `sdlc-hld-workflow` |
| Detailed design | `sdlc-lld-workflow` |
| Domain ownership or dependency boundaries | `sdlc-domain-boundary-modeling` |
| Modular monolith architecture | `sdlc-modular-monolith-architecture` |
| Durable architecture decision | `sdlc-architecture-decision-record` |
| Solution/spec package coordination | `$codex-next:sdlc-solution-spec-workflow` |
| Implementation-facing slice | `sdlc-spec-slice-writer` |
| Validation artifact | `sdlc-validation-plan-workflow` |
| Traceability | `sdlc-requirements-traceability` |
| Readiness review | `$codex-next:sdlc-readiness-review` |
| Baseline or scope change | `$codex-next:sdlc-change-control` |
| Dev handoff | `sdlc-dev-handoff-planning` |

## Output

Return:

```markdown
## SDLC Manager Route

- Intent:
- Current evidence:
- SDLC need:
- Next skill:
- Why:
- Not needed:
- Next action:
```

## Boundaries

- Do not create or edit files or external state.
- Do not invoke, imitate, or begin a downstream skill.
- Do not treat approval of a recommendation as explicit invocation.
- Do not turn clear direct-dev work into a full SDLC package.
- Do not bypass SDLC authoring when scope, Architecture, Domain, release risk,
  or validation baseline is unclear.
- Do not treat external proposals as accepted requirements without user or
  repository evidence.
- Do not let implementation silently rewrite SDLC baseline, architecture,
  domain, or traceability state.
