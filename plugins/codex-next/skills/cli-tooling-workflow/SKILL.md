---
name: cli-tooling-workflow
description: Use for designing, implementing, reviewing, or testing CLI tools, command surfaces, flags, config precedence, terminal output, and exit behavior.
---

# CLI tooling workflow

Use this workflow when a task changes or creates a command-line interface.

## Steps

1. Map the existing command surface.
   - Entry points
   - Help output
   - Subcommands
   - Flags and environment variables
   - Config file discovery
   - Output formats
   - Exit codes

2. Define user flows.
   - Human interactive use
   - Script/CI automation
   - Debug mode
   - Offline or failure behavior

3. Design compatibility.
   - Preserve existing flags and output where scripts may depend on them.
   - Add explicit non-interactive modes for automation.
   - Keep stdout/stderr separation intentional.

4. Implement ergonomically.
   - Clear help text
   - Useful error messages
   - Stable exit codes
   - Sensible defaults
   - Shell completion or config docs when appropriate

5. Validate.
   - Run `--help` or equivalent.
   - Run at least one success path and one failure path when feasible.
   - Add tests for parsing, config precedence, and exit behavior.

## Output

Return:

1. CLI surface
2. Compatibility notes
3. Implementation or review summary
4. Commands run
5. Remaining risks

## Do not

- Do not add prompts that block automation without a bypass.
- Do not silently change stdout, JSON shape, or exit codes.
- Do not invent config precedence without checking existing docs or code.
