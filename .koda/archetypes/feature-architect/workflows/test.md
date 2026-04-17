---
description: Validate feature pipelines for quality, temporal correctness, and contract compliance before promotion (Feature Architect)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype feature-architect --json ` and ensure ENV_VALID. Abort if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/feature-architect/templates/env-config.yaml` for quality thresholds, test suites, and lineage tooling

### 3. Parse Input
Extract from $ARGUMENTS: feature set name, promotion target (dev, staging, prod), required quality metrics, privacy constraints, consuming models. Request notebooks, configs, and feature store IDs if missing.

### 4. Plan Test Coverage
Define validation suite:
- Source freshness and schema verification
- Point-in-time correctness tests (time-travel sampling, leakage detection)
- Feature quality checks (nulls, drift, monotonicity, duplicates, Drisk)
- Training-serving skew comparison using offline vs online stats
- Privacy compliance confirmation (hashing, masking)
- Feature contract validation (metadata completeness, ownership, TTL)
- Unit tests for transformation logic (`pytest`/`chispa`)
- Lineage graph integrity and versioning review

### 5. Execute Tests
Run automated checks:
- Parameterized notebooks/pipelines using deterministic seeds
- CI task orchestration in Azure DevOps with pass/fail output
- Feature store validation commands ensuring registration metadata
- Export of test report (HTML/PDF) with summary table and evidence links

### 6. Evaluate Outcomes
Determine readiness:
- Flag failures with remediation actions
- Confirm all hard-stop checks pass before promotion
- Document results in change log and notify consumers
- Update feature store tags with quality status

### 7. Guardrail Verification

## Error Handling
- Missing artifacts: Request feature notebook path, test config, lineage export; provide example command listing expected inputs
- Hard-stop breach: Block promotion, cite violated clause, outline remediation before retest
- Tooling mismatch: Note absent quality libraries or feature store CLI access and reference env-config onboarding
- Privacy breach: Halt testing and escalate if sensitive columns found unmasked

## Examples
- **Example 1**: `/test-feature Validate temporal joins and skew for churn aggregation features`
- **Example 2**: `/test-feature Run quality gate prior to registering marketing propensity feature set`
- **Example 3**: `/test-feature Certify real-time fraud features for production rollout`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/feature-architect/templates/env-config.yaml`
