---
description: Refactor existing XFlow JSON configuration to apply best practices, fix violations, and optimize (XFlow Orchestrator)
---

User input: $ARGUMENTS

## Execution Steps

## Execution Rules (NON-NEGOTIABLE)

**These rules govern HOW this workflow executes. Violating them is a hard-stop.**

1. **ONE question per message.** Each interactive question MUST be its own separate `ask_user_question` call. NEVER combine multiple questions into a single prompt.
2. **NO skipping steps.** Every interactive question in Step 3b MUST be asked in order. The ONLY exception is when the user already provided the information in $ARGUMENTS.
3. **WAIT for user response** before proceeding to the next question. Do not assume defaults unless the workflow explicitly says to apply a default silently.
4. **NEVER apply changes before collecting all required input.** If refactoring goal or fix application preference is unclear, ASK before proceeding.
5. **If "Review each" is selected**, present EACH proposed change individually with its own `ask_user_question` call. NEVER batch multiple changes into one prompt.

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
- Load `templates/env-config.yaml` for recommended defaults

### 3. Parse Input
Extract from $ARGUMENTS:
- **Config file path**: path to the existing XFlow JSON config to refactor — read and parse the file completely
- **Refactoring goals** (one or more):
  - `security` — add encryption to PII columns, move credentials to secret scopes, add encrypted flags
  - `performance` — optimize fetchSize, add numPartitions, fix writeMode, add compression, tune cluster
  - `data-quality` — add validations (notNull, primaryKey, numericRange, allowedValues, regex, duplicateFileCheck, schema), add globalTransformation
  - `partitioning` — add/optimize partition columns, add partitionOrder, align writeMode with partitions
  - `modernize` — upgrade legacy config to current standards (Delta format, controlColumns, error handling, naming)
  - `compliance` — fix all constitution violations, add missing mandatory fields, align with RIM policy
  - `full` — apply all tiers (security + performance + data-quality + partitioning + modernize + compliance)
- **Constraints**: fields that must NOT change, backward compatibility requirements, specific columns to exclude from encryption
- **PII columns**: if security goal, which columns contain PII (email, phone, SSN, name, address, etc.)

If a config file is referenced, read and parse it. Request clarification if no config file is provided.

### 3b. Interactive Refactoring Setup

**If refactoring goal is not specified in $ARGUMENTS, ASK:**

**Question 1 — Refactoring Goal:**
> What is your refactoring goal?
> - **Security** — fix credential issues, add PII encryption, secret scope migration
> - **Performance** — optimize fetch size, partitioning, compression, cluster sizing
> - **Data quality** — add validations, global transformations, null handling
> - **Compliance** — full constitution compliance audit + fix all violations

Use `ask_user_question` with these 4 options.

<!-- HALT: Wait for user response before continuing to Question 2 -->

**Question 2 — Fix Application:**
> Should I apply changes automatically, or review each change with you?
> - **Auto-apply** — apply all recommended changes for the selected goal
> - **Review each** — walk through each proposed change for your approval before applying

Use `ask_user_question` with these 2 options.

<!-- HALT: Wait for user response before continuing to Step 4 -->

**If "Review each":** For each proposed change during Step 5, present it and ask:
> Proposed change: [field_path] — [current] → [new] (Reason: [rule/best practice])
> - **Apply** — accept this change
> - **Skip** — leave as-is
> - **Modify** — I'll provide a different value

### 4. Analyze Existing Config

**Load the config and perform a comprehensive audit against all three tiers. Report EVERY finding.**

---

#### Tier 1 — Hard-Stop Violations (MUST fix — constitution Section I)

**Root-Level Structure:**
| Check | Field | Rule | Fix |
|-------|-------|------|-----|
| Missing srcId | `srcId` | Mandatory root field | Add from user input |
| Missing appId | `appId` | Mandatory root field | Add from user input |
| Missing createdBy | `createdBy` | Mandatory root field | Add user email |
| Missing dataLibrary | `dataLibrary` | Mandatory root field | Add from user input |
| Missing rimPolicyName | `rimPolicyName` | Mandatory root field | Add from user input |
| Missing sourceContact | `sourceContact` | Mandatory root field | Add from user input |
| Missing motsId | `motsId` | Mandatory root field | Add from user input |
| Invalid email | `createdBy`, `sourceContact` | Must contain `@` | Fix email format |
| Invalid feedType | `feedType` | Must be `ING` or `MGR` | Default to `ING` |
| targets not array | `targets` | Must be JSON array | Wrap in `[]` |

