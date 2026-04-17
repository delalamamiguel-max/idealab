# Impact Analyzer Scripts

Use this directory for helper utilities that support dependency scans, evidence capture, and guardrail validation.

## Bundled Scripts
- `python ../../../00-core-orchestration/scripts/validate_env.py --archetype impact-analyzer` — Verifies repo structure, required CLIs, and config artifacts.
- `python/collect-impact-stats.py` — Walks the provided workspace, tallies impacted files per layer, and writes metrics to `cache/impact_scope_stats.json`.

## Contribution Guidelines
- Keep scripts idempotent; accept explicit arguments rather than relying on stateful environment variables.
- Read scan configuration from `templates/env-config.yaml` or CLI flags.
- Emit structured JSON so workflows can embed the results inside Markdown reports.
- Document optional dependencies (e.g., GNU tools, Databricks CLI) at the top of each script.
