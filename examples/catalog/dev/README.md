# Development Catalog

[中文](README_CN.md) | English

Agents and skills for software engineering work: repository exploration, implementation, review, testing, security, documentation, API design, frontend, backend, performance, release, and Git workflows.

## Contents

```text
agents/   14 development agents
skills/   20 public skills
```

## Agent Groups

- Mapping and planning: `dev_code_mapper`, `dev_architect_reviewer`, `dev_docs_researcher`.
- Implementation: `dev_implementer`, `dev_backend_engineer`, `dev_frontend_engineer`, `dev_python_engineer`, `dev_cli_engineer`.
- Review and validation: `dev_code_reviewer`, `dev_security_reviewer`, `dev_test_runner`, `dev_performance_engineer`.
- Design and documentation: `dev_api_designer`, `dev_docs_engineer`.

## Skills

```text
dev-accessibility-audit      dev-api-contract-review      dev-bugfix
dev-build-optimization       dev-cli-tooling-workflow     dev-dependency-upgrade
dev-frontend-ui-implementation
dev-fullstack-feature        dev-git-workflow             dev-migration-plan
dev-performance-diagnosis    dev-pr-review                dev-prompt-evaluation
dev-python-quality           dev-refactor-plan            dev-release-check
dev-repo-onboarding          dev-security-review          dev-spec-driven-implementation
dev-test-strategy
```

## Usage Notes

Use this catalog when the task involves a codebase, build system, API, UI, test suite, security surface, or release workflow. It is SDLC-aware: when SRS, NFR, HLD, LLD, ADR, Domain Boundary Map, SPEC slices, handoff, or traceability materials exist, dev agents should follow them. Missing SDLC artifacts are a risk signal, not an automatic stop condition for clear direct-dev tasks. Prefer read-only mapper/reviewer agents before broad implementation. Keep examples and instructions framework-neutral unless a skill explicitly targets a known tool family.

## Maintenance Notes

Do not add project-private architecture, secret workflow names, internal endpoints, or company-specific release rules. New development skills should state trigger conditions, workflow steps, validation expectations, output format, and clear limits.