**Credential Security:**
| Check | Detection | Fix |
|-------|-----------|-----|
| Plaintext password | Config contains `password`, `pwd`, `pass` keys | Remove, add logonScopeName/logonSecretName |
| Plaintext connection string | Config contains `connectionString`, `jdbcUrl` | Remove, use connectionType + secret scope |
| Plaintext API key | Config contains `apiKey`, `token`, `secret` | Remove, use secret scope |
| Credentials in comments | JSON comments with credential hints | Remove comments |

**Schema:**
| Check | Detection | Fix |
|-------|-----------|-----|
| Missing columnName | Schema entry without `columnName` | Add column name |
| Missing columnType | Schema entry without `columnType` | Add type (default `string`) |
| Invalid columnType | Type not in valid Spark SQL types | Map to valid type |
| Duplicate columnName | Same name appears twice | Remove duplicate or rename |
| Partition without partitionOrder | Partition column missing `partitionOrder` | Add sequential partitionOrder |

**Source-Specific:**
| Check | Source Type | Detection | Fix |
|-------|-----------|-----------|-----|
| Missing connectionType | JDBC | No connectionType | Add from user input |
| Invalid connectionType | JDBC | Not in valid enum | Map to valid value |
| Missing credentials | JDBC | No logonScopeName/logonSecretName | Add from env-config |
| Missing sqlFileLocation | JDBC | No SQL file path | Add sqlFileLocation from user input |
| dbTable in JDBC source | JDBC | Deprecated field | Replace with sqlFileLocation pointing to SQL file |
| Missing Snowflake fields | JDBC+Snowflake | No sfDatabaseName/sfSchemaName/sfWarehouse | Add all three |
| Missing bootstrapServers | Kafka | No broker addresses | Add from user input |
| Missing subscribe | Kafka | No topic name | Add from user input |
| Missing groupId | Kafka | No consumer group | Add default |
| kafkatext schema mismatch | Kafka | Non-partition columns with kafkatext | Fix schema |
| Missing sourceLocation | File | No file path | Add from user input |
| Missing sourceFileFormat | File | No format | Add from user input |
| fixed without fixedLengthCounts | File | Fixed format, no lengths | Add lengths |
| xml without xmlRowPath | File | XML format, no row path | Add row path |
| Missing Azure Files config | Azure Files | Incomplete sourcePullConfig | Add full config |

**Target-Specific:**
| Check | Detection | Fix |
|-------|-----------|-----|
| Missing targetLocation | No target path | Add ADLS path |
| Invalid targetLocation | Not abfss:// | Fix to abfss:// format |
| Invalid writeMode | Not valid enum | Map to valid value |
| Upsert without PK/mergeKeys | writeMode=upsert, no keys | Add pk or mergeKeys |
| overwritePartition without partitions | No partition columns | Add partitionOrder |
| Database without databaseTarget | targetFileFormat=database | Add databaseTarget section |

**Transformation-Specific:**
| Check | Detection | Fix |
|-------|-----------|-----|
| hashingAndEncrypt missing encryptIdentity | No identity | Add `DL_IDENTITY@ATT.COM` |
| hashingAndEncrypt missing encryptFormat | No format | Add `ALPHA_NUM` |
| dateFormat missing params | No dateSourceFormats or generatedValue | Add appropriate params |
| regex missing pattern | No pattern | Add from user input |
| replace missing removePatterns | No patterns | Add from user input |
| epochToTimestamp missing sourceEpochUnit | No unit | Add `seconds` or `milliseconds` |
| sourceColumns nonexistent | Column not in source schema | Fix column name |

**Validation-Specific:**
| Check | Detection | Fix |
|-------|-----------|-----|
| regex missing pattern | No pattern in params | Add pattern |
| duplicateFileCheck missing daysBack | No lookback | Add `daysBack: 60` |
| sourceColumns nonexistent | Column not in schema | Fix column name |

**Error Handling:**
| Check | Detection | Fix |
|-------|-----------|-----|
| moveToRejectInd without location | moveToRejectInd=true, no sourceRejectLocation | Add reject location |

---

#### Tier 2 — Missing Mandatory Patterns (SHOULD fix — constitution Section II)

