---
description: Diagnose production model incidents and restore telemetry, alerting, and lifecycle compliance (Model Ops Steward)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype model-ops-steward --json ` and confirm ENV_VALID. Stop if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/model-ops-steward/templates/env-config.yaml` for telemetry endpoints, alert integrations, and lifecycle policies

### 3. Parse Input
Gather from $ARGUMENTS: service name, incident description (SLO breach, drift alert, logging failure), environment, timestamp, recent deployments, impacted stakeholders. Request telemetry snapshots, alert history, and incident tickets if missing.

### 4. Reproduce Issue
Investigate by:
- Reviewing SLO dashboards for trend and breach context
- Checking telemetry pipeline integrity (prediction logs, latency, resource metrics)
- Inspecting drift metrics and PSI/KS outputs
- Verifying alert routing (PagerDuty/Teams) and acknowledging statuses
- Assessing incident playbook execution and response timeline
- Confirming fallback/rollback activation and outcome
- Checking retraining schedule and backlog triggers
- Auditing access logs and RBAC for unauthorized changes
- Inspecting MLflow registry tags for lifecycle updates

### 5. Apply Fixes
Recommend remediation:
- Restore telemetry streams and backfill missing logs
- Tune SLO thresholds or autoscaling parameters while preserving guardrails
- Reset or adjust drift thresholds with documented rationale
- Repair alert integrations, on-call rotations, and escalation paths
- Update incident playbook and communicate lessons learned
- Trigger retraining or rollback/fallback actions as needed
- Synchronize MLflow tags and governance trackers with incident status
- Record compliance audit entries for incident handling

### 6. Prevent Recurrence
Propose safeguards:
- Automate heartbeat checks for telemetry pipelines and alerts
- Schedule chaos drills or game days to test response
- Implement self-healing scripts for common remediation tasks
- Add cost and utilization monitoring to prevent resource constraints
- Update training cadence triggers and backlog management
- Publish incident summary to knowledge base for future reference

### 7. Validate and Report

## Error Handling
- Missing evidence: Request telemetry dump, alert logs, incident ticket; include example command listing required inputs
- Hard-stop unresolved: Refuse closure if SLOs undefined, logging absent, or escalation path broken
- Tooling outage: Escalate to platform teams if monitoring stack down; reference env-config contingency plan
- Governance escalation: Notify compliance if incident not logged or follow-up overdue

## Examples
- **Example 1**: `/debug-model-ops Production churn API breaching latency SLO without alerts`
- **Example 2**: `/debug-model-ops Drift detector silent after schema change`
- **Example 3**: `/debug-model-ops Incident playbook missed PagerDuty escalation`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/model-ops-steward/templates/env-config.yaml`
