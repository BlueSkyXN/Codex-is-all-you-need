# Data Catalog

[中文](README_CN.md) | English

Agents and skills for data profiling, SQL review, reproducible analysis scripts, pipeline design, and evidence-backed insight review. This group is intended for public-safe data workflows, not private datasets or business-specific metrics.

## Contents

```text
agents/   5 data-focused agents
skills/   4 public skills
```

## Agent Roles

- `data_profile_analyst`: inspect tabular data quality, missingness, duplicates, and suspicious values.
- `data_sql_analyst`: review SQL joins, filters, aggregations, date logic, and metric definitions.
- `data_script_builder`: create reproducible Python, SQL, or shell scripts for analysis and transformations.
- `data_pipeline_engineer`: design or review ETL/ELT pipelines, checks, orchestration, and monitoring.
- `data_insight_reviewer`: verify that reports, charts, conclusions, and recommendations are supported by data.

## Skills

- `data-tabular-analysis`: summarize CSV, Excel, parquet, or table-like files reproducibly.
- `data-sql-analysis`: create or review SQL for analysis, joins, filters, metrics, and validation.
- `data-cleaning`: plan safe cleaning, deduplication, missing-value handling, and anomaly handling.
- `data-analysis-report`: turn analysis results into a clear report with assumptions, findings, validation, limits, and next steps.

## Maintenance Notes

Keep examples abstract and remove private table names, credentials, dataset paths, and business-only metric definitions. When adding an agent or skill, ensure it is reusable outside a single company or dataset and validate the structure from `../AGENTS.md`.
