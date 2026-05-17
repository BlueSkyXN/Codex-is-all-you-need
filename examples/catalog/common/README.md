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
  codex-agents-md-builder/
```

## Agent Roles

- `common_task_planner`: split complex tasks into phases, deliverables, and validation steps.
- `common_orchestrator`: coordinate multi-step or cross-domain work and merge findings.
- `common_context_summarizer`: produce concise handoff briefings from long context.
- `common_docs_researcher`: verify local docs, official docs, CLI flags, and config keys.
- `common_file_organizer`: organize folders, drafts, materials, and indexes without deleting sources.
- `common_quality_reviewer`: review outputs for completeness, correctness, missed constraints, and unsupported claims.

## Skills

- `codex-agents-md-builder`: design, audit, or restructure repository `AGENTS.md` files for the Codex loading model.

## Maintenance Notes

Keep this group broadly reusable. Do not add domain-specific implementation details here if they belong in `dev`, `data`, `office`, or `research`. Follow the publication boundary in `../PUBLIC-SUBSET.md` and the catalog rules in `../AGENTS.md`.
