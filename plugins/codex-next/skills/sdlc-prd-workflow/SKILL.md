---
name: sdlc-prd-workflow
description: Use to draft or refine PRDs covering product goals, scope, features, user flows, priorities, exceptions, and acceptance criteria.
---

# PRD Workflow

Use this skill to produce product requirements after business and user direction is clear enough to define product behavior.

A PRD defines what the product should deliver and how success will be accepted. It should not replace SRS, NFR, SPEC, dev handoff, or implementation work.

## Use when

- A feature, product change, MVP, app, module, or product workflow needs formal product requirements.
- The user wants a PRD that can be handed to design, SRS, SPEC, or dev planning.
- The product scope, non-scope, user flows, states, fields, copy, exceptions, or acceptance criteria are unclear.
- AI coding would otherwise proceed from vague product intent.

## Inputs

Collect:

- BRD, URS, requirements package, user feedback, research notes, roadmap item, stakeholder request, or concept note.
- Existing product behavior, repo evidence, screenshots, prototype, design draft, or capability map.
- Business constraints, platform constraints, delivery window, success metrics.
- Required downstream artifacts: SRS, NFR, UI SPEC, API SPEC, Data SPEC, Dev Handoff, RTM.

## Workflow

1. Align product direction.
   - Product goal.
   - Target users.
   - Core scenario.
   - Scope and non-scope.
   - Success metrics.
   - Required release or delivery constraints.

2. Freeze the product scope baseline.
   - State what is in scope.
   - State what is out of scope.
   - State what may be future scope.
   - State what assumptions require confirmation.
   - If the trade-off set is still contested, run `core-grilling` on it before
     freezing the decision.
   - Do not proceed to detailed product requirements when core scope is unresolved.

3. Define feature list and priority.
   - Feature ID.
   - Feature name.
   - User value.
   - Priority.
   - Required for this delivery profile?
   - Related user requirement or business objective.

4. Detail each core feature.
   - User flow.
   - State machine.
   - Field rules.
   - Copy rules.
   - Exception handling.
   - Permissions.
   - Data or tracking notes, when needed.
   - Acceptance criteria.

5. Prepare downstream handoff.
   - Which PRD items become SRS requirements?
   - Which features need UI/API/Data/Admin/Permission SPEC?
   - Which NFRs are implied?
   - Which items need traceability IDs?
   - Which decisions block dev?

## Required detail coverage

For every core product behavior, cover these areas:

1. User flow
   - Entry point
   - Normal path
   - Alternative path
   - Exit path
   - Recovery path

2. State machine
   - Initial state
   - Empty state
   - Loading state
   - Success state
   - Failure state
   - Disabled or unavailable state
   - Permission-limited state

3. Field rules
   - Required or optional
   - Type
   - Format
   - Length
   - Default
   - Validation
   - Error message

4. Copy rules
   - Button text
   - Empty state
   - Loading message
   - Success message
   - Failure message
   - Confirmation text
   - Tone and localization notes

5. Exception handling
   - Network failure
   - Timeout
   - No data
   - Permission denied
   - Duplicate submit
   - Conflict
   - Validation failure
   - Dependency unavailable

## Output

Return a PRD with:

1. Product summary
2. Scope baseline
3. Feature list and priorities
4. User flows
5. State machine details
6. Field rules
7. Copy rules
8. Exception handling
9. Acceptance criteria
10. Downstream SRS/SPEC/NFR/handoff needs

## Recommended Markdown structure

```markdown
# PRD: <Name>

## 1. Document Control
- Owner:
- Status: Draft / Review / Baseline / Changed
- Version:
- Related BRD:
- Related URS:
- Related project/repo:
- Target release:

## 2. Product Summary
-

## 3. Goals and Success Metrics
| Goal | Metric | Baseline | Target | Window |
|---|---|---|---|---|

## 4. Target Users and Scenarios
-

## 5. Scope Baseline
### In Scope
-

### Out of Scope
-

### Future Scope
-

## 6. Feature List
| Feature ID | Feature | Priority | User value | Related UR/BR |
|---|---|---|---|---|

## 7. Feature Details

### F-001: <Feature>
#### User Flow
| Step | User action | System response | Next state |
|---|---|---|---|

#### State Machine
| State | Enter condition | Allowed actions | Exit condition | Next state |
|---|---|---|---|---|

#### Field Rules
| Field | Required | Type | Limit | Validation | Error copy |
|---|---|---|---|---|---|

#### Copy Rules
| Scenario | Copy | Tone | Notes |
|---|---|---|---|

#### Exceptions
| Exception | Trigger | User feedback | Recovery | Logging / tracking |
|---|---|---|---|---|

#### Acceptance Criteria
- Given ...
- When ...
- Then ...

## 8. Dependencies and Risks
| Item | Type | Owner | Risk | Mitigation |
|---|---|---|---|---|

## 9. Downstream Artifacts
- SRS requirements needed:
- NFR items needed:
- SPEC slices needed:
- Dev handoff needed:
- Traceability needed:

## 10. Open Questions
| ID | Question | Required before SRS/dev? | Owner |
|---|---|---|---|
```

## Validation

Check that:

- Scope and non-scope are explicit.
- Each core feature has a user flow, states, field rules, copy rules, exceptions, and acceptance criteria.
- Acceptance criteria are testable.
- Product behavior does not depend on hidden assumptions.
- User, business, and delivery constraints are not mixed with implementation instructions.
- Downstream SRS/SPEC/NFR/handoff needs are visible.

## Boundaries

- Do not edit code.
- Do not define final architecture, database schema, or code-level implementation.
- Do not omit negative paths, empty states, loading states, permission states, or field validation for core behavior.
- Do not treat future scope as current scope.
- Do not mark requirements as confirmed unless they are confirmed by the user or source material.

## Handoff

After PRD:

- Use `sdlc-srs-workflow` to convert product behavior into software requirements.
- Use `sdlc-nfr-spec` for quality, security, privacy, performance, availability, accessibility, compatibility, observability, or compliance.
- Use `sdlc-spec-slice-writer` for UI/API/Data/Admin/Permission/Directory specs.
- Use `sdlc-dev-handoff-planning` only after SRS/SPEC inputs are sufficient for implementation tasks.
