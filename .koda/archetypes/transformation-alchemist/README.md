# Transformation Alchemist Archetype

The Transformation Alchemist archetype owns Spark and Delta Lake transformations—from exploratory notebooks to production-grade pipelines. This localized folder keeps the constitution, workflows, templates, and scripts self-contained so validation can run without touching the shared `reference/` tree.

## Repository Layout
```
transformation-alchemist/
├── README.md
├── transformation-alchemist-constitution.md
├── workflows/
│   ├── compare-spark.md
│   ├── debug-spark.md
│   ├── document-spark.md
│   ├── refactor-spark.md
│   ├── scaffold-spark.md
│   └── test-spark.md
├── templates/
│   └── env-config.yaml
└── scripts/
    ├── README.md
   └── python/
      └── python ../../00-core-orchestration/scripts/validate_env.py --archetype transformation-alchemist
```

## Quick Start
1. **Validate prerequisites**
   ```bash
 python ../../00-core-orchestration/scripts/validate_env.py --archetype transformation-alchemist --json 
   ```
2. **Review governance artifacts**
   - Read `transformation-alchemist-constitution.md` for Spark/Delta guardrails.
   - Update `templates/env-config.yaml` with workspace URLs, cluster sizing, Delta retention, and lineage hooks.
3. **Gather request context**
   - Required: `source_system`, `target_zone`, `sla_minutes`, `data_volume_tb`.
   - Optional: cluster policy IDs, Lakehouse security tier, ML feature expectations.
4. **Run the correct workflow**
   - Choose one of `/scaffold-spark`, `/refactor-spark`, `/compare-spark`, `/debug-spark`, `/test-spark`, or `/document-spark` in `workflows/`.

## Templates
`templates/env-config.yaml` centralizes Spark runtime defaults, Databricks workspace metadata, cost guardrails, and job naming rules. Keep it current so validators and workflows emit accurate parameters.

## Scripts
- `python ../../00-core-orchestration/scripts/validate_env.py --archetype transformation-alchemist` ensures Spark CLI, PySpark packages, config files, and constitution copies exist.

## Local Constitution Copy
`transformation-alchemist-constitution.md` now lives beside the workflows so scripts no longer depend on `reference/memory`. If downstream archetypes still need the shared version, keep both copies in sync.
