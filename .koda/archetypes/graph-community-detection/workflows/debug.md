---
description: Diagnose graph community detection failures and restore compliant, explainable outputs (Graph Community Detection)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype graph-community-detection --json ` and require ENV_VALID. Stop if false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/graph-community-detection/templates/env-config.yaml` for engine thresholds, monitoring defaults, and CI references

### 3. Parse Input
Collect from $ARGUMENTS: workload identifier, failure symptom (scale crash, privacy alert, anomalous communities, fairness rejection), environment, recent code changes, stakeholders. Request logs, MLflow runs, and monitoring alerts when absent.

### 4. Reproduce Issue
Investigate by:
- Validating data lineage and consent for affected graph slice
- Checking engine resource utilization vs `max_inmemory_*` thresholds and GPU availability
- Inspecting algorithm parameters and random seeds for reproducibility
- Comparing community metrics (modularity, conductance) against baselines
- Running privacy leakage scans (node/edge de-identification, k-anonymity)
- Evaluating fairness/harm metrics across protected cohorts
- Reviewing monitoring dashboards for drift or instability signals
- Ensuring tooling aligns with approved stack (NetworkX, Kuzu, cuGraph, RelationalAI, Neo4j)
- Auditing integration endpoints for schema or SLA mismatches

### 5. Apply Fixes
Recommend remediation:
- Rebuild data contract and update lineage metadata
- Migrate workload to appropriate engine tier or optimize partitioning
- Tune or swap algorithms with documented parameters and MLflow logging
- Reinforce privacy controls (hashing, aggregation, DP noise)
- Correct fairness issues with mitigation strategy and documentation
- Restore monitoring alerts and recalibrate thresholds
- Patch integration tests and schemas for downstream consumers

### 6. Prevent Recurrence
Propose safeguards:
- Automated scale benchmarking in CI pipelines
- Scheduled fairness and privacy audits with alerting
- Knowledge base entry documenting failure signature and fix
- Versioned algorithm configuration registry for traceability
- Expanded visualization dashboards for early anomaly detection

### 7. Validate and Report

## Error Handling
- Missing evidence: Request logs, MLflow runs, drift metrics; provide example command clarifying expectations
- Hard-stop unresolved: Refuse assistance until privacy, scale, or fairness issues addressed
- Tooling outage: Escalate if GPU cluster, RelationalAI, or Neo4j services unavailable; reference env-config contingency plans
- Governance escalation: Notify compliance if sensitive relationship exposure confirmed

## Examples
- **Example 1**: `/debug-graph-community cuGraph job failing during Louvain due to GPU memory limits`
- **Example 2**: `/debug-graph-community Privacy review flagged exposed call graph edges`
- **Example 3**: `/debug-graph-community Community assignments drifting after schema change`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/graph-community-detection/templates/env-config.yaml`
