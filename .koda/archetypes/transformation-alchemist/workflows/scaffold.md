---
description: Generate PySpark/Scala transformation scaffold with Delta Lake and quality checks (Transformation Alchemist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype transformation-alchemist --json ` and parse for DATABRICKS_VERSION, SPARK_VERSION, DELTA_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/transformation-alchemist/templates/env-config.yaml` for runtime, cluster specs, paths

### 3. Parse Input
Extract from $ARGUMENTS: input schemas with sample rows, transformation goal (join/SCD-2/feature engineering), output requirements, quality thresholds. Request clarification if incomplete.

### 4. Validate Constraints
Check against hard-stop rules:
- ✘ Refuse non-idempotent writes without MERGE or overwriteDynamic
- ✘ Refuse missing input schema or sample data
- ✘ Refuse transformations without quality checks
- ✘ Refuse functions >75 LOC without refactoring
If violated, explain clearly and suggest compliant alternative.

### 5. Generate Transformation Scaffold

Create PySpark notebook with modular phases: configuration, extraction with schema validation, transformation with business logic, loading with idempotent writes (Delta MERGE), quality validation with thresholds.

Structure includes: config loading from YAML, Spark session initialization with Delta extensions, extract function with schema assertions, transform function with modular logic (≤75 LOC per function), load function using Delta MERGE for idempotency, validate function with quality checks, main execution with try/except/finally, structured logging with timestamps and metrics.

Apply mandatory patterns: idempotent writes using MERGE or overwriteDynamic, schema validation before processing, quality checks with fail-fast on threshold breaches, modular functions ≤75 LOC, retry logic for external I/O (≥3 retries with exponential backoff), structured logging with stage/record_count/sample_hash, configuration-driven parameters from YAML, separation of extract/transform/validate phases.

### 6. Add Recommendations

Include inline comments for: broadcast joins when dataset ≤10MB, caching when reuse >2, partition pruning strategies, dynamic shuffle partition tuning, checkpoint usage for stateful operations.

### 7. Validate and Report


Generate mandatory pytest test harness covering edge cases. Report completion with file paths, applied guardrails, next steps, and recommendations.

## Error Handling

**Hard-Stop Violations**: Explain violation (e.g., missing MERGE for idempotency), suggest compliant alternative with code example.

**Incomplete Input**: List missing information (input schema with types, sample rows, transformation requirements), provide well-formed example.

**Environment Failure**: Report missing Spark/Delta/Databricks configuration, suggest installation and setup steps.

## Examples

**Customer Aggregation**: `/scaffold-spark Calculate customer lifetime value from orders table, aggregate by customer_id, write to Delta table with MERGE`
Output: PySpark notebook with extract/transform/load phases, quality checks, idempotent Delta MERGE.

**SCD Type 2**: `/scaffold-spark Implement SCD Type 2 for customer dimension, track changes with valid_from/valid_to, use Delta MERGE`
Output: PySpark notebook with SCD-2 logic, history tracking, Delta operations, quality validation.

**Feature Engineering**: `/scaffold-spark Engineer ML features from user activity, calculate recency/frequency/monetary, partition by date`
Output: PySpark notebook with feature calculations, partitioning strategy, quality checks.

## References

Original: `prompts/01_scaffold_prompt.md` | Constitution: (pre-loaded above)
