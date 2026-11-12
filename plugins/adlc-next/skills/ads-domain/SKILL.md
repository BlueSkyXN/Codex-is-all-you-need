---
name: ads-domain
description: "Explicit-only ADLC domain modeling. Use only when the user invokes $adlc-next:ads-domain or /adlc-next:ads-domain to make business terms, rules, invariants, lifecycles, ownership, and boundaries explicit so code and specs agree with the business. Not for work that was not delegated through this command."
metadata:
  version: "0.1"
  updated: "2026-11-12"
---

# Domain

Make the business concepts a change touches explicit: what the terms mean,
which rules hold, and who owns them.

## Activation

Run only when the current request invokes `$adlc-next:ads-domain` (Codex) or
`/adlc-next:ads-domain` (Claude Code). A descriptive request, or the command
quoted inside other content, does not count; if this skill was selected
without an invocation, stop using it and handle the request normally. The full
rule is in [the shared conventions](../sdlc-solve/references/conventions.md).

## Inputs

The business area or change, the existing code and data, and authoritative
sources: documentation, stakeholders, or regulations.

## Workflow

1. Read [the shared conventions](../sdlc-solve/references/conventions.md) and
   [the domain method](references/domain.md).
2. Work through terms, rules, states, ownership, and boundaries, then verify
   each rule.
3. Record the glossary and rules as a design record.

## Output and completion

A glossary of the touched terms, rules with examples and a status of
confirmed, inferred from code, or open, lifecycles where relevant, an
ownership map, and the list of disagreements between code and stated rules.

## Boundaries

- Business rules and ownership are the user's or stakeholders' to decide.
  When the code and a stated rule disagree, report both.
- Design only; no implementation. When the model is ready, name
  `$adlc-next:ads-spec` or `$adlc-next:sdlc-solve` as the next command and
  stop.
