---
description: Refactor graph community detection pipeline to restore governance, scalability, and transparency (Graph Community Detection)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype graph-community-detection --json ` and ensure ENV_VALID. Abort if false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/graph-community-detection/templates/env-config.yaml` for engine thresholds, monitoring defaults, and CI hooks

### 3. Parse Input
Extract from $ARGUMENTS: pipeline path, identified issues (scale, privacy, explainability gaps), graph size metrics, algorithm choices, deployment context, stakeholders, deadlines. Request notebooks, MLflow runs, and monitoring reports if missing.

### 4. Assess Current State
Review for:
- Missing data provenance or consent artifacts
- Sensitive relationship exposure without masking/aggregation
- Engine selection mismatch vs scale thresholds
- Undocumented algorithm parameters or opaque behavior
- Absent fairness/harm assessments
- Missing drift/community stability monitoring
- Unapproved tooling usage
- Weak integration with downstream systems or broken SLAs

### 5. Design Refactor
Recommend updates:
- Restore data contract and lineage documentation
- Re-platform workload to appropriate engine (e.g., upgrade to cuGraph/Neo4j) with benchmark evidence
- Log algorithm parameters and evaluation metrics via MLflow
- Implement privacy controls (hashing, aggregation, differential privacy) per policy
- Add explainability artifacts and visualization templates
- Execute fairness review with mitigation plan
- Instrument monitoring for community drift and stability metrics
- Update integration contracts and regression tests for consumers

### 6. Strengthen Operations
Suggest enhancements:
- Introduce automated algorithm benchmarking harness with seeded runs
- Add streaming ingestion or micro-batch refresh options
- Expand documentation linking to knowledge base and prior incidents
- Schedule governance reviews and training for downstream teams
- Embed cost and performance telemetry dashboards

### 7. Validate and Report

## Error Handling
- Hard-stop persists: Halt refactor until privacy, scale, or fairness requirements satisfied
- Missing evidence: Request MLflow runs, benchmark data, monitoring logs; provide example command
- Tooling gap: Flag need for GPU cluster, RelationalAI access, or Neo4j licensing; reference env-config onboarding
- Governance conflict: Escalate if mitigation owners not assigned

## Examples
- **Example 1**: `/refactor-graph-community Upgrade NetworkX prototype to cuGraph for 50M edge workload`
- **Example 2**: `/refactor-graph-community Restore privacy masking in community reporting dashboard`
- **Example 3**: `/refactor-graph-community Add fairness diagnostics to Kuzu-based social graph pipeline`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/graph-community-detection/templates/env-config.yaml`
