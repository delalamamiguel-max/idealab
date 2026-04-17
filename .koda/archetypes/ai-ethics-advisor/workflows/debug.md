---
description: Diagnose Responsible AI assessment defects and restore compliance with ethical guardrails (AI Ethics Advisor)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype ai-ethics-advisor --json ` and parse for FAIRNESS_LIBS, EXPLAINABILITY_TOOLS, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/ai-ethics-advisor/templates/env-config.yaml` for required tooling, approval matrix, monitoring thresholds

### 3. Parse Input
Extract from $ARGUMENTS: failing artifact or review (risk register, fairness report, monitoring alert), error message or audit finding, deployment stage, policy threshold breached, impacted cohort or stakeholder. Request clarification if incomplete.

### 4. Reproduce and Classify Issue
Investigate reported defect:
- Verify consent provenance, lineage, and data usage rights
- Inspect for unauthorized protected attribute usage or missing mitigation plans
- Check algorithmic impact assessment completion and risk tiering
- Audit fairness metrics for coverage, correctness, threshold breaches
- Validate existence and fidelity of explainability artifacts
- Inspect sign-off workflow for missing approvals or expired attestations
- Review monitoring setup for absent drift/fairness alerts or disabled logging
- Confirm privacy/security checklist completion and evidence storage
Categorize issue severity and potential harm.

### 5. Apply Fixes
- Restore missing documentation (consent evidence, lineage, approvals)
- Regenerate fairness metrics with correct cohorts and mitigation actions
- Produce or update explainability artifacts tied to policy transparency requirements
- Rebuild governance workflow records, capture approver attestations, reset SLA clock if needed
- Reinstate monitoring controls, alert routing, audit log capture, and appeal pathways
- Complete privacy/security checklist items with verified evidence locations
- Update stakeholder communications to reflect changes and recourse mechanisms

### 6. Prevent Regression
- Recommend scenario testing, red-team exercises, or adversarial probes to validate fix
- Schedule participatory review sessions with impacted groups
- Enable ethics scoring dashboards and automated alerts
- Propose human factors evaluation for decision support experience
- Link remediation summary to knowledge base for future audits

### 7. Validate and Report
Publish debug report summarizing root cause, remediation steps, validation evidence, remaining risks, and follow-up actions.

## Error Handling
- Missing reproduction steps: Request full assessor notes, evidence, and audit log excerpts
- Policy override attempts: Escalate to governance board and block deployment pending approval
- Tooling mismatch: Recommend compatible library versions or alternative platforms per env config

## Examples
- `/debug-ai-ethics Fairness dashboard shows disparate impact violation after retrain` → Identifies metric drift, adds mitigation plan, updates monitoring alerts
- `/debug-ai-ethics Compliance audit flagged missing consent documentation` → Restores consent lineage, updates privacy checklist, notifies approvers
- `/debug-ai-ethics Sign-off workflow lost legal approval due to expired evidence` → Re-collects attestations, refreshes governance tracker, resets SLA clock

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/ai-ethics-advisor/templates/env-config.yaml`
