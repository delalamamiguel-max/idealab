---
description: Generate validation test suite for XFlow JSON configurations (XFlow Orchestrator)
---

User input: $ARGUMENTS

## Execution Steps

## Execution Rules (NON-NEGOTIABLE)

**These rules govern HOW this workflow executes. Violating them is a hard-stop.**

1. **ONE question per message.** Each interactive question MUST be its own separate `ask_user_question` call. NEVER combine multiple questions into a single prompt.
2. **NO skipping steps.** Every interactive question in Step 3b MUST be asked in order. The ONLY exception is when the user already provided the information in $ARGUMENTS.
3. **WAIT for user response** before proceeding to the next question. Do not assume defaults unless the workflow explicitly says to apply a default silently.
4. **NEVER generate the test suite before collecting all required input.** If test scope, output format, or strictness is unclear, ASK before generating.

---

### 0. Set ARCHETYPES_BASEDIR [⋯]
 
**SUCCESS CRITERIA**:
- Search for directory: "00-core-orchestration"
- Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory
 
**HALT IF**:
- Directory "00-core-orchestration" is not found
- `${ARCHETYPES_BASEDIR}` is not set (workflow will halt if this variable is not present in the environment)
 
// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Environment Setup
// turbo
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype xflow-orchestrator --json` and parse for ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- Read `xflow-orchestrator-constitution.md` for hard-stop rules (all sections I through IV)
- Load `templates/env-config.yaml` for reference defaults

### 3. Parse Input
Extract from $ARGUMENTS:
- **Config file path**: path to the XFlow JSON config to test — read and parse the file completely
- **Test scope** (one or more):
  - `all` — run all test categories (default)
  - `structural` — JSON syntax, root fields, array structure
  - `schema` — column definitions, types, duplicates, partitions
  - `source` — source-type-specific field validation
  - `target` — target configuration, write mode, control columns
  - `transformations` — transformation parameters and column references
  - `validations` — validation parameters and column references
  - `cross-field` — cross-field dependency checks
  - `security` — credential security, PII encryption
  - `compliance` — full constitution compliance audit
  - `performance` — performance-related settings audit
  - `data-quality` — global transformation and validation coverage
- **Output format**:
  - `pytest` — Python pytest test file (default)
  - `json` — JSON validation report
  - `inline` — direct analysis output
  - `ci` — CI/CD-compatible output with exit codes
- **Strictness level**:
  - `strict` — fail on any warning (all constitution rules enforced)
  - `standard` — fail on hard-stop violations, warn on mandatory patterns (default)
  - `lenient` — fail only on hard-stop violations

If a config file is referenced, read and parse it. Request clarification if no config file is provided.

### 3b. Interactive Test Setup

**If test scope, output format, or strictness is not specified in $ARGUMENTS, ASK these questions:**

**Question 1 — Test Scope:**
> What test scope do you want?
> - **All tests** — run all 107 tests across 11 categories
> - **Critical only** — structural + security + compliance tests
> - **Data quality** — schema + validations + transformations + cross-field tests
> - **Let me pick** — I'll choose specific test categories

Use `ask_user_question` with these 4 options.

<!-- HALT: Wait for user response before continuing -->

If "Let me pick", present the 11 categories as a multi-select:
> Select test categories (multiple allowed):
> - **Structural** — JSON syntax, root fields, array structure
> - **Schema** — column definitions, types, duplicates, partitions
> - **Source** — source-type-specific field validation
> - **Target** — target config, write mode, control columns
> - **Transformations** — transformation parameters and column references
> - **Validations** — validation parameters and column references
> - **Cross-field** — cross-field dependency checks
> - **Security** — credential security, PII encryption

Use `ask_user_question` (allowMultiple=true) with up to 4 options at a time.

<!-- HALT: Wait for user response before continuing to Question 2 -->

**Question 2 — Output Format:**
> What output format?
> - **pytest** — Python pytest test file you can run directly
> - **JSON report** — structured validation report with pass/fail/warn counts
> - **Inline** — direct analysis output in chat
> - **CI/CD** — JUnit XML compatible for CI pipelines

Use `ask_user_question` with these 4 options.

<!-- HALT: Wait for user response before continuing to Question 3 -->

**Question 3 — Strictness Level:**
> How strict should the tests be?
> - **Strict** — fail on any warning (all constitution rules enforced as hard failures)
> - **Standard** (default) — fail on hard-stop violations, warn on mandatory patterns
> - **Lenient** — fail only on hard-stop violations, ignore all other rules

Use `ask_user_question` with these 3 options.

<!-- HALT: Wait for user response before continuing to Step 4 -->

### 4. Analyze Config for Testable Components

**Parse the XFlow JSON config and generate tests for EVERY constitution rule and cross-field dependency.**

---

#### Test Category 1 — JSON Structural Tests (9 tests)

| Test ID | Test Name | Rule | Check |
|---------|-----------|------|-------|
| S-001 | `test_valid_json` | Basic | Config is valid JSON, parseable without errors |
| S-002 | `test_is_dict` | Basic | Root is a JSON object (dict), not array or primitive |
| S-003 | `test_mandatory_root_fields` | I.Root.1 | All 9 mandatory fields present: srcId, appId, createdBy, dataLibrary, rimPolicyName, sourceContact, motsId, source, targets |
| S-004 | `test_targets_is_array` | I.Root.2 | `targets` is a JSON array `[]`, not object `{}` |
| S-005 | `test_targets_not_empty` | I.Root.2 | `targets` array has at least one element |
| S-006 | `test_valid_feed_type` | I.Root.3 | `feedType` is `"ING"` or `"MGR"` (if present) |
| S-007 | `test_created_by_email` | I.Root.4 | `createdBy` contains `@` |
| S-008 | `test_source_contact_email` | I.Root.4 | `sourceContact` contains `@` |
| S-009 | `test_mots_id_integer` | I.Root.1 | `motsId` is an integer |

---

#### Test Category 2 — Schema Tests (12 tests)

| Test ID | Test Name | Rule | Check |
|---------|-----------|------|-------|
| SC-001 | `test_source_schema_exists` | II.Schema.1 | Source has `schema` array with at least one column |
| SC-002 | `test_source_columns_have_name` | I.Schema.1 | Every source schema entry has `columnName` |
| SC-003 | `test_source_columns_have_type` | I.Schema.1 | Every source schema entry has `columnType` |
| SC-004 | `test_source_column_types_valid` | I.Schema.2 | All `columnType` values are valid Spark SQL types: string, int, integer, long, bigint, double, float, boolean, date, timestamp, decimal, binary, short, byte |
| SC-005 | `test_source_no_duplicate_columns` | I.Schema.3 | No duplicate `columnName` in source schema |
| SC-006 | `test_target_schema_exists` | II.Schema.2 | Each target has `schema` array |
| SC-007 | `test_target_columns_have_name` | I.Schema.1 | Every target schema entry has `columnName` |
| SC-008 | `test_target_columns_have_type` | I.Schema.1 | Every target schema entry has `columnType` |
| SC-009 | `test_target_column_types_valid` | I.Schema.2 | All target `columnType` values are valid |
| SC-010 | `test_target_no_duplicate_columns` | I.Schema.3 | No duplicate `columnName` in target schema |
| SC-011 | `test_partition_columns_have_order` | I.Schema.4 | Columns with `partitionOrder` have sequential integer values starting from 1 |
| SC-012 | `test_decimal_columns_have_precision` | II.Column.2 | Decimal columns have `precision` and `scale` |

---

#### Test Category 3 — Source Configuration Tests (per source type)

**JDBC Source Tests (10 tests):**

| Test ID | Test Name | Rule | Check |
|---------|-----------|------|-------|
| SJ-001 | `test_jdbc_connection_type` | I.JDBC.1 | `connectionType` present and in valid enum: ORACLE, SQL_SERVER, MY_SQL, VERTICA, TERRADATA, SNOWFLAKE, TRINO, POSTGRESQL, GENERIC |
| SJ-002 | `test_jdbc_logon_scope` | I.JDBC.1 | `logonScopeName` present |
| SJ-003 | `test_jdbc_logon_secret` | I.JDBC.1 | `logonSecretName` present |
| SJ-004 | `test_jdbc_sql_file_location` | I.JDBC.1 | `sqlFileLocation` is present (mandatory for all JDBC sources, `dbTable` not allowed as source) |
| SJ-005 | `test_snowflake_database` | I.JDBC.3 | If connectionType=SNOWFLAKE, `sfDatabaseName` present |
| SJ-006 | `test_snowflake_schema` | I.JDBC.3 | If connectionType=SNOWFLAKE, `sfSchemaName` present |
| SJ-007 | `test_snowflake_warehouse` | I.JDBC.3 | If connectionType=SNOWFLAKE, `sfWarehouse` present |
| SJ-008 | `test_jdbc_fetch_size` | III.Source.1 | `fetchSize` >= 1000 (warn if < 20000) |

**Kafka Source Tests (7 tests):**

| Test ID | Test Name | Rule | Check |
|---------|-----------|------|-------|
| SK-001 | `test_kafka_bootstrap_servers` | I.Kafka.1 | `bootstrapServers` present |
| SK-002 | `test_kafka_subscribe` | I.Kafka.1 | `subscribe` present |
| SK-003 | `test_kafka_group_id` | I.Kafka.1 | `groupId` present |
| SK-004 | `test_kafka_logon_scope` | I.Kafka.1 | `logonScopeName` present |
| SK-005 | `test_kafka_logon_secret` | I.Kafka.1 | `logonSecretName` present |
| SK-006 | `test_kafkatext_schema` | I.Kafka.2 | If sourceFileFormat=kafkatext, schema has only partition columns |
| SK-007 | `test_kafka_security_protocol` | III.Source.5 | `securityProtocol` is `"SASL_SSL"` (warn if missing) |

**File Source Tests (8 tests):**

| Test ID | Test Name | Rule | Check |
|---------|-----------|------|-------|
| SF-001 | `test_file_source_location` | I.File.1 | `sourceLocation` present |
| SF-002 | `test_file_source_format` | I.File.2 | `sourceFileFormat` present and in valid enum: parquet, orc, avro, csv, fixed, xml, json, kafkatext |
| SF-003 | `test_fixed_length_counts` | I.File.3 | If sourceFileFormat=fixed, `fixedLengthCounts` present |
| SF-004 | `test_xml_row_path` | I.File.4 | If sourceFileFormat=xml, `xmlRowPath` present |
| SF-005 | `test_csv_delimiter` | III.Source.4 | If sourceFileFormat=csv, `csvDelimiter` present (warn if missing) |
| SF-006 | `test_csv_header` | III.Source.4 | If sourceFileFormat=csv, `csvIgnoreHeaderInd` present (warn if missing) |
| SF-007 | `test_file_retention` | III.Source.6 | `fileRetentionDays` present (warn if missing) |
| SF-008 | `test_source_location_abfss` | I.File.1 | `sourceLocation` starts with `abfss://` |

