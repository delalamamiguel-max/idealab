---
description: Scaffold interpretability workflow with transparent methods, fairness context, and compliant artifact packaging (Interpretability Analyst)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype interpretability-analyst --json ` and ensure ENV_VALID. Halt if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/interpretability-analyst/templates/env-config.yaml` for approved libraries, storage locations, and reporting templates

### 3. Parse Input
Extract from $ARGUMENTS: model identifier, audience (compliance, business, technical), explanation scope (global, local, counterfactual), fairness attributes, delivery format. Request missing context (MLflow run, dataset version, governance ticket).

### 4. Validate Constraints
Enforce hard stops:
- ✘ Reject explanations lacking method transparency or limitations statement
- ✘ Block privacy breaches (no individual-level sensitive data exposure)
- ✘ Prevent causal claims without causal evidence
- ✘ Require fairness metrics for protected groups when applicable
- ✘ Demand artifact storage in MLflow or approved RAI repository
- ✘ Use only approved interpretability libraries
- ✘ Include stakeholder guidance/caveats

### 5. Generate Explanation Blueprint
Provide scaffold comprising:
- Model card skeleton covering purpose, data, evaluation, ethical considerations, maintenance plan
- Explainability pipeline structure (global SHAP, partial dependence, local LIME/SHAP) with deterministic seeds
- Counterfactual or sensitivity analysis module outlining inputs and safeguards
- Fairness diagnostic section (disparate impact, equal opportunity, calibration)
- Visualization templates with accessibility annotations (alt text, high contrast)
- Artifact packaging instructions for MLflow (notebooks, JSON, PDFs)
- Stakeholder summaries separated by technical, operational, ethical perspectives
- Compliance metadata capture (author, timestamp, model version)

### 6. Recommend Enhancements
Suggest optional additions:
- Interactive RAI dashboard integration
- Automated refresh hooks triggered on new model versions or data drift
- Explainability benchmarking across techniques for robustness
- Sensitivity heatmaps for multi-feature perturbations
- Template-based communications for executives and customers
- Documentation links to policy references and glossary terms

### 7. Validate and Report

## Error Handling
- Hard-stop triggered: Halt scaffold, cite violated clause, provide remediation steps
- Missing inputs: Request MLflow run, feature list, fairness attributes; share example command
- Tooling gap: Flag absent approved libraries or storage permissions; reference env-config onboarding
- Governance requirement: Escalate if compliance packaging or approvals undefined

## Examples
- **Example 1**: `/scaffold-interpretability Prepare model card and SHAP analysis for churn model`
- **Example 2**: `/scaffold-interpretability Plan counterfactual explanations for credit decisioning`
- **Example 3**: `/scaffold-interpretability Create stakeholder briefing for recommendation engine transparency`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/interpretability-analyst/templates/env-config.yaml`
