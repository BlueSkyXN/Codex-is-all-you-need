---
name: dev-security-review
description: Use to review software security across auth, permissions, input validation, secrets, dependencies, workflows, and config.
metadata:
  version: "0.3"
  updated: "2026-06-12"
---

# Security review workflow

Use this workflow when reviewing software for security risk.

## Steps

1. Scope the review.
   - Diff, module, endpoint, workflow, config, dependency, or repository area.
   - Identify trust boundaries and attacker-controlled inputs.

2. Inspect high-risk surfaces.
   - Authentication and authorization
   - Input validation and injection
   - File and path handling
   - Network calls and SSRF risk
   - Secrets and tokens
   - Deserialization and template rendering
   - CI/CD permissions
   - Dependency and supply-chain risk

3. Separate findings.
   - Confirmed vulnerability
   - Likely risk needing reproduction
   - Hardening suggestion
   - False positive or accepted risk

4. Provide evidence.
   - File path and symbol
   - Data/control path
   - Reproduction command or request when safe
   - Impact and exploit preconditions

5. Recommend fixes.
   - Minimal remediation
   - Tests or checks to add
   - Operational follow-up if code change is not enough

## Output

Return:

1. Findings by severity
2. Evidence
3. Exploit or failure path
4. Remediation
5. Test or verification plan

## Do not

- Do not report generic checklist items without repo evidence.
- Do not print or expose real secrets unnecessarily.
- Do not modify files when acting as a reviewer unless explicitly asked.
