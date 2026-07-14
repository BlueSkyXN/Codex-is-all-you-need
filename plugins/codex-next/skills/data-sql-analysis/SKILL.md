---
name: data-sql-analysis
description: Use when reviewing or creating SQL for analysis, metric definitions, joins, filters, aggregation, and validation queries.
metadata:
  version: "0.2"
  updated: "2026-06-11"
---

# SQL Analysis Skill

Use this workflow for SQL review or SQL-based analysis.

## Steps

1. Identify the business question and expected output grain.
2. Review source tables and join keys.
3. Check join cardinality and risk of fan-out or dropped rows.
4. Check filters, date ranges, timezone assumptions, null handling, and status fields.
5. Review grouping, window functions, and aggregation logic.
6. Verify numerator, denominator, and metric definitions.
7. Add validation queries for row counts, totals, duplicates, and edge cases.
8. Explain limitations and ambiguous definitions.

## Do not

- Do not execute destructive SQL.
- Do not assume metric definitions that are not stated.
- Do not hide ambiguous filters, time ranges, or denominators.

## Output

Return:

1. Query purpose and grain
2. Logic review
3. Metric definition review
4. Risk list
5. Validation queries
6. Recommended changes
