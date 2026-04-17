---
description: Package model operations runbooks, telemetry evidence, and governance reports for stakeholders (Model Ops Steward)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype model-ops-steward --json ` and ensure ENV_VALID. Stop if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/model-ops-steward/templates/env-config.yaml` for runbook templates, telemetry exports, and reporting channels

### 3. Parse Input
Extract from $ARGUMENTS: model/service scope, audiences (operations, compliance, leadership), required artifacts (runbooks, dashboards, incident summaries, drift reports), cadence, confidentiality level. Request monitoring outputs and incident logs if missing.

### 4. Assemble Core Artifacts
Ensure package includes:
- Current SLO definitions and measurement methodology
- Telemetry architecture diagram and data retention policy
- Drift monitoring summary with recent PSI/KS results and trends
- Alert routing map with on-call roster and escalation ladder
- Incident playbook and recent RCA summaries with actions
- Retraining schedule and trigger matrix
- Fallback/rollback procedures and test evidence
- MLflow lifecycle sync report (tags, status, incident notes)
- Compliance audit logs covering access and configuration changes
- Stakeholder health report summarizing key metrics and risks

### 5. Tailor Deliverables
Produce outputs for different audiences:
- Operations runbook with detailed procedures and SOPs
- Compliance dossier consolidating logs, SLO evidence, drift reports
- Executive dashboard snapshot and narrative of production health
- Knowledge base entry documenting updates and linking to resources

### 6. Quality Checks
- Verify PII absence in logs and ensure secure storage locations
- Confirm RBAC and access controls for shared artifacts
- Validate accuracy and freshness of telemetry snapshots and SLO metrics
- Store documentation in governed repository with retention metadata
- Notify stakeholders and collect required approvals/sign-offs

### 7. Guardrail Validation

## Error Handling
- Missing data: Request telemetry exports, incident logs, alert roster; provide example command clarifying expectations
- Hard-stop unmet: Refuse publication until SLOs, drift monitoring, or logging evidence complete
- Storage conflict: Direct artifacts to approved repositories per env-config guidance
- Audience ambiguity: Ask for stakeholder breakdown to tailor documentation appropriately

## Examples
- **Example 1**: `/document-model-ops Publish quarterly operations health report for churn service`
- **Example 2**: `/document-model-ops Prepare compliance package for credit risk model monitoring`
- **Example 3**: `/document-model-ops Update runbook and on-call guide for recommendation platform`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/model-ops-steward/templates/env-config.yaml`