**HTTP File Source Tests (4 tests):**

| Test ID | Test Name | Rule | Check |
|---------|-----------|------|-------|
| SH-001 | `test_http_feed_id` | I.HTTP.1 | `feedId` present |
| SH-002 | `test_http_filter_regex` | III.HTTP.1 | `filterRegex` present (warn if missing) |
| SH-003 | `test_http_file_actions_valid` | I.HTTP.2 | All fileActions have valid actionType |
| SH-004 | `test_http_duplicate_check` | III.HTTP.2 | `duplicateFileCheckInd` present (warn if missing) |

**Azure Files Source Tests (6 tests):**

| Test ID | Test Name | Rule | Check |
|---------|-----------|------|-------|
| SA-001 | `test_azure_pull_config` | I.Azure.1 | `sourcePullConfig` present |
| SA-002 | `test_azure_file_share_name` | I.Azure.1 | `azureFileShare.fileShareName` present |
| SA-003 | `test_azure_account_name` | I.Azure.1 | `azureFileShare.accountName` present |
| SA-004 | `test_azure_sas_vault` | I.Azure.1 | `azureFileShare.sasTokenVaultName` present |
| SA-005 | `test_azure_sas_key` | I.Azure.1 | `azureFileShare.sasTokenSecretKey` present |
| SA-006 | `test_azure_resource_path` | I.Azure.1 | `azureFileShare.resourcePath` present |

---

#### Test Category 4 — Target Configuration Tests (13 tests)

