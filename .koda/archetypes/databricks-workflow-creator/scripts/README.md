# Scripts Directory

Use this folder for helpers that keep Databricks workflow engagements deterministic.

Suggested utilities:
- **jobs_diff.py** — Compare local JSON specs with deployed Databricks Jobs and flag drift in retries, clusters, or ACLs.
- **expectation_register.sh** — Sync Delta expectation suites from `templates/env-config.yaml` into DLT pipelines.
- **cluster_policy_audit.py** — Validate cluster definitions (runtime, autoscale bands, Photon, cost tags) before deployment.
- **observability_export.py** — Stream run status, DBU usage, and expectation metrics to the central observability fabric.

Guidelines:
- Load workspace, cluster, and observability settings from `../templates/env-config.yaml` and local `templates/env-config.local.yaml` variables.
- Emit structured logs (`job_id`, `workspace_url`, `owner`, `change_type`) for guardrail and audit ingestion.
- Keep scripts idempotent and parameterized via CLI flags; never hard-code tokens or workspace URLs.
