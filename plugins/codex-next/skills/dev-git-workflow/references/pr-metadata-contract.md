# PR Metadata Contract

Use this contract when drafting, creating, editing, or validating a pull request
title or body. The headings may vary with repository conventions; the required
information and evidence may not.

## Contents

- [Evidence Basis](#evidence-basis)
- [Language and Audience](#language-and-audience)
- [Title Contract](#title-contract)
- [Body Contract](#body-contract)
- [Exact Delivery State](#exact-delivery-state)
- [Remote Readback Gate](#remote-readback-gate)
- [Prohibited Shortcuts](#prohibited-shortcuts)

## Evidence Basis

Build PR metadata from current evidence:

- the user's goal and explicit constraints;
- the nearest repository instructions, contribution guide, and PR template;
- the resolved base/head branches and the full base-to-head diff;
- the complete commit range, not only the latest commit subject;
- tests and checks actually run, including failures, pending checks, and skips;
- the current remote PR title, body, head SHA, state, and checks when updating;
- release, deployment, and runtime readback when those states are mentioned.

Do not use stale handoff notes or an implementation diary as the source of truth
when live Git, GitHub, release, or runtime evidence is available.

## Language and Audience

Choose the PR language in this order:

1. explicit user instruction;
2. repository instructions or required PR template;
3. the user's current conversation language;
4. established repository convention.

Keep code identifiers, paths, commands, API names, and error text exact. Do not
default to English merely because commit subjects or source code are English.

Write for a reviewer who has not read the agent session, implementation notes,
or an earlier PR. The reviewer should understand the purpose, scope, evidence,
and important constraints from the PR page alone.

## Title Contract

The title must:

- summarize the complete diff rather than a single commit;
- identify the affected scope or object and the action or result;
- stand alone without requiring an issue, previous PR, or chat thread;
- preserve a required repository prefix or conventional format without letting
  that format determine the language of the descriptive text;
- avoid claiming merge, release, deployment, or runtime outcomes not yet proven.

Avoid context-dependent titles such as `follow up`, `updates`, `cleanup`,
`misc fixes`, or `address feedback` unless the affected behavior and outcome are
also named.

## Body Contract

Keep the body proportional to the diff. Small PRs may combine sections, but a
reviewer-facing body must make these facts easy to find:

1. **Outcome and problem** - what was wrong or needed, and what this PR changes.
2. **Why** - the motivation or root cause when it materially affects review.
3. **Changes** - the important behavior, interface, data, or workflow changes.
4. **Impact and compatibility** - who or what is affected and what remains stable.
5. **Boundaries** - non-goals, deferred work, and states not reached.
6. **Validation** - commands/checks actually run and their decisive results;
   list failed, pending, flaky, or skipped checks honestly.
7. **Risks and constraints** - migration, rollback, merge-method, release, or
   runtime constraints that could change the review or merge decision.
8. **Review focus** - for non-trivial changes, point reviewers at the decisions
   or files that deserve the most attention.

Put decision-changing information on the first screen. A critical merge method,
data-loss risk, compatibility break, or "not deployed" boundary must not be
buried after implementation details or long validation lists.

## Exact Delivery State

Use state language that cannot be confused with a later delivery stage:

| Proven state | Accurate wording |
|---|---|
| Local commit only | committed locally; not pushed |
| Branch pushed | branch pushed; no PR unless one is confirmed |
| PR opened with base `main` | PR opened against `main`; not merged |
| Draft PR | draft; not ready for review unless explicitly changed |
| Checks passed | checks passed for the reported head; not proof of merge |
| PR merged | merged only after remote state confirms it |
| Release created | released only after the release/artifact is read back |
| Runtime updated | deployed only after the target runtime and version are read back |

Do not say the change is "in main", "submitted into main", or the equivalent in
another language for an open PR whose base is `main`. Name the base branch and
the unmerged state separately.

## Remote Readback Gate

After creating or editing a PR, read back at least:

- title and body;
- base and head branches;
- head SHA;
- open/closed/merged state and draft status;
- mergeability or merge state when available;
- checks and their status.

Confirm that the remote copy matches the current head and passes two tests:

- **First-screen test** - the result, problem, and any decision-changing
  constraint are visible before implementation detail.
- **Standalone reviewer test** - a reviewer without session history can identify
  why the PR exists, what changes, what does not, and how it was validated.

If new commits materially change the diff, update the metadata and run the gate
again.

## Prohibited Shortcuts

- Do not publish auto-filled title/body as final copy without reviewing it.
- Do not turn a terse commit subject into the PR title by default.
- Do not lead with an internal audit taxonomy, implementation diary, or long
  checklist before explaining the user-visible or maintainer-visible result.
- Do not include memory citations, private absolute paths, temporary body files,
  agent process labels, internal session URLs, credentials, or private data.
- Do not describe commands as passed when they were not run in the reported tree.
