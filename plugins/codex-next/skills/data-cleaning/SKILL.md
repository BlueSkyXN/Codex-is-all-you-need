---
name: data-cleaning
description: Use when planning safe data cleaning, deduplication, missing-value handling, anomaly handling, and reproducible cleaned outputs.
---

# Data Cleaning Skill

Use this workflow for data cleaning plans or scripts.

## Steps

1. Identify raw inputs and preserve them unchanged.
2. Define the target output format and location.
3. Classify issues: missing values, duplicates, type errors, invalid categories, outliers, date problems, and inconsistent identifiers.
4. Decide handling rules and document assumptions.
5. Implement cleaning in a reproducible script if requested.
6. Write cleaned outputs to `outputs/` or a task-specific directory, not `raw/`.
7. Validate before/after row counts, key counts, missingness, and edge cases.

## Do not

- Do not overwrite raw files.
- Do not silently drop rows or impute values without documenting rules.
- Do not treat outliers as errors without evidence.

## Output

Return:

1. Cleaning issues found
2. Cleaning rules
3. Files/scripts created
4. Before/after validation
5. Residual risks
