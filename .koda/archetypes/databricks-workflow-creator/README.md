# Databricks Workflow Creator Archetype

The Databricks Workflow Creator archetype helps teams build, orchestrate, and harden Databricks job pipelines while keeping guardrails for config, lineage, and automation intact. It enforces workspace policies, secret management, catalog metadata, and runtime approvals for production-grade workflows.

## Repository Layout
```
databricks-workflow-creator/
├── README.md
├── databricks-workflow-creator-constitution.md
├── templates/
│   └── env-config.yaml
├── workflows/
│   ├── scaffold-databricks-workflow.md
│   ├── refactor-databricks-workflow.md
│   ├── compare-databricks-workflow.md
│   ├── debug-databricks-workflow.md
│   ├── test-databricks-workflow.md
│   └── document-databricks-workflow.md
├── scripts/
│   ├── README.md
│   └── python/
│       └── python ../../00-core-orchestration/scripts/validate_env.py --archetype databricks-workflow-creator
└── memory/
```

## Quick Start
1. **Validate the environment**
   ```bash
 python ../../00-core-orchestration/scripts/validate_env.py --archetype databricks-workflow-creator --json 
   ```
2. **Load governance artifacts**
   - Read `databricks-workflow-creator-constitution.md` for hard-stop policies and mandatory patterns.
   - Review `copilot-instructions.md` for prompt structure and audit expectations.
3. **Capture inputs**
   - Fill in `templates/env-config.yaml` with workspace URLs, cluster policies, job owners, and approved library bundles.
   - Collect job definitions, cluster/lake configuration, and secret scope information for automation workflows.
4. **Choose a workflow**
   - `/scaffold-databricks-workflow` – start a governed Databricks job pipeline with scheduling, retries, and logging.
   - `/refactor-databricks-workflow` – harden an existing job or notebook to meet guardrails.
   - `/debug-databricks-workflow` – troubleshoot failure patterns, credentials, or config drift.
   - `/test-databricks-workflow` – certify jobs against guardrails before release.
   - `/compare-databricks-workflow` – contrast two job definitions for policy alignment.
   - `/document-databricks-workflow` – publish catalog-ready documentation, lineage logs, and automation notes.
5. **Extend with scripts (optional)**
   - Drop helper utilities into `scripts/` (see README there) for job generation, secret management, or log parsing.

## Workflow Expectations
Each workflow enforces:
- Workspace policy metadata (cluster policy, permissions, owner).
- Secret scope usage instead of embedded credentials.
- Automated logging/monitoring for job runs and retry behavior.
- Catalog metadata snapshots for any tables read/written.
- Job scheduling / orchestration configuration with restart handling.

## Templates
`templates/env-config.yaml` centralizes approved clusters, workspace URLs, secret scopes, job owners, and automation hooks. Reference it from scripts, guardrails, and prompts instead of duplicating values across workflows.

## Scripts
- Keep reusable helpers inside `scripts/python/`. Load config from `templates/env-config.yaml`, keep secrets in scopes, and emit structured logs (`workflow`, `owner`, `job`, `request_id`) for guardrail workflows.

## Related References
- Delta job patterns: `reference/workflows/03-data-engineering/job-orchestration/`
- Automation standards: `../data-pipeline-builder/`
