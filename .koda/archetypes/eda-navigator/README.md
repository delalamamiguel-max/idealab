# EDA Navigator Archetype

The EDA Navigator archetype governs exploratory data analysis notebooks so they remain reproducible, collaborative, and compliant with governance guardrails. It enforces provenance metadata, sampling limits, approved visualization stacks, and audit-ready collaboration patterns before insights are shared.

## Repository Layout
```
eda-navigator/
├── README.md
├── eda-navigator-constitution.md
├── templates/
│   └── env-config.yaml
├── workflows/
│   ├── scaffold-eda.md
│   ├── refactor-eda.md
│   ├── compare-eda.md
│   ├── debug-eda.md
│   ├── test-eda.md
│   └── document-eda.md
├── scripts/
│   ├── README.md
│   └── python/
```

## Quick Start
1. **Validate the environment**
   ```bash
 python ../../00-core-orchestration/scripts/validate_env.py --archetype eda-navigator --json 
   ```
2. **Load governance artifacts**
   - Read `eda-navigator-constitution.md` for hard-stop and mandatory notebook rules.
   - Review `copilot-instructions.md` for prompt structure and refusal criteria.
3. **Capture inputs**
   - Copy `templates/env-config.yaml` and fill in cluster policies, MLflow locations, visualization approvals, and collaboration settings.
   - Collect dataset provenance (source dataset, refresh timestamp, validation status) plus reviewer assignments.
4. **Choose a workflow**
   - `/scaffold-eda` – create a governed notebook skeleton with widgets, profiling, and collaboration cells.
   - `/refactor-eda` – harden an existing notebook to meet governance and accessibility standards.
   - `/debug-eda` – diagnose provenance gaps, sampling violations, or visualization drift.
   - `/test-eda` – certify the notebook before launch or audit review.
   - `/compare-eda` – contrast two notebooks for coverage, reproducibility, or visualization alignment.
   - `/document-eda` – produce documentation packages, approval logs, and monitoring commitments.
5. **Extend with scripts (optional)**
   - Drop helper utilities into `scripts/` (see README there) for MLflow log scrapers, widget validators, or provenance collectors.

## Workflow Expectations
Each workflow enforces:
- Recorded provenance metadata (`source_dataset`, `refresh_ts`, `validation_status`).
- Sampling widgets with `limit`, `fraction`, and filter controls tied to approved budgets.
- Approved visualization stack (Plotly/Matplotlib/Seaborn) with accessibility notes and alt-text.
- Collaboration metadata (author, reviewer, approval timestamp, change log) persisted to MLflow or Delta.
- Structured logging to MLflow runs or Delta tables for executed cells, dataset versions, and outcomes.
- Cluster policy alignment and warning visibility (no silent suppression).

## Templates
-- `templates/env-config.yaml` centralizes Spark runtime versions, approved libraries, shared MLflow paths, dashboard targets, and automation pipelines. Reference it from workflows, scripts, and prompt inputs instead of duplicating values.

## Scripts
- Place reusable helpers inside `scripts/python/`. Keep them idempotent, parameterize via `templates/env-config.yaml`, and emit structured logs (`dataset`, `owner`, `request_id`, `purpose`) for downstream guardrail checks.

## Related References
-- Notebook collaboration controls: `reference/workflows/06-application-development/notebook-collaboration-coach/`
-- Data sourcing inputs: `../data-sourcing-specialist/`
