---
name: dev-python-quality
description: Use for Python implementation, typing, async, packaging, pytest, ruff/mypy checks, scripts, and performance cleanup.
---

# Python quality workflow

Use this workflow when Python code, packaging, tests, scripts, or modernization are the main task.

## Steps

1. Read project conventions.
   - `pyproject.toml`, `setup.cfg`, `setup.py`, `requirements*.txt`, `uv.lock`, `poetry.lock`
   - Test layout
   - Lint/type tools
   - Supported Python versions
   - Existing style patterns

2. Define the Python change.
   - API/service code
   - CLI/script
   - Data processing
   - Async/concurrency
   - Packaging
   - Modernization
   - Performance

3. Implement idiomatically.
   - Clear function boundaries
   - Type hints on public interfaces
   - Context managers for resources
   - Structured exceptions
   - Dataclasses or typed models when useful
   - Async only when it matches the I/O model

4. Validate.
   - Smallest relevant `pytest`
   - `ruff` or project linter
   - `mypy` or type checks when configured
   - Package/build checks if packaging changed
   - Performance check if performance was the goal

5. Keep compatibility explicit.
   - Python version
   - Dependency changes
   - Public API behavior
   - Script output and exit codes

## Output

Return:

1. Python scope
2. Implementation summary
3. Compatibility notes
4. Checks run
5. Remaining risk

## Do not

- Do not impose a formatter or type checker that the project does not use unless asked.
- Do not add heavy dependencies without approval.
- Do not rewrite working code just to match a preferred style.
