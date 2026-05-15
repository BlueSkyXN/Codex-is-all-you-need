---
name: change-spec-adapter
description: Use to convert approved PRD/spec/tech/task artifacts into repository change-spec assets such as proposal, design, tasks, and spec deltas.
---

# Change Spec Adapter

## Purpose

Convert product-engineering artifacts into repository-ready change proposal, design, task, and behavior delta documents.

## Boundary

This workflow adapts existing artifacts. It does not redefine PRD scope, invent missing behavior, or implement code. OpenSpec-style output is supported when the repository uses that workflow, but the core pattern is repository change-spec handoff.

## Workflow

1. Read PRD, scope lock, functional spec, technical bridge, task breakdown, and readiness review.
2. Choose a stable change ID only from project convention or user instruction.
3. Produce proposal content from product intent, scope, and user value.
4. Produce design content from technical bridge decisions and open questions.
5. Produce task content from delivery-planning output.
6. Produce behavior or spec delta files from functional behavior changes.
7. Preserve open questions and assumptions instead of hiding them.

## Outputs

- `changes/{change-id}/proposal.md`
- `changes/{change-id}/design.md`
- `changes/{change-id}/tasks.md`
- `changes/{change-id}/specs/{domain}/spec.md` or equivalent behavior delta

Use templates in `references/` when a durable artifact is requested.

## References / Load When

- `references/openspec-proposal-template.md` - load when producing `proposal.md` for a change.
- `references/openspec-design-template.md` - load when producing `design.md` from an approved technical bridge.
- `references/openspec-tasks-template.md` - load when converting task cards into repository task format.
- `references/spec-delta-template.md` - load when producing behavior or spec deltas against existing repository specs.

## Validation

- The change does not expand beyond the scope lock.
- Proposal maps to PRD intent.
- Design maps to technical bridge, not unsupported architecture choices.
- Tasks map to delivery-planning output.
- Spec deltas are behavior-level and testable.
