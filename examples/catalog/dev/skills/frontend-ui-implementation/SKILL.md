---
name: frontend-ui-implementation
description: Use for implementing or reviewing frontend UI, components, routing, state, responsive layout, accessibility, browser behavior, and API integration.
---

# Frontend UI implementation workflow

Use this workflow when building or changing a user-facing frontend experience.

## Steps

1. Read the existing UI system.
   - Framework
   - Routing
   - Component patterns
   - Styling system
   - Icons
   - State management
   - Tests
   - Existing visual language

2. Define the user workflow.
   - Main task
   - Empty/loading/error states
   - Permissions and disabled states
   - Mobile and desktop behavior
   - API assumptions

3. Implement within the system.
   - Reuse local components and tokens.
   - Keep text inside containers at all target widths.
   - Use familiar controls and icons where possible.
   - Preserve keyboard navigation and semantic markup.

4. Validate.
   - Typecheck/lint/build
   - Unit or component tests
   - Browser smoke test for meaningful UI changes
   - Screenshot checks across desktop and mobile when layout risk is nontrivial

5. Review integration.
   - API data shape
   - Error handling
   - Performance and bundle impact
   - Accessibility and focus behavior

## Output

Return:

1. User-visible change
2. Component/state/API impact
3. Files changed
4. Validation run
5. UI risks or follow-ups

## Do not

- Do not create a landing page when the task calls for an app/tool experience.
- Do not introduce a new visual style if the repo already has one.
- Do not skip real browser validation for substantial UI changes.
