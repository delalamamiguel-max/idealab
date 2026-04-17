---
description: Generate documentation for data ingestion pipelines (Pipeline Builder)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-pipeline-builder --json ` and parse for SPARK_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- Read `data-pipeline-builder-constitution.md` for hard-stop rules
- Load `templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: ingestion pipeline file, target audience, documentation scope (README, data flow, operational runbook). Request clarification if incomplete.

### 4. Analyze Code/System

### 5. Generate Documentation

Create comprehensive documentation with: pipeline overview and purpose, source/target documentation, data flow diagram, merge strategy explanation, configuration guide, monitoring and alerting, troubleshooting guide, operational runbook.

Include README.md, data flow diagrams, operational runbook, configuration reference.

### 6. Add Recommendations

Include recommendations for documentation maintenance, operational procedures, monitoring setup, data quality checks, disaster recovery.

### 7. Validate and Report


Generate documentation artifacts. Report completion.

## Error Handling

**Insufficient Context**: Request source/target details and business requirements.

**Complex Pipeline**: Break documentation by ingestion stage.

**Missing SLAs**: Request data freshness and reliability requirements.

## Examples

**Example 1**: `/document-pipeline Create docs for customer_ingestion pipeline` - Output: README with data flow, merge logic, monitoring

**Example 2**: `/document-pipeline Generate operational runbook for orders pipeline` - Output: Runbook with procedures, troubleshooting, escalation

**Example 3**: `/document-pipeline Document incremental loading strategy` - Output: Technical docs with watermark management and recovery procedures

## References