| Check | Current State | Recommended State | Impact |
|-------|--------------|-------------------|--------|
| Missing controlColumns | No controlColumns on target | Add `fileNameColumnInd: true, creationTimestampColumnInd: true` | Data lineage tracking |
| writeMode misaligned | e.g., `overwrite` for large table | Align with data pattern (see constitution II.Target) | Performance, data safety |
| Missing source schema | No schema array | Add explicit schema | Schema enforcement |
| Missing target schema | No schema array | Add target schema | Column validation |
| Schema inconsistency | Target has columns not in source, no transformations | Add transformations for derived columns | Runtime errors |
| Invalid column types | Non-standard types | Normalize to valid Spark SQL types | Type errors |
| Missing decimal precision | Decimal without precision/scale | Add `precision: 18, scale: 2` | Precision loss |
| Missing trimSpacesInd | No globalTransformation or trimSpacesInd not set | Add `globalTransformation.trimSpacesInd: true` | Data quality |
| Missing transformation onError | Encryption without onError | Add `onError: {failRecordInd: true, replaceFailedValueWith: "NULL"}` | Error handling |
| Missing fileFailureThreshold | No threshold set | Add `fileFailureThresholdPercentage: 0` | Error handling |
| Missing encrypted flag | hashingAndEncrypt but no `encrypted: true` on target column | Add `encrypted: true` | Metadata accuracy |

---

#### Tier 3 — Optimization Opportunities (RECOMMENDED — constitution Section III)

**Target Optimizations:**
| Check | Current | Recommended | Impact |
|-------|---------|-------------|--------|
| Not Delta format | parquet/csv | `targetFileFormat: "delta"` | ACID, time-travel, schema evolution |
| Missing vacuumDaysOld | Not set (delta targets only) | `vacuumDaysOld: 7` (ONLY for delta targets) | Storage management |
| Invalid vacuumDaysOld | Present on parquet/csv/database | Remove `vacuumDaysOld` (only valid for delta) | Fix validation error |
| writeOneFileInd wrong | Incorrect for source/target combination | `true` when source is JDBC and target is file-based; not applicable for other sources | Correct parallelism/output |

**Source Optimizations:**
| Check | Current | Recommended | Impact |
|-------|---------|-------------|--------|
| Low fetchSize | < 10000 | `fetchSize: 20000` (JDBC) | Read performance |
| Missing numPartitions | Not set | Add based on table size | Parallel extraction |
| Missing dbTablePartitioning | Not set for large tables | Add for tables > 10M rows | Parallel reads |
| Missing CSV settings | No delimiter/header config | Add csvDelimiter, csvIgnoreHeaderInd | Parse correctness |
| sourceFileFormat on JDBC/Kafka | Present on non-file source | Remove field | Field only for file-based sources |
| Missing Kafka security | No securityProtocol | `securityProtocol: "SASL_SSL"` | Security |

**Global Transformation Optimizations:**
| Check | Current | Recommended | Impact |
|-------|---------|-------------|--------|
| No globalTransformation | Missing block | Add with trimSpacesInd, replaceValues | Data quality |
| No null standardization | No replaceValues | Add `["", "NA", "NULL", "reserved:NULL"] → "Null"` | Null consistency |
| No quote removal (CSV) | No removeStartCharacters/removeEndCharacters | Add for CSV sources | Data cleanliness |

**Naming and Metadata:**
| Check | Current | Recommended | Impact |
|-------|---------|-------------|--------|
| srcId not snake_case | CamelCase or mixed | Convert to snake_case | Naming convention |
| Missing feedType | Not set | `feedType: "ING"` | Metadata completeness |
| Missing supportTeam | Not set | `supportTeam: "datalake"` | Operational support |
| Missing bypassSoftlimit | Not set | `bypassSoftlimit: false` | Safety |

**Error Handling Optimizations:**
| Check | Current | Recommended | Impact |
|-------|---------|-------------|--------|
| No onFailure block | Missing | Add with badFileInd: true | Debugging |
| No sourceRejectLocation | Missing | Add ADLS reject path | Data quality monitoring |
| No skipMalformedRecsInd | Missing | `skipMalformedRecsInd: true` (file sources) | Resilience |
| No errorTableLocation | Missing | Add ADLS error table path | Error tracking |

**Security Optimizations:**
| Check | Current | Recommended | Impact |
|-------|---------|-------------|--------|
| PII columns unencrypted | email, phone, SSN, name, address without encryption | Add hashingAndEncrypt transformations | Compliance |
| Missing onError for encryption | No error handling on encrypt | Add onError block | Resilience |
| Missing padding for phone | Phone encryption without padding | Add padding config | Encryption accuracy |

