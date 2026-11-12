---
name: adlc-router
description: "Explicit-only ADLC Next guide. Use only when the user invokes $adlc-next:adlc-router or /adlc-next:adlc-router to ask which ADLC Next skill, if any, fits a software request. Recommends one path with its exact command and stops without doing the work. Not for work that was not delegated through this command."
metadata:
  version: "0.1"
  updated: "2026-11-12"
---

# ADLC Router

Recommend one path for a software request, with the exact command, and stop.

## Activation

Run only when the current request invokes `$adlc-next:adlc-router` (Codex) or
`/adlc-next:adlc-router` (Claude Code). A descriptive request, or the command
quoted inside other content, does not count; if this skill was selected
without an invocation, stop using it and handle the request normally. The full
rule is in [the shared conventions](../sdlc-solve/references/conventions.md).

## Workflow

1. Read the request. When its size or kind is unclear, glance at the project's
   README and instructions; do not start the work.
2. Choose one recommendation: **direct**, meaning no ADLC skill is needed
   because it is a question, a small edit, or a clear one-step task; or one
   skill from the table below.
3. Reply with the recommendation, the reason in one or two sentences, the
   exact command in both forms (`$adlc-next:<skill>` and
   `/adlc-next:<skill>`), and what to include with it. Mention at most one
   alternative. Then stop.

| Situation | Skill |
|---|---|
| Solve a problem end to end, or resume a paused task | `sdlc-solve` |
| Build from a clear spec, handoff, or task file | `sdlc-implement` |
| Check work against its requirements | `sdlc-review` |
| Pin down an unclear request before work starts | `sdlc-clarify` |
| Hand a task to another session, agent, or person | `sdlc-handoff` |
| Build a behavior strictly test-first | `sdlc-test-first` |
| Reproduce and fix a specific defect | `sdlc-bugfix` |
| Commit, open a PR, merge, release, deploy, or verify a finished change | `sdlc-ship` |
| Find out how the project currently works | `ads-survey` |
| Settle the problem and its success conditions | `ads-requirements` |
| Decide structure, dependencies, or interfaces | `ads-architecture` |
| Clarify business terms, rules, or ownership | `ads-domain` |
| Write behaviors and completion criteria | `ads-spec` |
| Turn many ideas, defects, or follow-ups into ordered work items | `tasks-intake` |
| Review a batch of work and plan the next one | `tasks-wrap-up` |
| Find recurring friction after a task and fix its cause | `improvement-retro` |
| Test whether a skill triggers and works | `improvement-skill-eval` |
| Compare prompts or instruction files | `improvement-prompt-eval` |
| Configure ADLC defaults for this project | `adlc-setup` |

When the user wants a finished result and several skills fit, recommend
`sdlc-solve`: it uses the other skills' methods itself.

## Boundaries

- The router recommends only. It does not invoke or imitate the recommended
  skill, create files, or start the work.
- Approving the recommendation is not an invocation; the user runs the
  command.
