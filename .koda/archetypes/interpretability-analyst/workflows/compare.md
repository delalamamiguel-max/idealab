---
description: Compare interpretability strategies for transparency, fairness coverage, and stakeholder usability (Interpretability Analyst)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype interpretability-analyst --json ` and confirm ENV_VALID. Halt if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/interpretability-analyst/templates/env-config.yaml` for approved libraries, storage guidelines, and communication templates

### 3. Parse Input
Extract from $ARGUMENTS: candidate explanation techniques (SHAP, LIME, counterfactuals, surrogate models), target stakeholders, fairness requirements, regulatory expectations, delivery formats. Request related artifacts or prior reports if missing.

### 4. Define Comparison Criteria
Assess options on:
- Method transparency and ability to communicate limitations
- Alignment with approved tooling and reproducibility standards
- Privacy safety (exposure of sensitive data)
- Fairness coverage and diagnostic depth for protected groups
- Suitability for audience (technical vs business vs compliance)
- Artifact packaging readiness (MLflow storage, metadata)
- Visualization accessibility and interpretability
- Maintenance effort for refresh cycles and automation
- Benchmark robustness and sensitivity coverage

### 5. Evaluate Alternatives
For each technique or workflow:
- Score against criteria with evidence and sample outputs
- Flag hard-stop violations (non-approved library, fairness omission, privacy risk)
- Highlight strengths (global insight, local explanation, speed) and limitations
- Estimate remediation or complementary steps needed to satisfy guardrails

### 6. Recommend Approach
Provide recommendation:
- Preferred combination (e.g., SHAP global + counterfactual local) with rationale
- Supplementary artifacts required for comprehensive coverage
- Governance implications (additional approvals, documentation updates)
- Suggested enhancements (interactive dashboards, automated refresh)

### 7. Summarize Decision

## Error Handling
- Missing context: Request model details, stakeholder expectations, fairness obligations; provide example command clarifying inputs
- Hard-stop triggered: Exclude option and cite constitution clause with remediation guidance
- Conflicting priorities: Facilitate trade-off discussion between transparency depth, privacy, and maintenance effort
- Tooling gap: Flag need for licensed or approved library access; reference env-config onboarding

## Examples
- **Example 1**: `/compare-interpretability Choose techniques for regulator-facing credit model explanations`
- **Example 2**: `/compare-interpretability Evaluate SHAP vs surrogate tree for churn model operations team`
- **Example 3**: `/compare-interpretability Decide on counterfactual vs sensitivity dashboard for marketing stakeholders`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/interpretability-analyst/templates/env-config.yaml`
