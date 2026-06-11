---
name: dev-fullstack-feature
description: Use for planning and implementing features that span frontend, backend, API, database, scripts, or tests.
---

# Full-stack feature workflow

Use this workflow when a task spans multiple layers of an application.

## Steps

1. Define the feature boundary.
   - User-visible behavior
   - Backend behavior
   - API or CLI contract
   - Data model requirements
   - Non-goals

2. Map affected layers.
   - Frontend routes/components/state
   - API endpoints or CLI commands
   - Backend services
   - Database/schema/migrations
   - Tests and fixtures

3. Confirm contracts.
   - Request/response shapes
   - Error behavior
   - Auth and permissions
   - Backward compatibility

4. Plan implementation order.
   - Data/schema changes first if needed
   - Backend/API changes
   - Frontend/client changes
   - Tests and validation

5. Validate with layered checks.
   - Unit tests
   - Integration/API tests
   - Typecheck/lint/build
   - Manual reproduction if relevant

## Output

Return:

1. Feature scope
2. Affected layers
3. Implementation plan
4. Files likely to change
5. Validation plan
6. Risks and assumptions

## Do not

- Do not change API contracts silently.
- Do not add dependencies without approval.
- Do not skip tests for changed behavior.
- Do not let frontend and backend behavior drift.
