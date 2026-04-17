---
description: Generate documentation for data quality suites and validation rules (Quality Guardian)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype quality-guardian --json ` and parse for GE_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/quality-guardian/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: quality suite file, target audience, documentation scope (validation rules, quality metrics, runbook). Request clarification if incomplete.

### 4. Analyze Code/System

Analyze quality suite: identify all expectations and validations, document thresholds and parameters, explain business rules, note data profiling results, identify failure actions, document quality metrics and KPIs.

### 5. Generate Documentation

Create comprehensive documentation with: quality suite overview, validation rules reference, threshold documentation, quality metrics dashboard, troubleshooting guide for failures, operational runbook.

Include README.md, validation rules catalog, quality dashboard config, runbook.

### 6. Add Recommendations

Include recommendations for documentation maintenance, quality monitoring, threshold tuning, stakeholder communication, continuous improvement.

### 7. Validate and Report


Generate documentation artifacts. Report completion.

## Error Handling

**Insufficient Context**: Request business rules and quality requirements.

**Complex Suite**: Break documentation by data domain or validation type.

**Missing Thresholds**: Request threshold justification and tuning history.

## Examples

**Example 1**: `/document-quality Create docs for sales_validation suite` - Output: Validation rules docs with business context

**Example 2**: `/document-quality Generate quality metrics dashboard docs` - Output: Dashboard docs with KPIs and interpretation

**Example 3**: `/document-quality Document quality suite for data stewards` - Output: Non-technical docs with quality rules and actions

## References

