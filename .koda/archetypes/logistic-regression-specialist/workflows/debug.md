---
description: Diagnose logistic regression training, scoring, and calibration issues (Logistic Regression Specialist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype logistic-regression-specialist --json ` and capture `ENV_VALID`, `calibration_method`, and `class_imbalance_threshold`. Abort if `ENV_VALID` is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/logistic-regression-specialist/templates/env-config.yaml` for registry paths, monitoring expectations, and alert metrics.

### 3. Parse Input
Extract from $ARGUMENTS: failing component (training script, scoring endpoint, evaluation notebook), error logs or stack traces, metric degradation history, data drift signals, class distribution, fairness attributes, threshold policies, and deployment stage. Request missing details.

### 4. Classify Issue
Determine category:
- **Training Failures**: solver convergence warnings, singular matrix errors, memory constraints, incompatible feature encodings.
- **Probability Quality**: miscalibrated predictions, extreme logit values, threshold misalignment, class imbalance not addressed.
- **Performance Metrics**: ROC-AUC decline, lifted conversions falling, fairness metrics breaches, drift alerts triggered.
- **Operational Breaks**: MLflow registry promotions failing, endpoint latency, monitoring gaps, missing audit logs.

### 5. Root Cause Analysis
For each category:
- Inspect data preprocessing; check for unseen categories, scaling mismatches, or leakage.
- Evaluate regularization and solver choices relative to feature sparsity.
- Examine class distribution vs. `class_imbalance_threshold`; ensure class weights or resampling applied.
- Review calibration method and hold-out results; compute Brier score and calibration curves.
- Verify fairness metrics for declared attributes; identify segments violating thresholds.
- Audit MLflow experiment runs and registry events for completeness.

Document findings in structured format:
```
Root Cause Analysis:
Issue Type: [Training/Calibration/Performance/Operational]
Root Cause: [Detailed explanation]
Impact: [Metric degradation, deployment failure, compliance risk]
Contributing Factors:
- [Factor 1]
- [Factor 2]
```

### 6. Generate Fix
Provide targeted remediation steps and code snippets:
- Adjust preprocessing (update `ColumnTransformer`, handle missing categories, add feature scaling).
- Tune solver or regularization path (switch to `saga`, enable `multi_class='multinomial'`).
- Introduce class weights, SMOTE, or threshold optimization flows.
- Add or update calibration (`CalibratedClassifierCV`) with evaluation charts.
- Extend fairness evaluation using `MetricFrame` or `fairlearn` with remediation recommendations.
- Repair MLflow logging, registry promotion scripts, and monitoring webhooks.

Include inline comments clarifying the change and referencing guardrail compliance.

### 7. Verification Plan
Recommend immediate tests:
- Re-run unit/integration tests, retrain on sample dataset, compute ROC-AUC, PR-AUC, Brier score, fairness metrics.
- Execute calibration diagnostics and ensure thresholds align with business KPIs.
- Validate monitoring dashboards (drift, alert metrics) and confirm MLflow artifacts present.

### 8. Validate and Report

Deliver final summary:
- Root cause and fix applied.
- Metrics to monitor post-deployment.
- Outstanding risks or assumptions (e.g., pending data steward review, limited sample size).
- Next actions for the team (shadow deployment, fairness re-audit, schedule retrain).

## Error Handling

**Insufficient Error Detail**: Request stack trace, MLflow run IDs, or reproduction steps.

**Non-Logistic Model**: If evidence shows tree-based model or other algorithm, recommend switching to appropriate archetype.

**Policy Violations**: Highlight missing governance artifacts and block further debugging until remediated.

## Examples

**Solver Failure**: `/debug-logistic Investigate convergence warning in marketing_lead_scoring train_logreg.py run_id=abc123; include recommended regularization and scaling fixes.`

**Calibration Drift**: `/debug-logistic Production endpoint returning overconfident probabilities; inspect calibration curves and provide recalibration plan.`

**Fairness Alert**: `/debug-logistic Model triggered disparate impact alert for gender; analyze feature contributions and mitigation strategies.`

## References

Constitution: (pre-loaded above)
Environment: `${ARCHETYPES_BASEDIR}/logistic-regression-specialist/templates/env-config.yaml`
