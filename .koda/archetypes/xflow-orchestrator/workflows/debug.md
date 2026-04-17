---
description: Debug XFlow JSON configuration errors, validation failures, and runtime issues (XFlow Orchestrator)
---

User input: $ARGUMENTS

## Execution Steps

## Execution Rules (NON-NEGOTIABLE)

**These rules govern HOW this workflow executes. Violating them is a hard-stop.**

1. **ONE question per message.** Each interactive question MUST be its own separate `ask_user_question` call. NEVER combine multiple questions into a single prompt.
2. **NO skipping steps.** Every analysis category (1–11) MUST be checked. The fix preference step (4c) is MANDATORY — always ask the user how to proceed before applying fixes.
3. **WAIT for user response** before proceeding to the next step. Do not assume defaults unless the workflow explicitly says to apply a default silently.
4. **NEVER apply fixes without asking.** Step 4c (Interactive Fix Preference) MUST be executed. Do not auto-fix without user consent.
5. **If "Review each fix" is selected**, present EACH fix individually with its own `ask_user_question` call. NEVER batch multiple fixes into one prompt.

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
- Load `templates/env-config.yaml` for default values and fix suggestions

### 3. Parse Input
Extract from $ARGUMENTS:
- **Config file path**: path to the XFlow JSON config with the issue — read and parse the file
- **Error message**: exact error text from XFlow validation, Pydantic validation, Databricks job logs, or user description
- **Symptoms**: what is failing — config rejected at submission, job fails at runtime, data not loading, wrong output format, missing columns in target, duplicate data, encryption failures, partition errors, performance issues
- **Context**: source type (JDBC/Kafka/File/HTTP/Azure Files), target type (Delta/Parquet/CSV/Database), recent changes made, environment (dev/staging/prod)
- **Severity**: blocking (cannot run at all) vs degraded (runs but wrong output) vs warning (runs but suboptimal)

If a config file is referenced, read and parse it completely. If no config or error is provided, request both.

### 4. Analyze Problem

**Step 4a: Parse the config file and attempt JSON validation first.**

If JSON parsing fails, report the exact syntax error (line, character, expected token) before proceeding.

**Step 4b: Run through ALL error categories systematically. Report EVERY issue found, not just the first one.**

---

**Category 1 — JSON Structural Errors:**

| Error | Detection | Root Cause | Fix |
|-------|-----------|------------|-----|
| Invalid JSON syntax | JSON parse fails | Missing/extra braces, trailing commas, unquoted keys, single quotes instead of double | Fix syntax at reported line/character |
| `targets` is object not array | `typeof targets === "object" && !Array.isArray(targets)` | Common copy-paste error | Wrap in `[]` |
| Missing mandatory root field | Check for: srcId, appId, createdBy, dataLibrary, rimPolicyName, sourceContact, motsId, source, targets | Field omitted or misspelled | Add field with value from user input or env-config.yaml default |
| Empty/null mandatory field | Field exists but value is `""`, `null`, or `0` for motsId | Placeholder not filled | Prompt user for actual value |
| Invalid feedType | feedType not in `["ING", "MGR"]` | Typo or wrong value | Default to `"ING"` |
| Invalid email | createdBy/sourceContact missing `@` | Not a valid email | Fix email format |
| motsId not integer | motsId is string or float | Wrong type | Cast to integer |

---

**Category 2 — Schema Errors:**

| Error | Detection | Root Cause | Fix |
|-------|-----------|------------|-----|
| Missing columnName | Schema entry has no `columnName` key | Incomplete column definition | Add columnName |
| Missing columnType | Schema entry has no `columnType` key | Incomplete column definition | Add columnType (default `"string"`) |
| Invalid columnType | columnType not in valid Spark SQL types | Typo or wrong type name | Map to valid type: `varchar`→`string`, `integer`→`int`, `bigint`→`long`, `number`→`double`, `datetime`→`timestamp`, `bool`→`boolean` |
| Duplicate columnName | Same columnName appears twice in schema | Copy-paste error | Remove duplicate or rename |
| Partition column missing partitionOrder | Column used in partitioning but no `partitionOrder` | Forgot to add partition metadata | Add `"partitionOrder": N` (sequential from 1) |
| partitionOrder not sequential | partitionOrder values skip numbers or start from 0 | Wrong numbering | Renumber sequentially from 1 |
| Decimal missing precision/scale | columnType is `decimal` but no precision/scale | Incomplete decimal definition | Add `"precision": 18, "scale": 2` (common defaults) |
| Source-target schema mismatch | Column in target not in source, no transformation | Derived column without derivation logic | Add transformation or remove from target |
| Target missing source columns | Source column not in target schema | Accidental omission | Add column to target schema |