**Validation Optimizations:**
| Check | Current | Recommended | Impact |
|-------|---------|-------------|--------|
| No validations | Empty or missing | Add notNull, primaryKey, schema at minimum | Data quality |
| No duplicateFileCheck | Missing | Add with daysBack: 60 | Duplicate prevention |
| No notNull on PK columns | PK columns without notNull | Add notNull validation | Data integrity |
| No numericRange on amounts | Numeric columns without range | Add range validation | Data quality |
| No allowedValues on enums | Enum columns without validation | Add allowedValues | Data quality |
| No email validation | Email columns without validation | Add email validation | Data quality |

**Performance Optimizations:**
| Check | Current | Recommended | Impact |
|-------|---------|-------------|--------|
| No partitioning | No partition columns | Add data_dt partition with dateFormat transformation | Query performance |
| Wrong cluster size | Default or too small | Recommend based on data volume | Job performance |
| No overwriteType | overwritePartition without type | Add `overwriteType: "DYNAMIC"` | Partition management |

Report ALL findings with: tier, check name, field path, current value, recommended value, impact assessment, and constitution reference.

### 5. Generate Refactored Config

**Apply fixes in strict priority order. The output must be a COMPLETE valid JSON config.**

**Tier 1 fixes (ALWAYS apply — non-negotiable):**
1. Fix JSON structure (targets as array, valid syntax)
2. Add all missing mandatory root fields
3. Fix email fields
4. Remove plaintext credentials → use secret scopes
5. Fix all schema issues (columnName, columnType, duplicates, partitionOrder)
6. Fix source-specific issues (JDBC, Kafka, File, HTTP, Azure Files)
7. Fix target issues (targetLocation, writeMode, upsert keys, database target)
8. Fix transformation parameter issues
9. Fix validation parameter issues
10. Fix error handling dependencies

**Tier 2 fixes (apply unless user explicitly opts out):**
1. Add controlColumns to all targets
2. Align writeMode with data pattern
3. Add/fix source and target schemas
4. Fix schema consistency (derived columns → transformations)
5. Normalize column types
6. Add decimal precision/scale
7. Set globalTransformation.trimSpacesInd: true
8. Add transformation onError blocks
9. Add fileFailureThresholdPercentage
10. Add encrypted flags on encrypted columns

**Tier 3 optimizations (apply based on refactoring goals):**

For `security` goal:
- Add hashingAndEncrypt for all identified PII columns
- Add encryptIdentity: "DL_IDENTITY@ATT.COM", encryptFormat: "ALPHA_NUM"
- Add padding for phone numbers (padSide: "left", padWidth: "0", padToLength: 10)
- Add onError for each encryption transformation
- Add encrypted: true flag on target schema columns
- Rename target columns to indicate encryption (e.g., email → email_encrypted)

For `performance` goal:
- Set fetchSize: 20000+ for JDBC
- Add numPartitions based on table size
- Add dbTablePartitioning for large tables
- Switch to Delta format
- Add snappy compression
- Set writeOneFileInd: false
- Recommend appropriate clusterSize
- Add overwriteType: "DYNAMIC" for overwritePartition

For `data-quality` goal:
- Add globalTransformation with trimSpacesInd, replaceValues, quote removal
- Add notNull validation for all PK and mandatory columns
- Add primaryKey validation for PK columns
- Add schema validation with validateDataTypes
- Add duplicateFileCheck with daysBack: 60
- Add numericRange for numeric columns
- Add allowedValues for enum columns
- Add email validation for email columns
- Add length validation for fixed-length columns

For `partitioning` goal:
- Add data_dt partition column to target schema with partitionOrder: 1
- Add dateFormat transformation to generate data_dt (generatedValue: "SYSDATE", dateTargetFormat: "yyyyMMdd")
- Align writeMode to overwritePartition if daily batch
- Add overwriteType: "DYNAMIC"
- Add vacuumDaysOld: 7

For `modernize` goal:
- Switch to Delta format
- Add controlColumns
- Add globalTransformation
- Add onFailure error handling
- Rename srcId to snake_case
- Add feedType, supportTeam
- Add vacuumDaysOld: 7
- Add basic validations (notNull, schema)
- Set writeOneFileInd: true when source is JDBC and target is file-based; not applicable for other sources
- Remove sourceFileFormat from JDBC/Kafka sources

