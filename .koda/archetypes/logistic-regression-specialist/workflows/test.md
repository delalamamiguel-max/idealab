---
description: Validate logistic regression pipeline for quality, fairness, and promotion readiness (Logistic Regression Specialist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype logistic-regression-specialist --json ` and parse for SKLEARN_VERSION, PYTEST_VERSION, MLFLOW_TRACKING_URI, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/logistic-regression-specialist/templates/env-config.yaml` for test configuration

### 3. Parse Input
Extract from $ARGUMENTS: model artifact location (MLflow run ID or registry URI), test data specifications, coverage requirements (unit, integration, fairness), acceptance thresholds. Request clarification if incomplete.

### 4. Analyze Model Pipeline

Identify testable components: feature preprocessing (scaling, encoding, imputation), model training (reproducibility, convergence), calibration (Platt/isotonic methods), inference pipeline (feature store integration, prediction API), monitoring (drift detection, fairness metrics).

Determine test scenarios: data quality tests (schema validation, missing values, outliers), model training tests (reproducibility with seeds, convergence checks, coefficient stability), performance tests (AUC thresholds, precision/recall at operating points), calibration tests (Brier score, reliability diagrams, probability distributions), fairness tests (disparate impact, demographic parity, equal opportunity), integration tests (feature store, MLflow registry, scoring endpoint), regression tests (backward compatibility, prediction consistency).

### 5. Generate Test Suite

Create comprehensive test suite with fixtures (test datasets, trained models, mock services), unit tests (feature transformers, encoding logic, scaling functions), integration tests (end-to-end pipeline execution, MLflow tracking validation), performance tests (metric thresholds, statistical significance tests), calibration tests (calibration curve validation, probability quality checks), fairness tests (protected attribute parity, bias metrics), regression tests (model versioning, API contract validation).

Include pytest configuration, test data generation scripts, assertion helpers for probabilistic outputs, CI/CD integration hooks.

### 6. Add Recommendations

Include recommendations for test execution (use holdout test set, validate with production-like data, mock external dependencies), CI/CD integration (run on every PR, gate deployments on test results, track test coverage trends), coverage improvements (test edge cases, validate all error handling, stress test calibration), monitoring (track test execution time, alert on test failures, maintain test data freshness).

Provide test execution command and expected runtime.

### 7. Validate and Report


Execute test suite: `pytest tests/ --cov --cov-report=html --junitxml=results.xml`

Generate test report with pass/fail status, coverage metrics, performance benchmarks, fairness validation results. Report completion.

## Error Handling

**Model Not Found**: Verify MLflow tracking URI and model registry access.

**Test Data Missing**: Provide instructions for generating synthetic test data or accessing holdout sets.

**Fairness Metrics Fail**: Document failures and recommend bias mitigation strategies.

**Calibration Out of Bounds**: Flag calibration issues and suggest recalibration approaches.

## Examples

**Example 1**: `/test-logistic Validate churn_model_v3 from MLflow registry` - Output: 45 tests covering all components with fairness validation

**Example 2**: `/test-logistic Create test suite for fraud detection pipeline` - Output: Comprehensive test suite with calibration and bias checks

**Example 3**: `/test-logistic Run regression tests for logistic_model staging` - Output: Backward compatibility and API contract tests

## References