---

**Category 3 — JDBC Source Errors:**

| Error | Detection | Root Cause | Fix |
|-------|-----------|------------|-----|
| Missing connectionType | `jdbcSource` has no `connectionType` | Required field omitted | Add from user input (ORACLE, SQL_SERVER, etc.) |
| Invalid connectionType | Not in valid enum | Typo or unsupported DB | Map to valid: `oracle`→`ORACLE`, `sqlserver`→`SQL_SERVER`, `postgres`→`POSTGRESQL`, `mysql`→`MY_SQL` |
| Missing logonScopeName | No secret scope | Required for credentials | Add from env-config.yaml `secret_scope` |
| Missing logonSecretName | No secret key | Required for credentials | Add based on naming convention: `logon-{connectionType.lower()}-{env}` |
| Missing sqlFileLocation | JDBC source has no sqlFileLocation | Required for all JDBC sources | Add sqlFileLocation (ADLS path to SQL file) from user input |
| dbTable used instead of sqlFileLocation | JDBC source uses dbTable | dbTable removed from JDBC sources | Replace with sqlFileLocation pointing to a SQL file containing `SELECT * FROM SCHEMA.TABLE` |
| Plaintext credentials | Config contains `password`, `connectionString`, `apiKey` fields | Security violation | Remove and use logonScopeName/logonSecretName |
| Snowflake missing extra fields | connectionType=SNOWFLAKE but no sfDatabaseName/sfSchemaName/sfWarehouse | Snowflake-specific requirement | Add all three from user input |
| fetchSize too low | fetchSize < 1000 | Performance issue | Recommend 20000 |

---

**Category 4 — Kafka Source Errors:**

| Error | Detection | Root Cause | Fix |
|-------|-----------|------------|-----|
| Missing bootstrapServers | No broker addresses | Required field | Add from user input |
| Missing subscribe | No topic name | Required field | Add from user input |
| Missing groupId | No consumer group | Required field | Add: `"xflow_{srcId}"` |
| Missing credentials | No logonScopeName/logonSecretName | Required for auth | Add from env-config.yaml |
| kafkatext schema has non-partition columns | sourceFileFormat=kafkatext but schema has columns without partitionOrder | kafkatext stores raw message | Remove non-partition columns or change sourceFileFormat |
| Invalid securityProtocol | Not PLAINTEXT/SSL/SASL_SSL | Typo | Default to `"SASL_SSL"` |
| Invalid startingOffsets | Not latest/earliest | Typo | Default to `"latest"` |

---

**Category 5 — File Source Errors:**

| Error | Detection | Root Cause | Fix |
|-------|-----------|------------|-----|
| Missing sourceLocation | No file path | Required for file sources | Add ADLS path from user input |
| sourceLocation not abfss:// | Wrong protocol | Must be ADLS URI | Fix to `abfss://` format |
| Missing sourceFileFormat | No format specified | Required field | Infer from file extension or ask user |
| Invalid sourceFileFormat | Not in valid enum | Typo | Map: `text`→`csv`, `jsonl`→`json` |
| fixed without fixedLengthCounts | sourceFileFormat=fixed, no lengths | Required for fixed-width | Add fixedLengthCounts array |
| xml without xmlRowPath | sourceFileFormat=xml, no row path | Required for XML | Add xmlRowPath |
| CSV wrong delimiter | Data not parsing correctly | Delimiter mismatch | Check file and set correct csvDelimiter |
| Missing csvIgnoreHeaderInd | CSV with header row not being skipped | Header treated as data | Add `"csvIgnoreHeaderInd": true` |

---

