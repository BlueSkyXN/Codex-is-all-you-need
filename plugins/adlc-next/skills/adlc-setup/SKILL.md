---
name: adlc-setup
description: "Explicit-only ADLC Next setup. Use only when the user invokes $adlc-next:adlc-setup or /adlc-next:adlc-setup to create or update local/adlc/adlc-next.toml, the personal defaults that all worktrees of the repository share, for task files, delivery point, work items, design records, and language. Not for work that was not delegated through this command."
disable-model-invocation: true
metadata:
  version: "0.1"
  updated: "2026-11-13"
---

# ADLC Setup

Create or update `local/adlc/adlc-next.toml`, the personal project settings
that ADLC skills read at the start of a run. All worktrees of the repository
share the copy in the main worktree.

## Activation

Run only when the current request invokes `$adlc-next:adlc-setup` (Codex) or
`/adlc-next:adlc-setup` (Claude Code). A descriptive request, or the command
quoted inside other content, does not count; if this skill was selected
without an invocation, stop using it and handle the request normally. The full
rule is in [the shared conventions](../sdlc-solve/references/conventions.md).

## Inputs

The repository, any existing `local/adlc/adlc-next.toml` in its main
worktree, and the preferences stated in the request.

## Workflow

1. Read [the shared conventions](../sdlc-solve/references/conventions.md) and
   [the settings example](assets/adlc-next.toml.example), which lists every
   key and its default.
2. Find the main worktree as the conventions describe; the file lives there
   even when this run is in a linked worktree. Then inspect the project:
   existing locations for working notes, task tracking, and design records;
   ignore rules, including whether `local/` is ignored; and how the project
   delivers changes.
3. Choose a value for each key from the request first, then from what the
   project already does. Omit keys whose value equals the default unless the
   user asked for them.
4. Write the file. When it exists, keep the user's keys and comments and
   change only what this request covers.
5. Check the result: it parses as TOML, every path is relative and stays
   inside the project, and each value is one the example allows.

## Output and completion

The path written and the final file content; for each non-default value, what
it changes and why it was chosen; and whether the settings file, `task_root`,
and
`work_items_file` are ignored by Git, with the ignore line to add for any that
is not.

## Boundaries

- Write only `local/adlc/adlc-next.toml` in the main worktree. Do not create
  a copy in a linked worktree, create task folders, move existing notes, or
  edit ignore rules; when an ignore rule is needed, show the line and leave
  the edit to the user.
- The settings file is personal working state: do not stage or commit it.
  When the user wants a default shared with the team, say that it belongs in
  the project instructions.
