---
description: Compare Responsible AI strategies, governance patterns, and mitigation options for ethical risk management (AI Ethics Advisor)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype ai-ethics-advisor --json ` and parse for ANALYSIS_LIBS, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/ai-ethics-advisor/templates/env-config.yaml` for tooling expectations and approval workflow parameters

### 3. Parse Input
Extract from $ARGUMENTS: ethical decision scenario, options to compare (mitigation strategies, governance models, tooling), evaluation criteria (fairness, transparency, operational overhead, compliance risk), stakeholders, regulatory requirements. Request clarification if incomplete.

### 4. Define Evaluation Framework
Establish comparison dimensions:
- Compliance adherence (consent provenance, protected attribute handling, policy thresholds)
- Fairness impact (metric coverage, mitigation strength, cohort inclusion)
- Explainability and transparency (artifact availability, reviewer accessibility, user comprehension)
- Governance operations (approval overhead, SLA impact, audit readiness, monitoring effort)
- Stakeholder experience (user disclosures, recourse effectiveness, human-in-loop reliance)
- Implementation complexity and cost (tooling, training, integration with existing systems)

### 5. Develop Alternatives
For each option:
- Describe mitigation/governance approach and prerequisites
- Detail fairness techniques (reweighing, post-processing, data augmentation) and expected outcomes
- Specify explainability workflows (model cards, SHAP reporting, narrative summaries)
- Outline governance touchpoints (approvers, evidence required, SLA)
- Summarize monitoring plan (metrics tracked, alert thresholds, recertification cadence)
- Identify risks, residual harms, and mitigation feasibility

### 6. Generate Comparison Matrix
- Score each option across evaluation dimensions using qualitative or quantitative scales
- Highlight policy compliance gaps, resource demands, and stakeholder impacts
- Include heatmap/table showing risk level, fairness improvement, transparency, operational load
- Provide narrative analysis referencing constitution guardrails and mitigation trade-offs

### 7. Recommend Path Forward
- Select preferred option with rationale aligned to business goals and ethical obligations
- Suggest mitigation roadmap for rejected options (e.g., prerequisites, required data, governance upgrades)
- Outline transition plan (pilot scope, stakeholder engagement, monitoring setup, approval sequence)

### 8. Validate and Share
Distribute recommendation summary to governance board, product owners, and Responsible AI office.

## Error Handling
- Ambiguous options: Request clearer strategy definitions or provide canonical alternatives (e.g., pre-processing vs. post-processing fairness)
- Conflicting criteria: Facilitate prioritization workshop and document decisions
- Missing policy inputs: Fetch relevant regulatory or corporate policy references before comparing

## Examples
- `/compare-ai-ethics Evaluate pre-processing vs in-processing fairness mitigations for hiring model` → Delivers comparison matrix with fairness lift, governance effort, compliance residuals
- `/compare-ai-ethics Centralized vs federated approval workflow for AI governance` → Produces analysis of SLA impact, accountability, stakeholder coverage
- `/compare-ai-ethics Contrast explainability toolchains (RAI dashboard vs custom SHAP notebooks)` → Provides transparency scorecards, reviewer usability findings, maintenance cost comparison

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/ai-ethics-advisor/templates/env-config.yaml`
