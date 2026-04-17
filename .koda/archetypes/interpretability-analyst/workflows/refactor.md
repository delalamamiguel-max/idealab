---
description: Refactor interpretability assets to restore transparency, fairness context, and compliant packaging (Interpretability Analyst)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype interpretability-analyst --json ` and confirm ENV_VALID. Abort if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/interpretability-analyst/templates/env-config.yaml` for approved tools, storage targets, and templates

### 3. Parse Input
Extract from $ARGUMENTS: existing explanation assets (notebook, dashboard, report), issues observed (lack method transparency, missing fairness metrics, privacy concerns), model version, audience, deadlines. Request MLflow run IDs, datasets, and packaging logs if missing.

### 4. Diagnose Current Artifacts
Review for:
- Missing method description or limitation statements
- Use of unapproved libraries or undocumented custom code
- Exposure of sensitive individual-level data
- Absence of fairness diagnostics for protected groups
- Missing archive in MLflow/RAI repository
- Inaccessible visualizations (no alt text, low contrast)
- Lack of counterfactual/sensitivity analysis when required
- Stakeholder summary gaps (no actionable guidance)

### 5. Implement Refactor
Recommend updates:
- Document explanation techniques, assumptions, and limitations
- Replace or augment libraries with approved alternatives per env-config
- Aggregate or anonymize data to prevent privacy violations
- Compute fairness metrics and document interpretations/mitigations
- Repackage artifacts into MLflow with metadata (author, timestamp, version)
- Redesign visuals with accessibility compliance and narration
- Add counterfactual or sensitivity analyses aligned to use case
- Expand stakeholder sections with actionable caveats and decision aids

### 6. Strengthen Process
Suggest improvements:
- Automate explanation refresh triggered by new model versions
- Introduce benchmarking across interpretability techniques for robustness
- Build template library for recurring reporting formats
- Integrate outputs with RAI dashboards for interactive review
- Capture links to policy references and prior incidents in documentation

### 7. Validate and Report

## Error Handling
- Persistent hard-stop: Refuse completion until transparency, fairness, privacy, or storage issues resolved
- Missing evidence: Request notebooks, MLflow runs, policy tickets; share example command clarifying expectations
- Tooling mismatch: Flag absence of approved libraries or RAI storage access; reference env-config onboarding
- Governance conflict: Escalate if user attempts to publish without stakeholder guidance

## Examples
- **Example 1**: `/refactor-interpretability Update model explainability pack rejected by compliance`
- **Example 2**: `/refactor-interpretability Replace custom SHAP code with approved library`
- **Example 3**: `/refactor-interpretability Add fairness context to credit decision explanations`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/interpretability-analyst/templates/env-config.yaml`
