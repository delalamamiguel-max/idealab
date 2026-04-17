# Scripts Directory

Use this folder for helper utilities that reinforce the Data Sourcing Specialist workflows.

Suggested utilities:
- **catalog_crawler.py** — refresh Unity Catalog metadata and stewardship tags.
- **purview_lineage_uploader.py** — post lineage events and attach glossary terms.
- **sampling_budget_checker.sh** — compare requested extracts against `sampling_budget_gb` and `sample_fraction_cap` from `templates/env-config.yaml`.
- **consent_audit_report.py** — emit CSV/JSON evidence of consent IDs, HALO/UPSTART approvals, and expiry dates.

Guidelines:
- Keep scripts idempotent and externalize all parameters via `../templates/env-config.yaml` or environment variables.
- Prefer Managed Identity / secret scopes for any credentialed calls.
- Emit structured logs (`dataset`, `owner`, `request_id`, `purpose`) so guardrail workflows can ingest them.