| Test ID | Test Name | Rule | Check |
|---------|-----------|------|-------|
| T-001 | `test_target_location` | I.Target.1 | Every target has `targetLocation` |
| T-002 | `test_target_location_abfss` | I.Target.1 | `targetLocation` starts with `abfss://` |
| T-003 | `test_valid_write_mode` | I.Target.2 | `writeMode` in: append, overwrite, overwritePartition, upsert |
| T-004 | `test_upsert_has_keys` | I.Target.3 | If writeMode=upsert, at least one column has `pk: true` OR `mergeKeys` array present |
| T-005 | `test_overwrite_partition_has_partitions` | I.Target.4 | If writeMode=overwritePartition, at least one column has `partitionOrder` |
| T-006 | `test_valid_target_format` | I.Target.6 | `targetFileFormat` in: delta, parquet, csv, database |
| T-007 | `test_database_target_config` | I.Target.5 | If targetFileFormat=database, `databaseTarget` section present |
| T-008 | `test_control_columns` | II.Target.1 | `controlColumns` present with `fileNameColumnInd` and `creationTimestampColumnInd` |
| T-009 | `test_vacuum_days_delta_only` | I.Target.7 | `vacuumDaysOld` ONLY present when targetFileFormat=delta (FAIL if present for parquet/csv/database) |
| T-010 | `test_vacuum_days_recommended` | III.Target.2 | If targetFileFormat=delta, `vacuumDaysOld` present (warn if missing) |
| T-011 | `test_write_mode_alignment` | II.Target.2 | writeMode aligns with data pattern (warn if overwrite on large table) |
| T-012 | `test_jdbc_write_one_file` | III.Target.3 | If source is JDBC and target is file-based (delta/parquet/csv), `writeOneFileInd` is true (warn if false or missing). Not applicable for non-JDBC sources |
| T-013 | `test_overwrite_type` | III.Target.4 | If writeMode=overwritePartition, `overwriteType` present (warn if missing) |
| T-014 | `test_no_source_file_format_jdbc` | I.File.2 | JDBC sources must not have `sourceFileFormat` field |
| T-015 | `test_no_source_file_format_kafka` | I.File.2 | Kafka sources must not have `sourceFileFormat` field |

---

#### Test Category 5 — Transformation Tests (16 tests)

| Test ID | Test Name | Rule | Check |
|---------|-----------|------|-------|
| TR-001 | `test_transformation_structure` | II.Transform.3 | Each transformation has `targetColumnName`, `sourceColumns`, `transformationSteps` |
| TR-002 | `test_transformation_steps_not_empty` | II.Transform.3 | `transformationSteps` array has at least one step |
| TR-003 | `test_transformation_type_valid` | I.Transform.1 | `transformationType` is valid: hashingAndEncrypt, dateFormat, regex, replace, uppercase, lowercase, epochToTimestamp, addColumn, concatenate, substring, cast, nullHandling, conditional, sql |
| TR-004 | `test_hashing_encrypt_identity` | I.Transform.1 | hashingAndEncrypt has `encryptIdentity` |
| TR-005 | `test_hashing_encrypt_format` | I.Transform.1 | hashingAndEncrypt has `encryptFormat` |
| TR-006 | `test_date_format_params` | I.Transform.2 | dateFormat has `dateSourceFormats` OR `generatedValue` |
| TR-007 | `test_date_format_target` | I.Transform.2 | dateFormat has `dateTargetFormat` (for string target columns) |
| TR-008 | `test_regex_pattern` | I.Transform.3 | regex has `pattern` |
| TR-009 | `test_regex_output_format` | I.Transform.3 | regex has `outputFormat` |
| TR-010 | `test_replace_patterns` | I.Transform.4 | replace has `removePatterns` |
| TR-011 | `test_replace_with` | I.Transform.4 | replace has `replaceWith` |
| TR-012 | `test_epoch_unit` | I.Transform.5 | epochToTimestamp has `sourceEpochUnit` |
| TR-013 | `test_source_columns_exist` | I.Transform.6 | `sourceColumns` reference columns that exist in source schema (except addColumn) |
| TR-014 | `test_derived_columns_have_transformations` | II.Transform.1 | Columns in target but not in source have corresponding transformations |
| TR-015 | `test_encrypted_columns_flagged` | II.Transform.2 | Columns with hashingAndEncrypt have `encrypted: true` in target schema |
| TR-016 | `test_transformation_on_error` | II.Transform.4 | Non-critical transformations have `onError` block (warn if missing) |

---

#### Test Category 6 — Validation Tests (8 tests)

| Test ID | Test Name | Rule | Check |
|---------|-----------|------|-------|
| V-001 | `test_validation_type_valid` | I.Valid.1 | `validationType` is valid: schema, regex, duplicateFileCheck, notNull, notEmpty, primaryKey, unique, numericRange, length, allowedValues, dateFormat, dateRange, email, phone, foreignKey, count, duplicateCount, sql, custom |
| V-002 | `test_regex_validation_pattern` | I.Valid.1 | regex validation has `pattern` in validationParameters |
| V-003 | `test_duplicate_file_check_days` | I.Valid.2 | duplicateFileCheck has `daysBack` in validationParameters |
| V-004 | `test_validation_columns_exist` | I.Valid.3 | `sourceColumns` reference columns that exist in schema |
| V-005 | `test_valid_failure_action` | I.Valid.4 | `failureAction` is fail, warn, or skip |
| V-006 | `test_numeric_range_has_bounds` | II.Valid.1 | numericRange has at least one of minValue/maxValue |
| V-007 | `test_allowed_values_not_empty` | II.Valid.2 | allowedValues has non-empty array |
| V-008 | `test_foreign_key_has_reference` | II.Valid.3 | foreignKey has referenceTable and referenceColumns |

---

#### Test Category 7 — Cross-Field Dependency Tests (10 tests)

