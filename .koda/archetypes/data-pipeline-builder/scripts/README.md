# Scripts Directory

Use this folder for helper utilities that support the Data Pipeline Builder archetype.

Suggested contents:
- **validate_ingest.py** — run schema checks against landing/staging tables.
- **backfill_runner.py** — orchestrate one-off historical loads with retries.
- **dq_report.sh** — summarize recent data-quality failures.

Keep scripts idempotent and reference shared config by loading `../templates/env-config.yaml`.
