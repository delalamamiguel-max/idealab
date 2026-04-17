---
description: Diagnose Forecasting Analyst training, scoring, and deployment issues (Forecasting Analyst)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype forecasting-analyst --json ` and parse for MLFLOW_TRACKING_URI, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/forecasting-analyst/templates/env-config.yaml` for debugging tools

### 3. Parse Input
Extract from $ARGUMENTS: failure type, error messages, model ID, environment. Request clarification if incomplete.

### 4. Diagnose Issue
Check training failures, convergence issues, scoring errors, performance degradation, fairness violations.

### 5. Generate Fix Recommendations
Provide targeted fixes with code changes and configuration updates.

### 6. Add Prevention Measures
Recommend enhanced monitoring, automated testing, continuous validation.

### 7. Validate and Report
Generate debug report. Report completion.

## Error Handling
**Training Failure**: Analyze data and hyperparameters.
**Performance Degradation**: Check for data drift and model staleness.

## Examples
**Example 1**: `/debug-forecasting-analyst Model convergence issues` - Output: Analysis with hyperparameter recommendations
**Example 2**: `/debug-forecasting-analyst Scoring latency problems` - Output: Performance optimization

## References
