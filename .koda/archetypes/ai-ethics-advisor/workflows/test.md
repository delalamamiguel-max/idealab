---
description: Test Responsible AI assessment package for policy compliance, monitoring readiness, and governance completeness (AI Ethics Advisor)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype ai-ethics-advisor --json ` and parse for FAIRNESS_LIBS, EXPLAINABILITY_TOOLS, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/ai-ethics-advisor/templates/env-config.yaml` for monitoring parameters, approval SLA, and disclosure templates

### 3. Parse Input
Extract from $ARGUMENTS: assessment artifact path, policy thresholds to validate, cohorts of interest, monitoring targets, approval status, deployment stage. Request clarification if incomplete.

### 4. Define Test Plan
Cover the following domains:
- Consent and lineage validation (registry lookups, usage rights)
- Protected attribute handling and mitigation documentation
- Algorithmic impact assessment completeness and risk tier confirmation
- Fairness metric coverage, methodology, threshold adherence, mitigation actions
- Explainability artifacts presence, correctness, and accessibility for reviewers
- Governance workflow status (approvals, evidence, escalation paths)
- Monitoring readiness (drift, fairness, audit logging, appeal intake)
- Privacy/security checklist verification (de-identification, access controls)

### 5. Execute Tests
- Run fairness metric calculations for specified cohorts; assert thresholds within policy limits
- Validate explainability artifacts using SHAP/LIME outputs and counterfactual consistency
- Verify presence of approved model card and datasheet entries with current versioning
- Confirm sign-off workflow completeness (legal, compliance, business approvals, timestamps)
- Simulate monitoring triggers (drift > threshold, fairness delta > 0.05) and confirm alert routing
- Inspect audit log pipeline for completeness and retention policies
- Review stakeholder communication brief for correct disclosures and recourse instructions
Document pass/fail results with evidence links.

### 6. Report Findings
- Summarize test outcomes, noting critical failures, warnings, and passes
- Recommend remediation actions for failing items and assign owners
- Provide overall compliance score or risk grade aligned with governance taxonomy
- Record next review date and monitoring cadence

### 7. Validate and Archive
Store test artifacts in designated audit repository and notify governing board of status.

## Error Handling
- Missing artifacts: Request updated assessment package or rerun scaffold workflow
- Tooling failure: Suggest alternate fairness/explainability libraries from env config
- Policy ambiguity: Escalate to Responsible AI board for interpretation and document decision

## Examples
- `/test-ai-ethics Validate monitoring and appeal readiness before production launch` → Produces test matrix confirming drift alerts, appeal workflows, audit logs
- `/test-ai-ethics Confirm fairness metrics meet thresholds for healthcare triage model` → Generates metric validation report with mitigation recommendations
- `/test-ai-ethics Audit explainability artifacts for regulated credit model` → Delivers test results verifying SHAP packages, narrative explanations, reviewer access

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/ai-ethics-advisor/templates/env-config.yaml`
