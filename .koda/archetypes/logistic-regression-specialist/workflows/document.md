---
description: Document logistic regression solution for stakeholders and governance (Logistic Regression Specialist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype logistic-regression-specialist --json ` and parse for MLFLOW_TRACKING_URI, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/logistic-regression-specialist/templates/env-config.yaml` for documentation templates

### 3. Parse Input
Extract from $ARGUMENTS: model identifier (MLflow run ID or registry URI), target audience (data scientists, business stakeholders, governance reviewers, ML engineers), documentation scope (model card, technical spec, user guide, governance checklist). Request clarification if incomplete.

### 4. Analyze Model Artifacts

Extract model metadata from MLflow: hyperparameters (regularization type, penalty strength, solver, class weights), training data (dataset version, time period, feature counts, class distribution), performance metrics (AUC-ROC, AUC-PR, Brier score, confusion matrices), calibration results (calibration method, calibration metrics, reliability curves), fairness metrics (disparate impact, demographic parity, equal opportunity), feature importance (coefficients, odds ratios, VIF scores).

Identify documentation requirements: intended use cases, model limitations, ethical considerations, monitoring requirements, retraining triggers.

### 5. Generate Documentation Package

Create comprehensive documentation suite with model card (overview, intended use, performance metrics, fairness assessment, limitations, ethical considerations, owner information), technical specification (feature engineering pipeline, model architecture, training procedure, hyperparameters, reproducibility instructions, inference code examples), user guide (for data scientists: training instructions, evaluation procedures, hyperparameter tuning; for ML engineers: deployment guide, monitoring setup, rollback procedures; for business users: score interpretation, decision thresholds, escalation paths), governance checklist (documentation completeness, testing validation, compliance requirements, fairness assessment, audit trail, approval signatures).

Include supporting artifacts: coefficient table with odds ratios, calibration plots and reliability diagrams, confusion matrices at key thresholds, ROC and PR curves, feature importance visualizations, fairness metrics by protected attributes, MLflow experiment links and registry URIs.

### 6. Add Recommendations

Include recommendations for documentation maintenance (update on retraining, version with model releases, track in git alongside code), operational procedures (monitoring dashboard setup, alert thresholds, incident response), stakeholder communication (technical vs business language, visualization guidelines, report cadence), compliance tracking (audit readiness, regulatory alignment, review schedules).

Provide documentation checklist and governance approval workflow.

### 7. Validate and Report


Generate documentation artifacts (MODEL_CARD.md, TECHNICAL_SPEC.md, USER_GUIDE.md, GOVERNANCE_CHECKLIST.md, supporting plots and tables). Report completion with artifact locations.

## Error Handling

**Model Metadata Missing**: Request complete MLflow experiment tracking or model registry information.

**Fairness Data Unavailable**: Document limitation and note fairness assessment pending.

**Performance Metrics Incomplete**: Flag missing metrics and recommend full evaluation suite execution.

## Examples

**Example 1**: `/document-logistic Create model card for churn_prediction_v3` - Output: Complete model card with fairness assessment

**Example 2**: `/document-logistic Generate technical documentation for fraud_detection_model` - Output: Technical spec with reproducibility guide

**Example 3**: `/document-logistic Package governance documentation for credit_risk_model production promotion` - Output: Full governance package with approval checklist

## References

