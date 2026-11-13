# Survey method

Shared by `ads-survey` and `sdlc-solve`. Establish how the project currently
stands on a question, with sources.

## Frame the question

State what needs to be known and which decision or task it serves. Survey only
what serves that question.

## Read in this order

1. Project instructions, README, and contribution documents.
2. Build, test, and CI configuration, for the real commands.
3. Structure: the entry points, modules, and dependencies relevant to the
   question.
4. Existing decisions: architecture notes, decision records, specs, domain
   documents, issues, and recent history that touches the area.
5. The code paths themselves, and the tests that pin their behavior.

Run read-only commands when they answer faster than reading.

## Record findings

Give each finding its source: `path:line`, a command and its output, a
document section, or a link. Keep three groups apart:

- **Facts** confirmed by the source.
- **Inferences**, with what they rest on.
- **Unknowns**, with how they could be resolved.

Where documentation and code disagree, the code's actual behavior is the fact
and the disagreement is itself a finding.

## Done

The question is answered or the remaining unknowns are named, every finding
has a source, and the relevant entry points and commands are listed.