| Test ID | Test Name | Rule | Check |
|---------|-----------|------|-------|
| X-001 | `test_reject_location_with_move` | I.Error.1 | If onFailure.moveToRejectInd=true, `sourceRejectLocation` exists |
| X-002 | `test_single_source_type` | I.Source.1 | Only one source type defined (not both jdbcSource and kafkaSource) |
| X-003 | `test_schema_consistency` | II.Schema.3 | All source columns present in target (or explicitly dropped) |
| X-004 | `test_partition_columns_in_schema` | I.Schema.4 | partitionBy columns exist in target schema |
| X-005 | `test_merge_keys_in_schema` | I.Target.3 | mergeKeys columns exist in target schema |
| X-006 | `test_encrypted_columns_have_transform` | II.Transform.2 | Columns with `encrypted: true` have hashingAndEncrypt transformation |
| X-007 | `test_source_format_dependencies` | I.File.3-4 | Format-specific fields present (fixed→fixedLengthCounts, xml→xmlRowPath) |
| X-008 | `test_database_target_dependencies` | I.Target.5 | database target has full databaseTarget config |
| X-009 | `test_failure_threshold_with_handling` | II.Error.2 | If fileFailureThresholdPercentage > 0, onFailure config present |
| X-010 | `test_kafkatext_schema_consistency` | I.Kafka.2 | kafkatext source schema has only partition columns |

---

#### Test Category 8 — Security Tests (8 tests)

| Test ID | Test Name | Rule | Check |
|---------|-----------|------|-------|
| SEC-001 | `test_no_plaintext_password` | I.Credential.1 | Config does not contain keys: password, pwd, pass, passwd |
| SEC-002 | `test_no_plaintext_connection_string` | I.Credential.1 | Config does not contain keys: connectionString, jdbcUrl, connStr |
| SEC-003 | `test_no_plaintext_api_key` | I.Credential.1 | Config does not contain keys: apiKey, api_key, token, secret (as credential values) |
| SEC-004 | `test_credentials_use_secret_scope` | I.Credential.2 | All credential references use logonScopeName + logonSecretName |
| SEC-005 | `test_pii_columns_encrypted` | I.Credential.3 | Columns with PII-indicative names (email, phone, ssn, social_security, address, name) have hashingAndEncrypt |
| SEC-006 | `test_encrypt_identity_format` | I.Transform.1 | encryptIdentity contains `@` (email format) |
| SEC-007 | `test_encrypt_format_valid` | I.Transform.1 | encryptFormat is valid (ALPHA_NUM, etc.) |
| SEC-008 | `test_no_decrypted_persistence` | I.Credential.3 | No transformation decrypts data and writes to ADLS |

---

#### Test Category 9 — Global Transformation & Data Quality Tests (8 tests)

| Test ID | Test Name | Rule | Check |
|---------|-----------|------|-------|
| DQ-001 | `test_global_transformation_exists` | II.Global.1 | `globalTransformation` block present (warn if missing) |
| DQ-002 | `test_trim_spaces_ind` | II.Global.1 | `trimSpacesInd` is true (warn if false or missing) |
| DQ-003 | `test_null_standardization` | III.Global.1 | `replaceValues` present for null standardization (warn if missing) |
| DQ-004 | `test_csv_quote_removal` | III.Global.2 | If CSV source, `removeStartCharacters`/`removeEndCharacters` present (warn if missing) |
| DQ-005 | `test_has_validations` | III.Valid.1 | `validations` array present and non-empty (warn if missing) |
| DQ-006 | `test_pk_columns_have_not_null` | III.Valid.2 | PK columns have notNull validation (warn if missing) |
| DQ-007 | `test_has_schema_validation` | III.Valid.3 | schema validation present (warn if missing) |
| DQ-008 | `test_has_duplicate_file_check` | III.Valid.4 | duplicateFileCheck validation present for file sources (warn if missing) |

---

#### Test Category 10 — Performance Tests (8 tests)

| Test ID | Test Name | Rule | Check |
|---------|-----------|------|-------|
| P-001 | `test_delta_format` | III.Target.1 | targetFileFormat is delta (warn if not) |
| P-002 | `test_fetch_size_adequate` | III.Source.1 | JDBC fetchSize >= 20000 (warn if lower) |
| P-003 | `test_write_one_file_jdbc_to_file` | III.Perf.1 | If source is JDBC and target is file-based, writeOneFileInd is true (warn if false) |
| P-004 | `test_write_one_file_not_applicable` | III.Target.3 | If source is not JDBC (Kafka, File, DataRouter, Azure Files), writeOneFileInd should not be set or is not applicable (info) |
| P-005 | `test_has_partitioning` | III.Perf.2 | At least one partition column exists (warn if none) |
| P-006 | `test_vacuum_configured` | III.Target.2 | Delta targets have vacuumDaysOld (warn if missing) |
| P-007 | `test_jdbc_partitioning` | III.Perf.3 | Large JDBC tables have numPartitions or dbTablePartitioning (info) |
| P-008 | `test_cluster_size` | III.Perf.4 | clusterSize or numWorkers configured (info) |

---

#### Test Category 11 — Naming & Metadata Tests (6 tests)

| Test ID | Test Name | Rule | Check |
|---------|-----------|------|-------|
| N-001 | `test_src_id_snake_case` | III.Naming.1 | srcId is snake_case (warn if not) |
| N-002 | `test_feed_type_set` | III.Naming.2 | feedType present (warn if missing) |
| N-003 | `test_support_team_set` | III.Naming.3 | supportTeam present (warn if missing) |
| N-004 | `test_bypass_softlimit` | III.Naming.4 | bypassSoftlimit present (warn if missing) |
| N-005 | `test_target_location_convention` | III.Location.1 | targetLocation follows convention `abfss://{appId}@.../{srcId}` (warn if not) |

### 5. Generate Test Suite

**Generate the COMPLETE test suite in the requested format.**

**Format A — Python pytest (default):**

