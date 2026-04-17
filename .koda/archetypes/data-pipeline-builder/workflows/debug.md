---
description: Debug data ingestion pipeline failures (Pipeline Builder)
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
Extract from $ARGUMENTS: ingestion pipeline file, error message (merge failed, duplicate key, checkpoint error), symptoms (data not loading, partial loads, duplicates), context (source, target, data volume). Request clarification if incomplete.

### 4. Analyze Problem

Identify error category: merge errors (duplicate keys, constraint violations, schema mismatch), checkpoint errors (corrupted state, version conflicts), data quality issues (malformed data, schema violations), performance issues (slow ingestion, timeouts). Analyze error logs, data samples, and pipeline code. Report findings with error type, root cause, data impact.

### 5. Generate Fix

Create fixed pipeline addressing root cause: fix merge logic (handle duplicates, add deduplication, fix key logic), fix checkpointing (reset checkpoint, fix state management), fix data quality (add validation, handle malformed data), optimize performance (parallel loading, partition tuning). Include complete fixed pipeline with proper error handling and recovery.

### 6. Add Recommendations

Include recommendations for prevention (data validation, testing, monitoring), testing (test with edge cases, schema changes, large volumes), monitoring (ingestion metrics, data freshness, error rates). Provide summary with root cause, fix, data recovery steps.

### 7. Validate and Report


## Error Handling

**Insufficient Error Information**: Request complete error logs, data samples, and pipeline configuration.

**Cannot Reproduce**: Request source data, environment details, and execution context.

**Data Loss Risk**: Provide immediate mitigation steps and recovery procedures.

## Examples

**Example 1: Duplicate Key Error**
```
/debug-pipeline MERGE failing with "duplicate key violation"

Root Cause: Source has duplicate records, merge key not unique
Fix: Added deduplication step, implemented last-write-wins logic
```

**Example 2: Checkpoint Corruption**
```
/debug-pipeline Streaming ingestion failing to restart from checkpoint

Root Cause: Checkpoint directory corrupted after cluster failure
Fix: Reset checkpoint, implemented checkpoint backup strategy
```

**Example 3: Schema Mismatch**
```
/debug-pipeline Ingestion failing with "column not found" error

Root Cause: Source schema changed, added new column
Fix: Implemented schema evolution, added schema validation step
```

## References

