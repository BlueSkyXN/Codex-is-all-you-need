# Feedback Loop Menu

Use this when the obvious test seam is missing or the loop is too slow, broad,
or flaky. Pick the smallest loop that goes red on the user's exact symptom.

| Loop | Use When | Minimal Shape | Tighten It |
|---|---|---|---|
| Failing test at the seam | The bug crosses a stable unit, integration, or e2e boundary. | Add one test that sets up the smallest failing case and asserts the exact symptom. | Avoid asserting implementation details. Keep setup data minimal. |
| `curl` or HTTP script | The symptom is an API, webhook, auth, routing, or response-shape failure. | Start a dev server, call one endpoint, assert status/body/header with `jq` or a small script. | Freeze env/config, use a fixture payload, and print only the decisive diff. |
| CLI fixture diff | A command produces bad stdout, stderr, exit code, files, or JSON. | Run command with a fixture directory, capture output, compare against a known-good snapshot. | Normalize temp paths, timestamps, ordering, and ANSI color. |
| Headless browser assertion | The bug is visible through DOM, console, network, routing, or hydration. | Navigate to one URL and assert the target state with a browser automation script. | Assert one user-visible symptom and capture console/network failures. |
| Replay trace or payload | You have a real request, event, trace, queue message, or log sample. | Feed the captured input into the parser/handler/reducer without external services. | Redact secrets, pin versions, and shrink the payload field by field. |
| Throwaway function harness | The code path is reachable with one direct call but has no test seam yet. | Create a temporary script that imports the target and prints a small verdict. | Keep it outside product code; delete it or turn it into a real test in Phase 6. |
| Property or fuzz loop | Output is sometimes wrong across many inputs or edge cases. | Generate many inputs, assert invariants, and print the seed or minimal counterexample. | Pin seed, store the counterexample, and reduce the input before fixing. |
| Bisection harness | The bug appeared between two commits, versions, configs, or data snapshots. | Script checkout/setup/test so `git bisect run` or equivalent can drive it. | Cache dependencies and make the verdict exit code unambiguous. |
| Differential old/new loop | One version, backend, serializer, or implementation is believed correct. | Run same input through both sides and diff outputs. | Normalize tolerated differences; assert only the contract that should match. |
| HITL bash script | A human must perform a step that cannot be automated yet. | Copy `scripts/hitl-loop.template.sh`, encode prompts, capture human verdicts as `KEY=VALUE`. | Make each human action precise, short, and repeatable; replace with automation when possible. |

Loop quality checklist:

- Red-capable: fails on the reported bug, not an adjacent issue.
- Fast: seconds where possible; narrow setup and cache slow prerequisites.
- Deterministic: pin time, seed randomness, isolate filesystem and network.
- Sharp: assert the smallest observable symptom.
- Agent-runnable: no hidden manual steps unless encoded in the HITL template.
