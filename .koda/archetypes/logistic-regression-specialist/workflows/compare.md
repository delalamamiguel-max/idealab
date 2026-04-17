---
description: Compare logistic regression solutions for compliance, calibration, and maintainability (Logistic Regression Specialist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype logistic-regression-specialist --json ` and parse for SKLEARN_VERSION, MLFLOW_TRACKING_URI, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/logistic-regression-specialist/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: candidate approaches (baseline vs experimental), comparison criteria (AUC, calibration, explainability, fairness), model specifications (regularization, features, class balance handling), business constraints. Request clarification if incomplete.

### 4. Generate Comparison Matrix

Compare approaches on: performance metrics (AUC-ROC, AUC-PR, confusion matrices), calibration quality (Brier score, reliability diagrams), interpretability (coefficient analysis, odds ratios, VIF), fairness metrics (disparate impact, demographic parity, equal opportunity), computational cost (training time, inference latency), maintenance complexity (feature dependencies, drift monitoring), governance compliance (MLflow tracking, model cards, audit trails).

### 5. Analyze Trade-offs

Document trade-offs: accuracy vs interpretability, calibration vs raw performance, regularization strength vs feature retention, class balance handling impact, computational budget constraints. Include technical justification for each approach.

### 6. Add Recommendations

Recommend approach with rationale based on: business requirements alignment, fairness and compliance posture, operational feasibility, model governance requirements, stakeholder explainability needs.

Include implementation roadmap: feature engineering approach, hyperparameter tuning strategy, calibration method selection, monitoring and alerting plan, retraining triggers.

### 7. Validate and Report


Generate comparison report with decision matrix. Report completion.

## Error Handling

**Insufficient Context**: Request model specifications, training data characteristics, and business requirements.

**Missing Baseline**: Require current production model metrics for fair comparison.

**Fairness Data Unavailable**: Document limitation and recommend fairness assessment when protected attributes become available.

## Examples

**Example 1**: `/compare-logistic Compare L1 vs L2 regularization for churn prediction` - Output: Regularization comparison with feature selection impact

**Example 2**: `/compare-logistic Evaluate SMOTE vs class weights for imbalanced fraud detection` - Output: Class imbalance strategy comparison

**Example 3**: `/compare-logistic Compare Platt vs isotonic calibration methods` - Output: Calibration approach comparison with reliability curves

## References