For `compliance` goal:
- Fix ALL Tier 1 violations
- Fix ALL Tier 2 issues
- Add encryption for PII columns
- Verify RIM policy alignment
- Verify data library classification
- Add audit columns (load_timestamp via dateFormat transformation)

For `full` goal:
- Apply ALL Tier 1, 2, and 3 fixes

### 6. Add Recommendations

**Change Summary Table:**

```
| # | Tier | Field Path | Before | After | Impact | Constitution Ref |
|---|------|-----------|--------|-------|--------|-----------------|
| 1 | T1   | source.jdbcSource.logonScopeName | (missing) | "dl-eastus2-dev-sec-kv-scope" | Security | I.Credential.2 |
| 2 | T1   | targets | {object} | [{object}] | Structure | I.Root.2 |
| 3 | T2   | targets[0].controlColumns | (missing) | {fileNameColumnInd: true, ...} | Lineage | II.Target.1 |
| 4 | T3   | globalTransformation | (missing) | {trimSpacesInd: true, ...} | Quality | III.Global.1 |
...
```

**Impact Assessment:**
- **Breaking changes**: Any changes that alter pipeline behavior (writeMode change, schema change, new partitioning)
- **Non-breaking changes**: Additions that don't affect existing behavior (controlColumns, globalTransformation, validations)
- **Performance impact**: Expected improvement or degradation

**Migration Notes:**
- If writeMode changed: explain data implications, recommend initial full load
- If schema changed: explain column additions/removals
- If partitioning added: explain partition column derivation
- If encryption added: explain that existing unencrypted data remains, new data will be encrypted

**Testing Guidance:**
- Run `/test-xflow-orchestrator` on the refactored config
- Test with small dataset first (limit source to 1000 rows)
- Verify target schema matches expected output
- Verify transformations produce correct values
- Verify validations catch expected errors

**Further Improvements:**
- List optimizations NOT applied in this pass (with rationale)
- Suggest follow-up refactoring tasks

### 7. Validate and Report

// turbo

Validate refactored config against ALL constitution hard-stop rules. Report with:
- Total findings by tier: T1 (critical), T2 (mandatory), T3 (recommended)
- Fixes applied by tier
- Change summary table (field path, before, after)
- Validation status of refactored config (PASS/FAIL)
- Breaking vs non-breaking changes
- Recommended next steps

## Error Handling

**Hard-Stop Violations in Original**: These are NON-NEGOTIABLE. Explain each violation clearly, show the fix, and note that the refactored config MUST fix these regardless of user constraints.

**Incomplete Input**: Request:
1. Config file path
2. Refactoring goals (security/performance/data-quality/partitioning/modernize/compliance/full)
3. PII columns (if security goal)
4. Constraints (fields that must not change)

**Conflicting Goals**: If user goals conflict with constitution rules:
- "Remove encryption from PII" → Explain hard-stop rule, refuse, suggest alternative
- "Use overwrite for large table" → Explain risk, recommend overwritePartition
- "Remove controlColumns" → Explain mandatory pattern, refuse
- "Skip validations" → Explain data quality risk, recommend minimum set

**Large Config (>100 fields)**: Break analysis into sections:
1. Root metadata audit
2. Source configuration audit
3. Schema audit (source + target)
4. Target configuration audit
5. Transformation audit
6. Validation audit
7. Global transformation audit
8. Error handling audit

## Examples

**Example 1: Full Security Refactor**
```
/refactor-xflow-orchestrator security — Add encryption to PII columns in customer_config.json
PII columns: email, phone, ssn, customer_name

Changes (12):
T1: 0 fixes (no violations)
T2: 2 fixes (add encrypted flags, add onError)
T3: 4 optimizations (4 hashingAndEncrypt transformations with encryptIdentity, encryptFormat, padding for phone)

New transformations:
- email → email_encrypted (hashingAndEncrypt, ALPHA_NUM)
- phone → phone_encrypted (hashingAndEncrypt, ALPHA_NUM, padding left/0/10)
- ssn → ssn_encrypted (hashingAndEncrypt, ALPHA_NUM)
- customer_name → customer_name_encrypted (hashingAndEncrypt, ALPHA_NUM)

Target schema updated: 4 columns renamed with _encrypted suffix, encrypted: true flag added
```

