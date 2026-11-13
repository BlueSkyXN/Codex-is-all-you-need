# Codebase structure method

Shared by `ads-architecture`, `sdlc-implement`, `sdlc-review`, and
`sdlc-solve`. Decide or repair how code is divided into entry points, modules,
processes, packages, and directories, so that a change touches only the units
that have their own reason to change, and every dependency has a reason.

Use it within the steps for a structural decision in
[the architecture method](architecture.md); the rules under its Choosing
section apply throughout. The map records the current structure, the boundary
and split rules shape the options, and the change scenarios state the
consequences. Scale it to the decision: a single-package tool needs only its
entry points, the module that holds its rules, and its dependency rules.

## Separate the boundaries

Decide each kind of boundary on its own; they rarely line up one to one.

| Boundary | Question it answers | Examples |
|---|---|---|
| Entry point | Who uses the system, through which contract | CLI, GUI, web UI, HTTP or RPC API, SDK, plugin API |
| Module | Which rules change together, and who owns them | billing, export, sync, a computation engine |
| Process | What runs on its own | CLI process, desktop app, browser bundle, server, worker |
| Package | What is built, versioned, and released on its own | library, executable, container image, installer |
| Directory | Where files live | follows from the rows above and the build tool's layout |

Several entry points can share one module, one process can host many modules,
and a directory split does not need a package split.

- A **library** is a package that other code imports. An **SDK** is a
  contract for outside developers: a library or a client for a remote API,
  with documentation and a compatibility promise. Before publishing an
  internal library, narrow its exports to what outside developers should rely
  on: everything it exports becomes part of that contract.
- Entry points that talk across processes or languages share a contract with
  one source, such as a schema, an IDL file, or a shared types package. Each
  side is generated from that source or checked against it.

## Map the structure

Record one row per unit in scope. The directory tree follows from the map.

| Path | Kind | Owns | Runs in / ships as | Public interface | Must not depend on |
|---|---|---|---|---|---|

Kinds are entry point, module, adapter (database, network, file system, or
third-party service), contract, composition root (where a process is wired),
and build or tooling. Read the current map from the code: build manifests,
entry-point declarations, export lists, and the import graph from the
project's tools or a read-only command. In a proposal, mark the rows that
change.

## Diagnose an existing structure

For the pieces the task touches, ask whether they should change together, and
record each place where the code answers wrongly:

- **Hidden coupling:** pieces that must change together although the code does
  not show it, such as copies of a rule or value, a module that relies on state
  another sets, a call order callers have to remember, or one feature spread
  across distant directories.
- **Needless coupling:** pieces tied together that change for different
  reasons, such as callers that use another module's internals, stable code
  that imports volatile code, a general function with a parameter for one
  caller, or an interface that changes whenever its implementation does.
- **Unneeded structure:** pieces with no reason of their own to change, such
  as pass-through wrappers, extension points or settings for variation that
  does not exist, and dead code. First check that the piece carries no
  contract, such as access control, logging, compatibility, or a public
  export.

Special cases are clues: a branch for one value, a parameter for one caller, a
swallowed exception, a retry or sleep, a disabled test. Find out why each
exists. Some answer a real external constraint and stay, with the constraint
named; others mark a concept the design is missing.

Back each finding with code locations, and dependency findings with the
import graph. Treat files that change together in Git history as a lead to
confirm in the code: formatting, generated files, renames, and release commits
also move files together. In a large area, read symbols and signatures before
bodies.

Group the problems under the fewest fixes that remove them; one fix often
removes several problems that look unrelated. Write each fix above the
problems it solves.

## Split and lay out

A separate package or process needs at least one reason: a different
consumer, such as outside developers; a different release cadence or
compatibility promise; a different runtime or language; dependencies its
consumers must not inherit, such as server libraries in a client SDK; a
security or trust boundary; or independent scaling or failure isolation. Name
the cost as well: build and release configuration, versions, and changes that
must be coordinated across packages. A split moves the coupling between the
parts onto an interface or the network; it does not remove it. Without a
reason, use a module inside the existing package. Split or not, consumers of a
library or SDK do not inherit dependencies that only one entry point needs;
keep them apart with the build tool's own mechanism.

Lay out directories by the build tool's and framework's conventions first,
then by the project's existing layout. Within those, keep files that change
together close: group by capability when a package holds several, and by
technical layer within a capability or a small package. Prefer boundaries the
tools enforce, such as internal packages and export lists.

## Check with change scenarios

Pick two or three changes the project is likely to need, drawn from the task,
its issues and roadmap, or its history: for example a new command, a new
output format, a changed business rule, or a new field in a public response.
For each, list the units that must change, before and after the decision, and
why each one changes. The structure fits when every touched unit has its own
reason to change, no rule has to be updated by hand in several places, and no
unrelated unit is forced to change. Compare options by how many units each
scenario touches; that count is not a pass threshold.

Express each dependency rule as a check: a rule in the project's existing
tool when it has one, otherwise a read-only command that lists the imports the
rule forbids.

## Move code safely

- Change the structure the task needs. Other problems are follow-ups, and a
  reorganization the task does not need is a task of its own.
- Move code in steps small enough to check, and run the checks after each.
  Keep moves separate from behavior changes; when the delivery point includes
  commits, commit them separately.
- Keep public import paths, command names and flags, output formats, and
  exported names working, for example by re-exporting from the old location.
  Removing one is a compatibility decision for the user.
- Keep the existing tests passing at every step, and add focused tests first
  where the code being moved has none.

## Record

Keep the decision as a design record, as
[the shared conventions](../../sdlc-solve/references/conventions.md)
describe: the map, the dependency rules and their checks, the change scenarios
with before and after, and, for a repair, each fix with the problems it
solves.

## Done

Every unit in scope has a row in the map, shared areas are defined, every
split has a reason, the dependency rules have checks, the change scenarios
show which units each change touches and why, and problems outside the task
are recorded as follow-ups.
