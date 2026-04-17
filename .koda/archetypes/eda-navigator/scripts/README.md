# Scripts Directory

Use this folder for helper utilities that reinforce the EDA Navigator workflows.

Suggested utilities:
- **mlflow_log_scraper.py** — aggregate MLflow run metadata, reviewer notes, and approval timestamps for notebooks.
- **widget_policy_checker.py** — validate that sampling widgets align with `templates/env-config.yaml` budgets and enforce defaults.
- **viz_accessibility_linter.py** — ensure generated plots follow approved color palettes, include alt-text, and pass contrast thresholds.
- **provenance_harvester.sh** — capture `source_dataset`, `refresh_ts`, and validation flags from Unity Catalog/Delta tables and populate notebooks automatically.

Guidelines:
- Keep scripts idempotent; read runtime settings from `../templates/env-config.yaml` or environment variables.
- Authenticate via Managed Identity or Databricks secret scopes rather than embedding credentials.
- Emit structured logs (`dataset`, `owner`, `request_id`, `purpose`, `notebook_path`) so guardrail workflows can trace notebook lineage and approvals.
