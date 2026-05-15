---
name: prd-workflow
description: "Use for idea-to-PRD work: concept PRD, scope lock, detailed PRD, and spec handoff. Not for API, schema, tasks, or code."
---

# PRD Workflow

## Purpose

Turn vague product ideas into scoped, reviewable Product Requirements Documents that can be handed off to functional specification.

## Boundary

PRD work answers why to build, who it serves, what to build, what not to build, and how success is measured. It does not define final architecture, API contracts, database schemas, or implementation tasks.

## Workflow

1. Intake the idea, users, scenarios, constraints, target platform, timing, and business assumptions.
2. Separate evidence, guesses, risks, blockers, and open questions.
3. Diagnose from user, business, and technical lenses.
4. Cut MVP scope and list explicit non-goals.
5. Produce a short concept PRD when the idea is still early.
6. Produce a scope lock before detailed PRD work.
7. Produce a detailed PRD with flows, states, fields, copy, exceptions, privacy/data notes, and high-level acceptance criteria.
8. Produce a spec handoff for functional-spec.

## Outputs

- `concept-prd.md`
- `scope-lock.md`
- `prd.md`
- `spec-handoff.md`

Use templates in `references/` when a durable artifact is requested.

## References / Load When

- `references/concept-prd-template.md` - load when producing `concept-prd.md` from an early idea or discovery conversation.
- `references/scope-lock-template.md` - load before detailed PRD work or whenever MVP boundaries must be frozen.
- `references/detailed-prd-template.md` - load when producing the durable `prd.md` artifact.
- `references/spec-handoff-template.md` - load when preparing the handoff into `functional-spec`.

## Validation

- Target user, problem, MVP goal, in-scope, out-of-scope, success metrics, and P0 features are explicit.
- P0 features have acceptance summaries.
- Major user-facing actions include loading, empty, success, failure, permission, timeout, or offline behavior when applicable.
- Input fields include type, required status, validation, and error copy when applicable.
- Assumptions are not written as facts.
- No technical implementation decision is invented.