**Category 6 — HTTP/Azure Files Source Errors:**

| Error | Detection | Root Cause | Fix |
|-------|-----------|------------|-----|
| HTTP missing filterRegex | No file filter pattern | May process wrong files | Add filterRegex based on file naming |
| Azure Files missing sourcePullConfig | No pull configuration | Required for Azure Files | Add complete sourcePullConfig block |
| Azure Files missing azureFileShare fields | Incomplete file share config | Missing required nested fields | Add: fileShareName, accountName, sasTokenVaultName, sasTokenSecretKey, resourcePath |
| Invalid fileActions actionType | Unknown action type | Typo | Valid: EMPTY_FILE_VALIDATION, RECORD_COUNT_VALIDATION, CLEANSE, COMPRESSION, EXTRACT_HEADER_TRAILER, CREATE_AUDIT, DEST_FILE_PATTERN, DEST_PARTITIONING |

---

**Category 7 — Target Configuration Errors:**

| Error | Detection | Root Cause | Fix |
|-------|-----------|------------|-----|
| Missing targetLocation | No target path | Required field | Add ADLS path |
| targetLocation not abfss:// | Wrong protocol | Must be ADLS URI | Fix to `abfss://container@account.dfs.core.windows.net/path` |
| Invalid writeMode | Not append/overwrite/overwritePartition/upsert | Typo | Map: `insert`→`append`, `merge`→`upsert`, `replace`→`overwrite` |
| Upsert without PK or mergeKeys | writeMode=upsert, no pk columns, no mergeKeys | Missing key definition | Add `"pk": true` to key columns OR add `"mergeKeys": [...]` |
| overwritePartition without partitions | writeMode=overwritePartition, no partitionOrder columns | No partition definition | Add partitionOrder to partition columns |
| Missing controlColumns | No controlColumns block | Required pattern | Add `{"fileNameColumnInd": true, "creationTimestampColumnInd": true}` |
| Invalid targetFileFormat | Not delta/parquet/csv/database | Typo | Default to `"delta"` |
| Database target without databaseTarget | targetFileFormat=database, no databaseTarget section | Missing config | Add databaseTarget with connectionType, logonScopeName, logonSecretName, dbTable |
| JDBC source missing writeOneFileInd | Source is JDBC and target is file-based (parquet/csv), writeOneFileInd not true | Required for JDBC-to-file writes | Set `"writeOneFileInd": true` when source is database (JDBC) and target is a file format. Not applicable for other source types |
| vacuumDaysOld on non-delta target | parquet/csv/database target has vacuumDaysOld field | Hard-stop violation | Remove `vacuumDaysOld` (only valid for delta targets) |
| Missing vacuumDaysOld | Delta target without vacuum | Storage bloat risk | Add `"vacuumDaysOld": 7` |
| sourceFileFormat on JDBC/Kafka | JDBC or Kafka source has sourceFileFormat field | Invalid field for non-file sources | Remove sourceFileFormat field |

---

**Category 8 — Transformation Errors:**

| Error | Detection | Root Cause | Fix |
|-------|-----------|------------|-----|
| hashingAndEncrypt missing encryptIdentity | No encryption identity | Required param | Add `"encryptIdentity": "DL_IDENTITY@ATT.COM"` |
| hashingAndEncrypt missing encryptFormat | No format specified | Required param | Add `"encryptFormat": "ALPHA_NUM"` |
| dateFormat missing both dateSourceFormats and generatedValue | Neither conversion nor generation | Must have one | Add dateSourceFormats for conversion or generatedValue for generation |
| dateFormat missing dateTargetFormat | No output format | Required for string targets | Add dateTargetFormat pattern |
| regex missing pattern | No regex pattern | Required param | Add pattern from user |
| regex missing outputFormat | No output template | Required param | Add outputFormat with `{groupNumber}` references |
| replace missing removePatterns | No patterns to match | Required param | Add removePatterns array |
| replace missing replaceWith | No replacement value | Required param | Add replaceWith (string or reserved keyword) |
| epochToTimestamp missing sourceEpochUnit | No unit specified | Required param | Add `"seconds"` or `"milliseconds"` |
| sourceColumns references nonexistent column | Column not in source schema | Typo or wrong column name | Fix column name or add to source schema |
| Derived column without transformation | Column in target but not source, no transformation | Missing derivation logic | Add transformation (dateFormat with generatedValue, addColumn, etc.) |
| Encrypted column without encrypted flag | hashingAndEncrypt transformation but target column missing `"encrypted": true` | Missing flag | Add `"encrypted": true` to target schema column |
| Missing onError for encryption | hashingAndEncrypt without onError | Encryption can fail | Add `"onError": {"failRecordInd": true, "replaceFailedValueWith": "NULL"}` |
| Invalid transformationType | Unknown type | Typo | Valid: hashingAndEncrypt, dateFormat, regex, replace, uppercase, lowercase, epochToTimestamp, addColumn, concatenate, substring, cast, nullHandling, conditional, sql |

