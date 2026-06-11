---
name: api-contract-review
description: Use for designing or reviewing API contracts, including REST, GraphQL, OpenAPI, auth, pagination, versioning, errors, and backward compatibility.
---

# API contract review workflow

Use this workflow when API behavior is being designed, changed, reviewed, or documented.

## Steps

1. Establish current contract evidence.
   - Routes, handlers, schemas, serializers, generated clients, OpenAPI specs, docs, fixtures, tests, and live CLI/API output.

2. Define the boundary.
   - Resources or operations
   - Request shape
   - Response shape
   - Error format
   - Auth and permission behavior
   - Pagination, filtering, sorting, rate limits
   - Versioning and deprecation impact

3. Check compatibility.
   - Existing clients
   - Backward-compatible additions
   - Breaking changes
   - Migration path
   - Feature flags or staged rollout if needed

4. Validate semantics.
   - REST method/status-code semantics
   - GraphQL schema and resolver implications
   - Idempotency and retry behavior
   - Data validation and partial failure handling

5. Tie to tests.
   - Unit tests for validation and errors
   - Integration/API tests for success and failure paths
   - Contract tests or generated-client checks when available

## Output

Return:

1. Current contract evidence
2. Proposed or reviewed contract
3. Compatibility assessment
4. Test plan
5. Open questions

## Do not

- Do not invent API conventions when repo conventions are visible.
- Do not change auth, versioning, or response formats silently.
- Do not claim OpenAPI/client compatibility without checking the actual spec or generator path.