```python
"""
XFlow Configuration Validation Test Suite
Generated by /test-xflow-orchestrator
Config: {config_file_path}
Generated: {timestamp}
"""

import json
import re
import pytest
from pathlib import Path

# ==================== Configuration ====================

CONFIG_PATH = "{config_file_path}"
VALID_SPARK_TYPES = {
    "string", "int", "integer", "long", "bigint", "double", "float",
    "boolean", "date", "timestamp", "decimal", "binary", "short", "byte"
}
VALID_CONNECTION_TYPES = {
    "ORACLE", "SQL_SERVER", "MY_SQL", "VERTICA", "TERRADATA",
    "SNOWFLAKE", "TRINO", "POSTGRESQL", "GENERIC"
}
VALID_WRITE_MODES = {"append", "overwrite", "overwritePartition", "upsert"}
VALID_TARGET_FORMATS = {"delta", "parquet", "csv", "database"}
VALID_SOURCE_FORMATS = {"parquet", "orc", "avro", "csv", "fixed", "xml", "json", "kafkatext"}
VALID_TRANSFORMATION_TYPES = {
    "hashingAndEncrypt", "dateFormat", "regex", "replace", "uppercase",
    "lowercase", "epochToTimestamp", "addColumn", "concatenate",
    "substring", "cast", "nullHandling", "conditional", "sql"
}
VALID_VALIDATION_TYPES = {
    "schema", "regex", "duplicateFileCheck", "notNull", "notEmpty",
    "primaryKey", "unique", "numericRange", "length", "allowedValues",
    "dateFormat", "dateRange", "email", "phone", "foreignKey",
    "count", "duplicateCount", "sql", "custom"
}
VALID_FAILURE_ACTIONS = {"fail", "warn", "skip"}
PII_COLUMN_PATTERNS = {"email", "phone", "ssn", "social_security", "address", "name"}
CREDENTIAL_KEYS = {"password", "pwd", "pass", "passwd", "connectionString", "jdbcUrl", "connStr", "apiKey", "api_key", "token", "secret"}


@pytest.fixture(scope="module")
def config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


@pytest.fixture(scope="module")
def source(config):
    return config.get("source", {})


@pytest.fixture(scope="module")
def source_schema(source):
    return source.get("schema", [])


@pytest.fixture(scope="module")
def targets(config):
    return config.get("targets", [])


@pytest.fixture(scope="module")
def transformations(config):
    return config.get("transformations", [])


@pytest.fixture(scope="module")
def validations(config):
    return config.get("validations", [])


@pytest.fixture(scope="module")
def global_transform(config):
    return config.get("globalTransformation", {})


# Helper functions
def get_source_type(source):
    if "jdbcSource" in source:
        return "jdbc"
    elif "kafkaSource" in source:
        return "kafka"
    elif "httpFileSource" in source:
        return "http"
    elif "azureFilesSource" in source:
        return "azure_files"
    elif "sourceLocation" in source:
        return "file"
    return "unknown"


def get_source_column_names(source):
    return {col["columnName"] for col in source.get("schema", []) if "columnName" in col}


def find_all_keys(obj, depth=0):
    """Recursively find all keys in a nested dict."""
    keys = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            keys.add(k.lower())
            keys.update(find_all_keys(v, depth + 1))
    elif isinstance(obj, list):
        for item in obj:
            keys.update(find_all_keys(item, depth + 1))
    return keys


# ==================== Category 1: Structural Tests ====================

class TestStructural:
    def test_s001_valid_json(self, config):
        """Config is a valid JSON object."""
        assert isinstance(config, dict), "Config root must be a JSON object"

    def test_s002_mandatory_root_fields(self, config):
        """All 9 mandatory root fields present."""
        required = ["srcId", "appId", "createdBy", "dataLibrary",
                     "rimPolicyName", "sourceContact", "motsId",
                     "source", "targets"]
        missing = [f for f in required if f not in config]
        assert not missing, f"Missing mandatory root fields: {missing}"

    def test_s003_targets_is_array(self, config):
        """targets must be a JSON array."""
        assert isinstance(config.get("targets"), list), "targets must be an array []"

    def test_s004_targets_not_empty(self, targets):
        """targets array has at least one element."""
        assert len(targets) > 0, "targets array must have at least one target"

    def test_s005_valid_feed_type(self, config):
        """feedType is ING or MGR."""
        if "feedType" in config:
            assert config["feedType"] in ("ING", "MGR"), f"Invalid feedType: {config['feedType']}"

    def test_s006_created_by_email(self, config):
        """createdBy contains @."""
        assert "@" in str(config.get("createdBy", "")), "createdBy must be a valid email"

    def test_s007_source_contact_email(self, config):
        """sourceContact contains @."""
        assert "@" in str(config.get("sourceContact", "")), "sourceContact must be a valid email"

    def test_s008_mots_id_integer(self, config):
        """motsId is an integer."""
        assert isinstance(config.get("motsId"), int), "motsId must be an integer"


# ==================== Category 2: Schema Tests ====================

class TestSchema:
    def test_sc001_source_schema_exists(self, source):
        """Source has schema array."""
        schema = source.get("schema", [])
        assert len(schema) > 0, "Source must have schema with at least one column"

    def test_sc002_source_columns_have_name(self, source_schema):
        """Every source column has columnName."""
        for i, col in enumerate(source_schema):
            assert "columnName" in col, f"Source column {i} missing columnName"

    def test_sc003_source_columns_have_type(self, source_schema):
        """Every source column has columnType."""
        for i, col in enumerate(source_schema):
            assert "columnType" in col, f"Source column {i} ({col.get('columnName', '?')}) missing columnType"

    def test_sc004_source_column_types_valid(self, source_schema):
        """All source columnType values are valid Spark SQL types."""
        for col in source_schema:
            ct = col.get("columnType", "")
            assert ct in VALID_SPARK_TYPES, f"Invalid columnType '{ct}' for column '{col.get('columnName')}'"

    def test_sc005_source_no_duplicate_columns(self, source_schema):
        """No duplicate columnName in source schema."""
        names = [c["columnName"] for c in source_schema if "columnName" in c]
        dupes = [n for n in names if names.count(n) > 1]
        assert not dupes, f"Duplicate source columns: {set(dupes)}"

    def test_sc006_target_schema_exists(self, targets):
        """Each target has schema array."""
        for i, t in enumerate(targets):
            assert "schema" in t and len(t["schema"]) > 0, f"Target {i} missing schema"

    def test_sc007_target_column_types_valid(self, targets):
        """All target columnType values are valid."""
        for i, t in enumerate(targets):
            for col in t.get("schema", []):
                ct = col.get("columnType", "")
                assert ct in VALID_SPARK_TYPES, f"Target {i}: invalid type '{ct}' for '{col.get('columnName')}'"

    def test_sc008_target_no_duplicate_columns(self, targets):
        """No duplicate columnName in target schema."""
        for i, t in enumerate(targets):
            names = [c["columnName"] for c in t.get("schema", []) if "columnName" in c]
            dupes = [n for n in names if names.count(n) > 1]
            assert not dupes, f"Target {i}: duplicate columns: {set(dupes)}"

    def test_sc009_partition_columns_sequential(self, targets):
        """Partition columns have sequential partitionOrder starting from 1."""
        for i, t in enumerate(targets):
            orders = sorted([c["partitionOrder"] for c in t.get("schema", []) if "partitionOrder" in c])
            if orders:
                expected = list(range(1, len(orders) + 1))
                assert orders == expected, f"Target {i}: partitionOrder must be sequential from 1, got {orders}"

    def test_sc010_decimal_precision(self, source_schema):
        """Decimal columns have precision and scale."""
        for col in source_schema:
            if col.get("columnType") == "decimal":
                assert "precision" in col and "scale" in col, \
                    f"Decimal column '{col.get('columnName')}' missing precision/scale"


# ==================== Category 3: Source Tests (JDBC) ====================

class TestJDBCSource:
    @pytest.fixture(autouse=True)
    def _skip_if_not_jdbc(self, source):
        if "jdbcSource" not in source:
            pytest.skip("Not a JDBC source")

    def test_sj001_connection_type(self, source):
        jdbc = source["jdbcSource"]
        assert jdbc.get("connectionType") in VALID_CONNECTION_TYPES, \
            f"Invalid connectionType: {jdbc.get('connectionType')}"

    def test_sj002_logon_scope(self, source):
        assert "logonScopeName" in source["jdbcSource"], "Missing logonScopeName"

    def test_sj003_logon_secret(self, source):
        assert "logonSecretName" in source["jdbcSource"], "Missing logonSecretName"

    def test_sj004_sql_file_location(self, source):
        jdbc = source["jdbcSource"]
        assert "sqlFileLocation" in jdbc, "sqlFileLocation is mandatory for all JDBC sources"
        assert "dbTable" not in jdbc, "dbTable is not allowed in JDBC source — use sqlFileLocation instead"

    def test_sj005_snowflake_fields(self, source):
        jdbc = source["jdbcSource"]
        if jdbc.get("connectionType") == "SNOWFLAKE":
            for field in ["sfDatabaseName", "sfSchemaName", "sfWarehouse"]:
                assert field in jdbc, f"Snowflake source missing {field}"


# ==================== Category 4: Target Tests ====================

class TestTarget:
    def test_t001_target_location(self, targets):
        for i, t in enumerate(targets):
            assert "targetLocation" in t, f"Target {i} missing targetLocation"

    def test_t002_target_location_abfss(self, targets):
        for i, t in enumerate(targets):
            loc = t.get("targetLocation", "")
            assert loc.startswith("abfss://"), f"Target {i}: targetLocation must start with abfss://"

    def test_t003_valid_write_mode(self, targets):
        for i, t in enumerate(targets):
            wm = t.get("writeMode", "append")
            assert wm in VALID_WRITE_MODES, f"Target {i}: invalid writeMode '{wm}'"

    def test_t004_upsert_has_keys(self, targets):
        for i, t in enumerate(targets):
            if t.get("writeMode") == "upsert":
                has_pk = any(c.get("pk") for c in t.get("schema", []))
                has_merge = bool(t.get("mergeKeys"))
                assert has_pk or has_merge, f"Target {i}: upsert requires pk columns or mergeKeys"

    def test_t005_overwrite_partition_has_partitions(self, targets):
        for i, t in enumerate(targets):
            if t.get("writeMode") == "overwritePartition":
                has_partition = any("partitionOrder" in c for c in t.get("schema", []))
                assert has_partition, f"Target {i}: overwritePartition requires partition columns"

    def test_t006_valid_target_format(self, targets):
        for i, t in enumerate(targets):
            fmt = t.get("targetFileFormat", "delta")
            assert fmt in VALID_TARGET_FORMATS, f"Target {i}: invalid targetFileFormat '{fmt}'"

    def test_t007_control_columns(self, targets):
        for i, t in enumerate(targets):
            cc = t.get("controlColumns", {})
            assert cc.get("fileNameColumnInd") is True, f"Target {i}: missing controlColumns.fileNameColumnInd"
            assert cc.get("creationTimestampColumnInd") is True, f"Target {i}: missing controlColumns.creationTimestampColumnInd"


# ==================== Category 5: Transformation Tests ====================

class TestTransformations:
    def test_tr001_structure(self, transformations):
        for i, t in enumerate(transformations):
            assert "targetColumnName" in t, f"Transformation {i} missing targetColumnName"
            assert "sourceColumns" in t, f"Transformation {i} missing sourceColumns"
            assert "transformationSteps" in t, f"Transformation {i} missing transformationSteps"

    def test_tr002_valid_types(self, transformations):
        for t in transformations:
            for step in t.get("transformationSteps", []):
                tt = step.get("transformationType")
                assert tt in VALID_TRANSFORMATION_TYPES, f"Invalid transformationType: {tt}"

    def test_tr003_hashing_encrypt_params(self, transformations):
        for t in transformations:
            for step in t.get("transformationSteps", []):
                if step.get("transformationType") == "hashingAndEncrypt":
                    params = step.get("transformationParameters", {})
                    assert "encryptIdentity" in params, f"hashingAndEncrypt missing encryptIdentity for {t['targetColumnName']}"
                    assert "encryptFormat" in params, f"hashingAndEncrypt missing encryptFormat for {t['targetColumnName']}"

    def test_tr004_date_format_params(self, transformations):
        for t in transformations:
            for step in t.get("transformationSteps", []):
                if step.get("transformationType") == "dateFormat":
                    params = step.get("transformationParameters", {})
                    has_source = "dateSourceFormats" in params
                    has_generated = "generatedValue" in params
                    assert has_source or has_generated, \
                        f"dateFormat missing dateSourceFormats or generatedValue for {t['targetColumnName']}"

    def test_tr005_regex_params(self, transformations):
        for t in transformations:
            for step in t.get("transformationSteps", []):
                if step.get("transformationType") == "regex":
                    params = step.get("transformationParameters", {})
                    assert "pattern" in params, f"regex missing pattern for {t['targetColumnName']}"
                    assert "outputFormat" in params, f"regex missing outputFormat for {t['targetColumnName']}"

    def test_tr006_replace_params(self, transformations):
        for t in transformations:
            for step in t.get("transformationSteps", []):
                if step.get("transformationType") == "replace":
                    params = step.get("transformationParameters", {})
                    assert "removePatterns" in params, f"replace missing removePatterns for {t['targetColumnName']}"
                    assert "replaceWith" in params, f"replace missing replaceWith for {t['targetColumnName']}"

    def test_tr007_epoch_params(self, transformations):
        for t in transformations:
            for step in t.get("transformationSteps", []):
                if step.get("transformationType") == "epochToTimestamp":
                    params = step.get("transformationParameters", {})
                    assert "sourceEpochUnit" in params, f"epochToTimestamp missing sourceEpochUnit for {t['targetColumnName']}"

    def test_tr008_source_columns_exist(self, transformations, source):
        src_cols = get_source_column_names(source)
        for t in transformations:
            for step in t.get("transformationSteps", []):
                if step.get("transformationType") != "addColumn":
                    for col in t.get("sourceColumns", []):
                        assert col in src_cols, f"Transformation references nonexistent source column: {col}"

    def test_tr009_derived_columns_covered(self, source, targets, transformations):
        src_cols = get_source_column_names(source)
        transform_targets = {t["targetColumnName"] for t in transformations}
        for target in targets:
            for col in target.get("schema", []):
                name = col.get("columnName", "")
                if name not in src_cols:
                    assert name in transform_targets, \
                        f"Derived column '{name}' in target has no transformation"


# ==================== Category 6: Validation Tests ====================

class TestValidations:
    def test_v001_valid_types(self, validations):
        for v in validations:
            vt = v.get("validationType")
            assert vt in VALID_VALIDATION_TYPES, f"Invalid validationType: {vt}"

    def test_v002_regex_has_pattern(self, validations):
        for v in validations:
            if v.get("validationType") == "regex":
                params = v.get("validationParameters", {})
                assert "pattern" in params, "regex validation missing pattern"

    def test_v003_duplicate_check_days(self, validations):
        for v in validations:
            if v.get("validationType") == "duplicateFileCheck":
                params = v.get("validationParameters", {})
                assert "daysBack" in params, "duplicateFileCheck missing daysBack"

    def test_v004_valid_failure_action(self, validations):
        for v in validations:
            fa = v.get("failureAction", "warn")
            assert fa in VALID_FAILURE_ACTIONS, f"Invalid failureAction: {fa}"


# ==================== Category 7: Security Tests ====================

class TestSecurity:
    def test_sec001_no_plaintext_credentials(self, config):
        all_keys = find_all_keys(config)
        found = all_keys.intersection(CREDENTIAL_KEYS)
        assert not found, f"Plaintext credential keys found: {found}"

    def test_sec002_credentials_use_scope(self, source):
        src_type = get_source_type(source)
        if src_type in ("jdbc", "kafka"):
            src_obj = source.get("jdbcSource") or source.get("kafkaSource") or {}
            assert "logonScopeName" in src_obj, "Missing logonScopeName for credential management"
            assert "logonSecretName" in src_obj, "Missing logonSecretName for credential management"


# ==================== Category 8: Global Transform & Data Quality ====================

class TestDataQuality:
    def test_dq001_global_transform_exists(self, global_transform):
        assert global_transform, "globalTransformation block missing (recommended)"

    def test_dq002_trim_spaces(self, global_transform):
        if global_transform:
            assert global_transform.get("trimSpacesInd") is True, "trimSpacesInd should be true"


# ==================== Category 9: Cross-Field Dependency Tests ====================

class TestCrossField:
    def test_x001_reject_location(self, config):
        on_failure = config.get("onFailure", {})
        if on_failure.get("moveToRejectInd"):
            assert "sourceRejectLocation" in config, \
                "moveToRejectInd=true requires sourceRejectLocation"

    def test_x002_single_source_type(self, source):
        source_types = sum([
            "jdbcSource" in source,
            "kafkaSource" in source,
            "httpFileSource" in source,
            "azureFilesSource" in source,
        ])
        assert source_types <= 1, "Multiple source types defined — only one allowed"
```

