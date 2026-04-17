---
description: Produce deployment runbooks, compliance packets, and stakeholder briefs for inference services (Inference Orchestrator)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype inference-orchestrator --json ` and confirm ENV_VALID. Stop if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/inference-orchestrator/templates/env-config.yaml` for runbook templates, monitoring exports, and approval routing

### 3. Parse Input
Extract from $ARGUMENTS: service name, environment, intended audience (operations, compliance, leadership), required artifacts (IaC, monitoring dashboards, SLO summaries), retention/policy needs. Request MLflow run links, load test reports, and approval IDs if missing.

### 4. Assemble Core Artifacts
Ensure documentation bundle contains:
- Architecture overview with IaC references and dependency diagram
- MLflow registry metadata (model version, approvals, signature)
- Traffic management plan (canary/blue-green, rollback procedures)
- Performance and load test results mapped to SLOs
- Observability assets (dashboards, alert runbooks, log schema)
- Security posture summary (TLS, network isolation, Key Vault secrets)
- Batch/stream orchestration details (schedules, retries, idempotency)
- Drift monitoring configuration and data retention plan
- Incident response playbook with escalation paths and contact list
- Cost governance overview and scaling levers

### 5. Tailor Outputs
Create targeted deliverables:
- Operations runbook with step-by-step procedures
- Compliance packet with monitoring evidence, approval logs, vulnerability scans
- Executive brief summarizing business impact, readiness, and risks
- Knowledge base article linking to dashboards, MLflow runs, and pipelines

### 6. Quality and Compliance Checks
- Verify sensitive information handled per security policy (no secrets in docs)
- Ensure accessibility (alt text, contrast) for dashboards and visuals
- Store artifacts in approved repository (MLflow, SharePoint, Azure DevOps) with retention metadata
- Notify stakeholders and gather required sign-offs

### 7. Guardrail Validation

## Error Handling
- Missing documentation inputs: Request IaC repo, monitoring export, load test results; include sample command listing expectations
- Hard-stop unmet: Refuse publication if observability, security, or registry alignment lacks evidence
- Storage conflict: Redirect to approved repositories per env-config guidance
- Audience ambiguity: Request clarification to tailor content appropriately

## Examples
- **Example 1**: `/document-inference Package production launch runbook for churn API`
- **Example 2**: `/document-inference Prepare compliance dossier for credit risk batch scoring`
- **Example 3**: `/document-inference Summarize observability posture for personalization service review`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/inference-orchestrator/templates/env-config.yaml`
