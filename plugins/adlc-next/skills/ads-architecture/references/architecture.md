# Architecture method

Shared by `ads-architecture` and `sdlc-solve`. Decide module structure,
dependencies, interfaces, and technical choices at the depth the change needs.

## Size the decision

| Size | When | What to do |
|---|---|---|
| Local | The change fits the existing structure and does not have to be repeated in copies elsewhere | Read the relevant existing decisions and follow them; record nothing new |
| Bounded | A new module, interface, dependency, shared area, or top-level directory inside one area, or a change that has to be repeated in several copies of one rule | Check the options against the rules under [Choosing](#choosing), decide briefly, and record the reason in the task file or beside the code |
| Structural | Crosses modules or services, changes a public interface or data ownership, affects a quality attribute such as performance or availability, or sets how the code is divided: a new project, a new kind of entry point, or a package or process split or merge | Follow the steps below and record a decision |

A structural decision about how the code is divided, and a task to untangle
existing structure, also follow
[the codebase structure method](structure.md).

## Steps for a structural decision

1. **Drivers.** The requirements and quality attributes that constrain the
   choice, with sources, and the existing decisions that still hold.
2. **Current structure.** The modules, dependencies, and interfaces involved,
   read from the code.
3. **Options.** Two or three viable options, including the smallest change to
   the current structure. For each: how it meets the drivers, cost, risk,
   reversibility, and impact on existing modules.
4. **Decision.** The chosen option and why; what was rejected and why.
5. **Consequences.** Affected interfaces, data, migrations, and tests; what
   becomes easier or harder; how to tell later that the decision was wrong.
6. **Domain fit.** Module boundaries should follow business ownership. When
   they conflict, use [the domain method](../../ads-domain/references/domain.md)
   before settling.

## Choosing

Prefer the option that fits the existing structure and conventions, meets the
drivers, and is easiest to reverse. Add abstraction only for variation that
exists now.

New and changed code follows these rules:

- Code that changes for the same reason lives together; code that changes for
  different reasons is not tied together.
- Each business rule has one home. Entry points, such as a CLI command, a GUI
  action, a web route, an API handler, or an SDK method, translate their input
  and output and call that home; they keep only their own presentation and
  interaction.
- Dependencies point toward code that changes less, and modules form no
  cycles.
- Business rules and reusable use cases take configuration and dependencies
  as parameters and report through results and errors. They do not read the
  environment or global configuration, write to the terminal, or exit the
  process: output belongs to the entry point, and the exit code to the process
  boundary.
- Configuration is loaded and refreshed, and implementations are chosen, in
  one place owned by the entry point, which passes the results in.
- A public interface exposes only what its consumers are meant to depend on.
  A framework, third-party, or storage type in it is a deliberate dependency:
  record that choice and the versions or compatibility it commits to.
- A shared area, such as `core`, `common`, `shared`, or `utils`, states in a
  short note beside it what it holds, what it must not hold, and who uses it.
- When the current change touches several copies of one rule that must change
  together, change every copy, and give them one source, merged or generated,
  when that is small; otherwise record it as a follow-up. A copy that has to
  stay, such as client-side validation that mirrors the server's, names its
  source. Code that only looks alike and changes for different reasons stays
  separate.

Where the framework the project builds on prescribes another arrangement,
such as reading configuration through its settings object, follow the
framework. When following a rule would mean restructuring beyond the task,
follow the existing structure and record the gap as a follow-up, as
[the shared conventions](../../sdlc-solve/references/conventions.md)
describe.

## Record

Write structural decisions as a decision record in the project's existing
format and location, following the design-record rule in
[the shared conventions](../../sdlc-solve/references/conventions.md). Mark a
superseded decision instead of deleting it.

## User decisions

Choices that change compatibility, cost, external commitments, or a confirmed
goal go to the user with the options and a recommendation. Purely technical
choices within the drivers are made here.

## Done

The decision is sized correctly, its drivers and options are traceable, the
affected interfaces and tests are named, and rule gaps left in place are
recorded as follow-ups.
