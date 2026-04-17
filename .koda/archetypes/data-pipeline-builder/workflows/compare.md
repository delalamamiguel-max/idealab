---
description: Compare data ingestion approaches and patterns (Pipeline Builder)
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
Extract from $ARGUMENTS: ingestion problem, comparison criteria (latency, reliability, cost), data characteristics, constraints. Request clarification if incomplete.

### 4. Generate Alternatives

Create 2-3 ingestion approaches: Batch ingestion (scheduled, efficient), Streaming ingestion (real-time, complex), Micro-batch (balanced). Each with implementation, use cases, pros/cons.

### 5. Generate Comparison Matrix

Compare on: latency, reliability, cost, complexity, scalability, data freshness, error handling. Provide scores and analysis.

### 6. Add Recommendations

Recommend approach with justification. Include implementation guidance, testing strategy, monitoring setup, migration path.

### 7. Validate and Report


## Error Handling

**Insufficient Context**: Request data volume, latency requirements, source characteristics.

**Unclear Requirements**: Clarify real-time vs near-real-time vs batch needs.

**Complexity Concerns**: Address operational overhead and team capabilities.

## Examples

**Example 1**: `/compare-pipeline Compare batch vs streaming for customer data` - Output: Approach comparison with latency analysis

**Example 2**: `/compare-pipeline Full load vs incremental ingestion patterns` - Output: Pattern comparison with efficiency analysis

**Example 3**: `/compare-pipeline Compare merge strategies (SCD Type 1 vs Type 2)` - Output: Strategy comparison with storage implications

## References