---

**Category 9 — Validation Errors:**

| Error | Detection | Root Cause | Fix |
|-------|-----------|------------|-----|
| Invalid validationType | Unknown type | Typo | Valid: schema, regex, duplicateFileCheck, notNull, notEmpty, primaryKey, unique, numericRange, length, allowedValues, dateFormat, dateRange, email, phone, foreignKey, count, duplicateCount, sql, custom |
| regex validation missing pattern | No pattern in validationParameters | Required param | Add pattern |
| duplicateFileCheck missing daysBack | No lookback period | Required param | Add `"daysBack": 60` |
| sourceColumns references nonexistent column | Column not in schema | Typo | Fix column name |
| numericRange missing both min and max | No range defined | At least one needed | Add minValue and/or maxValue |
| allowedValues empty array | No values to check against | Useless validation | Add values or remove validation |
| Invalid failureAction | Not fail/warn/skip | Typo | Default to `"warn"` |

---

**Category 10 — Cross-Field Dependency Errors:**

| Error | Detection | Root Cause | Fix |
|-------|-----------|------------|-----|
| moveToRejectInd=true without sourceRejectLocation | onFailure.moveToRejectInd is true but no reject path | Missing dependent field | Add sourceRejectLocation ADLS path |
| fileFailureThresholdPercentage > 0 without error handling | Threshold set but no onFailure config | Incomplete error handling | Add onFailure block |
| Encrypted columns without hashingAndEncrypt | Target column has `"encrypted": true` but no transformation | Missing transformation | Add hashingAndEncrypt transformation |
| Multiple source types defined | Both jdbcSource and kafkaSource present | Only one allowed | Remove the incorrect one |
| writeMode mismatch with data pattern | append for CDC data, overwrite for large tables | Wrong mode for use case | Recommend correct writeMode |
| Partition columns not in schema | partitionBy references columns not in target schema | Wrong column names | Fix partitionBy or add columns to schema |

---

**Category 11 — Performance and Runtime Errors:**

| Error | Detection | Root Cause | Fix |
|-------|-----------|------------|-----|
| JDBC timeout | Job fails with connection timeout | fetchSize too large or no partitioning | Reduce fetchSize, add numPartitions |
| Out of memory | Executor OOM errors | Too much data in single partition | Add dbTablePartitioning for JDBC, increase cluster size |
| Slow writes | Job takes hours | Wrong writeMode or parallelism settings | Consider overwritePartition vs append. For JDBC sources writing to file targets (not delta), set writeOneFileInd: true |
| Duplicate records | Target has duplicates | append mode without dedup | Switch to upsert or add primaryKey validation |
| Schema evolution failure | New columns in source break job | Schema mismatch | Update source and target schemas, add new columns |
| Encryption failure | Voltage errors | Wrong encryptIdentity or encryptFormat | Verify Voltage configuration, check onError handling |

Report ALL findings with: error category, severity (critical/warning/info), root cause, affected field path, data impact assessment, and suggested fix.

### 4c. Interactive Fix Preference

**After presenting the analysis, ASK the user how they want to proceed:**

> I found the following issues in your config:
> - [N] Critical errors (hard-stop violations)
> - [N] High-severity issues
> - [N] Medium/Low warnings
>
> How would you like to proceed?
> - **Auto-fix all** — apply all recommended fixes automatically
> - **Review each fix** — walk through each fix one by one for your approval
> - **Fix critical only** — fix hard-stop violations, skip warnings and recommendations

