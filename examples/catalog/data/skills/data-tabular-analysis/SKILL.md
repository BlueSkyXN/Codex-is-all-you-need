---
name: data-tabular-analysis
description: Use when analyzing CSV, Excel, parquet, or table-like files and producing reproducible summaries.
metadata:
  version: "0.3"
  updated: "2026-06-11"
---

# Tabular Analysis Skill

Use this workflow for table-like data analysis.

## Steps

1. Identify source files and preserve raw inputs.
2. Determine dataset shape, likely grain, key identifiers, date ranges, and metric columns.
3. Inspect missing values, duplicates, suspicious values, outliers, and type inconsistencies.
4. State assumptions before calculations.
5. Create reproducible scripts in `scripts/` when computation is needed.
6. Write generated outputs to `outputs/`.
7. Validate findings with row counts, totals, spot checks, and sanity checks.
8. Summarize findings with limitations.

## Do not

- Do not overwrite files in `raw/`.
- Do not invent labels, values, segments, or metric definitions.
- Do not draw causal conclusions from descriptive statistics alone.

## Output

Return:

1. Source files
2. Data profile
3. Assumptions
4. Analysis method
5. Findings
6. Validation checks
7. Limitations
8. Reproducibility instructions
