---
description: Generate data ingestion pipeline with merge/overwrite logic and incremental loading (Pipeline Builder)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-pipeline-builder --json ` and parse for SPARK_VERSION, DELTA_VERSION, INGEST_TYPE, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- Read `aifc-master-aggregation-repo/archetypes/03-data-engineering/data-pipeline-builder-constitution.md` for hard-stop rules
- Load `aifc-master-aggregation-repo/archetypes/03-data-engineering/templates/env-config.yaml` for source config, target config, merge keys

### 3. Parse Input
Extract from $ARGUMENTS: data source (database/API/files), ingestion pattern (full/incremental/CDC), target destination, merge logic (insert/update/upsert), quality requirements. Request clarification if incomplete.

### 4. Validate Constraints
Check against hard-stop rules:
- ✘ Refuse ingestion without idempotency (merge keys)
- ✘ Refuse missing error handling and retry logic
- ✘ Refuse no data quality validation
- ✘ Refuse full loads without justification for large tables
If violated, explain clearly and suggest compliant alternative.

### 5. Generate Ingestion Pipeline

**Determine Input/Output Pattern**:
- If Legacy/Shell-based: Use `os.environ.get('VAR')` for config.
- If Databricks: Use `dbutils.widgets.get('var')`.
- Default: Use `.yaml` config loader.

Create ingestion pipeline with phases: source connection with retry logic, incremental extraction using watermark (timestamp/sequence), data validation and cleansing, schema evolution handling, target write with merge/overwrite logic, watermark update for next run, metrics collection and logging.

Ingestion patterns: full load (overwrite entire table, use for small dimensions), incremental load (filter by watermark, append new records), upsert (merge on key, update existing + insert new), CDC (capture changes, apply to target), SCD Type 2 (track history with valid_from/valid_to).

Merge logic: identify merge keys (primary key or business key), detect changes (compare hash or all columns), handle deletes (soft delete flag or hard delete), manage conflicts (last write wins or custom logic), optimize merge performance (partition by merge key).

Apply mandatory patterns: idempotent writes using merge keys, incremental loading with watermark, retry logic for source connections (≥3 retries), data validation before write, schema evolution support, metrics emission (rows read/written/failed), structured logging with run metadata, error handling with alerting.

### 6. Add Recommendations

Include comments for: partition strategy for target table, compaction schedule for Delta, vacuum policy for old versions, monitoring for data freshness, alerting for ingestion failures.

### 7. Validate and Report


Generate optional integration tests with sample data. Report completion with file paths, ingestion pattern, merge logic, next steps.

## Error Handling

**Hard-Stop Violations**: Explain violation (e.g., missing merge keys), suggest compliant alternative with merge configuration.

**Incomplete Input**: List missing information (source, target, merge keys, pattern), provide well-formed example.

**Environment Failure**: Report missing Spark/Delta configuration, suggest setup steps.

## Examples

**Database Ingestion**: `/scaffold-pipeline Ingest customer table from PostgreSQL, incremental by updated_at, upsert to Delta table by customer_id`
Output: PySpark pipeline with JDBC source, watermark tracking, Delta merge, quality checks.

**API Ingestion**: `/scaffold-pipeline Ingest orders from REST API, paginated, incremental by order_date, append to Delta table`
Output: PySpark pipeline with API client, pagination handling, incremental logic, error retry.

**File Ingestion**: `/scaffold-pipeline Ingest CSV files from S3, full load daily, overwrite target table, validate schema`
Output: PySpark pipeline with S3 source, schema validation, overwrite mode, metrics.

## References

