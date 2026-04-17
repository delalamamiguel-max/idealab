---
description: Compare data quality validation approaches and frameworks (Quality Guardian)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-validation --json ` and parse for VALIDATION_FRAMEWORK, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/data-validation/templates/env-config.yaml` for comparison framework

### 3. Parse Input
Extract from $ARGUMENTS: comparison type, candidate frameworks, evaluation criteria. Request clarification if incomplete.

### 4. Generate Comparison Framework
Evaluate validation frameworks (Great Expectations vs Deequ vs custom), validation approaches, threshold strategies.

### 5. Create Comparison Matrix
Generate comparison with coverage, performance, integration, cost.

### 6. Add Recommendations
Recommend framework with justification and implementation guidance.

### 7. Validate and Report
Generate report. Report completion.

## Error Handling
**Insufficient Context**: Request data characteristics and quality requirements.
**Framework Compatibility**: Evaluate integration with existing tools.

## Examples
**Example 1**: `/compare-data-validation Great Expectations vs Deequ` - Output: Framework comparison with integration analysis
**Example 2**: `/compare-data-validation Validation threshold strategies` - Output: Strategy comparison with best practices

## References
