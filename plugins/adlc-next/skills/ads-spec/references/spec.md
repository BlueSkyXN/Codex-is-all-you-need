# Spec method

Shared by `ads-spec` and `sdlc-solve`. Turn confirmed goals and design
decisions into observable behaviors and completion criteria that
implementation and review both use.

## Write each behavior

One item per behavior:

- a given-when-then statement, or an equivalent plain statement, of the
  observable behavior;
- the source it rests on: a requirement, a decision, or a domain rule;
- how it will be verified: a test, a command, or an observation point.

Cover normal cases, edge cases, error and failure cases, and existing
behavior that must not change. Add performance, security, or compatibility
criteria only where they matter for this change, each with a threshold.

## Check

- Someone else can judge each item met or not met.
- No item prescribes implementation unless the implementation is itself the
  requirement.
- Conflicting items are resolved, or given to the user.
- Every in-scope requirement maps to at least one item.

## Record and maintain

Write the spec as a design record, as described in
[the shared conventions](../../sdlc-solve/references/conventions.md);
task-sized specs can live in the task file. Keep one set of completion
criteria: a task file references the spec instead of copying it. When a
requirement changes, update the spec and apply the conventions' change
procedure.

## Done

Every in-scope requirement maps to observable items with a verification
method, and the spec's location is recorded.
