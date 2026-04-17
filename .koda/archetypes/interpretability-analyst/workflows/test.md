---
description: Validate interpretability deliverables for transparency, fairness, and compliance readiness (Interpretability Analyst)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype interpretability-analyst --json ` and ensure ENV_VALID. Abort if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/interpretability-analyst/templates/env-config.yaml` for approved library checks, storage requirements, and reporting templates

### 3. Parse Input
Extract from $ARGUMENTS: model version, explanation artifacts (notebook, dashboard, report), audiences, fairness attributes, compliance deadlines. Request MLflow run links and governance tickets if missing.

### 4. Plan Validation Suite
Coverage should include:
- Method transparency review (technique descriptions, limitations)
- Library compliance and reproducibility (versions, deterministic seeds)
- Privacy audit ensuring no sensitive individual data exposed
- Fairness metrics computed for protected cohorts with thresholds
- Artifact storage verification in MLflow/RAI repository with metadata
- Visualization accessibility checks (contrast, alt text, keyboard navigation)
- Counterfactual/sensitivity analysis completeness and correctness
- Stakeholder summaries ensuring actionable guidance
- Model card completeness and alignment with latest model metrics

### 5. Execute Tests
Outline execution steps:
- Run automated scripts to recompute SHAP/LIME with controlled seeds
- Use env-config manifest to validate library versions
- Perform fairness diagnostics and compare to thresholds
- Inspect artifacts for PII using automated scanners or sampling
- Verify MLflow artifact logging and retention metadata
- Apply accessibility tooling to visuals and narratives
- Review stakeholder sections for clarity and compliance requirements

### 6. Assess Outcomes
Summarize pass/fail results:
- Highlight any hard-stop violations blocking publication
- Document remediation tasks with owners and deadlines
- Update governance tracker with validation status and expiration date
- Notify stakeholders of pending approvals and next steps

### 7. Guardrail Verification

## Error Handling
- Missing artifacts: Request notebooks, dashboards, fairness reports; provide example command listing expectations
- Hard-stop breaches: Block release, cite constitution clause, require remediation before retest
- Tooling gaps: Flag absent approved libraries or accessibility tooling; reference env-config onboarding
- Governance dependencies: Escalate if compliance ticket or stakeholder approval missing

## Examples
- **Example 1**: `/test-interpretability Certify explainability pack for credit decision model`
- **Example 2**: `/test-interpretability Validate counterfactual dashboard prior to regulator review`
- **Example 3**: `/test-interpretability Check fairness narratives for marketing recommendation explanations`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/interpretability-analyst/templates/env-config.yaml`
