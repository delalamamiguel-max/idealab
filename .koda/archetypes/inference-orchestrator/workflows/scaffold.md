---
description: Scaffold production inference deployment with MLflow registry alignment, AKS IaC, and observability guardrails (Inference Orchestrator)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype inference-orchestrator --json ` and require ENV_VALID. Halt if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/inference-orchestrator/templates/env-config.yaml` for cluster settings, registry names, monitoring resources, and approval flows

### 3. Parse Input
Extract from $ARGUMENTS: MLflow model URI/stage, target environment (dev/stage/prod), traffic profile, SLOs, security posture, batch vs real-time needs, rollout timeline. Request clarification if incomplete.

### 4. Validate Constraints
Check proposal against hard stops:
- ✘ Reject models not in MLflow registry `Production` stage with approval metadata
- ✘ Block observability gaps (missing App Insights/Prometheus/logging)
- ✘ Refuse lack of TLS, private networking, or Key Vault secrets
- ✘ Require rollback strategy (blue/green or canary) with automation
- ✘ Demand load/perf tests aligned to SLOs before cutover
- ✘ Enforce approved container registries with vulnerability scans
- ✘ Require input/output schema validation and payload limits
Explain violations and remediation steps.

### 5. Generate Deployment Blueprint
Provide scaffold covering:
- IaC templates (Bicep/Terraform/Helm) for AKS, ingress, autoscale, managed identity, secret references
- MLflow registry fetch and container build pipeline
- Canary or blue/green traffic management plan with metrics-based gates
- Batch + streaming orchestration (scheduling, retries, idempotency)
- Observability stack (App Insights dashboards, Prometheus scrape configs, structured logging)
- Drift and data logging hooks storing predictions and features to Delta/Lakehouse
- Security posture (network policies, TLS configuration, Key Vault integration)
- Azure DevOps CI/CD pipeline with approvals, smoke tests, load test stages
- Operational runbook skeleton (SLOs, scaling levers, incident contacts)

### 6. Add Recommended Enhancements
Suggest optional upgrades:
- Shadow deployment flow for pre-production validation
- Dynamic routing strategies (segment-based model selection)
- GPU-aware scheduling guidance if applicable
- Cost dashboards tracking AKS utilization vs budget
- Chaos testing plan for resilience validation

### 7. Validate and Report

## Error Handling
- Hard-stop triggered: Block scaffold, cite constitution clause, and supply remediation checklist
- Missing inputs: Request MLflow model URI, SLOs, security requirements; provide example command
- Tooling gap: Flag absence of IaC repository, monitoring resources, or load testing scripts; reference env-config onboarding
- Governance misalignment: Escalate if approvals or risk assessments are missing

## Examples
- **Example 1**: `/scaffold-inference Deploy churn model to AKS with canary rollout and Prometheus monitoring`
- **Example 2**: `/scaffold-inference Build batch scoring pipeline with MLflow registry and Key Vault secrets`
- **Example 3**: `/scaffold-inference Prepare low-latency fraud inference service with GPU autoscaling`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/inference-orchestrator/templates/env-config.yaml`
