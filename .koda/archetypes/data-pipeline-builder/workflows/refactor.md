---
description: Refactor data ingestion pipeline to improve reliability, performance, and idempotency (Pipeline Builder)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-pipeline-builder --json ` and parse for SPARK_VERSION, DELTA_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- Read `data-pipeline-builder-constitution.md` for hard-stop rules
- Load `templates/env-config.yaml` for ingestion patterns, merge strategies

### 3. Parse Input
Extract from $ARGUMENTS: existing ingestion code file path, refactoring goals (incremental loading, merge logic, error handling, performance), constraints. Request clarification if incomplete.

### 4. Analyze Existing Code
Load and analyze existing ingestion pipeline: identify hard-stop rule violations (full load only, no incremental support, missing merge logic, no watermark tracking, missing error handling, no data validation, hardcoded paths), identify missing mandatory patterns (incremental loading with watermarks, merge/upsert logic, retry with backoff, data quality checks, structured logging, idempotent operations), identify optimization opportunities (partition pruning, predicate pushdown, parallel ingestion, compression).

Report findings with line numbers and impact assessment.

### 5. Generate Refactored Pipeline

Create refactored ingestion pipeline applying hard-stop fixes (implement incremental loading, add merge/upsert logic, add watermark tracking, implement error handling, add data validation, parameterize paths), mandatory patterns (watermark-based incremental loading, Delta MERGE for upserts, retry logic, quality validation, structured logging, external configuration), and preferred patterns (partition pruning, parallel loading, compression, monitoring hooks).

Include complete code example with watermark management, merge logic, and error handling.

### 6. Add Recommendations

Include inline comments for scalability (parallel ingestion, partition strategies), reliability (checkpointing, exactly-once semantics), monitoring (ingestion metrics, data freshness alerts), and cost optimization (compression, partition pruning).

Provide summary with performance improvements and operational benefits.

### 7. Validate and Report


Generate optional test cases with sample data. Report completion with file paths, improvements, next steps.

## Error Handling

**Hard-Stop Violations in Original**: Explain violation, show compliant alternative with incremental loading and merge logic.

**Incomplete Input**: List missing information, provide well-formed example.

**Environment Failure**: Report missing Spark/Delta configuration, suggest setup steps.

## Examples

**Example 1: Add Incremental Loading**
```
/refactor-pipeline Convert full load to incremental in customer_ingest.py

Input: Full table reload every run
Output: Refactored with watermark-based incremental loading, merge logic
```

**Example 2: Improve Merge Logic**
```
/refactor-pipeline Add upsert logic to orders_ingestion.py

Input: Overwrite mode causing data loss
Output: Refactored with Delta MERGE, SCD Type 1 logic, audit columns
```

**Example 3: Add Error Handling**
```
/refactor-pipeline Add retry and validation to product_pipeline.py

Input: Pipeline fails on transient errors
Output: Refactored with retry logic, data validation, error logging
```

## References

