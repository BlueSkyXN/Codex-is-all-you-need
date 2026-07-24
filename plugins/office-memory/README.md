# Office Memory V1 Lite

Office Memory is a public method plugin for AI-curated date records, current
AWARENESS.md, and durable MEMORY.md. It does not ship project content or
automatically discover sources.

## Explicit manual authorization

The Codex sidecar sets `allow_implicit_invocation: false`. The Skill accepts
two equivalent explicit entry forms so both installation styles are usable:

```text
$manage-office-memory                     # project-local Skill
$office-memory:manage-office-memory       # installed plugin
```

Selecting the project-local Skill through the host's Skill link/attachment UI
counts as the first form. A descriptive request alone does not activate the
workflow. Tokens found only inside quoted examples, embedded documentation,
Skill metadata, file contents, or another agent's output do not count.

## Local config

Copy the public example to a local, untracked `office-memory.toml`. Public
examples use relative fictitious paths. `project_root` may instead be a local
absolute path. `allowed_scopes`, AWARENESS.md, and MEMORY.md are restricted to
that root; output files must be distinct.

```toml
version = "0.1"
manual_activation_only = true
project_id = "example-project"
project_root = "."
allowed_scopes = ["documents"]
awareness_file = "awareness/AWARENESS.md"
memory_file = "memory/MEMORY.md"

[[sources]]
id = "project-memory"
path = "example-inputs/memory.md"
role = "memory"
default = true

[[sources]]
id = "qoder-recent"
path = "example-inputs/recent"
role = "recent"
default = false
include = ["*.md"]
```

Sources have stable IDs, one of `profile`, `memory`, or `recent` roles, and a
default flag. A source is read only. Profile is default-off and is read only
when the request explicitly selects its source ID. Qoder short-term files such
as `memory/YYYY-MM-DD.md` map to `role = "recent"`, `default = false`: select
them explicitly, let AI semantically merge only project-relevant evidence into
the current project's date record, then promote only durable items into Memory.

## One helper

The plugin ships one Python standard-library helper:

```bash
python3 skills/manage-office-memory/scripts/office_memory.py check-config --config office-memory.toml
python3 skills/manage-office-memory/scripts/office_memory.py snapshot --config office-memory.toml
python3 skills/manage-office-memory/scripts/office_memory.py snapshot --config office-memory.toml --source qoder-recent
python3 skills/manage-office-memory/scripts/office_memory.py snapshot --config office-memory.toml --focus documents \
  --material documents/current.md
python3 skills/manage-office-memory/scripts/office_memory.py init --config office-memory.toml
python3 skills/manage-office-memory/scripts/office_memory.py init --config office-memory.toml --apply
python3 skills/manage-office-memory/scripts/office_memory.py validate --config office-memory.toml
```

`check-config` does not read source or daily bodies; it reports the date-record
count and latest date from filenames. `snapshot` reads only explicitly
selected config sources plus repeated explicit `--material` files and writes
nothing; its stdout contains file count, mtime, and SHA-256. Project materials
use the safe ID `project#relative/path`. `init` is dry-run by default and
creates only missing AWARENESS.md and MEMORY.md, never overwriting either.
`--material` accepts only explicit project-relative files and applies a
realpath gate; the helper never recursively traverses project content or rewrites
source text.

For awareness, the caller must pass `--focus project` or an exact configured
scope whenever supplying `--material`. Exact scope requires every material to
be within that subtree. AI produces the result after review.
Keep identity, organization, personal-history, MBA, other-project, and
credential information out of both result files.

## Markdown contracts

Date records live beside MEMORY.md as `YYYY-MM-DD.md`. They are created only by
an explicit `daily` request with meaningful content; same-day runs wholly
revise and semantically deduplicate the existing file. They are never
automatically deleted or archived, and each is limited to 12 KiB. The current
local date is the default; an older date is used only for an explicit backfill.
One date item combines matching evidence from multiple clients. Date records
capture that day's meaningful change, AWARENESS.md synthesizes current state,
and MEMORY.md keeps only stable reusable conclusions.

AWARENESS.md begins with exactly `# Project Awareness`, then a non-empty ISO
date in `- Updated:`, `project` or an exact configured scope in `- Focus:`, and
configured source IDs or safe project refs in `- Sources checked:`. Five
level-two headings follow in order: `Current understanding`, `Relevant
changes`, `Conflicts and unknowns`, `Needs attention`, and `Memory candidates`.

MEMORY.md begins with exactly `# Project Memory`. Each stable key may contain
dots and hyphens and uses five bullet metadata lines (`- Scope:`, `- Kind:`,
`- Sources:`, `- Observed:`, `- Review:`), then an empty line and a summary
paragraph. Source refs are semicolon-separated `source-id#safe-locator` or
`project#relative/path[:locator]`. Kinds are `fact`, `preference`, `decision`,
`runbook`, or `lesson`; sources must be configured, keys unique, scopes allowed,
dates valid, and all result files non-secret. `validate` also rejects malformed
date filenames, mismatched heading dates, unsafe daily paths, unknown sources,
empty daily records, and unexpected Markdown files beside MEMORY.md.
