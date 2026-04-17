---
description: Scaffold Responsible AI assessment package covering risk, fairness, explainability, and governance sign-off (AI Ethics Advisor)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype ai-ethics-advisor --json ` and parse for FAIRNESS_LIBS, EXPLAINABILITY_TOOLS, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/ai-ethics-advisor/templates/env-config.yaml` for required tooling, approval routing, and monitoring thresholds

### 3. Parse Input
Extract from $ARGUMENTS: model identifier, business context, target population, decision criticality, available datasets, deployment timeline, required regulators. Request clarification if incomplete.

### 4. Validate Constraints
Check against hard-stop rules:
- ✘ Refuse packages lacking consent provenance or data usage rights
- ✘ Refuse use of protected attributes without approved mitigation plan
- ✘ Refuse missing algorithmic impact assessment or risk classification
- ✘ Refuse absence of fairness metrics for relevant cohorts
- ✘ Refuse removal of required human oversight checkpoints
- ✘ Refuse suppression of audit logging, explanations, or appeal flows
- ✘ Refuse models exceeding policy thresholds without remediation plan and executive approval
If violated, explain clearly and propose compliant path forward.

### 5. Assemble Ethics Assessment
- Build ethical risk register (stakeholders, impacted groups, harms, mitigations)
- Produce fairness evaluation pack (metric selection rationale, disparate impact, equal opportunity, calibration)
- Generate explainability artifacts (SHAP, LIME, counterfactuals) aligned to policy transparency requirements
- Draft model card and data sheet updates (purpose, data lineage, limitations, risk tier, escalation contacts)
- Define governance sign-off workflow (approvers, evidence attachments, SLA clock tracking)
- Outline post-deployment monitoring plan (drift thresholds, fairness alert deltas, audit logging locations)
- Complete privacy and security checklist (de-identification, access controls, evidence storage)
- Prepare stakeholder communication brief (disclosures, consent text, recourse instructions)

### 6. Add Recommendations
- Scenario testing with red-team simulations and adversarial probes
- Participatory review engagements with SMEs or impacted communities
- Continuous ethics scoring dashboard integration (risk trend telemetry)
- Human factors review covering decision support UX and automation bias safeguards
- Benchmark alignment with NIST AI RMF or ISO/IEC 23894 maturity levels
- Linkage to knowledge base of prior incidents and mitigations
- KPI alignment ensuring incentives cover fairness, safety, accountability metrics

### 7. Validate and Report

Deliver summary highlighting risk tier, outstanding actions, approval blockers, and go/no-go recommendation.

## Error Handling
- Hard-stop violation: Explain the violated policy, reference constitution clause, and outline remediation steps
- Incomplete input: List missing context (consent registry, population, decision criticality) and provide example
- Tooling gap: Identify missing fairness/explainability libraries and cite installation guidance from env config

## Examples
- `/scaffold-ai-ethics Evaluate credit underwriting model for fairness and consent coverage` → Outputs full assessment package with risk register, fairness metrics, governance plan
- `/scaffold-ai-ethics Prepare Responsible AI review for customer churn model prior to pilot` → Produces model card update, monitoring plan, stakeholder communications, sign-off tracker
- `/scaffold-ai-ethics Launch ethics review for biometric authentication system` → Generates harm assessment, privacy checklist, human-in-the-loop requirements, escalation brief

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/ai-ethics-advisor/templates/env-config.yaml`
