---
description: Refactor Responsible AI assessment artifacts to close ethics gaps and strengthen governance evidence (AI Ethics Advisor)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype ai-ethics-advisor --json ` and parse for FAIRNESS_LIBS, EXPLAINABILITY_TOOLS, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/ai-ethics-advisor/templates/env-config.yaml` for tooling inventory, approval SLA, monitoring triggers

### 3. Parse Input
Extract from $ARGUMENTS: assessment artifact paths (risk register, fairness report, model card), identified gaps, target deployment stage, required approvers, policy thresholds. Request clarification if incomplete.

### 4. Analyze Existing Artifacts
Assess current package for:
- Missing consent provenance or lineage evidence
- Protected attribute usage without policy exemption
- Absent or insufficient algorithmic impact assessment
- Gaps in fairness metrics (coverage, methodology, threshold breaches)
- Missing explainability artifacts or transparency narratives
- Governance sign-off trail gaps (missing approvals, outdated attestations)
- Monitoring plan deficiencies (drift detection, audit logging, appeal handling)
- Privacy/security checklist omissions (de-identification, access controls)
Document findings with severity, impacted stakeholders, and remediation urgency.

### 5. Implement Refactor
- Update ethical risk register with new harms, mitigations, owners, and timelines
- Expand fairness evaluation pack with additional cohorts, sensitivity analysis, mitigation plan
- Refresh explainability artifacts (SHAP summaries, counterfactuals) and link to documentation
- Revise model card and datasheet sections (purpose, limitations, policy alignment, escalation contacts)
- Reconstruct governance sign-off workflow (approval chain, evidence attachments, SLA tracking)
- Enhance monitoring plan (alert thresholds, audit cadence, appeal triage)
- Complete privacy/security checklist with evidence locations and responsible parties
- Rewrite stakeholder communication brief with updated disclosures, consent language, recourse options
Ensure every change references the policy trigger or issue addressed.

### 6. Add Recommendations
- Plan scenario testing and red-team simulations to validate mitigations
- Engage participatory review sessions with impacted communities or SMEs
- Implement ethics scoring dashboard with trend alerts and ownership
- Conduct human factors audit for decision support clarity
- Benchmark against NIST AI RMF/ISO 23894 controls to identify maturity gaps
- Record knowledge base entries summarizing issues and mitigations for reuse
- Align incentives by updating KPIs with fairness and accountability measures

### 7. Validate and Report
Produce remediation summary covering closed gaps, remaining risks, approval status, and go/no-go recommendation with action owners.

## Error Handling
- Missing artifacts: Request original assessment documents or repository links
- Hard-stop violation persists: Block approval, document risk, and escalate per governance workflow
- Tooling unavailable: Suggest compatible alternatives from env config or provide install guidance

## Examples
- `/refactor-ai-ethics Update fairness evidence for lending model flagged by compliance` → Adds disparate impact metrics, mitigation plan, updated approvals
- `/refactor-ai-ethics Strengthen monitoring plan before enterprise rollout` → Delivers enhanced drift alerts, audit logging, appeal playbook
- `/refactor-ai-ethics Close policy gaps found in privacy review` → Completes consent provenance, secure storage controls, stakeholder communications

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/ai-ethics-advisor/templates/env-config.yaml`
