---
name: urs-workflow
description: Use to create or refine User Requirements Specifications covering users, roles, jobs, scenarios, constraints, current alternatives, user value, and acceptance-relevant user outcomes.
---

# URS Workflow

Use this skill to produce user requirements before or alongside PRD/SRS work.

A URS explains who the users are, what they need to accomplish, where the current experience fails, and what user outcomes must be supported.

## Use when

- Target users, roles, personas, jobs, or scenarios are unclear.
- A product idea may be solving a self-imagined or poorly evidenced problem.
- The work depends on user behavior, frequency, environment, device, permissions, accessibility, or support context.
- A feature needs user stories, journeys, scenarios, or user outcome acceptance criteria.
- PRD or SRS would be speculative without user requirements.

## Inputs

Collect:

- User interviews, support tickets, analytics, feedback, sales notes, community posts, bug reports, or stakeholder descriptions.
- User roles and permission models.
- Current workflows and alternatives.
- Frequency, environment, device, channel, and context of use.
- User constraints: time, skill, accessibility, compliance, privacy, trust, cost, network, device, locale.

## Workflow

1. Identify user groups.
   - Primary users.
   - Secondary users.
   - Admin or operator users.
   - Reviewers, approvers, support users, or auditors.
   - Excluded users.

2. Define user jobs and scenarios.
   - What is the user trying to accomplish?
   - What triggers the scenario?
   - What does the user do today?
   - Where does the current workflow fail?
   - What does success look like from the user perspective?

3. Map user constraints.
   - Device, platform, language, network, location, ability, permission, account state.
   - Time pressure, trust, error tolerance, privacy sensitivity.
   - Domain knowledge or skill level.

4. Write user requirements.
   - Use clear user requirement IDs.
   - Express user need, not implementation.
   - Add priority and evidence.
   - Link to product requirements when available.

5. Prepare acceptance-relevant scenarios.
   - Happy path.
   - Alternative path.
   - Error path.
   - Empty, loading, success, failure, permission, timeout, duplicate action, and unavailable-data states.

## Output

Return a URS with:

1. User groups
2. User jobs and scenarios
3. Current alternatives
4. User pain and desired outcome
5. User constraints
6. User requirements
7. Scenario coverage
8. Open questions
9. PRD/SRS inputs

## Recommended Markdown structure

```markdown
# URS: <Name>

## 1. Document Control
- Owner:
- Status:
- Version:
- Related BRD:
- Related PRD/SRS:

## 2. User Groups
| ID | User group | Role | Frequency | Notes |
|---|---|---|---|---|

## 3. User Jobs
| Job ID | User | Job to be done | Trigger | Success outcome |
|---|---|---|---|---|

## 4. Current Alternatives
| User | Current method | Pain | Evidence |
|---|---|---|---|

## 5. User Scenarios
### USCN-001: <Scenario name>
- User:
- Context:
- Trigger:
- Current path:
- Desired path:
- Success outcome:
- Constraints:

## 6. User Requirements
| UR ID | Requirement | Priority | Evidence | Related PRD/SRS |
|---|---|---|---|---|

## 7. Scenario Coverage
| Scenario | Happy path | Alternate path | Error path | Edge cases |
|---|---|---|---|---|

## 8. Open Questions
| ID | Question | Required before PRD/SRS? | Owner |
|---|---|---|---|
```

## Validation

Check that:

- Each core user has a concrete scenario.
- User needs are not merely internal stakeholder preferences.
- The URS separates user problem from product solution.
- Current alternatives and pain are visible.
- User constraints are explicit enough to influence PRD, SRS, NFR, and SPEC.
- Edge cases are not postponed when they are required for acceptance.

## Boundaries

- Do not write detailed product features unless the user requirement is already clear.
- Do not prescribe UI layout, API shape, data schema, or implementation.
- Do not invent personas or usage frequency.
- Do not ignore accessibility, language, device, permission, or trust constraints when they affect user success.
- Do not claim user validation when the input is only stakeholder opinion.

## Handoff

After URS:

- Use `prd-workflow` to turn user requirements into product scope and feature behavior.
- Use `srs-workflow` to turn user requirements into software-facing requirements.
- Use `nfr-spec` if user constraints imply accessibility, performance, privacy, security, reliability, localization, or compatibility requirements.
- Use `spec-slice-writer` when scenarios require UI, API, Data, Admin, Permission, or Release slices.
