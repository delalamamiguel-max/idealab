---
description: Validate graph community detection pipeline for scale fitness, fairness, and operational readiness (Graph Community Detection)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype graph-community-detection --json ` and confirm ENV_VALID. Abort if false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/graph-community-detection/templates/env-config.yaml` for benchmarking jobs, monitoring thresholds, and CI expectations

### 3. Parse Input
Extract from $ARGUMENTS: pipeline path, dataset snapshot, target engine, algorithm selection, performance targets, fairness thresholds, deployment stage, downstream consumers. Request MLflow experiment IDs and monitoring configs if missing.

### 4. Assemble Test Suite
Plan validation coverage:
- Data contract verification (schema, lineage, consent, retention)
- Engine scale tests (node/edge counts vs resource utilization, GPU/CPU benchmarks)
- Algorithm reproducibility (seed consistency, parameter sweeps, MLflow logs)
- Community quality metrics (modularity, conductance, silhouette) with baseline comparison
- Fairness and harm metrics for protected cohorts with mitigation checks
- Privacy assessments confirming masking/aggregation and k-anonymity thresholds
- Monitoring readiness (drift metrics, community stability index, alert routing)
- Integration tests for downstream APIs, dashboards, knowledge graphs
- Operational rehearsal (refresh cadence, rollback/fallback drills)

### 5. Execute Tests
Outline execution steps:
- Run benchmarking notebooks or CI jobs (`graph-unit-tests`, `graph-scale-benchmark`)
- Trigger MLflow runs capturing evaluation metrics and artifacts
- Perform fairness and privacy notebooks with documented results
- Stress-test engine with synthetic loads where applicable
- Validate monitoring dashboards and alert firing
- Execute integration tests and capture evidence
- Produce consolidated validation report with links and approvals

### 6. Evaluate Results
Summarize pass/fail outcomes:
- Highlight hard-stop violations blocking promotion
- Provide remediation backlog with owners and timelines
- Update governance tracker with validation status, expiration, and reviewers
- Notify stakeholders for sign-off and readiness decisions

### 7. Guardrail Verification

## Error Handling
- Missing artifacts: Request dataset snapshot, MLflow run, monitoring export; include example command clarifying expectations
- Hard-stop breach: Block promotion, cite constitution clause, detail remediation before retest
- Tooling gap: Flag absence of benchmark cluster, fairness tooling, or monitoring workspace; reference env-config onboarding
- Governance delay: Escalate if approvals or mitigation plans not assigned

## Examples
- **Example 1**: `/test-graph-community Certify RelationalAI community detection before regulatory review`
- **Example 2**: `/test-graph-community Validate cuGraph pipeline for fraud ring detection`
- **Example 3**: `/test-graph-community Run fairness and privacy checks on Kuzu customer graph`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/graph-community-detection/templates/env-config.yaml`
