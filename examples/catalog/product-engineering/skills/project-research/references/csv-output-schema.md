# Capability Table CSV Schema

Default output file:

```text
capability-table.csv
```

Use UTF-8 CSV with exactly this header:

```csv
l1_domain,l2_module,l3_function,function_desc,evidence,current_status,next_step,notes
```

## Columns

| Column | Meaning |
|---|---|
| `l1_domain` | L1 capability domain / subsystem, written in Simplified Chinese. |
| `l2_module` | L2 function group / module, written in Simplified Chinese unless it is an exact code/module name. |
| `l3_function` | L3 observable function point. |
| `function_desc` | Short description of the function point. |
| `evidence` | Code/doc/config/test path, or `[INFERRED] ...`, or `[UNKNOWN] ...`. |
| `current_status` | One of: `已规划`, `已设计`, `已开发`, `可运行`, `待验证`, `已废弃/重构`, `未发现证据`. |
| `next_step` | One concise next-step note for the L2 module. Repeating the same L2 note across rows is acceptable. |
| `notes` | Optional caveat, evidence limitation, or owner-confirmation need. Do not put long prose here. |

## Rules

- Do not create multiple CSV files by default.
- Do not add percentage, score, weight, schedule, cost, staffing, owner, maturity, WBS, PBS, blocker, or tracking-matrix columns.
- Keep values short enough for spreadsheet import and filtering.
- Redact secrets and personal data.
