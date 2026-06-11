---
name: brd-workflow
description: Use to create or refine Business Requirements Documents covering business problem, goals, value, constraints, success metrics, risks, and investment rationale before product or software requirements.
---

# BRD Workflow

Use this skill to produce business requirements before product and software specification work.

A BRD explains why the work matters from a business or operating perspective. It should not define implementation details.

## Use when

- The request needs business justification before product requirements.
- Stakeholders need to align on business goal, value, expected result, constraints, or investment rationale.
- The work affects revenue, cost, growth, retention, operations, risk, compliance, support load, or strategic positioning.
- A feature idea is attractive but the business reason is unclear.
- A project may need system/program-depth materials because business risk, compliance, launch, or multi-wave coordination is material.

BRD is an incubation artifact. Do not require it for bugfix, clear small feature work, pure refactor, or direct-dev just because the SDLC suite contains this skill.

## Inputs

Collect:

- Business request, roadmap theme, strategy note, OKR, support escalation, sales/customer input, market evidence, or executive request.
- Current metrics, baseline performance, operating pain, cost, risk, or opportunity.
- Existing alternatives and why they are insufficient.
- Target business outcome and measurement window.
- Constraints: budget, time, team, compliance, partner, contractual, operational.

## Workflow

1. Define the business problem.
   - What is happening now?
   - Who is affected inside or outside the organization?
   - What measurable harm, cost, risk, or missed opportunity exists?
   - Why is now the right time?

2. Identify business objectives.
   - Primary business goal.
   - Secondary goals.
   - Non-goals.
   - Target release, milestone, or decision point.

3. Establish business value.
   - Revenue, retention, conversion, activation, usage, efficiency, support, risk reduction, compliance, quality, or strategic value.
   - Separate measurable value from narrative value.
   - State what evidence is available and what remains assumed.

4. Identify constraints and dependencies.
   - Budget or staffing.
   - Timeline or release window.
   - Legal, privacy, security, compliance, procurement, partner, operational constraints.
   - Internal or external dependencies.

5. Define success metrics.
   - Baseline.
   - Target.
   - Measurement method.
   - Observation window.
   - Owner.

6. Decide downstream artifact needs.
   - URS needed?
   - PRD needed?
   - NFR needed?
   - SRS needed?
   - SPEC slices needed?
   - RTM needed?

## Output

Return a BRD with:

1. Business context
2. Problem statement
3. Business objectives
4. Value hypothesis
5. Scope and non-scope at business level
6. Success metrics
7. Constraints and dependencies
8. Risks and mitigations
9. Downstream requirement needs
10. Open decisions

## Recommended Markdown structure

```markdown
# BRD: <Name>

## 1. Document Control
- Owner:
- Status: Draft / Review / Baseline / Changed
- Version:
- Source materials:
- Related artifacts:

## 2. Business Context
-

## 3. Business Problem
-

## 4. Business Objectives
| ID | Objective | Priority | Success signal |
|---|---|---|---|

## 5. Business Value
| Value area | Expected value | Evidence | Confidence |
|---|---|---|---|

## 6. Scope
### In Scope
-

### Out of Scope
-

## 7. Success Metrics
| Metric | Baseline | Target | Measurement method | Window | Owner |
|---|---|---|---|---|---|

## 8. Constraints
| Constraint | Type | Impact | Owner |
|---|---|---|---|

## 9. Risks
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|

## 10. Downstream Artifacts
- URS:
- PRD:
- NFR:
- SRS:
- SPEC:
- RTM:

## 11. Open Decisions
| ID | Decision needed | Required before | Owner |
|---|---|---|---|
```

## Validation

Check that:

- The business problem is not merely a feature request.
- At least one success metric or evidence signal exists.
- Business goals do not contradict the stated non-goals.
- Constraints are explicit.
- The BRD can guide PRD/URS/SRS without forcing implementation design.
- The cost of not doing the work is visible when relevant.

## Boundaries

- Do not write implementation plans.
- Do not prescribe architecture, code structure, database schema, or API design.
- Do not invent market data, financial projections, or customer evidence.
- Do not promote a solution before the business problem is clear.
- Do not use vague claims such as “improve experience” without a measurable or observable signal.

## Handoff

After BRD:

- Use `urs-workflow` to define users, tasks, scenarios, and constraints.
- Use `prd-workflow` to define product scope, features, user flows, and acceptance.
- Use `nfr-spec` if business risk implies security, privacy, availability, performance, compliance, or reliability requirements.
- Use `requirements-traceability` once downstream requirements and tasks exist.
