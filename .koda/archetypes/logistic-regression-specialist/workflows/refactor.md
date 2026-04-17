---
description: Refactor logistic regression solutions for compliance, calibration, and maintainability (Logistic Regression Specialist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype logistic-regression-specialist --json ` and record `ENV_VALID`, `class_imbalance_threshold`, and `calibration_method`. Stop if `ENV_VALID` is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/logistic-regression-specialist/templates/env-config.yaml` for registry paths, monitoring hooks, and CI expectations.

### 3. Parse Input
Extract from $ARGUMENTS: code paths or notebooks to refactor, current pain points (performance drift, calibration issues, fairness gaps), target schema, feature lineage, evaluation metrics, deployment context, and compliance requirements. Request any missing context.

### 4. Assess Current State
Review supplied artifacts (summaries, snippets, or references) and classify issues:
- **Architecture**: Monolithic scripts, missing pipeline abstraction, or duplicated preprocessing.
- **Data Handling**: Lack of feature scaling, leakage, or inconsistent encoding between train and inference.
- **Modeling**: Fixed regularization, unsupported multi-class handling, or outdated solver selection.
- **Evaluation**: Missing ROC/PR metrics, absent calibration curves, limited fairness analysis, or outdated baseline comparisons.
- **Operations**: No MLflow tracking, missing registry promotions, absent monitoring hooks, or insecure secrets handling.

Document findings in a concise table with severity tags (High/Medium/Low) and direct links if paths provided.

### 5. Design Refactor Plan
Propose incremental steps:
- Modularize into reusable components (data prep, training, calibration, evaluation, registry).
- Introduce `Pipeline` + `ColumnTransformer` for consistent preprocessing.
- Replace manual hyperparameter tuning with cross-validated search covering `default_regularization_grid`.
- Add probabilistic calibration following `calibration_method` and evaluate lift.
- Embed fairness metrics (e.g., `MetricFrame`) across declared attributes, with documentation updates.
- Wire MLflow logging, model cards, and CI checks (unit tests, linting, security scans).

### 6. Publish Refactored Snippets
Provide revised code segments:
- Updated configuration file (`params.yaml` or MLproject) with separation of concerns.
- Refactored training script illustrating new pipeline, search, and calibration logic.
- Enhanced evaluation notebook section capturing ROC, PR, calibration, fairness charts.
- Deployment script updates ensuring staged promotion, signature capture, and approval workflow.

Annotate each snippet with comments explaining the improvement and how it satisfies constitution mandates.

### 7. Regression Safety Nets
Recommend automated tests:
- Unit tests verifying preprocessing, class weight handling, and probability calibration.
- Data validation ensuring feature schemas and drift thresholds.
- CI/CD integration steps leveraging Azure DevOps pipeline from configuration.

### 8. Validate and Report

Deliver report:
- Issue summary with severity matrix.
- Refactor actions performed (or recommended if code cannot be edited directly).
- Remaining risks or dependencies (e.g., awaiting data steward approval).
- Next steps for teams (update secrets, schedule shadow deployment, refresh documentation).

## Error Handling

**Insufficient Artifacts**: Request file excerpts, metrics dashboards, or pipeline configs to assess refactor scope.

**Guardrail Violations**: If existing artifacts break hard-stop rules (no MLflow, missing fairness), call them out with remediation steps before proceeding.

**Unsupported Technology**: If stack uses unsupported solver (e.g., legacy GLM library), recommend migration paths with risk assessment.

## Examples

**Legacy Notebook Cleanup**: `/refactor-logistic Improve notebook train_churn.ipynb that lacks calibration and fairness metrics; output modular pipeline ready for MLflow.`

**CI Modernization**: `/refactor-logistic Update Azure DevOps pipeline to add unit tests, linting, and registry promotion approval gates for marketing_lead_scoring.`

**Class Imbalance Fix**: `/refactor-logistic Rework fraud training script to use class weights, SMOTE, and threshold tuning to meet false positive budget.`

## References

Constitution: (pre-loaded above)
Environment: `${ARCHETYPES_BASEDIR}/logistic-regression-specialist/templates/env-config.yaml`
