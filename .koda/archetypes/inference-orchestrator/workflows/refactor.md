---
description: Refactor inference deployment to restore registry alignment, observability, and secure rollout practices (Inference Orchestrator)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype inference-orchestrator --json ` and confirm ENV_VALID. Abort if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/inference-orchestrator/templates/env-config.yaml` for IaC modules, monitoring defaults, and approval flows

### 3. Parse Input
Extract from $ARGUMENTS: deployment asset (repo path, pipeline, helm chart), observed issues (missing telemetry, insecure endpoints, absent rollback), targeted environment, SLA breaches. Request MLflow run IDs, IaC artifacts, and pipeline logs if missing.

### 4. Assess Current Deployment
Review for:
- MLflow registry misalignment or unmanaged models
- Missing observability (App Insights, Prometheus, logging)
- Security gaps (no TLS, public ingress, unmanaged secrets)
- Lack of rollback/canary strategy or automation
- Absent load/perf test evidence vs SLOs
- Unapproved container registries or failing vulnerability scans
- Input/output schema validation gaps
- Drift capture and feature logging omissions
- CI/CD pipeline bypassing approvals or smoke tests

### 5. Define Refactor Plan
Recommend updates:
- Rebuild IaC with managed identity, network policies, secret integration
- Introduce canary/blue-green rollout flows with metric gating
- Reinstate observability dashboards and structured logging
- Add load testing stage, capacity planning, and SLO validation
- Enforce MLflow registry promotion workflow and tagging
- Wire drift/delta logging, feature capture, and monitoring alerts
- Tighten security posture (private endpoints, TLS enforcement, Key Vault)
- Update Azure DevOps pipeline with approvals, smoke tests, rollback hooks

### 6. Future Safeguards
Propose enhancements:
- Shadow deployment stage before traffic shift
- Dynamic routing for segment-aware inference
- GPU-aware or spot nodepool guidance where applicable
- Cost monitoring integration with Azure Monitor
- Chaos testing scripts for resilience validation

### 7. Validate and Report

## Error Handling
- Persistent hard-stop: Halt assistance until registry alignment, observability, or security restored
- Evidence gap: Request IaC repo, pipeline logs, SLO docs; share example command for clarity
- Tooling mismatch: Flag missing monitoring resources or load-testing suite; direct to env-config onboarding
- Governance exception: Escalate if user requests bypass of approval or risk assessments

## Examples
- **Example 1**: `/refactor-inference Harden fraud scoring service lacking TLS and rollback`
- **Example 2**: `/refactor-inference Align churn batch pipeline with MLflow registry approvals`
- **Example 3**: `/refactor-inference Rebuild observability for personalization API after incident`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/inference-orchestrator/templates/env-config.yaml`
