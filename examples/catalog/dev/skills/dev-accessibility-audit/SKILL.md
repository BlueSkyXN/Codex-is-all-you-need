---
name: dev-accessibility-audit
description: Use to audit web/app accessibility, including semantics, keyboard flow, focus, labels, ARIA, contrast, and responsive behavior.
metadata:
  version: "0.3"
  updated: "2026-06-12"
---

# Accessibility audit workflow

Use this workflow when a frontend change or existing UI needs accessibility review.

## Steps

1. Define the scope.
   - Pages, routes, components, dialogs, forms, tables, navigation, or flows.
   - Target platforms and any stated compliance level.
   - Known user complaints or previous violations.

2. Collect evidence.
   - Source components and templates.
   - Existing tests, Storybook stories, screenshots, or browser states.
   - Design tokens for color, spacing, focus, and typography.

3. Check core interaction requirements.
   - Semantic HTML and landmark structure.
   - Keyboard-only navigation and visible focus.
   - Logical tab order and focus trapping for modals.
   - Labels, descriptions, errors, and required field announcements.
   - Button, link, menu, tab, combobox, table, and dialog roles.

4. Check perception and responsiveness.
   - Color contrast and non-color cues.
   - Text wrapping and zoom behavior.
   - Hit target size for touch interfaces.
   - Motion, animation, reduced-motion support, and loading states.

5. Validate with available tools.
   - Run lint, tests, browser inspection, accessibility tree snapshots, axe-like checks, or manual keyboard smoke tests when available.
   - Record what was not tested when assistive technology is unavailable.

6. Prioritize remediation.
   - Blocking issues that prevent task completion.
   - High-risk WCAG or keyboard failures.
   - Usability improvements and regression tests.

## Output

Return:

1. Scope reviewed
2. Blocking accessibility findings
3. Important non-blocking findings
4. Recommended fixes
5. Validation performed
6. Residual risk and untested assistive technology

## Do not

- Do not claim formal WCAG compliance without the required test evidence.
- Do not rely only on automated checks.
- Do not add ARIA when semantic HTML already solves the problem.
- Do not ignore keyboard and focus behavior.
