# Scripts Directory

Use this folder for helpers that accelerate Data Solution Architect engagements.

Suggested utilities:
- **solution_intake.py** — Convert HALO/UPSTART tickets into the `templates/env-config.yaml` structure.
- **delegation_tracker.sh** — Compare the delegation matrix against Azure Boards or Jira epics and flag missing owners.
- **sla_matrix_builder.py** — Generate SLA and failure-strategy tables for inclusion in `docs/SOLUTION_DESIGN.md`.
- **cost_sizer.py** — Estimate compute/storage usage and map it to the required t-shirt size thresholds.

Guidelines:
- Read shared context from `../templates/env-config.yaml` (do not duplicate constants).
- Emit structured logs (`program_name`, `request_id`, `owner`, `decision`) so `/scaffold-solution` transcripts stay auditable.
 - Keep scripts idempotent and parameterized via CLI flags or environment variables that mirror `templates/env-config.yaml`.
