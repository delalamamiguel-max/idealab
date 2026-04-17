# Impact Analyzer Archetype

The Impact Analyzer archetype scans SQL jobs, orchestration manifests, and downstream application code to quantify the blast radius of schema or logic changes before implementation begins.

## Repository Layout
```
impact-analyzer/
├── README.md
├── impact-analyzer-constitution.md
├── workflows/
│   └── impact-analysis.md
├── templates/
│   ├── env-config.yaml
│   └── estimation-config.json
├── scripts/
│   ├── README.md
│   └── python/
│       ├── collect-impact-stats.py
│       ├── python ../../00-core-orchestration/scripts/validate_env.py --archetype impact-analyzer
└── cache/
```

## Quick Start
1. **Validate the environment**
   ```bash
 python ../../00-core-orchestration/scripts/validate_env.py --archetype impact-analyzer --json 
   ```
2. **Load governance artifacts**
   - Study `../impact-analyzer-constitution.md` for search scope, risk rules, and reporting requirements.
   - Review `../templates/env-config.yaml` for scan depth, ignore patterns, and keyword lists.
3. **Capture inputs**
   - Required: `target_object`, `change_type`, and absolute `codebase_path`.
   - Optional: downstream schedule identifiers, table owners, or escalation contacts.
4. **Run the workflow**
   - Execute `/impact-analysis` (see `workflows/impact-analysis.md`) with the collected inputs to generate the Markdown impact report.
5. **Quantify impact**
   - Let `collect-impact-stats.py` emit metrics into `cache/impact_scope_stats.json` and summarize the results in the final report.

## Templates
- `env-config.yaml` defines file patterns, ignore lists, and keyword triggers for the scanners.
- `estimation-config.json` maps detected artifacts to baseline hours and buffer multipliers for the single unified estimate table.

## Scripts
- `python ../../00-core-orchestration/scripts/validate_env.py --archetype impact-analyzer` ensures required CLIs, repo layout, and config files exist before any scanning begins.
- `collect-impact-stats.py` walks the workspace to count impacted files per layer and writes metrics to `cache/impact_scope_stats.json`.

## Cache Artifacts
- `cache/impact_scope_stats*.json` stores the most recent metrics consumed by estimation workflows. Keep these under version control for reproducibility or export them with your final report.
