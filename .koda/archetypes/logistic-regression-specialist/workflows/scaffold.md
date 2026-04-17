---
description: Scaffold a governed logistic regression training pipeline with calibrated probabilities (Logistic Regression Specialist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype logistic-regression-specialist --json ` and capture `ENV_VALID`, `class_imbalance_threshold`, and `default_regularization_grid`. Halt if `ENV_VALID` is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/logistic-regression-specialist/templates/env-config.yaml` to retrieve `mlflow.experiment_path`, `variables.calibration_method`, `monitoring.metric_alerts`, and CI expectations.

### 3. Parse Input
Extract from $ARGUMENTS: dataset source (Delta table, feature view, or CSV path), target column, positive class label, feature list or feature store references, fairness attributes, imbalance indicators, metric priorities, deployment target, and decision threshold guidance. Request clarification if any of these are missing.

### 4. Guardrail Pre-Checks
Validate information before generating code:
- Confirm target is binary or multinomial categorical. If not, refuse and suggest alternative archetypes.
- Ensure feature sources reference governed tables or feature store entries; refuse ad-hoc extracts without lineage.
- Check whether class prevalence is below `class_imbalance_threshold`; if so, plan to apply reweighting or resampling.
- Require fairness attributes or justification if none exist.

### 5. Generate Pipeline Scaffold
Produce a structured project layout:
- `notebooks/` for exploratory analysis with Unity Catalog hooks.
- `src/training/` containing modular Python files (`data_prep.py`, `model_train.py`, `calibration.py`, `evaluate.py`, `register.py`).
- `src/reference/config/` with `params.yaml` capturing training metadata and regularization grid.
- `src/pipelines/train_logreg.py` orchestrating the steps using Databricks Jobs or Azure ML CLI.
- `tests/` folder with unit tests for preprocessing and probability calibration.

Apply mandatory patterns:
- Use `scikit-learn` pipeline with `ColumnTransformer`, `StandardScaler`, and encoded categorical transformers.
- Configure `LogisticRegression` with solver selection logic, multi-class handling, and cross-validated `LogisticRegressionCV` over `default_regularization_grid`.
- Attach MLflow autologging, structured evaluation logging (ROC-AUC, PR-AUC, calibration curves), fairness metrics (e.g., `fairlearn` if available), and confusion matrices by segment.
- Implement imbalance mitigation (class weights or SMOTE) when prevalence threshold is triggered.
- Generate model cards in `docs/model_card.md` summarizing objective, data, metrics, fairness insights, and retrain cadence.

### 6. Probability Calibration & Thresholding
Include calibration logic referencing `variables.calibration_method` (Platt or isotonic) and produce helper code to compute optimal thresholds (Youden, cost-sensitive). Document decision guidance inline.

### 7. Monitoring Hooks
Embed placeholders for logging drift statistics to Azure ML monitoring workspace (`monitoring.metric_alerts`) and capturing SHAP-based explanations for dashboards.

### 8. Validate and Report

Report output:
- Summary of scaffolded files with brief purpose.
- Highlight applied guardrails (feature governance, imbalance handling, fairness checks, calibration).
- Suggest next steps: configure secrets, connect to data sources, execute notebook pipeline.

## Error Handling

**Invalid Target**: If the target is not binary/multinomial, explain the violation and direct to `model-architect` or `experiment-scientist` archetype.

**Missing Governance**: If feature lineage or access approvals are absent, refuse and instruct to onboard through Unity Catalog or feature store.

**Insufficient Input**: List missing parameters (target, metrics, fairness attributes) and provide a filled example request.

**Environment Failure**: Surface missing dependencies or configs, citing lines from validation output and recommended fixes.

## Examples

**Binary Churn Model**: `/scaffold-logistic Build a churn model on telco_customers (target: churn_flag, positive: "Yes") with features from fs.telco_customer_features and fairness across gender and age_band.`

**Multinomial Risk Tiering**: `/scaffold-logistic Train multinomial logistic regression for credit risk (target: risk_tier in {Low, Medium, High}) using engineered features from main.feature_store.credit_features, require calibration and confusion matrix by tier.`

**Fraud Detection**: `/scaffold-logistic Create imbalanced fraud detection pipeline (target: is_fraud) with SMOTE, threshold tuning by cost matrix, fairness metrics across region.`

## References

Constitution: (pre-loaded above)
Environment: `${ARCHETYPES_BASEDIR}/logistic-regression-specialist/templates/env-config.yaml`
