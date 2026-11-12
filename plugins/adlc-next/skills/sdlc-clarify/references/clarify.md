# Clarification method

Shared by `sdlc-clarify`, `sdlc-solve`, and the ADS skills. Find out what a
request needs without asking the user for anything the material or the code
can answer.

## Sort the unknowns

List what is unknown about the goal, scope, constraints, acceptance, and
delivery point, then sort each item:

| Kind | Example | Action |
|---|---|---|
| Answered by existing material | The issue already names the failing endpoint | Cite the source; do not ask |
| Answerable by investigation | Which modules call the function | Read code, docs, or history, or run a read-only command |
| Needs the user's intent or decision | Whether partial refunds are in scope | Ask |
| Technical unknown | Whether the library supports streaming | Resolve with a small experiment, or record it as a risk |

## Ask well

- Ask only what blocks the work or changes its result. Batch the questions you
  have now, most consequential first.
- For each question, say why it matters and give the options, with a
  recommended default when you have one, so the user can answer briefly.
- Do not ask for what you can find, and do not ask about cases that would not
  change the work.
- When a new question appears later, ask it then and say why it appeared now.

## Record

- **Confirmed:** the point and its source (user message, issue, document, or
  code).
- **Assumed:** the point and why it is a safe default. Work may proceed on it.
- **Open:** the point, who decides, and what it blocks.

Acceptance conditions must be observable: someone else can tell whether they
hold.

## Done

No item that blocks the work is left unsorted. Each one is confirmed, assumed,
or open with an owner.
