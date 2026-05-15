# Data Catalog / 数据目录

[English](README.md) | 中文

这里存放数据画像、SQL 复核、可复现分析脚本、数据管道设计和数据结论复核相关的 agents 与 skills。本分组面向可公开的数据工作流，不应包含私有数据集或业务专属指标。

## 内容清单

```text
agents/   5 个数据相关 agents
skills/   4 个公开 skills
```

## Agent 角色

- `data_profile_analyst`：检查表格数据质量、缺失、重复和异常值。
- `data_sql_analyst`：复核 SQL 的 join、filter、aggregation、日期逻辑和指标定义。
- `data_script_builder`：创建可复现的 Python、SQL 或 shell 分析与转换脚本。
- `data_pipeline_engineer`：设计或复核 ETL/ELT 管道、质量检查、调度和监控。
- `data_insight_reviewer`：确认报告、图表、结论和建议是否有数据支撑。

## Skills

- `tabular-analysis`：可复现地分析 CSV、Excel、parquet 或表格类文件。
- `sql-analysis`：编写或复核分析 SQL、join、filter、指标和验证查询。
- `data-cleaning`：规划清洗、去重、缺失值处理和异常值处理。
- `analysis-report`：将分析结果整理成包含假设、发现、验证、限制和下一步的报告。

## 维护说明

示例应保持抽象，移除私有表名、凭证、数据集路径和业务专属指标定义。新增 agent 或 skill 时，确认它可以在单一公司或数据集之外复用，并按 `../AGENTS.md` 的命令验证结构。
