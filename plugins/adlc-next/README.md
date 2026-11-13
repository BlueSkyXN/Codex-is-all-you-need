# ADLC Next

ADLC Next is a standalone plugin for agent-driven software delivery. You hand
a software task to the agent once; it investigates, chooses the approach,
implements, checks, and reworks until the result reaches the delivery point
you asked for, or until a decision only you can make comes up. Around that
core, the plugin provides design, work-item, and method-improvement skills.

`sdlc-solve` and `adlc-router` also start from a plain request; the other 18
skills run only on their command. The package adds no scheduler, hooks,
background services, or scripts: it is skills, shared methods, and two
templates.

## Using it

Invoke a skill with its plugin namespace. In Claude Code, start the message
with the command:

```text
$adlc-next:sdlc-solve        # Codex
/adlc-next:sdlc-solve        # Claude Code
```

You can also start `sdlc-solve` by handing a task over in plain words, for
example "see it through and verify it" or "take it all the way to a PR", or by
naming it. Questions, analysis, small edits, and work you direct step by step
stay with the host as usual.

For most tasks, `sdlc-solve` is the only skill you need: once started, it
reads the other skills' methods itself (survey, clarification, design,
test-first, bug-fix, review, shipping, handoff) and keeps going. Invoke
another skill when you want only that kind of result, for example a review
without fixes or a design without implementation. `adlc-router` answers when
you ask which ADLC skill fits, then stops.

## Skills

The skills fall into four groups by what they work on, plus two plugin-level
entries. Group membership is expressed by the name prefix; the directory stays
flat.

### SDLC: getting one task done

| Skill | Use it to | Ends when |
|---|---|---|
| `sdlc-solve` | Solve a problem end to end, or resume a paused task | The goal is met at the delivery point, or a pause condition applies |
| `sdlc-implement` | Build from a clear spec, handoff, or task file | The change is implemented, self-checked, and reported |
| `sdlc-review` | Check work against its current requirements | Every requirement and finding is classified as met, issue, or cannot judge |
| `sdlc-clarify` | Pin down an unclear request before work starts | Every blocking unknown is confirmed, assumed, or open with an owner |
| `sdlc-handoff` | Make an in-progress task resumable by someone else | The task file passes the receiver test and the code state is reachable |
| `sdlc-test-first` | Build behavior through red-green-refactor | Every behavior has a test seen failing and then passing |
| `sdlc-bugfix` | Reproduce, diagnose, fix, and guard a defect | The cause is explained and the original scenario passes |
| `sdlc-ship` | Take a verified change to commit, PR, merge, release, or real-environment verification | The requested stage is reached with evidence for each stage |

### ADS: requirements and design decisions

| Skill | Use it to | Ends when |
|---|---|---|
| `ads-survey` | Find out how the project currently works, with sources | The question is answered or the unknowns are named |
| `ads-requirements` | Settle the problem and its success conditions | Problem, outcome, scope, constraints, and success conditions are written |
| `ads-architecture` | Decide structure, codebase layout, dependencies, and interfaces | The decision is sized, reasoned, and recorded |
| `ads-domain` | Make business terms, rules, and ownership explicit | Terms are defined, rules have a status, and ownership is assigned |
| `ads-spec` | Write observable behaviors and completion criteria | Every in-scope requirement maps to verifiable items |

### Tasks: relationships between work items

| Skill | Use it to | Ends when |
|---|---|---|
| `tasks-intake` | Turn ideas, defects, and follow-ups into ordered work items | Items have outcomes, done conditions, dependencies, and an order |
| `tasks-wrap-up` | Review a batch against evidence and set up the next | Statuses are evidence-backed and the next batch is proposed |

### Improvement: how the work is done

| Skill | Use it to | Ends when |
|---|---|---|
| `improvement-retro` | Turn recurring friction into small, placed fixes | Each finding has evidence, cause, location, and an observation plan |
| `improvement-skill-eval` | Test whether a skill triggers and works | Every case has a judged result |
| `improvement-prompt-eval` | Compare prompts or instruction files by effect | Every case has a judged result and instruction findings are listed |

### Plugin-level

| Skill | Use it to | Ends when |
|---|---|---|
| `adlc-router` | Get a recommendation for which skill fits | One recommendation with its command is given |
| `adlc-setup` | Configure personal project defaults in `local/adlc/adlc-next.toml` | The settings file is written and checked |

## Invocation boundary

Two skills are visible to the model on both hosts; the other 18 are not.

- `sdlc-solve` and `adlc-router` set `allow_implicit_invocation: true` for
  Codex and omit Claude Code's `disable-model-invocation`. The model may start
  them when a request meets their activation rules: handing a whole task over,
  or asking which ADLC skill fits. When started this way, `sdlc-solve` says so
  in one line before it proceeds.
- The other 18 set `allow_implicit_invocation: false` and
  `disable-model-invocation: true`. They run only from their commands, and
  their descriptions stay out of the model's skill list. In Claude Code, a
  scheduled task or `/loop` passes their commands to the model as plain text
  instead of running them.

Codex ignores the Claude field. Each skill body checks its own start condition
and, when it was selected for a request that does not meet it, stops and
leaves the request to the host without recommending ADLC.

