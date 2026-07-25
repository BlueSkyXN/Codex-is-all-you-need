---
name: core-router
description: Use when the user asks how to use Codex Next, which bundled skill fits, or whether a workflow is needed. Do not trigger for a clear task that can be completed directly.
metadata:
  version: "1.0"
  updated: "2026-07-26"
---

# Codex Next Router

Treat this skill as the optional discovery entrance to Codex Next, not as a
mandatory gateway. Recommend the smallest useful path and stop. Do not invoke,
reproduce, or begin the recommended workflow.

## Route Choices

Choose exactly one primary route:

1. **Direct execution** — no Codex Next skill is needed.
2. **One bounded skill** — the user already requested the result that skill
   produces, such as a PR review, HLD, weekly report, or data analysis.
3. **One explicit control workflow** — the work would introduce interrogation,
   persistent tracking, SDLC governance, readiness gating, change control, or
   multi-artifact coordination.

Direct execution is a successful routing result. Do not recommend a skill only
because one exists.

## Capability Map

- `core-*`: optional discovery, explicit plan interrogation, goal tracking, and
  skill evaluation.
- `dev-*`: implementation, diagnosis, review, Git, release, and focused
  engineering workflows.
- `sdlc-*`: user-requested requirements, design, validation, traceability, and
  explicit SDLC control workflows.
- `data-*`: bounded tabular, SQL, cleaning, and analysis-report work.
- `office-*`: bounded meeting, report, briefing, weekly-report, and presentation
  outline outputs.
- `research-*`: evidence tables, source deduplication, and synthesis from
  supplied or already mapped material.

## Decision Rules

1. Prefer direct work for clear, local, reversible, and verifiable requests.
2. Recommend a bounded skill only when its output matches the user's stated
   outcome without adding prerequisites or artifacts.
3. Do not infer that a midstream project needs BRD, PRD, SRS, HLD, RTM,
   readiness review, or a handoff package merely because those skills exist.
4. When a control workflow is justified, show its explicit `$skill` name and
   wait for the user to invoke or approve it. Authorization does not transfer
   from this router to another skill.
5. Ask at most one question, and only when its answer would change the primary
   route. Include the recommended default.

## Output

Return a compact recommendation:

```markdown
## Codex Next Route

- Path: direct / bounded skill / explicit control workflow
- Recommendation: <no skill or one skill name>
- Why: <one concrete sentence>
- Avoid: <unnecessary workflow or artifact, when relevant>
```

If the path is direct, write `Recommendation: no skill; complete the task
directly`.

## Boundaries

- Do not call another skill or imitate its workflow.
- Do not create or edit files, trackers, plans, or SDLC artifacts.
- Do not run commands, spawn agents, or change Git or external state.
- Do not turn ambiguity alone into an unknowns, grilling, or readiness process.
- Do not return several equally weighted routes. Recommend the best path; name
  one alternative only when a real user decision remains.
