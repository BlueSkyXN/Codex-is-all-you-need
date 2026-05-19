# CSV Output Schema

The research pack has two layers:

- Markdown files explain the project and preserve readable evidence.
- CSV files under `tables/` are the manageable tracking data. They are meant to be imported into spreadsheets, Notion, Airtable, BI tools, or downstream reporting scripts.

CSV rows must stay short, evidence-backed, and ID-linked. Do not put long prose into CSV cells when a Markdown artifact already carries the detail.

## General rules

- Use UTF-8 CSV with a header row.
- Keep CSV file names and header names in stable English `snake_case` for import compatibility.
- Write human-readable cell content in Simplified Chinese unless the value is an ID, path, command, package name, API name, config key, code identifier, or exact source reference.
- Use stable IDs. Do not renumber unchanged rows on incremental runs.
- Use `parent_id` for hierarchy expansion.
- Use comma-separated ID lists only when a true many-to-many relationship is needed.
- Prefer references such as `CAP-001`, `FP-001`, `WP-001`, `EVD-001`, `BLK-001` over duplicated descriptions.
- Use `[UNKNOWN]` and `[INFERRED]` exactly as in the Markdown files.
- Do not include completion percentages, weights, scores, schedule dates, resource estimates, cost estimates, staffing assignments, tokens, secrets, credentials, private URLs, or raw personal data.

## Required CSV files by tier

Quick tier:

- `tables/capability_tree.csv`
- `tables/function_inventory.csv`
- `tables/blockers.csv`
- `tables/tracking_matrix.csv`

Standard tier:

- all quick CSV files
- `tables/product_structure.csv`
- `tables/wbs.csv`
- `tables/evidence_map.csv`
- `tables/maturity.csv`

Deep tier:

- all standard CSV files
- `tables/spec_candidates.csv`
- `tables/task_cards.csv` when WBS packages are drilled down

## `tables/capability_tree.csv`

One row per capability hierarchy node.

```csv
id,parent_id,level,type,name,description,status_tags,maturity,evidence_refs,source_refs,notes
CAP-000,,L0,project_goal,...
CAP-001,CAP-000,L1,capability_domain,...
CAP-001-01,CAP-001,L2,capability_module,...
FP-001,CAP-001-01,L3,function_point,...
SPEC-001,FP-001,L4,spec_candidate,...
```

Allowed `type` values: `project_goal`, `capability_domain`, `capability_module`, `function_point`, `spec_candidate`.

## `tables/function_inventory.csv`

One row per function point.

```csv
function_point_id,capability_id,module_id,name,actor_or_trigger,input,output,status_tags,spec_candidate_ids,evidence_refs,blocker_ids,next_action,confidence,source_refs
FP-001,CAP-001,CAP-001-01,...
```

Use this as the function-point inventory for later spec work.

## `tables/spec_candidates.csv`

Deep tier, or standard tier if the project has obvious spec gaps. One row per spec candidate.

```csv
spec_candidate_id,function_point_id,capability_id,actor_or_trigger,input,output,acceptance_signal,open_question,status,source_refs
SPEC-001,FP-001,CAP-001,...
```

Spec candidates are drafts, not approved functional specs.

## `tables/product_structure.csv`

One row per shipped or repo-visible product artifact.

```csv
product_id,parent_id,level,type,name,path_or_ref,role,linked_capability_ids,linked_function_point_ids,evidence_refs,notes
PBS-001,,subsystem,...
PBS-001-01,PBS-001,module,...
```

Allowed `type` values: `subsystem`, `module`, `component`, `integration`, `runtime_artifact`, `deployment_artifact`, `data_artifact`, `test_artifact`, `documentation`.

## `tables/wbs.csv`

One row per WBS work package. Standard tier stops at work-package level.

```csv
work_package_id,parent_id,level,title,linked_capability_ids,linked_function_point_ids,maturity_transition,tracking_status,management_unit,depends_on,blocked_by,definition_of_done,evidence_needed,source_refs
WP-001,,work_package,...
```

Allowed `tracking_status` values: `not-started`, `in-progress`, `blocked`, `done`, `deprecated`, `unknown`.

Allowed `management_unit` values: `yes`, `split-needed`, `merge-needed`, `unknown`.

Do not include person-weeks, target dates, cost, staffing, or owners unless a repository source explicitly provides an owner and the row is marked as evidenced owner metadata.

## `tables/evidence_map.csv`

One row per evidence claim.

```csv
evidence_id,object_type,object_id,evidence_type,path,line_or_range,evidence_strength,confidence,notes
EVD-001,function_point,FP-001,code,src/app.py,120,strong,high,...
```

Allowed `object_type` values: `capability`, `function_point`, `spec_candidate`, `product_item`, `work_package`, `blocker`, `maturity`.

## `tables/blockers.csv`

One row per blocker.

```csv
blocker_id,type,severity_scope,linked_capability_ids,linked_function_point_ids,linked_work_package_ids,symptom,hypothesis,attempted_fixes,next_step,blocks_e2e,source_refs
BLK-001,test,...
```

`severity_scope` is descriptive, not a score. Suggested values: `local`, `capability`, `e2e`, `deployment`, `unknown`.

## `tables/maturity.csv`

One row per capability maturity claim.

```csv
capability_id,baseline_maturity,critical_path_maturity,status_tags,evidence_refs,blocker_ids,reason,next_maturity_step,source_refs
CAP-001,M4,M6,...
```

`baseline_maturity` is the conservative capability maturity. `critical_path_maturity` records the maturity of the main demonstrable path when it differs from the baseline.

## `tables/tracking_matrix.csv`

The main importable management index. One row per tracked function point or work package.

```csv
tracking_id,row_type,capability_id,function_point_id,spec_candidate_id,product_ids,work_package_id,evidence_refs,status_tags,baseline_maturity,critical_path_maturity,blocker_ids,next_action,source_refs
TRK-001,function_point,CAP-001,FP-001,SPEC-001,PBS-001-01,WP-001,EVD-001,implemented;blocked,M4,M6,BLK-001,...
```

Allowed `row_type` values: `function_point`, `work_package`, `capability_summary`.

## `tables/task_cards.csv`

Deep tier only, and only for drilled-down WBS packages.

```csv
task_id,parent_work_package_id,title,role_hint,acceptance_signal,depends_on,blocked_by,evidence_needed,source_refs
WP-001-T1,WP-001,...
```

`role_hint` is a functional role such as `frontend`, `backend`, `data`, `AI`, `ops`, or `unknown`; it is not a staffing assignment.
