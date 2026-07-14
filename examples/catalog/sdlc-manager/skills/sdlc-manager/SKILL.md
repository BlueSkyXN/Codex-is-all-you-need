---
name: sdlc-manager
description: Use as SDLC control plane for requirements, architecture, domain, specs, validation, RTM, readiness, change control, handoff, local/sdlc, and external proposal intake.
metadata:
  version: "0.2"
  updated: "2026-06-12"
---

# SDLC Manager

Use this skill as the SDLC entrypoint inside Codex Next. It manages which SDLC
workflow should run next, while keeping `sdlc-router` focused on lane, ADS, and
minimum-material classification.

This skill coordinates. It does not replace the authoring skills.

## Operating Model

For canonical lane, ADS, dev path, ID, `local/sdlc`, delivery card, and
midstream-intake vocabulary, follow:

```text
../sdlc-router/references/sdlc-operating-model.md
```

## Workflow

1. Identify whether this is SDLC work.
   - Requirements, BRD, URS, PRD, SRS, NFR, architecture, HLD, LLD, ADR,
     domain boundaries, SPEC, validation, traceability, readiness, handoff,
     change control, `local/sdlc`, or release-risk planning are SDLC work.
   - Clear implementation, bugfix, test execution, PR review, or release checks
     with no SDLC uncertainty should route to the relevant `dev-*` skill.

2. Decide whether routing is enough.
   - If the only need is lane, ADS, dev path, or minimum-material classification,
     use `sdlc-router`.
   - If a concrete artifact should be written or updated, choose the smallest
     authoring skill below.
   - If the user asks to implement and the SDLC path is already clear, route to
     `dev-spec-driven-implementation` or the relevant `dev-*` skill instead of
     stopping at planning.

3. Treat external proposals as reference input.
   - Web, GPT, other-AI, pasted chat, or research outputs are not executable
     truth until accepted by the user or supported by repository/local evidence.
   - Short external input can be summarized into the current state.
   - Long external input should be kept as external discussion before accepted
     pieces become `REQ`, `TASK`, or `VAL`.

## Route Table

| Need | Next skill |
|---|---|
| Lane, ADS, dev path, or minimum materials | `sdlc-router` |
| Existing repo capability map | `sdlc-project-research` |
| Requirements package | `sdlc-requirements-workflow` |
| Business, user, or product incubation | `sdlc-brd-workflow`, `sdlc-urs-workflow`, or `sdlc-prd-workflow` |
| Software requirements | `sdlc-srs-workflow` |
| Measurable quality constraints | `sdlc-nfr-spec` |
| Architecture or high-level design | `sdlc-hld-workflow` |
| Detailed design | `sdlc-lld-workflow` |
| Domain ownership or dependency boundaries | `sdlc-domain-boundary-modeling` |
| Modular monolith architecture | `sdlc-modular-monolith-architecture` |
| Durable architecture decision | `sdlc-architecture-decision-record` |
| Solution/spec package coordination | `sdlc-solution-spec-workflow` |
| Implementation-facing slice | `sdlc-spec-slice-writer` |
| Validation artifact | `sdlc-validation-plan-workflow` |
| Traceability | `sdlc-requirements-traceability` |
| Readiness review | `sdlc-readiness-review` |
| Baseline or scope change | `sdlc-change-control` |
| Dev handoff | `sdlc-dev-handoff-planning` |

## Output

When managing only, return:

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

When the user asks to solve, author, or implement, do not stop after routing.
Continue with the selected skill and report the actual result.

## Boundaries

- Do not turn clear direct-dev work into a full SDLC package.
- Do not bypass SDLC authoring when scope, Architecture, Domain, release risk,
  or validation baseline is unclear.
- Do not treat external proposals as accepted requirements without user or
  repository evidence.
- Do not let implementation silently rewrite SDLC baseline, architecture,
  domain, or traceability state.
