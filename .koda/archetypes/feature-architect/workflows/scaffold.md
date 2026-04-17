---
description: Scaffold governed feature engineering workflow with point-in-time correctness and feature store registration (Feature Architect)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype feature-architect --json ` and confirm ENV_VALID. Halt if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/feature-architect/templates/env-config.yaml` for catalog paths, feature store targets, quality thresholds, and lineage tooling

### 3. Parse Input
Extract from $ARGUMENTS: business problem, target entities, source tables, freshness SLA, aggregation windows, privacy constraints, deployment targets. Request clarification if incomplete.

### 4. Validate Constraints
Apply hard-stop checks:
- ✘ Block workflows without source validation or freshness verification
- ✘ Refuse missing feature contracts (data types, ranges, definitions, owners)
- ✘ Reject temporal leakage (future joins, improper windows)
- ✘ Refuse bypass of governed feature store registration
- ✘ Reject PII usage without approved hashing/tokenization
- ✘ Reject non-deterministic transforms lacking seeded randomness
- ✘ Block missing versioning or history logging
Explain violations and prescribe remediation.

### 5. Generate Feature Blueprint
Include:
- Data quality profiling notebook with freshness, schema, and anomaly checks
- Point-in-time join scaffolding with time-travel, windowing, `as_of_ts`
- Parameterized aggregation pipeline (window size, filters) via YAML/JSON config
- Feature quality tests (nulls, monotonicity, duplicates, Drisk metrics)
- Feature store registration snippet (Databricks/Feast) capturing metadata fields
- Training-serving skew detection jobs comparing offline vs online stats
- Lineage logging (Purview/Unity Catalog) with dependency graph updates
- Unit test skeletons using `pytest` or `chispa`

### 6. Add Recommended Enhancements
Propose optional additions:
- Modular transformation library structure with semantic versioning
- Schema evolution workflow with approval gates
- Delta Live Tables or incremental materialization guidance
- Performance monitoring (compute cost, materialization duration)
- Business glossary linkage for feature documentation
- Interactive explainability notebook for steward review

### 7. Validate and Report

## Error Handling
- Hard-stop triggered: Halt scaffold, cite violated clause, supply remediation checklist
- Missing inputs: Request entity keys, timeline grain, quality targets; provide example invocation
- Tooling gap: Flag absent feature store credentials or lineage connectors and reference env-config onboarding steps
- Privacy concern: Escalate if PII handling lacks approved controls

## Examples
- **Example 1**: `/scaffold-feature Build churn propensity feature set with 30-day aggregates`
- **Example 2**: `/scaffold-feature Create credit risk bureau enrichment features with hashing`
- **Example 3**: `/scaffold-feature Design real-time customer profile features with skew monitoring`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/feature-architect/templates/env-config.yaml`
