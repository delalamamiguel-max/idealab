---
description: Scaffold production model operations plan with telemetry, drift monitoring, and incident playbooks (Model Ops Steward)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype model-ops-steward --json ` and require ENV_VALID. Halt if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/model-ops-steward/templates/env-config.yaml` for telemetry targets, alerting integrations, and lifecycle policies

### 3. Parse Input
Extract from $ARGUMENTS: model/service identifiers, environments, defined or required SLOs, telemetry sources, incident processes, retraining cadence, budget constraints. Request missing context if absent.

### 4. Validate Constraints
Enforce hard stops:
- ✘ Reject operations without defined latency/accuracy/error SLOs
- ✘ Block workflows lacking incident escalation paths
- ✘ Require drift detection thresholds and automated responses
- ✘ Demand durable logging of predictions, inputs, metadata
- ✘ Enforce RBAC on monitoring dashboards and audit trails
- ✘ Require documented retraining cadence per policy
- ✘ Ensure rollback/fallback strategy defined

### 5. Generate Operations Blueprint
Include:
- Unified telemetry pipeline design (predictions, outcomes, latency, resource usage)
- Alerting configuration (Azure Monitor, Grafana, Teams/PagerDuty) with severity tiers
- Drift analysis jobs (PSI/KS) and storage in Delta tables with threshold settings
- Incident playbook templates (triage steps, comms, RCA forms)
- CI/CD integration for monitoring IaC validation and dashboard deployment
- Lifecycle governance hooks (MLflow tag sync on SLO breach, maintenance status)
- Compliance audit logging plan (access logs, configuration changes)
- Stakeholder reporting cadence with dashboard references
- Retraining schedule and trigger logic tied to drift/performance metrics

### 6. Add Recommended Enhancements
Propose optional improvements:
- Automated retraining orchestration with approvals
- Canary rollback integration with inference orchestrator workflows
- Cost governance dashboards and budget alerts
- Chaos engineering drill schedule and tooling
- Self-healing automation scripts for common incidents
- Gamified on-call metrics to encourage responsiveness

### 7. Validate and Report

## Error Handling
- Hard-stop triggered: Halt scaffold, cite violated clause, provide remediation guidance
- Missing inputs: Request SLO definitions, telemetry targets, escalation contacts; share example command
- Tooling gap: Flag absence of monitoring workspace or alert integrations; reference env-config onboarding
- Governance dependency: Escalate if lifecycle policies or maintenance owners undefined

## Examples
- **Example 1**: `/scaffold-model-ops Launch monitoring runbook for churn inference service`
- **Example 2**: `/scaffold-model-ops Design drift and alerting strategy for fraud scoring`
- **Example 3**: `/scaffold-model-ops Build operations plan for recommendation platform with retraining cadence`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/model-ops-steward/templates/env-config.yaml`