**Format B — JSON Validation Report:**
```json
{
  "configFile": "{config_file_path}",
  "timestamp": "{timestamp}",
  "strictnessLevel": "standard",
  "summary": {
    "totalTests": 107,
    "passed": 102,
    "failed": 3,
    "warnings": 2,
    "skipped": 0,
    "categories": {
      "structural": {"total": 9, "passed": 9, "failed": 0},
      "schema": {"total": 12, "passed": 11, "failed": 1},
      "source": {"total": 10, "passed": 10, "failed": 0},
      "target": {"total": 12, "passed": 11, "failed": 1},
      "transformations": {"total": 16, "passed": 15, "failed": 1},
      "validations": {"total": 8, "passed": 8, "failed": 0},
      "crossField": {"total": 10, "passed": 10, "failed": 0},
      "security": {"total": 8, "passed": 8, "failed": 0},
      "dataQuality": {"total": 8, "passed": 6, "failed": 0, "warnings": 2},
      "performance": {"total": 8, "passed": 8, "failed": 0},
      "naming": {"total": 6, "passed": 6, "failed": 0}
    }
  },
  "results": [
    {"id": "S-001", "test": "test_valid_json", "category": "structural", "status": "PASS", "details": "Valid JSON object"},
    {"id": "SC-011", "test": "test_partition_columns_sequential", "category": "schema", "status": "FAIL", "details": "partitionOrder [0, 2] not sequential from 1", "fix": "Renumber to [1, 2]"},
    {"id": "T-008", "test": "test_control_columns", "category": "target", "status": "FAIL", "details": "Target 0 missing controlColumns", "fix": "Add controlColumns with fileNameColumnInd and creationTimestampColumnInd"},
    {"id": "TR-014", "test": "test_derived_columns_covered", "category": "transformations", "status": "FAIL", "details": "Derived column 'load_timestamp' has no transformation", "fix": "Add dateFormat transformation with generatedValue: SYSDATETIME"}
  ],
  "constitutionCompliance": {
    "hardStopRules": {"checked": 30, "passed": 29, "failed": 1},
    "mandatoryPatterns": {"checked": 11, "passed": 10, "failed": 1},
    "preferredPatterns": {"checked": 12, "adopted": 10, "skipped": 2}
  }
}
```

