---
description: Generate test harness for data ingestion pipelines (Pipeline Builder)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-pipeline-builder --json ` and parse for SPARK_VERSION, PYTEST_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- Read `aifc-master-aggregation-repo/archetypes/03-data-engineering/data-pipeline-builder-constitution.md` for hard-stop rules
- Load `aifc-master-aggregation-repo/archetypes/03-data-engineering/templates/env-config.yaml` for test configuration

### 3. Parse Input
Extract from $ARGUMENTS: ingestion pipeline file, testing framework (pytest), coverage goals (merge logic, data validation, incremental loading), test scenarios. Request clarification if incomplete.

### 4. Analyze Code

Identify testable components: merge/upsert logic, incremental loading, watermark management, data validation, error handling. Determine test scenarios: unit tests (merge logic, deduplication), integration tests (end-to-end ingestion), data quality tests (schema, duplicates), edge cases (empty data, schema changes). Report test coverage plan.

### 5. Generate Test Suite

Create pytest test suite with sample source data, unit tests for merge logic, integration tests for pipeline, data validation tests, edge case tests (empty, duplicates, schema changes). Include complete test code.

### 6. Add Recommendations

Include recommendations for test data (create realistic samples, include edge cases), CI/CD integration (test on PR, validate incremental logic), coverage improvements (test all merge scenarios, validate watermarks), monitoring (track ingestion metrics). Provide summary.

### 7. Validate and Report


## Error Handling

**Insufficient Code**: Request complete pipeline code.

**No Test Data**: Provide guidance on creating sample datasets.

**Missing Delta Setup**: Suggest Delta Lake test configuration.

## Examples

**Example 1**: `/test-pipeline Generate tests for customer_ingest.py` - Output: 12 tests covering merge and validation

**Example 2**: `/test-pipeline Create incremental tests for orders_pipeline.py` - Output: Watermark and incremental loading tests

**Example 3**: `/test-pipeline Add edge case tests for product_ingestion.py` - Output: Schema change and duplicate handling tests

## References

