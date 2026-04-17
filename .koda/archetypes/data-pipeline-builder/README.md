# Data Pipeline Builder Archetype

The Data Pipeline Builder archetype owns batch and streaming ingestion scaffolds. It standardizes how we land source data, build idempotent merges, and document ingestion patterns.

## Repository Layout
```
data-pipeline-builder/
├── README.md
├── data-pipeline-builder-constitution.md
├── copilot-instructions.md
├── workflows/
│   ├── scaffold-pipeline.md
│   ├── refactor-pipeline.md
│   ├── compare-pipeline.md
│   ├── test-pipeline.md
│   ├── debug-pipeline.md
│   └── document-pipeline.md
├── templates/
│   └── env-config.yaml
├── scripts/
│   ├── README.md
│   ├── python/
│   │   └── python ../../00-core-orchestration/scripts/validate_env.py --archetype data-pipeline-builder
```

## Quick Start
1. **Validate the environment**
   ```bash
 python ../../00-core-orchestration/scripts/validate_env.py --archetype data-pipeline-builder --json -builder
   ```
2. **Load governance artifacts**
   - Read `data-pipeline-builder-constitution.md` for hard-stop rules.
3. **Pick a workflow**
   - `/router` → Strategic Menu → choose Scaffold/Refactor/etc.
   - Run the matching file under `workflows/`.
4. **Fill out template inputs**
   - Copy `templates/env-config.yaml` and populate source + target metadata.
5. **Invoke specialist scripts (optional)**
   - Place utilities in `scripts/` (see README there) and call them from workflows or pipelines.

## Workflows
| File | Purpose |
| --- | --- |
| `workflows/scaffold-pipeline.md` | Generate a brand-new ingestion pipeline (landing zone, merge, monitoring). |
| `workflows/refactor-pipeline.md` | Modernize or optimize an existing ingestion job. |
| `workflows/compare-pipeline.md` | Compare two ingestion strategies/patterns with pros/cons. |
| `workflows/test-pipeline.md` | Build regression and data-quality tests for an ingestion flow. |
| `workflows/debug-pipeline.md` | Diagnose ingestion failures or drift. |
| `workflows/document-pipeline.md` | Produce detailed runbooks and lineage documentation. |

## Templates
- `templates/env-config.yaml` collects source, target, merge keys, SLAs, and data quality hooks.
- Copy it into your workspace (or parameter store) before running workflows to ensure consistent prompts.

## Scripts
- `scripts/README.md` explains how to add helper CLI utilities (backfill runners, validation hooks, etc.).
- Place reusable Python utilities there and reference them from workflows.
- Guardrail + environment validators now live locally under `scripts/python/` so prompts remain self-contained.

-## Related Docs
- Router governance: `../workflows/00-core-orchestration/solution/router.md`
- Impact analysis patterns: `../workflows/00-core-orchestration/solution/solution-compare.md`
- Upstream archetypes: `sql-query-crafter`, `transformation-alchemist`, `quality-guardian`
