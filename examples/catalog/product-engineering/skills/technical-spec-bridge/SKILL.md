---
name: technical-spec-bridge
description: "Use to turn functional specs into engineering bridge artifacts: architecture context, API/data drafts, NFRs, test draft, and open questions."
---

# Technical Spec Bridge

## Purpose

Translate behavior-level functional specification into engineering discussion artifacts without pretending to be the final architecture authority.

## Boundary

This workflow produces drafts and decision inputs. Final architecture, API compatibility, database migrations, code edits, and release checks should be handled by dev agents and repo-aware workflows when implementation begins.

## Workflow

1. Read functional spec, state machine, field spec, permissions, and acceptance criteria.
2. Identify affected capabilities, modules, data entities, APIs, integrations, and non-functional requirements.
3. Draft architecture context with options and tradeoffs.
4. Draft API contracts only where behavior requires an external or internal boundary.
5. Draft data model and persistence implications.
6. Draft security, privacy, reliability, accessibility, performance, compatibility, and observability requirements.
7. Draft test plan by test level and risk.
8. List engineering decisions that need repository evidence or owner approval.

## Outputs

- `technical-spec-brief.md`
- `architecture-brief.md`
- `api-contract-draft.md`
- `data-model-draft.md`
- `nfr-security-privacy.md`
- `engineering-open-questions.md`
- `test-plan-draft.md`

Use templates in `references/` when a durable artifact is requested.

## References / Load When

- `references/technical-spec-brief-template.md` - load when producing the main `technical-spec-brief.md`.
- `references/architecture-brief-template.md` - load when outlining modules, dependencies, system context, and boundaries.
- `references/api-contract-draft-template.md` - load when drafting request, response, and error contracts for engineering review.
- `references/data-model-draft-template.md` - load when drafting entities, fields, relationships, and constraints.
- `references/nfr-security-privacy-template.md` - load when specifying performance, reliability, privacy, security, observability, compatibility, or compliance needs.
- `references/engineering-open-questions-template.md` - load when separating draft assumptions from engineering decisions required.
- `references/test-plan-draft-template.md` - load when deriving unit, integration, E2E, edge, regression, or manual test implications.

## Validation

- Confirmed requirements and engineering assumptions are separate.
- Frameworks, dependencies, and architecture patterns are not introduced without constraints or evidence.
- API, data, and NFR items link back to functional requirements.
- Compatibility, migration, security, privacy, observability, rollback, and release concerns are visible.
