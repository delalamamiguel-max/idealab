---
description: Generate documentation for PySpark/Scala transformations (Transformation Alchemist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype transformation-alchemist --json ` and parse for SPARK_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/transformation-alchemist/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: Spark code file path, target audience, documentation scope (README, data flow, architecture). Request clarification if incomplete.

### 4. Analyze Code/System

Analyze transformation: identify input/output schemas, document transformation logic, explain data quality checks, note performance optimizations, identify configuration parameters, document dependencies and prerequisites.

### 5. Generate Documentation

Create comprehensive documentation with: transformation purpose and business logic, input/output schema documentation, data flow diagram, configuration guide, performance tuning guide, troubleshooting section, monitoring and alerting setup.

Include README.md, inline code docstrings, architecture diagrams, runbook.

### 6. Add Recommendations

Include recommendations for documentation maintenance, performance monitoring, data quality validation, operational procedures, disaster recovery.

### 7. Validate and Report


Generate documentation artifacts. Report completion.

## Error Handling

**Insufficient Context**: Request transformation purpose and data context.

**Complex Pipeline**: Break documentation by transformation stage.

**Missing Schema**: Request input/output schema documentation.

## Examples

**Example 1**: `/document-spark Create docs for customer_transform.py` - Output: README with transformation logic, schemas, examples

**Example 2**: `/document-spark Generate architecture docs for ETL pipeline` - Output: Architecture docs with data flow diagrams

**Example 3**: `/document-spark Document Spark job for operators` - Output: Operational runbook with monitoring and troubleshooting

## References

