# ADLC Next

ADLC Next is a standalone plugin for handing a software task to an agent once
and having it carried through. The user states the goal and makes the
important trade-offs; the agent investigates, chooses the approach,
implements, checks, and reworks until the result reaches the requested
delivery point or a decision only the user can make comes up.

The package is deliberately light: three explicit-only skills, one shared set
of conventions, and one task-file template. It adds no scheduler, hooks,
background services, or scripts.

## Skills

| Skill | Use it when | Ends when |
|---|---|---|
| `sdlc-solve` | You want a problem or goal solved end to end, or a paused task resumed | The goal is met at the requested delivery point, or a pause condition applies |
| `sdlc-implement` | You already have a clear task description, spec, handoff, or task file | The specified change is implemented, self-checked, and reported |
| `sdlc-review` | You want a change, branch, PR, or design checked against its requirements | Every requirement and finding is classified as met, issue, or cannot judge |

Invoke them explicitly:

```text
$adlc-next:sdlc-solve        # Codex
/adlc-next:sdlc-solve        # Claude Code
```

The same pattern applies to `sdlc-implement` and `sdlc-review`. Everyday
questions and small edits keep the host's normal behavior.

Once `sdlc-solve` is invoked, it reads the implementation and review methods
itself and keeps going; you do not invoke the other two skills to continue the
same task. A standalone `sdlc-review` only reports unless the request also
asks for fixes.

## Skill groups

Skills are organized into four groups by what they work on. Group membership
is expressed by the name prefix and this index; the directory stays flat.

| Group | Prefix | Works on | Status |
|---|---|---|---|
| SDLC | `sdlc-` | Getting one task done | `sdlc-solve`, `sdlc-implement`, `sdlc-review` |
| ADS | `ads-` | Requirements, architecture, domain, and spec decisions | Planned |
| Tasks | `tasks-` | Relationships between several work items | Planned |
| Improvement | `improvement-` | How the work is done: docs, rules, skills, checks | Planned |

The groups are a classification, not stages every task must pass through.
Planned groups are added only when real tasks show a need for them.

## Invocation boundary

Each skill's `agents/openai.yaml` sets `allow_implicit_invocation: false`, so
Codex selects them only on explicit invocation. The shared `SKILL.md` files
omit Claude's `disable-model-invocation: true`, following the repository rule
that current Codex plugin ingestion rejects that field. Claude Code therefore
has no hard per-skill gate here: narrow descriptions reduce automatic
selection, and each skill body stops when it was not explicitly invoked.

Invoking a skill delegates investigation, local edits within scope, and local
checks. Commits, pushes, PRs, merges, releases, deployments, and other
external writes still follow the user's request, the project's instructions,
and the host's settings.

## Task file

`sdlc-solve` keeps a task file only when a task may span sessions, be handed
off, wait on external results, or has several stages. It uses the project's
working-notes location, or `local/<YYYYMMDD>-<topic>/TASK.md`, and keeps the
file out of commits. Status is `in-progress`, `paused`, or `done`, and the file
is updated while the work proceeds so that a new session can resume it.

## Package layout

```text
plugins/adlc-next/
├── .codex-plugin/plugin.json
├── .claude-plugin/plugin.json
├── README.md
└── skills/
    ├── sdlc-solve/
    │   ├── SKILL.md
    │   ├── agents/openai.yaml
    │   ├── assets/task-template.md
    │   └── references/conventions.md      # shared by all three skills
    ├── sdlc-implement/
    │   ├── SKILL.md
    │   ├── agents/openai.yaml
    │   └── references/implement.md        # also read by sdlc-solve
    └── sdlc-review/
        ├── SKILL.md
        ├── agents/openai.yaml
        └── references/review.md           # also read by sdlc-solve and fix requests
```

Maintenance rules:

- Each method has one source file, owned by the skill it is named after.
  Other skills reference it by relative path.
- Cross-skill reuse reads another skill's `references/` only, never its
  `SKILL.md`.
- Every directory under `skills/` is a skill with its own `SKILL.md`; do not
  add an entry-less shared directory.
- Each skill carries its own `metadata.version` per
  [Skill Versioning](../../docs/skill-versioning.md). The plugin version in the
  two manifests stays identical.
- These skills are plugin-only; they have no `examples/catalog/` mirror.

## Relation to Codex Next

ADLC Next is installed and versioned separately from `codex-next`. Some
`codex-next` skills also use the `sdlc-` prefix; there it marks document-driven
SDLC workflows such as BRD, PRD, and HLD. The plugin namespaces keep the
invocation names distinct. Enabling both plugins at once makes overlapping
workflows (for example `dev-bugfix`, `dev-pr-review`) available side by side;
when evaluating ADLC Next, record which plugins were enabled.

## Install

Add the repository marketplace, then install the plugin.

Codex:

```bash
codex plugin marketplace add https://github.com/BlueSkyXN/Codex-is-all-you-need.git
codex plugin add adlc-next@codex-is-all-you-need
```

Claude Code:

```bash
claude plugin marketplace add https://github.com/BlueSkyXN/Codex-is-all-you-need.git
claude plugin install adlc-next@codex-is-all-you-need
```

If the marketplace was added earlier with an explicit sparse path list, re-add
it with `plugins/adlc-next` included, as described for
[Visual Brainstorming](../visual-brainstorming/README.md#existing-sparse-marketplace-installs).

## Local development

```bash
python3 scripts/check_skill_metadata.py check --base-ref origin/main
claude plugin validate --strict plugins/adlc-next
git diff --check -- plugins/adlc-next
```

## Status

Version `0.1.0` is the first public state. Behavior on Codex and Claude Code
has not yet been exercised with representative tasks; trigger behavior,
cross-skill reference reading, and resume quality are the first things to
check in real use.

## License

ADLC Next follows the repository license declared in the root `LICENSE` file.
