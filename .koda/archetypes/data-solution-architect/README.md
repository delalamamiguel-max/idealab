# Data Solution Architect Archetype

The Data Solution Architect is the technical lead for every complex data initiative. It interrogates requirements, enforces governance guardrails, and decomposes work into specialist archetype hand-offs before any code is generated. Use this package whenever a request spans multiple data domains (ingestion, transformation, governance, observability, or serving) and needs a single accountable owner.

## Repository Layout
```
data-solution-architect/
├── README.md
├── data-solution-architect-constitution.md
├── templates/
│   └── env-config.yaml
├── workflows/
│   ├── manifest.yaml
│   └── scaffold-solution.md
├── scripts/
│   ├── README.md
│   ├── python/
│   │   ├── discover-archetype.py
│   │   └── python ../../00-core-orchestration/scripts/validate_env.py --archetype data-solution-architect
```

## Quick Start
1. **Validate the environment**
   ```bash
 python ../../00-core-orchestration/scripts/validate_env.py -solution-architect --json -solution-architect
   ```
2. **Load governance artifacts**
   - Read `data-solution-architect-constitution.md` for hard-stop rules and delegation logic.
   - Review `copilot-instructions.md` for the interrogation script and response format.
3. **Capture intake inputs**
   - Clone `templates/env-config.yaml`, then fill in program identifiers, SLA targets, compliance tickets, data classifications, and initial archetype assignments.
4. **Run `/scaffold-solution`**
   - Provide the completed intake plus any design notes. The workflow generates `docs/SOLUTION_DESIGN.md`, a dependency graph, and the delegation plan.
5. **Extend with scripts**
   - Store automation helpers under `scripts/` (see README there). Typical utilities aggregate open HALO tickets, calculate T-shirt sizing, or sync delegation status with Program Increment boards.

## Workflow Expectations
- Every engagement must produce a numbered interrogation log, a validated `templates/env-config.yaml`, and a `docs/SOLUTION_DESIGN.md` artifact.
- Delegation plans must cite downstream archetypes (`pipeline-builder`, `transformation-alchemist`, `quality-guardian`, etc.) plus required test plans for each hand-off.
   - The architect enforces centralized configuration (`templates/env-config.yaml`) and rejects hardcoded credentials, regions, or schema names.
- Cost sizing (Small/Medium/Large) and failure strategy (fail-fast, DLQ, PagerDuty) are mandatory sections before code is approved.

## Templates
- `templates/env-config.yaml` captures the program dossier (sponsors, compliance tickets, SLA, medallion targets, failure strategy, and archetype delegations). Treat it as the single source of truth for prompts and helper scripts.

## Scripts
- Use `scripts/README.md` for guidance and drop utilities into `scripts/python`. Examples include requirement collectors, SLA matrix generators, and dependency graph builders. Load shared context from `templates/env-config.yaml` to keep executions deterministic.

## Related References
- Router governance: `reference/workflows/00-core-orchestration/solution/router.md`
- Discovery helper: `scripts/python/discover-archetype.py`
