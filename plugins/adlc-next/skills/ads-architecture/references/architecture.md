# Architecture method

Shared by `ads-architecture` and `sdlc-solve`. Decide module structure,
dependencies, interfaces, and technical choices at the depth the change needs.

## Size the decision

| Size | When | What to do |
|---|---|---|
| Local | The change fits the existing structure | Read the relevant existing decisions and follow them; record nothing new |
| Bounded | A new module, interface, or dependency inside one area | Decide briefly and record the reason in the task file or beside the code |
| Structural | Crosses modules or services, changes a public interface or data ownership, or affects a quality attribute such as performance or availability | Follow the steps below and record a decision |

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

The decision is sized correctly, its drivers and options are traceable, and
the affected interfaces and tests are named.
