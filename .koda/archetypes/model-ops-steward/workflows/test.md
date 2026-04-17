---
description: Validate model operations readiness across telemetry, alerts, drift detection, and governance (Model Ops Steward)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype model-ops-steward --json ` and ensure ENV_VALID. Abort if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/model-ops-steward/templates/env-config.yaml` for telemetry specs, alert routing, and lifecycle policies

### 3. Parse Input
Extract from $ARGUMENTS: model/service, environment, SLO targets, drift thresholds, alerting integrations, retraining cadence, compliance requirements. Request monitoring dashboards, IaC configs, and incident playbooks if missing.

### 4. Plan Validation Suite
Cover:
- SLO verification (latency, accuracy, error rate) with synthetic and real traffic
- Telemetry completeness (prediction inputs/outputs, metadata, resource metrics)
- Alert routing test (pager/Teams/email) with severity escalation
- Drift detection exercise using PSI/KS with seeded drift scenario
- Incident playbook tabletop or dry run with documented timings
- RBAC and access audit checks for dashboards and data stores
- Retraining pipeline trigger simulation and governance approvals
- Fallback/rollback drill to confirm readiness
- Lifecycle registry tag updates upon simulated breach
- Compliance audit log review for recent changes

### 5. Execute Tests
Outline execution steps:
- Run synthetic traffic through inference endpoints to measure SLO adherence
- Inject drift scenario and capture detection latency
- Fire test alerts and verify on-call acknowledgement workflow
- Conduct incident tabletop with assigned roles and capture outcomes
- Validate CI pipeline ensuring monitoring IaC passes tests
- Update MLflow tags and verify automated sync
- Collect evidence (screenshots, logs, audit records)

### 6. Evaluate Outcomes
Summarize pass/fail status:
- Highlight hard-stop violations blocking production readiness
- Document remediation tasks, owners, and due dates
- Update operations dashboard and governance trackers with validation status
- Notify stakeholders of findings and planned actions

### 7. Guardrail Verification

## Error Handling
- Missing artifacts: Request monitoring exports, alert configurations, incident playbook; provide example command clarifying expectations
- Hard-stop breach: Block go-live, cite constitution clause, outline remediation before retest
- Tooling gap: Flag absent monitoring platform or alert integration; reference env-config onboarding
- Resource constraint: Escalate if on-call coverage or budget insufficient to maintain SLOs

## Examples
- **Example 1**: `/test-model-ops Certify monitoring readiness for new fraud model rollout`
- **Example 2**: `/test-model-ops Validate drift detection and retraining triggers for personalization`
- **Example 3**: `/test-model-ops Run incident tabletop before credit risk model promotion`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/model-ops-steward/templates/env-config.yaml`
