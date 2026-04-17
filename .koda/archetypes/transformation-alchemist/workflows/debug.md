---
description: Debug PySpark/Scala transformation errors and performance issues (Transformation Alchemist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype transformation-alchemist --json ` and parse for SPARK_VERSION, DELTA_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/transformation-alchemist/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: PySpark/Scala file path or inline code, error message (Spark exceptions, Java stack traces), symptoms (job fails, OOM errors, data skew), context (cluster config, data volume). Request clarification if incomplete.

### 4. Analyze Problem

Identify error category: Spark errors (OutOfMemoryError, shuffle failures, executor lost), Delta errors (concurrent writes, schema mismatch), logic errors (wrong transformations, data quality issues), performance issues (data skew, inefficient operations, excessive shuffles).

Analyze Spark UI metrics, error messages, and code patterns. Check against constitution for violations.

Report findings with stage/task info, root cause, and performance impact.

### 5. Generate Fix

Create fixed transformation addressing root cause: fix memory issues (repartition, broadcast, caching strategy), fix Delta operations (proper MERGE, schema evolution), correct logic errors (fix transformations, add validations), optimize performance (pushdown filters, avoid UDFs, optimize joins).

Include complete fixed code with Spark configuration tuning and monitoring hooks.

### 6. Add Recommendations

Include recommendations for prevention (schema enforcement, quality checks, monitoring), testing (unit tests with sample data, integration tests, performance tests), monitoring (Spark metrics, data quality dashboards, alerting).

Provide summary with root cause, fix, performance impact, and prevention strategies.

### 7. Validate and Report


Generate optional test cases. Report completion with root cause, fix, performance metrics.

## Error Handling

**Insufficient Error Information**: Request Spark UI logs, executor logs, and cluster configuration.

**Cannot Reproduce**: Request data sample, cluster specs, and execution environment.

**Multiple Possible Causes**: Provide systematic debugging with Spark UI analysis.

## Examples

**Example 1: OutOfMemoryError**
```
/debug-spark Job failing with "java.lang.OutOfMemoryError: GC overhead limit exceeded"

Root Cause: Data skew causing single executor to process 80% of data
Fix: Repartitioned by key with salt, increased executor memory, optimized shuffle
Performance: Job now completes in 10min vs timing out at 60min
```

**Example 2: Schema Mismatch**
```
/debug-spark Delta MERGE failing with "schema mismatch" error

Root Cause: Source has new column not in target schema
Fix: Added schema evolution configuration, implemented column mapping
```

**Example 3: Slow Performance**
```
/debug-spark Transformation taking 2 hours, used to take 20 minutes

Root Cause: UDF replacing built-in function, causing deserialization overhead
Fix: Replaced UDF with native Spark function, added early filters
Performance: Reduced runtime from 2h to 15min
```

## References

