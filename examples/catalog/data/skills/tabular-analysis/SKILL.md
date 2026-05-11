---
name: tabular-analysis
description: Use when the task involves profiling, cleaning, summarizing, or validating CSV, TSV, database exports, or spreadsheet-like tables.
---

# Tabular Analysis

## Workflow

1. Identify the input format, delimiter, encoding, sheet/table name, and row count.
2. Profile columns, data types, missing values, duplicate keys, and suspicious outliers.
3. Preserve raw inputs unless destructive editing is explicitly requested.
4. Use a reproducible script for non-trivial cleaning or aggregation.
5. Separate factual data quality findings from interpretation.

## Validation

- Report row counts before and after filtering.
- Check aggregate totals against the source when possible.
- Save derived outputs separately from raw inputs.
- Re-run the script from a clean shell if a script is created.

## Output

Provide:

- Source inventory.
- Data quality summary.
- Key metrics or findings.
- Reproducibility notes.
- Limits and assumptions.
