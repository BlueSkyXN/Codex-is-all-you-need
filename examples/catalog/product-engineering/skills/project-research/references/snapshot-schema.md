# snapshot.json Schema

Persisted state of the most recent research run. Used by the next run to detect drift, capability removals, and target shifts (see `methodology.md` §6.5).

## Shape

```json
{
  "schema_version": 1,
  "project_root": "/abs/path/to/project",
  "scanned_at": "2026-05-19T00:00:00Z",
  "tier": "quick | standard | deep",
  "output_dir": "./local/research/",
  "project_signature": {
    "primary_language": "python",
    "frameworks": ["fastapi", "react"],
    "entry_points": ["services/api/main.py", "web/src/main.tsx"],
    "dependency_manifests": ["pyproject.toml", "web/package.json"],
    "deploy_configs": ["Dockerfile", "docker-compose.yml"],
    "test_dirs": ["tests/", "web/__tests__/"],
    "doc_dirs": ["docs/", "README.md"]
  },
  "capabilities": [
    {
      "id": "L1-tasks",
      "name": "task management",
      "maturity": "M5",
      "status_tags": ["implemented", "runnable", "blocked"],
      "function_points": [
        {
          "id": "FP-tasks-001",
          "name": "create task",
          "paths": ["services/api/tasks/routes.py:45-78"],
          "status_tags": ["implemented", "runnable", "tested"]
        }
      ]
    }
  ],
  "blockers": [
    {
      "id": "BLK-001",
      "type": "deployment",
      "title": "local Docker compose fails on db",
      "blocks_e2e": true,
      "first_seen": "2026-04-12"
    }
  ],
  "targets": {
    "explicit_goals_hash": "{stable hash of explicit-goal section}",
    "implicit_goals_hash": "{stable hash of implicit-goal section}",
    "last_shift_at": "2026-04-30"
  },
  "artifacts": {
    "markdown_files": [
      "capability-map.md",
      "product-structure.md",
      "work-breakdown.md",
      "tracking-matrix.md"
    ],
    "csv_tables": [
      "tables/capability_tree.csv",
      "tables/function_inventory.csv",
      "tables/product_structure.csv",
      "tables/wbs.csv",
      "tables/tracking_matrix.csv"
    ],
    "artifact_hashes": {
      "capability-map.md": "{sha256}",
      "tables/tracking_matrix.csv": "{sha256}"
    }
  },
  "removed_since_last_run": [
    {
      "kind": "function_point",
      "id": "FP-tasks-005",
      "was_in_snapshot": "{previous snapshot hash}",
      "reason": "code path no longer exists; commit def456"
    }
  ]
}
```

## Rules

- Append-only for `removed_since_last_run` within a run; cleared at the start of the next run after entries are copied to `target-shift-log.md`.
- `project_signature` is a fingerprint, not a full file list. Used to detect major project shape changes (language switch, framework swap) that warrant a full re-research rather than incremental update.
- `artifacts.csv_tables` records the CSV data layer produced by the run. `artifact_hashes` is used only for incremental drift checks; it is not a quality score.
- `schema_version` is bumped only when the shape changes incompatibly. Older snapshots remain readable; the skill upgrades them in place.
- Hashes are stable string hashes (sha256 of canonicalized text) used to detect goal drift without storing full goal text twice.
- Do not put scoring, weights, or completion percentages into this file. It is research state only.