`disable-model-invocation` is not an Agent Skills specification field.
Validators that accept only specification fields reject it, for example Codex
`skill-creator`'s `quick_validate.py` and the checks for uploading a single
skill to claude.ai or the Skills API. Install the skills as this plugin: they
read each other's files, so they do not work as separate uploads.

Explicit invocation is not transitive. An active skill reads other skills'
`references/` and `assets/` as methods but never loads their `SKILL.md`. A
standalone skill whose result calls for a different kind of work names the
exact command and stops.

Starting a skill delegates investigation, local edits within scope, and local
checks. Commits, pushes, PRs, merges, releases, deployments, tracker writes,
and other external actions still follow the user's request, the project's
instructions, and the host's settings.

## Task file and settings

`sdlc-solve` keeps a task file only when a task may span sessions, be handed
off, wait on external results, or has several stages. It uses the project's
working-notes location, or `<task_root>/<YYYYMMDD>-<topic>/TASK.md` with
`task_root` defaulting to `local`, and keeps the file out of commits. Status
is `in-progress`, `paused`, or `done`, and the file is updated while the work
proceeds so a new session can resume it.

`adlc-setup` writes optional personal defaults to `local/adlc/adlc-next.toml`:
task root, default delivery point, work-item location, design-record location,
and language. Like the task file, it stays out of commits; defaults the whole
team should share belong in the project instructions, which take precedence
over it. The keys are listed in
[the settings example](skills/adlc-setup/assets/adlc-next.toml.example).

With Git worktrees, task files stay in the worktree where the task runs. The
settings file and the work-items file live in the main worktree, and every
linked worktree uses that copy; the host may ask for permission to reach it.

## Package layout

```text
plugins/adlc-next/
├── .codex-plugin/plugin.json
├── .claude-plugin/plugin.json
├── README.md
└── skills/
    ├── sdlc-solve/            SKILL.md, references/conventions.md, assets/task-template.md
    ├── sdlc-implement/        SKILL.md, references/implement.md
    ├── sdlc-review/           SKILL.md, references/review.md
    ├── sdlc-clarify/          SKILL.md, references/clarify.md
    ├── sdlc-handoff/          SKILL.md, references/handoff.md
    ├── sdlc-test-first/       SKILL.md, references/test-first.md
    ├── sdlc-bugfix/           SKILL.md, references/bugfix.md
    ├── sdlc-ship/             SKILL.md, references/ship.md
    ├── ads-survey/            SKILL.md, references/survey.md
    ├── ads-requirements/      SKILL.md, references/requirements.md
    ├── ads-architecture/      SKILL.md, references/architecture.md, references/structure.md
    ├── ads-domain/            SKILL.md, references/domain.md
    ├── ads-spec/              SKILL.md, references/spec.md
    ├── tasks-intake/          SKILL.md, references/work-items.md
    ├── tasks-wrap-up/         SKILL.md
    ├── improvement-retro/     SKILL.md
    ├── improvement-skill-eval/ SKILL.md, references/evaluation.md
    ├── improvement-prompt-eval/ SKILL.md
    ├── adlc-router/           SKILL.md
    └── adlc-setup/            SKILL.md, assets/adlc-next.toml.example
```

Every skill also has `agents/openai.yaml`.

Maintenance rules:

- Each method has one source file, owned by one skill, usually the one it is
  named after; other skills reference it by relative path. `references/conventions.md` is the
  single source for activation, authorization, delivery points, the task file,
  requirements, and reporting.
- Cross-skill reuse reads another skill's `references/` or `assets/` only,
  never its `SKILL.md`.
- Every directory under `skills/` is a skill with its own `SKILL.md`; do not
  add an entry-less shared directory.
- Each skill carries its own `metadata.version` per
  [Skill Versioning](../../docs/skill-versioning.md). The plugin version in the
  two manifests stays identical.
- These skills are plugin-only; they have no `examples/catalog/` mirror.
- `tests/test_adlc_next.py` checks the package contract in CI: skill set,
  frontmatter, invocation policy on both hosts, reference resolution, manifests,
  marketplace entries, and this index.

## Relation to Codex Next

ADLC Next is installed and versioned separately from `codex-next`. Some
`codex-next` skills also use the `sdlc-` prefix; there it marks
document-driven SDLC workflows such as BRD, PRD, and HLD. The plugin
namespaces keep invocation names distinct. Enabling both plugins at once makes
overlapping workflows, such as `dev-bugfix` and `dev-pr-review`, available
side by side; when evaluating ADLC Next, record which plugins were enabled.

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
python3 -m unittest tests.test_adlc_next -v
python3 scripts/check_skill_metadata.py check --base-ref origin/main
claude plugin validate --strict plugins/adlc-next
git diff --check -- plugins/adlc-next
```

## Status

Behavior on Codex and Claude Code has not yet been exercised with
representative tasks; which requests start `sdlc-solve` on each host,
cross-skill reference reading, whether structural changes reach the codebase
structure method, and resume quality are the first things to check in real
use, for example with `improvement-skill-eval`.

## License

ADLC Next follows the repository license declared in the root `LICENSE` file.