**Format C — Inline Analysis:**
Direct markdown output with pass/fail for each test, organized by category with severity indicators.

**Format D — CI/CD Compatible:**
Same as pytest but with JUnit XML output and exit code:
- Exit 0: all tests pass
- Exit 1: any hard-stop violation (Tier 1 failure)
- Exit 2: mandatory pattern missing (Tier 2 failure)

### 6. Add Recommendations

**For each failed test:**
1. Test ID and name
2. Constitution rule reference
3. Current value (or "missing")
4. Required value
5. Fix command: suggest running `/debug-xflow-orchestrator` or `/refactor-xflow-orchestrator` with specific goals

**Missing test coverage:**
- Suggest additional validations based on schema analysis
- Recommend PII detection for unencrypted columns
- Suggest performance tests for large data volumes

**CI/CD Integration:**
```bash
# Run tests locally
pytest test_xflow_config.py -v --tb=short

# Run in CI/CD pipeline
pytest test_xflow_config.py --junitxml=results.xml -v

# Run specific category
pytest test_xflow_config.py -k "TestStructural" -v

# Run with strict mode (fail on warnings)
pytest test_xflow_config.py --strict-markers -v
```

**Pre-deployment checklist:**
1. Run `/test-xflow-orchestrator` — all tests PASS
2. Run `/document-xflow-orchestrator` — documentation up to date
3. Review with data steward — PII and compliance verified
4. Deploy to dev environment — test with small dataset
5. Validate target data — schema, counts, transformations correct
6. Deploy to prod — monitor first run

