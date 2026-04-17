---
description: Validate inference deployment readiness across performance, security, and governance guardrails (Inference Orchestrator)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype inference-orchestrator --json ` and confirm ENV_VALID. Abort if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/inference-orchestrator/templates/env-config.yaml` for SLO targets, security baselines, monitoring configs, and approval workflow details

### 3. Parse Input
Extract from $ARGUMENTS: MLflow model version, deployment environment, target SLOs, load profile, security requirements, approval milestones. Request IaC path, pipeline run IDs, and monitoring dashboards if missing.

### 4. Define Test Matrix
Plan validations for:
- MLflow registry integrity (stage, approvals, tags)
- Container provenance and vulnerability scans
- IaC compliance (network policies, managed identities, Key Vault secrets)
- Performance/load tests (latency, throughput, error rate) vs SLOs
- Autoscaling and resource utilization tests (CPU, memory, GPU)
- Observability checks (App Insights, Prometheus, log ingestion)
- Input/output schema validation and payload limit enforcement
- Batch workflow reliability (retry/idempotency) and streaming lag tests
- Security posture (TLS, private networking, firewall rules)
- Rollback/canary automation drills
- Drift logging and monitoring functionality

### 5. Execute Test Suite
Outline tooling usage:
- Azure DevOps pipeline stages with automated verification scripts
- Load testing via k6/Locust/JMeter with captured reports
- Container scanning via Microsoft Defender/Trivy
- Policy compliance via Azure Policy or OPA checks
- Smoke tests hitting inference endpoint with schema validation
- Batch pipeline dry runs with checkpoint validation

### 6. Review Outcomes
Summarize pass/fail status:
- Highlight any hard-stop violations blocking promotion
- Provide remediation plan with owners and timeline
- Update MLflow/DevOps tags to reflect validation state
- Prepare evidence bundle for governance sign-off

### 7. Final Guardrail Check

## Error Handling
- Missing artifacts: Request IaC repo, monitoring dashboards, load test outputs; include sample command listing requirements
- Hard-stop breach: Block promotion, cite constitution clause, and detail remediation before retest
- Tooling shortage: Flag absent load testing or monitoring resources and reference env-config onboarding steps
- Governance misalignment: Escalate if approvals or impact assessments not initiated

## Examples
- **Example 1**: `/test-inference Certify churn batch scoring job for production promotion`
- **Example 2**: `/test-inference Validate real-time fraud API against latency SLO and security controls`
- **Example 3**: `/test-inference Run rollout safety checks for personalization model with blue/green strategy`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/inference-orchestrator/templates/env-config.yaml`
