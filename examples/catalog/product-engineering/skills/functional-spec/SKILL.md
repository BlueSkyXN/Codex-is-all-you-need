---
name: functional-spec
description: "Use for behavior specs from a PRD or scope lock: flows, states, fields, permissions, UI states, errors, ACs, and traceability."
---

# Functional Spec

## Purpose

Translate confirmed PRD scope into implementation-ready behavior specification.

## Boundary

Functional spec work answers what exactly happens, in what state, under what condition, with what data, with what permissions, with what feedback, and how it is verified. It does not select final architecture, frameworks, database schema, or code-level implementation.

## Workflow

1. Read PRD, scope lock, and spec handoff.
2. Map PRD requirements to functional spec IDs.
3. Define main, alternative, and error flows.
4. Define states, transitions, triggers, guards, and user feedback.
5. Define fields, validation, default values, and error copy.
6. Define UI states and user-facing copy.
7. Define permission matrix and business rules.
8. Define acceptance criteria using Given / When / Then.
9. Produce traceability from PRD requirement to spec, acceptance criteria, test candidate, and task candidate.

## Outputs

- `functional-spec.md`
- `state-machine.md`
- `field-validation-spec.md`
- `ui-copy-error-spec.md`
- `permission-matrix.md`
- `acceptance-criteria.md`
- `traceability-matrix.md`

Use templates in `references/` when a durable artifact is requested.

## References / Load When

- `references/functional-spec-template.md` - load when producing the main `functional-spec.md`.
- `references/state-machine-template.md` - load when defining states, triggers, transitions, guards, and user feedback.
- `references/field-validation-template.md` - load when defining fields, defaults, validation rules, and error copy.
- `references/ui-copy-error-template.md` - load when defining loading, empty, success, failure, permission, timeout, or offline UI states.
- `references/permission-matrix-template.md` - load when roles or operations need explicit authorization rules.
- `references/acceptance-criteria-template.md` - load when writing Given / When / Then acceptance criteria.
- `references/traceability-matrix-template.md` - load when linking PRD requirements to spec sections, acceptance criteria, tests, and task candidates.

## Validation

- No P0/P1 PRD requirement is missing.
- No new feature is added without PRD support.
- Every user action has success and failure behavior.
- Every input has type, required status, validation, and error copy.
- Permissions are explicit for each role and operation.
- Acceptance criteria are testable.
