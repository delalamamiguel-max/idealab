---
description: Compare PySpark/Scala transformation approaches and patterns (Transformation Alchemist)
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
Extract from $ARGUMENTS: transformation problem, comparison criteria (performance, cost, maintainability), data volume, constraints. Request clarification if incomplete.

### 4. Generate Alternatives

Create 2-3 Spark approaches: DataFrame API (recommended), RDD-based (low-level control), SQL-based (familiar syntax). Each with code, performance characteristics, use cases.

### 5. Generate Comparison Matrix

Compare on: performance (execution time, shuffle), cost (compute, storage), maintainability, complexity, scalability, optimization potential. Provide metrics and analysis.

### 6. Add Recommendations

Recommend approach with justification. Include performance tuning, cost optimization, migration path, testing strategy.

### 7. Validate and Report


## Error Handling

**Insufficient Context**: Request data volume, transformation complexity, performance requirements.

**Unclear Trade-offs**: Explain key differentiators with examples.

**Performance Ambiguity**: Request baseline metrics or profiling data.

## Examples

**Example 1**: `/compare-spark Compare DataFrame vs RDD for complex joins` - Output: 2 approaches with performance comparison

**Example 2**: `/compare-spark Batch vs streaming for real-time pipeline` - Output: Architecture comparison with latency analysis

**Example 3**: `/compare-spark Compare partitioning strategies for skewed data` - Output: 3 strategies with data distribution analysis

## References

