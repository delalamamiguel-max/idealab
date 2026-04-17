---
description: Generate data quality validation suite with Great Expectations/Deequ and threshold enforcement (Quality Guardian)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-validation --json ` and parse for VALIDATION_FRAMEWORK, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/data-validation/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: dataset scope, quality dimensions, validation rules, threshold requirements. Request clarification if incomplete.

### 4. Generate Validation Suite
Create validation framework: expectations (completeness, uniqueness, range validation, format validation, referential integrity), threshold enforcement (warning vs critical thresholds, alerting configuration), suite organization (by table, by criticality, by frequency), execution scheduling (real-time, batch, on-demand).

### 5. Generate Quality Monitoring
Implement quality dashboards, validation reports, trend analysis, anomaly detection, quality SLAs.

### 6. Add Recommendations
Include validation best practices, quality improvement cycles, data profiling, stakeholder reporting.

### 7. Validate and Report
Generate suite. Report completion.

## Error Handling
**Missing Baselines**: Profile data and establish quality baselines.
**Threshold Violations**: Document and remediate quality issues.

## Examples
**Example 1**: `/scaffold-data-validation Create validation suite for customer tables` - Output: Complete validation with expectations and monitoring
**Example 2**: `/scaffold-data-validation Generate quality checks with Great Expectations` - Output: GE suite with threshold enforcement

## References
