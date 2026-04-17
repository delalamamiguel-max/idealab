---
description: Scaffold governed Q Learning Model training pipeline with MLflow tracking and compliance (Q Learning Model)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype q-learning-model --json ` and parse for MLFLOW_TRACKING_URI, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/q-learning-model/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: training data, model parameters, evaluation metrics, governance requirements. Request clarification if incomplete.

### 4. Generate Training Pipeline
Create ML pipeline with data preprocessing, model training, MLflow tracking, evaluation, model registry integration, governance controls.

### 5. Generate Validation
Implement quality checks, fairness assessment, performance validation, reproducibility controls.

### 6. Add Recommendations
Include best practices, hyperparameter tuning, monitoring, retraining triggers.

### 7. Validate and Report
Generate pipeline. Report completion.

## Error Handling
**Missing Governance**: Require MLflow tracking and model cards.
**Data Quality Issues**: Implement validation and monitoring.

## Examples
**Example 1**: `/scaffold-q-learning-model Create training pipeline with governance` - Output: Complete ML pipeline with MLflow
**Example 2**: `/scaffold-q-learning-model Generate model with fairness checks` - Output: Governed pipeline with fairness validation

## References