### 7. Validate and Report

// turbo

Report with:
- Total tests generated (by category)
- Test results: passed / failed / warnings / skipped
- Constitution compliance: hard-stop rules, mandatory patterns, preferred patterns
- Failed test details with fix suggestions
- Recommended next steps (debug, refactor, or deploy)

## Error Handling

**Insufficient Context**: Request:
1. Config file path
2. Test scope (all/structural/schema/source/target/transformations/validations/cross-field/security/compliance/performance/data-quality)
3. Output format (pytest/json/inline/ci)

**Config Too Large**: Generate tests in batches by category. Run structural and security first, then schema and source, then transformations and validations.

**Multiple Configs**: Generate shared fixtures and per-config test classes. Use pytest parametrize for common tests.

**Test Failures**: For each failure, provide:
1. Exact fix (field path, current value, required value)
2. Constitution rule reference
3. Suggest running `/debug-xflow-orchestrator` for complex fixes
4. Suggest running `/refactor-xflow-orchestrator` for systematic improvements

## Examples

**Example 1: Full Test Suite Generation**
```
/test-xflow-orchestrator all — Generate complete test suite for customer_pipeline.json as pytest

Output: Python test file with 107 tests across 11 categories
Results: 102 PASS, 3 FAIL, 2 WARN
- FAIL: SC-011 partitionOrder not sequential (fix: renumber 1,2)
- FAIL: T-008 missing controlColumns (fix: add block)
- FAIL: TR-014 derived column without transformation (fix: add dateFormat)
- WARN: DQ-003 missing null standardization (recommend: add replaceValues)
- WARN: P-003 fetchSize 5000 < 20000 (recommend: increase)
```

**Example 2: Constitution Compliance Audit**
```
/test-xflow-orchestrator compliance — Check constitution compliance for billing_config.json as json

Output: JSON compliance report
- Hard-stop rules: 30/30 PASS
- Mandatory patterns: 10/11 PASS (missing trimSpacesInd)
- Preferred patterns: 10/12 adopted (missing vacuumDaysOld, missing null standardization)
- Overall: COMPLIANT with 1 mandatory warning
```

**Example 3: Security Audit**
```
/test-xflow-orchestrator security — Security audit for sensitive_data_pipeline.json

Output: 8 security tests
- SEC-001 no plaintext password: PASS
- SEC-002 no plaintext connection string: PASS
- SEC-003 no plaintext API key: PASS
- SEC-004 credentials use secret scope: PASS
- SEC-005 PII columns encrypted: FAIL (email column not encrypted)
- SEC-006 encrypt identity format: PASS
- SEC-007 encrypt format valid: PASS
- SEC-008 no decrypted persistence: PASS
Fix: Run /refactor-xflow-orchestrator security for email encryption
```

**Example 4: Pre-Deployment Validation**
```
/test-xflow-orchestrator all — Pre-deployment validation for production_config.json as ci

Output: CI/CD compatible test results
Exit code: 0 (all pass)
107/107 tests passed
Constitution: fully compliant
Ready for deployment
```

**Example 5: Schema-Only Validation**
```
/test-xflow-orchestrator schema — Validate schema for orders_config.json

Output: 12 schema tests
- SC-001 source schema exists: PASS (15 columns)
- SC-002 columns have name: PASS
- SC-003 columns have type: PASS
- SC-004 valid types: FAIL (column 'amount' has type 'number' — should be 'double' or 'decimal')
- SC-005 no duplicates: PASS
- SC-009 partition order: PASS (data_dt: 1)
- SC-010 decimal precision: FAIL (column 'price' missing precision/scale)
```

**Example 6: Cross-Field Dependency Check**
```
/test-xflow-orchestrator cross-field — Validate dependencies in snowflake_extract.json

Output: 10 cross-field tests
- X-001 reject location: PASS
- X-002 single source type: PASS
- X-003 schema consistency: FAIL (target has 'year_month' not in source, no transformation)
- X-005 merge keys in schema: PASS
- X-006 encrypted columns have transform: PASS
- X-007 Snowflake fields: FAIL (missing sfWarehouse)
Fix: Add sfWarehouse and dateFormat transformation for year_month
```

## References

- XFlow Constitution: `xflow-orchestrator-constitution.md` (Sections I-IV — all rules mapped to test IDs)
- XFlow Pydantic Models: `xflow_models.py` (validation logic, field constraints, enums)
- XFlow Transformations: `xflow_transformations.py` (16 types with required parameters)
- XFlow Validations: `xflow_validations.py` (17 types with required parameters)
- XFlow Field Definitions: `XFlow_System_chunks.json` (field_0001 through field_0026)
- XFlow Source Types: `XFlow_System_chunks.json` (source_0027 through source_0030)
- XFlow Dependencies: `XFlow_System_chunks.json` (general_0041)
- XFlow Defaults: `XFlow_System_chunks.json` (general_0042)
- XFlow Best Practices: `XFlow_System_chunks.json` (general_0043)
