---
name: sdlc-architecture-decision-record
description: Use to record ADRs covering choices, tradeoffs, alternatives, consequences, status, and links to requirements/design evidence.
---

# Architecture Decision Record


Use this skill when an architecture choice needs to be recorded.

## Use when

- A system/module/API/data/deployment/security decision has long-term impact.
- Multiple alternatives exist.
- Dev needs to know why an approach is chosen.
- A decision affects HLD, LLD, SPEC, RTM, or future implementation.

## Inputs

- SRS, NFR, HLD, LLD, SPEC, project constraints, repo evidence.
- Alternatives and trade-offs.
- Decision owner and status.

## Workflow

1. Identify the decision.
2. State context and forces.
3. List considered options.
4. Record decision and rationale.
5. Record consequences.
6. Link affected artifacts.
7. Define review/expiry condition if needed.

## Validation

Check:

- Decision is specific.
- Alternatives are visible.
- Consequences are honest.
- Links to affected artifacts are included.
- Status is clear: proposed / accepted / superseded / rejected.

## Output

Return an ADR:

```markdown
# ADR-000: <Decision>

## Status
proposed / accepted / superseded / rejected

## Context

## Options considered

## Decision

## Consequences

## Related artifacts

## Review condition
```

## Boundaries

- Do not use ADR for every trivial code choice.
- Do not record decisions without owner or context.
- Do not edit code.
- Do not require ADRs for direct-dev tasks unless the task creates an architecture decision.

## Handoff

Use ADR links in HLD, LLD, SPEC, RTM, and Dev Handoff when relevant.

Dev fallback: Dev can use SDLC / ADD / DDD / SDD materials when they exist, but dev can also continue without them when the task is clear, bounded, and testable from user request, issue, bug report, failing test, local diff, or repository evidence. Missing artifacts are risk/context, not automatic refusal.
