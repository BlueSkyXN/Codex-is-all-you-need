---
name: data-analysis-report
description: Use when converting data analysis results into a clear report with assumptions, findings, validation, limitations, and next steps.
metadata:
  version: "0.2"
  updated: "2026-06-11"
---

# Analysis Report Skill

Use this workflow to draft analysis reports.

## Report structure

1. Executive summary
2. Data sources and scope
3. Assumptions and metric definitions
4. Method
5. Key findings
6. Validation checks
7. Limitations
8. Recommendations or next steps
9. Reproducibility notes

## Rules

- Separate facts, calculations, interpretations, and recommendations.
- Include limitations before recommendations.
- Avoid unsupported causal language.
- Mention missing data or unresolved ambiguity.
- Tie claims to source data, scripts, queries, or output tables.

## Do not

- Do not present unsupported correlations as causation.
- Do not hide missing data, weak validation, or unresolved ambiguity.
- Do not invent metrics, source tables, query results, or business context.

## Output

Write reports to `reports/` unless instructed otherwise.
Return the report path, source materials used, and unresolved questions.
