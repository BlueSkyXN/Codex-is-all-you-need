---
name: readiness-review
description: Use to check whether PRD, spec, tech bridge, task plan, or change-spec artifacts are ready for the next phase. Reviews only.
---

# Readiness Review

## Purpose

Check whether product-engineering artifacts are complete, consistent, testable, traceable, and safe to hand off.

## Gate Types

- PRD to functional spec
- Functional spec to technical bridge
- Technical bridge to delivery planning
- Delivery plan to dev handoff
- Change-spec artifacts to repository workflow

## Workflow

1. Identify the current gate and required source artifacts.
2. Check completeness, scope control, assumptions, contradictions, and traceability.
3. Classify issues as Blocking, Major, Minor, or Advisory.
4. Produce readiness score and next-step recommendation.
5. Do not silently fix missing requirements; surface them unless the user asks for a rewrite.

## Outputs

- `review-report.md`
- `blocking-issues.md`
- `readiness-score.md`
- `next-step-recommendation.md`

Use checklists and templates in `references/` according to the current gate.

## References / Load When

- `references/prd-review-checklist.md` - load when reviewing PRD readiness for functional specification.
- `references/functional-spec-review-checklist.md` - load when reviewing behavior, state, field, permission, and acceptance-criteria readiness.
- `references/tech-bridge-review-checklist.md` - load when reviewing engineering bridge readiness for task planning.
- `references/task-readiness-checklist.md` - load when reviewing task cards before coding.
- `references/readiness-report-template.md` - load when producing `review-report.md`, `blocking-issues.md`, or next-step recommendations.

## Validation

- Findings cite artifact section names, requirement IDs, acceptance criteria IDs, or task IDs.
- Scope creep is called out explicitly.
- Assumptions and open questions are not treated as approved facts.
- The recommendation says exactly whether to proceed, revise, or stop.
