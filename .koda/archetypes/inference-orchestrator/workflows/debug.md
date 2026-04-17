---
description: Diagnose inference deployment incidents and restore compliant, observable serving (Inference Orchestrator)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype inference-orchestrator --json ` and require ENV_VALID. Stop if validation fails.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/inference-orchestrator/templates/env-config.yaml` for cluster info, monitoring resources, and approval routing

### 3. Parse Input
Collect from $ARGUMENTS: service name, failure symptom (latency spike, error rate, drift alert, security finding), environment, incident timestamp, recent changes, MLflow model version. Request logs, dashboards, and pipeline runs if absent.

### 4. Reproduce and Investigate
Steps:
- Verify MLflow registry status and deployment metadata
- Inspect App Insights/Prometheus metrics for anomalies
- Review structured logs for schema validation or contract failures
- Confirm TLS, network restrictions, and Key Vault secrets functioning
- Examine canary/rollback status and recent releases
- Re-run load tests to replicate SLO breach
- Check drift hooks, feature logging, and data retention tables
- Validate container image provenance and vulnerability scans
- Review Azure DevOps pipeline history for skipped stages or failed approvals

### 5. Apply Fixes
Recommend remediation:
- Roll back to prior stable version via automated strategy
- Patch IaC or helm charts to restore security/observability settings
- Regenerate certificates, rotate secrets, or tighten firewall rules
- Re-enable logging/exporters and update dashboards/alerts
- Re-run load tests, adjust autoscaling, or re-size node pools
- Refresh drift pipelines and reconcile feature logging backlogs
- Document fixes in runbook and update MLflow/DevOps tags

### 6. Prevent Recurrence
Implement safeguards:
- Add automated preflight checks before promotion
- Configure alert thresholds and runbook links in dashboards
- Schedule chaos testing or game days
- Introduce shadow deployment stage for detection before traffic shift
- Update cost and capacity monitoring to forecast load requirements

### 7. Validate and Report

## Error Handling
- Missing evidence: Request logs, metrics, IaC snapshots; provide example command listing expected attachments
- Hard-stop unresolved: Refuse to proceed if observability disabled, MLflow registry bypassed, or security gaps persist
- Tooling outage: Escalate if monitoring infrastructure unavailable; reference env-config failover guidance
- Unauthorized override: Escalate security/compliance if user attempts to skip approvals or telemetry requirements

## Examples
- **Example 1**: `/debug-inference Production churn API failing SLO after blue/green cutover`
- **Example 2**: `/debug-inference Drift alerts firing without logged predictions`
- **Example 3**: `/debug-inference Security scan flagged unapproved container image`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/inference-orchestrator/templates/env-config.yaml`
