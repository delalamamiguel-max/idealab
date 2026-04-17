# Data Sourcing Specialist Archetype

The Data Sourcing Specialist archetype governs how analysts discover, profile, and request access to datasets inside Unity Catalog. It enforces catalog metadata checks, sampling guardrails, lineage capture, and PII controls before any data is handed to downstream engineers.

## Repository Layout
```
data-sourcing-specialist/
├── README.md
├── data-sourcing-specialist-constitution.md
├── templates/
│   └── env-config.yaml
├── workflows/
│   ├── scaffold-data-sourcing.md
│   ├── refactor-data-sourcing.md
│   ├── compare-data-sourcing.md
│   ├── debug-data-sourcing.md
│   ├── test-data-sourcing.md
│   └── document-data-sourcing.md
├── scripts/
│   ├── README.md
│   ├── python/
│   │   └── python ../../00-core-orchestration/scripts/validate_env.py --archetype data-sourcing-specialist
└── memory/
```

## Quick Start
1. **Validate the environment**
   ```bash
 python ../../00-core-orchestration/scripts/validate_env.py -sourcing-specialist --json -sourcing-specialist
   ```
2. **Load governance artifacts**
   - Read `data-sourcing-specialist-constitution.md` for hard-stop and mandatory rules.
   - Review `copilot-instructions.md` for prompting expectations.
3. **Capture inputs**
   - Copy `templates/env-config.yaml` and fill in catalog IDs, sampling budgets, retention policies, and steward contacts.
4. **Choose a workflow**
   - `/scaffold-data-sourcing` – build a governed notebook for new dataset exploration.
   - `/refactor-data-sourcing` – harden existing sourcing notebooks with sampling + lineage.
   - `/debug-data-sourcing` – investigate guardrail violations.
   - `/test-data-sourcing` – certify compliance before granting access.
   - `/compare-data-sourcing` – contrast two sourcing approaches or environments.
   - `/document-data-sourcing` – publish catalog-ready documentation.
5. **Extend with scripts (optional)**
   - Place helper utilities inside `scripts/` (see README there) for catalog crawlers, Purview lineage emitters, or sampling calculators.

## Workflow Expectations
Each workflow demands:
- Unity Catalog or Purview lookups for ownership, freshness, and SLA tags.
- Structured sampling with budget checks (`sample_fraction_cap`, `sampling_budget_gb`).
- Lineage events posted immediately after data copies.
- PII handling plans (masking, ABAC filters, consent verification).
- Access audit hooks with request IDs and steward approvals.

## Templates
- `templates/env-config.yaml` centralizes catalog identifiers, storage URIs, policy pipelines, and sampling budgets. Treat it as the single source of truth for prompts or scripts.

## Scripts
- Use `scripts/python/` for reusable helpers (catalog crawlers, lineage pushers, sampling analyzers). Keep them idempotent and load shared config from `templates/env-config.yaml`.
- Guardrail and environment validators now live locally under `scripts/python/` so workflows remain self-contained even when disconnected from `reference/`.

## Related References
- Router governance: `reference/workflows/00-core-orchestration/solution/router.md`
- Access policy rubrics: `../data-solution-architect/data-solution-architect-constitution.md`
- Impact analysis before sourcing: `../impact-analyzer/workflows/impact-analysis.md`
