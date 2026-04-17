---
description: Compare Isolation Forest Model approaches and patterns (Isolation Forest Model)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype isolation-forest-model --json ` and parse for MLFLOW_TRACKING_URI, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/isolation-forest-model/templates/env-config.yaml` for comparison framework

### 3. Parse Input
Extract from $ARGUMENTS: comparison type, candidate approaches, evaluation criteria. Request clarification if incomplete.

### 4. Generate Comparison Framework
Evaluate algorithms, hyperparameter strategies, feature engineering approaches.

### 5. Create Comparison Matrix
Generate comparison with performance, complexity, interpretability, governance fit.

### 6. Add Recommendations
Recommend approach with justification.

### 7. Validate and Report
Generate report. Report completion.

## Error Handling
**Insufficient Data**: Request evaluation metrics and requirements.
**Unclear Requirements**: Facilitate requirements gathering.

## Examples
**Example 1**: `/compare-isolation-forest-model Algorithm comparison` - Output: Analysis with recommendations
**Example 2**: `/compare-isolation-forest-model Feature engineering strategies` - Output: Strategy comparison

## References
