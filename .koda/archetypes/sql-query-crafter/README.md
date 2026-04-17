# SQL Query Crafter Archetype

The SQL Query Crafter archetype produces compliant, performant SQL (and SQLAlchemy) code with documented guardrails for Snowflake and Spark backends.

## Repository Layout
```
sql-query-crafter/
├── README.md
├── sql-query-crafter-constitution.md
├── workflows/
│   ├── compare-sql.md
│   ├── debug-sql.md
│   ├── document-sql.md
│   ├── refactor-sql.md
│   ├── scaffold-sql.md
│   └── test-sql.md
├── templates/
│   └── env-config.yaml
├── scripts/
│   └── python/
│       └── python ../../00-core-orchestration/scripts/validate_env.py --archetype sql-query-crafter
```

## Quick Start
1. **Validate the environment**
   ```bash
 python ../../00-core-orchestration/scripts/validate_env.py --archetype sql-query-crafter --json 
   ```
2. **Load governance artifacts**
   - Study `sql-query-crafter-constitution.md` for hard-stop rules and Snowflake-specific guidance.
   - Review `templates/env-config.yaml` for warehouse sizing, lint rules, and naming defaults.
3. **Capture inputs**
   - Required: `target_object`, `database`, `schema`, `change_type`.
   - Optional: query profile stats, expected concurrency, or ORM metadata.
4. **Run a workflow**
   - Execute `/scaffold-sql`, `/refactor-sql`, `/debug-sql`, `/compare-sql`, `/test-sql`, or `/document-sql` under `workflows/`.

## Templates
`templates/env-config.yaml` houses Snowflake/Spark defaults, lint toggles, warehouse sizing hints, and escalation contacts. Adjust this file before running workflows to ensure the archetype tailors recommendations to your environment.

## Scripts
- `python ../../00-core-orchestration/scripts/validate_env.py --archetype sql-query-crafter` validates CLI/tooling, directory layout, and required configuration.
