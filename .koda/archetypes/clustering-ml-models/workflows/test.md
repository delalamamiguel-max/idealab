---
description: Validate Clustering Ml Models pipeline for quality, fairness, and promotion readiness (Clustering Ml Models)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype clustering-ml-models --json ` and parse for MLFLOW_TRACKING_URI, PYTEST_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/clustering-ml-models/templates/env-config.yaml` for test specifications

### 3. Parse Input
Extract from $ARGUMENTS: pipeline location, test scope, acceptance criteria. Request clarification if incomplete.

### 4. Analyze Test Requirements
Identify testable components: data preprocessing, model training, evaluation, governance controls.

### 5. Generate Test Suite
Create comprehensive tests: unit tests, integration tests, performance tests, fairness tests.

### 6. Add Recommendations
Include testing best practices.

### 7. Validate and Report
Execute: `pytest tests/ --junitxml=results.xml --cov --cov-report=html`
Generate report. Report completion.

## Error Handling
**Test Failures**: Document and remediate.
**Performance Issues**: Optimize and retest.

## Examples
**Example 1**: `/test-clustering-ml-models Validate ML pipeline` - Output: Test suite with validation
**Example 2**: `/test-clustering-ml-models Fairness testing` - Output: Fairness validation suite

## References
