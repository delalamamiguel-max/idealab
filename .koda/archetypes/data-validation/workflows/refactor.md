---
description: Refactor data quality suite to enhance validation coverage and enforcement (Quality Guardian)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-validation --json ` and parse for VALIDATION_FRAMEWORK, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/data-validation/templates/env-config.yaml` for best practices

### 3. Parse Input
Extract from $ARGUMENTS: validation suite location, refactoring goals. Request clarification if incomplete.

### 4. Analyze Current State
Assess validation coverage, expectation accuracy, threshold appropriateness, execution efficiency.

### 5. Generate Refactoring Plan
Create improvements for expanded coverage, refined expectations, optimized thresholds, better monitoring.

### 6. Implement Refactorings
Generate enhanced validation suite with improved quality checks.

### 7. Validate and Report
Generate report. Report completion.

## Error Handling
**Coverage Gaps**: Prioritize critical tables and add validation incrementally.
**Performance Impact**: Optimize validation execution and sampling.

## Examples
**Example 1**: `/refactor-data-validation Expand validation coverage for data platform` - Output: Enhanced suite with additional expectations
**Example 2**: `/refactor-data-validation Optimize validation performance` - Output: Efficient suite with sampling

## References
