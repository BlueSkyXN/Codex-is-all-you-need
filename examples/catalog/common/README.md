# Common Catalog

[中文](README_CN.md) | English

Shared agents and skills for planning, coordination, research of local docs, file organization, quality review, context handoff, and Codex project instruction design. These roles are domain-neutral and can be combined with `dev`, `data`, `office`, or `research` presets.

## Contents

```text
agents/
  common_context_summarizer.toml
  common_docs_researcher.toml
  common_file_organizer.toml
  common_orchestrator.toml
  common_quality_reviewer.toml
  common_task_planner.toml
skills/
  core-codex-agents-md-builder/
  core-explore-unknowns/
  core-goal-run/
  core-grilling/
  core-skill-eval/
```

## Agent Roles

- `common_task_planner`: split complex tasks into phases, deliverables, and validation steps.
- `common_orchestrator`: coordinate multi-step or cross-domain work and merge findings.
- `common_context_summarizer`: produce concise handoff briefings from long context.
- `common_docs_researcher`: verify local docs, official docs, CLI flags, and config keys.
- `common_file_organizer`: organize folders, drafts, materials, and indexes without deleting sources.
- `common_quality_reviewer`: review outputs for completeness, correctness, missed constraints, and unsupported claims.

## Skills

- `core-codex-agents-md-builder`: design, audit, or restructure repository `AGENTS.md` files for the Codex loading model.
- `core-explore-unknowns`: map knowns and unknowns before implementation when a request is ambiguous, underspecified, or unfamiliar.
- `core-goal-run`: execute, resume, and hand off work from a local goal or plan file using `goal-tasks.md` for status and `goal-log.md` for evidence and notes.
- `core-grilling`: interrogate a plan or design one question at a time until assumptions, tradeoffs, and edge cases are explicit.
- `core-skill-eval`: evaluate skill behavior against golden cases with blind runs, evidence-backed judging, and targeted improvements.

## Maintenance Notes

Keep this group broadly reusable. Do not add domain-specific implementation details here if they belong in `dev`, `data`, `office`, or `research`. Follow the publication boundary in `../PUBLIC-SUBSET.md` and the catalog rules in `../AGENTS.md`.
