---
description: Refactor model operations workflows to reinforce telemetry, drift response, and governance compliance (Model Ops Steward)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype model-ops-steward --json ` and ensure ENV_VALID. Abort if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/model-ops-steward/templates/env-config.yaml` for telemetry patterns, alerting integrations, and lifecycle policies

### 3. Parse Input
Extract from $ARGUMENTS: existing monitoring assets, observed gaps (missing SLOs, inactive alerts, drift blind spots), environments, stakeholders, remediation deadlines. Request dashboards, logs, and incident history if missing.

### 4. Assess Current Operations
Review for:
- Undefined or outdated SLOs
- Missing or inactive incident escalation paths
- Drift metrics absent or thresholds undefined
- Prediction logging gaps or retention issues
- RBAC weaknesses on dashboards or runbooks
- Retraining cadences misaligned with policy
- Absent fallback/rollback procedures
- CI/CD pipeline missing monitoring IaC validation
- Lifecycle registry tags not updated on SLO breach
- Compliance audit logs incomplete

### 5. Design Refactor
Recommend updates:
- Define or refresh SLOs with owner sign-off
- Reinstate alert routing (PagerDuty/Teams) with severity tiers and paging policies
- Implement PSI/KS drift jobs with Delta storage and thresholds
- Harden telemetry pipeline for inputs/outputs/resource metrics with retention plan
- Apply RBAC and audit logging to dashboards and runbooks
- Schedule retraining triggers and maintenance calendar entries
- Document and automate rollback/fallback strategies
- Integrate monitoring assets into CI/CD validation steps
- Sync MLflow registry tags with operational health status
- Update compliance logging for access and configuration changes

### 6. Future Enhancements
Suggest improvements:
- Automated retraining workflow with approvals and testing gates
- Canary rollback integration with inference orchestrator
- Cost governance dashboards and budget alerts
- Chaos drills and tabletop exercises for incident readiness
- Self-healing scripts for common remediation tasks
- Gamified on-call metrics or dashboards to drive accountability

### 7. Validate and Report

## Error Handling
- Hard-stop persists: Halt progress until SLOs, drift detection, or logging restored
- Missing evidence: Request telemetry exports, alert configs, incident logs; provide example command for clarity
- Tooling mismatch: Flag absent monitoring workspace or alerting integration; reference env-config onboarding
- Governance challenges: Escalate if retraining cadence or fallback policy lacks owner approval

## Examples
- **Example 1**: `/refactor-model-ops Rebuild monitoring for personalization service after alert failure`
- **Example 2**: `/refactor-model-ops Align fraud model operations with new SLO policy`
- **Example 3**: `/refactor-model-ops Restore audit logging and drift checks for credit scoring`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/model-ops-steward/templates/env-config.yaml`
