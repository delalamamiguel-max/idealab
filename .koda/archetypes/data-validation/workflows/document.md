---
description: Generate documentation for data quality suites and validation rules (Quality Guardian)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-validation --json ` and parse for VALIDATION_FRAMEWORK, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/data-validation/templates/env-config.yaml` for documentation templates

### 3. Parse Input
Extract from $ARGUMENTS: validation suite location, target audience, documentation scope. Request clarification if incomplete.

### 4. Analyze Validation Suite
Extract expectations, thresholds, execution schedules, quality metrics.

### 5. Generate Documentation Package
Create: Validation Guide, Quality Standards, Threshold Documentation, Operations Runbook, Stakeholder Reports.

### 6. Add Recommendations
Include quality improvement procedures, validation reviews, continuous monitoring.

### 7. Validate and Report
Generate documentation. Report completion.

## Error Handling
**Incomplete Information**: Request validation configurations and quality metrics.
**Missing Documentation**: Document all expectations and thresholds.

## Examples
**Example 1**: `/document-data-validation Create validation documentation package` - Output: Complete docs with expectations and runbooks
**Example 2**: `/document-data-validation Generate quality standards documentation` - Output: Quality standards with stakeholder reports

## References
