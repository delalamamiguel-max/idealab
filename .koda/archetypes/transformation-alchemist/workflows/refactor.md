---
description: Refactor PySpark/Scala transformation to apply performance, quality, and idempotency patterns (Transformation Alchemist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype transformation-alchemist --json ` and parse for DATABRICKS_VERSION, SPARK_VERSION, DELTA_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/transformation-alchemist/templates/env-config.yaml` for runtime, cluster specs, paths

### 3. Parse Input
Extract from $ARGUMENTS: existing PySpark/Scala file path or inline code, refactoring goals (performance, idempotency, quality, caching), target improvements. Request clarification if incomplete.

### 4. Analyze Existing Code
Load and analyze existing transformation:
- Identify hard-stop rule violations (missing schema, df.collect() on unbounded data, non-idempotent writes, hard-coded paths, missing quality checks, cache without unpersist, UDFs when built-ins exist, hardcoded credentials)
- Identify missing mandatory patterns (idempotent writes, retry logic, quality validation, structured logging, schema enforcement, exception handling)
- Identify opportunities for preferred patterns (functions ≤75 LOC, early filters, partition pruning, broadcast hints)

Report findings with line numbers and severity.

### 5. Generate Refactored Transformation

Create refactored PySpark code applying hard-stop fixes (remove df.collect(), implement Delta MERGE, add unpersist(), replace UDFs with built-ins, move credentials to keyvault), mandatory patterns (schema enforcement, retry logic, structured logging, quality checks, external configs), and preferred patterns (early filters, repartition after wide transforms, broadcast small tables, explain() for complex queries).

Include complete code example with imports, configuration loading, logging functions, retry decorators, extract/transform/load phases, and quality validation.

### 6. Add Recommendations

Include inline comments for performance (broadcast joins, caching strategy, partition pruning), quality (Great Expectations checks), monitoring (Spark metrics), and cost optimization (cluster sizing, autoscaling).

Provide summary of improvements with performance impact estimates and next steps.

### 7. Validate and Report


Generate optional test cases with sample data. Report completion with file paths, applied improvements, performance estimates, next steps.

## Error Handling

**Hard-Stop Violations in Original**: Explain each violation clearly, show compliant alternative with code example.

**Incomplete Input**: List missing information (file path or code, refactoring goals, constraints), provide well-formed example.

**Environment Failure**: Report missing Spark/Delta configuration, suggest cluster setup and library installation.

## Examples

**Example 1: Idempotent Writes**
```
/refactor-spark Convert overwrite mode to Delta MERGE in customer_transform.py

Input: df.write.mode("overwrite").save(path)
Output: Refactored with Delta MERGE for idempotency, retry logic, quality checks
```

**Example 2: Performance Optimization**
```
/refactor-spark Optimize slow transformation with early filters and caching

Input: Complex transformation with late filters, multiple actions
Output: Refactored with early filter pushdown, proper caching/unpersist, repartitioning
```

**Example 3: Quality Integration**
```
/refactor-spark Add data quality validation to sales_pipeline.py

Input: Transformation without quality checks
Output: Refactored with Great Expectations checks, structured logging, exception handling
```

## References