**Example 2: Performance Optimization**
```
/refactor-xflow-orchestrator performance — Optimize slow JDBC extraction in large_table.json

Changes (7):
T1: 0 fixes
T2: 0 fixes
T3: 7 optimizations:
- fetchSize: 5000 → 50000
- Added numPartitions: 8
- Added dbTablePartitioning on created_date column
- writeOneFileInd: true (confirmed correct for JDBC-to-file)
- targetFileFormat: parquet → delta
- Added vacuumDaysOld: 7
- Recommended clusterSize: "medium"

Expected improvement: 4-6x faster extraction, 30% storage reduction with snappy compression
```

**Example 3: Full Data Quality Refactor**
```
/refactor-xflow-orchestrator data-quality — Add comprehensive validations to billing_pipeline.json

Changes (15):
T1: 0 fixes
T2: 2 fixes (add globalTransformation, add schema validation)
T3: 13 optimizations:
- Added globalTransformation: trimSpacesInd, replaceValues (null standardization), removeStartCharacters/removeEndCharacters (quote removal)
- Added 8 validations: notNull (3 columns), primaryKey (invoice_id), numericRange (amount), allowedValues (status), duplicateFileCheck (60 days), email (customer_email)
- Added sourceRejectLocation for rejected records
- Added onFailure with badFileInd: true
```

**Example 4: Modernize Legacy Config**
```
/refactor-xflow-orchestrator modernize — Upgrade legacy_ingestion.json to current standards

Changes (22):
T1: 3 fixes (missing rimPolicyName, targets as object, invalid columnType "varchar")
T2: 5 fixes (add controlColumns, fix schema consistency, add trimSpacesInd, add decimal precision, add fileFailureThreshold)
T3: 14 optimizations:
- parquet → delta with vacuumDaysOld: 7
- Added snappy compression
- srcId "CustomerData" → "customer_data"
- Added feedType: "ING", supportTeam: "datalake"
- Added globalTransformation with null standardization
- Added data_dt partition with dateFormat transformation
- writeMode: overwrite → overwritePartition
- Added 4 basic validations
- Added onFailure error handling
- Added fetchSize: 20000
```

**Example 5: Compliance Refactor**
```
/refactor-xflow-orchestrator compliance — Fix all constitution violations in audit_config.json

Changes (18):
T1: 5 fixes (missing dataLibrary, plaintext password removed, invalid columnType, upsert without PK, missing logonSecretName)
T2: 4 fixes (missing controlColumns, missing trimSpacesInd, derived column without transformation, missing encrypted flag)
T3: 9 optimizations (encryption for 3 PII columns, Delta format, compression, validations, error handling)

All constitution hard-stop rules: PASS
All mandatory patterns: PASS
Preferred patterns: 9/12 applied
```

**Example 6: Targeted Partitioning Refactor**
```
/refactor-xflow-orchestrator partitioning — Add date partitioning to orders_config.json
Constraint: Do not change source schema or writeMode

Changes (5):
T1: 0 fixes
T2: 0 fixes
T3: 5 optimizations:
- Added data_dt column to target schema with partitionOrder: 1
- Added dateFormat transformation: generatedValue: "SYSDATE", dateTargetFormat: "yyyyMMdd"
- Note: writeMode remains "append" per constraint (recommend overwritePartition in future)
- Added vacuumDaysOld: 7
- Added overwriteType: "DYNAMIC" (for future writeMode change)
```

## References

- XFlow Constitution: `xflow-orchestrator-constitution.md` (Sections I-IV, complete field reference)
- XFlow Field Definitions: `XFlow_System_chunks.json` (field_0001 through field_0026)
- XFlow Source Types: `XFlow_System_chunks.json` (source_0027 through source_0030)
- XFlow Transformations: `XFlow_System_chunks.json` (trans_0031 through trans_0037)
- XFlow Validations: `XFlow_System_chunks.json` (valid_0038 through valid_0040)
- XFlow Dependencies: `XFlow_System_chunks.json` (general_0041)
- XFlow Defaults: `XFlow_System_chunks.json` (general_0042)
- XFlow Best Practices: `XFlow_System_chunks.json` (general_0043)
- Pydantic Models: `xflow_models.py` (validation logic, field constraints, enums)
- Transformation Models: `xflow_transformations.py` (16 types with required params)
- Validation Models: `xflow_validations.py` (17 types with required params)