Use `ask_user_question` with these 3 options.

<!-- HALT: Wait for user response before continuing to Step 5 -->

**If "Review each fix":** For each error, present the fix and ask:
> Fix for [field_path]: change [current_value] → [new_value] (Constitution rule: [rule_ref])
> - **Apply** — accept this fix
> - **Skip** — leave as-is
> - **Modify** — I'll provide a different value

**If a fix has multiple valid options**, ASK:
> For [specific error], there are multiple fix options:
> - **Option A**: [description + trade-off]
> - **Option B**: [description + trade-off]
> Which do you prefer?

### 5. Generate Fix

**For each accepted fix, generate the specific change:**

1. Show the **exact field path** that needs to change (e.g., `source.jdbcSource.logonScopeName`)
2. Show the **current value** (or "missing")
3. Show the **corrected value** with explanation
4. Reference the **constitution rule** that requires this fix

**Then provide the COMPLETE corrected JSON config** — not just the changed sections. The output must be a valid JSON file ready to replace the broken one.

**Fix priority order:**
1. JSON syntax errors (must fix first — nothing else works without valid JSON)
2. Hard-stop violations (constitution Section I)
3. Missing mandatory patterns (constitution Section II)
4. Cross-field dependency errors
5. Performance and optimization issues (constitution Section III)

### 6. Add Recommendations

**Prevention checklist:**
- Run `/test-xflow-orchestrator` before deploying any config
- Use the constitution hard-stop rules as a pre-deployment checklist
- Set up CI/CD validation for config changes

**Testing guidance:**
- Specific test cases to validate the fix
- Edge cases to test (empty data, null values, schema changes)
- How to test with a small dataset before full deployment

**Monitoring:**
- What metrics to watch after applying the fix
- How to detect if the issue recurs
- Alerting recommendations

**Related issues:**
- Other potential problems in the same config (found during analysis)
- Common co-occurring errors
- Upstream/downstream impacts

### 7. Validate and Report

// turbo

Validate the fixed config against ALL constitution hard-stop rules. Report with:
- Total errors found (by category and severity)
- Each error: category, root cause, fix applied, field path changed
- Validation status of the corrected config (PASS/FAIL)
- Remaining warnings (non-critical)
- Recommended next steps

## Error Handling

**Insufficient Error Information**: Request:
1. Complete config file (path or paste JSON)
2. Exact error message (from XFlow, Pydantic, or Databricks logs)
3. What operation failed (submission, runtime, data quality)
4. Environment context (dev/staging/prod, cluster version)

**Cannot Reproduce**: Request:
1. The exact config JSON file
2. Databricks workspace and cluster details
3. Job execution logs (last 50 lines)
4. XFlow validation output

**Multiple Errors**: Fix ALL errors, prioritized by severity:
1. **Critical**: Hard-stop violations, invalid JSON, missing mandatory fields
2. **High**: Cross-field dependencies, wrong writeMode, missing transformations
3. **Medium**: Missing recommended patterns, suboptimal settings
4. **Low**: Naming conventions, documentation, preferred patterns

**Config Too Large**: If config is very large (>500 lines), focus analysis on:
1. The section referenced in the error message
2. All hard-stop rule checks
3. Cross-field dependency checks
Then provide targeted fixes rather than full config rewrite.

## Examples

**Example 1: Multiple JDBC Errors**
```
/debug-xflow-orchestrator customer_config.json fails with "validation error"

Analysis:
1. [CRITICAL] Missing logonScopeName in jdbcSource (Constitution I.JDBC.1)
2. [CRITICAL] connectionType "Oracle" should be "ORACLE" (Constitution I.JDBC.2)
3. [HIGH] targets is object, not array (Constitution I.Root.2)
4. [MEDIUM] Missing controlColumns on target (Constitution II.Target.1)
5. [LOW] srcId "CustomerData" should be "customer_data" (Constitution III.Naming.1)

Fix: Complete corrected JSON with all 5 issues resolved
```

