---
description: Refactor Isolation Forest Model pipeline for compliance, performance, and maintainability (Isolation Forest Model)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype isolation-forest-model --json ` and parse for MLFLOW_TRACKING_URI, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/isolation-forest-model/templates/env-config.yaml` for best practices

### 3. Parse Input
Extract from $ARGUMENTS: pipeline location, refactoring goals. Request clarification if incomplete.

### 4. Analyze Current State
Assess code quality, governance compliance, performance, maintainability.

### 5. Generate Refactoring Plan
Create improvements for governance, performance, code quality, monitoring.

### 6. Implement Refactorings
Generate refactored pipeline with improvements.

### 7. Validate and Report
Generate report. Report completion.

## Error Handling
**Breaking Changes**: Plan migration carefully.
**Performance Regression**: Benchmark before and after.

## Examples
**Example 1**: `/refactor-isolation-forest-model Add governance controls` - Output: Enhanced pipeline with MLflow and fairness
**Example 2**: `/refactor-isolation-forest-model Optimize training performance` - Output: Performance-optimized pipeline

## References