**Example 2: Kafka Schema Mismatch**
```
/debug-xflow-orchestrator streaming_config.json — kafkatext source has full schema

Analysis:
1. [CRITICAL] sourceFileFormat is "kafkatext" but schema has 12 non-partition columns (Constitution I.Kafka.2)
   kafkatext stores raw Kafka message as-is; schema should only have partition columns

Fix: Reduced schema to partition columns only, or changed sourceFileFormat to "json" if structured parsing is needed
```

**Example 3: Upsert Without Keys + Missing Transformations**
```
/debug-xflow-orchestrator orders_pipeline.json — upsert failing, load_timestamp missing

Analysis:
1. [CRITICAL] writeMode "upsert" but no pk columns and no mergeKeys (Constitution I.Target.3)
2. [HIGH] load_timestamp in target schema but not in source, no transformation (Constitution II.Transform.1)
3. [MEDIUM] Missing globalTransformation block (Constitution II.Global.1)

Fix: Added pk:true to order_id, added dateFormat transformation for load_timestamp, added globalTransformation
```

**Example 4: Snowflake Cross-Field Dependencies**
```
/debug-xflow-orchestrator snowflake_extract.json — Snowflake connection failing

Analysis:
1. [CRITICAL] connectionType is "SNOWFLAKE" but missing sfDatabaseName, sfSchemaName, sfWarehouse (Constitution I.JDBC.3)
2. [HIGH] sqlFileLocation must point to a valid SQL file in ADLS for Snowflake
3. [MEDIUM] fetchSize is 5000, recommend 20000+ for Snowflake (Constitution III.Source.1)

Fix: Added all three Snowflake fields, verified sqlFileLocation path, increased fetchSize
```

**Example 5: CSV File with Multiple Data Quality Issues**
```
/debug-xflow-orchestrator billing_ingest.json — data has quotes, nulls showing as "NA"

Analysis:
1. [HIGH] Missing globalTransformation.removeStartCharacters/removeEndCharacters for quotes
2. [HIGH] Missing replaceValues for null standardization ("NA", "NULL", "" → "Null")
3. [MEDIUM] csvIgnoreHeaderInd not set (header row may be loaded as data)
4. [MEDIUM] No sourceRejectLocation configured but moveToRejectInd is true (Constitution I.Error.1)
5. [LOW] Missing duplicateFileCheck validation

Fix: Added complete globalTransformation with quote removal and null standardization, set csvIgnoreHeaderInd, added sourceRejectLocation, added duplicateFileCheck
```

**Example 6: Performance Debugging**
```
/debug-xflow-orchestrator large_table_extract.json — JDBC extraction takes 6 hours

Analysis:
1. [HIGH] fetchSize is 1000 (too low for large table) — recommend 20000-50000
2. [HIGH] numPartitions not set — single-threaded extraction
3. [MEDIUM] No dbTablePartitioning — cannot parallelize reads
4. [INFO] writeOneFileInd is true — correct for JDBC-to-file (source is database, target is file (not delta))
5. [LOW] clusterSize is "low" (4 workers) — insufficient for large table

Fix: Increased fetchSize to 50000, added numPartitions: 8, added dbTablePartitioning on date column, recommended clusterSize: "medium"
```

## References

- XFlow Constitution: `xflow-orchestrator-constitution.md` (Sections I-IV)
- XFlow Field Definitions: `XFlow_System_chunks.json` (field_0001 through field_0026)
- XFlow Source Types: `XFlow_System_chunks.json` (source_0027 through source_0030)
- XFlow Transformations: `XFlow_System_chunks.json` (trans_0031 through trans_0037)
- XFlow Validations: `XFlow_System_chunks.json` (valid_0038 through valid_0040)
- XFlow Dependencies: `XFlow_System_chunks.json` (general_0041)
- XFlow Defaults: `XFlow_System_chunks.json` (general_0042)
- XFlow Best Practices: `XFlow_System_chunks.json` (general_0043)
- Pydantic Models: `xflow_models.py` (validation logic and error messages)
- Transformation Models: `xflow_transformations.py` (16 types with required params)
- Validation Models: `xflow_validations.py` (17 types with required params)
