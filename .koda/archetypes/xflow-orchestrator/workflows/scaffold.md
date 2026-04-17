---
description: Generate production-ready XFlow JSON configuration from natural language requirements (XFlow Orchestrator)
---

User input: $ARGUMENTS

## Execution Steps

## Execution Rules (NON-NEGOTIABLE)

**These rules govern HOW the wizard executes. Violating them is a hard-stop.**

1. **ONE question per message.** Each wizard step that requires user input MUST be its own separate `ask_user_question` call. NEVER combine multiple questions into a single prompt.
2. **NO skipping steps.** Every wizard step (4a through 4j) MUST be executed in order. The ONLY exception is when the user already provided the information in $ARGUMENTS — that specific sub-step may be skipped.
3. **NO batching metadata fields.** Even Step 4d (Pipeline Metadata) — if the user didn't provide values in $ARGUMENTS, ask for them. But this is the ONE step where multiple fields may be collected in a single prompt (as the workflow explicitly says "ask in one batch").
4. **WAIT for user response** before proceeding to the next step. Do not assume defaults for steps that require user input unless the workflow explicitly says to apply a default silently.
5. **NEVER jump to generation.** Steps 4f (Transformations), 4g (Validations), 4h (Global Transformation), and 4i (Error Handling) MUST be executed — but like all other steps, they may be skipped if $ARGUMENTS already provides the answer. Phrases like "no transformations", "no validations", "no global transform", "no error handling", "skip transformations", or "standard error handling" count as provided answers and the corresponding step should be silently applied without asking.
6. **NEVER save to file unless user requests it.** Step 4j says to generate the JSON inline as a fenced code block in chat. Do NOT write to a file unless the user explicitly asks.

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
- Read `xflow-orchestrator-constitution.md` for hard-stop rules (all sections I through VII)
- Load `templates/env-config.yaml` for default values
- **CRITICAL RULES** that apply to ALL generated configs:
  - `transformations`, `globalTransformation`, and `errorHandling` MUST be inside `targets[]` objects, NEVER at root level
  - `motsId` MUST be a string value (e.g., `"19062"`, not `19062`)
  - `deltaAutoloaderConfiguration` MUST always be present (default `[]`)
  - `TERADATA` (not `TERRADATA`)

### 3. Parse Initial Input & Start Wizard

Extract whatever details are present in $ARGUMENTS. Track what has been provided and what still needs to be collected. Then run the interactive wizard below — **skip any step where the user already provided the information in $ARGUMENTS**.

---

## Interactive Wizard

### Step 4a — Source Type

**ASK the user (if not already in $ARGUMENTS):**

> What type of data source?
> - **JDBC** — Database (Oracle, SQL Server, Snowflake, PostgreSQL, MySQL, Vertica, Teradata, Trino)
> - **Kafka** — Streaming topic ingestion
> - **File** — ADLS/blob file (CSV, Parquet, JSON, XML, Avro, ORC, Fixed-width)
> - **DataRouter** — HTTP push via DataRouter/FileGW (httpFileSource)
> - **Azure Files** — Azure File Share pull

Use `ask_user_question` with the first 4 options (Azure Files as custom input). If user already specified source type in $ARGUMENTS, skip this step.

<!-- HALT: Wait for user response before continuing to Step 4b -->

---

### Step 4b — Source Details (branched by source type)

**If JDBC — ASK sequentially:**

1. **Database type?** → Use `ask_user_question` with options: ORACLE, SQL_SERVER, SNOWFLAKE, POSTGRESQL, MY_SQL, VERTICA, TERADATA, TRINO, GENERIC
2. **Auto-populate driver defaults** → Based on the selected `connectionType`, automatically set `driverLocation` and `driverClassName` from `jdbc_driver_defaults` in `env-config.yaml`. Do NOT ask the user for these values — apply them silently:
   - `ORACLE` → `driverLocation: "/Volumes/30636_azuredl_prd/adl/adlcontainer-stl/3rd-party/ojdbc8.jar"`, `driverClassName: "oracle.jdbc.OracleDriver"`
   - `SQL_SERVER` → `driverLocation: "/Volumes/30636_azuredl_prd/adl/adlcontainer-stl/3rd-party/mssql-jdbc-8.2.2.jre8.jar"`, `driverClassName: "com.microsoft.sqlserver.jdbc.SQLServerDriver"`
   - `MY_SQL` → `driverLocation: "/Volumes/30636_azuredl_prd/adl/adlcontainer-stl/3rd-party/mssql-jdbc-8.2.2.jre8.jar"`, `driverClassName: "com.mysql.cj.jdbc.Driver"`
   - `VERTICA` → `driverLocation: "/Volumes/30636_azuredl_prd/adl/adlcontainer-stl/3rd-party/vertica-jdbc-9.2.1-0.jar"`, `driverClassName: "com.vertica.jdbc.Driver"`
   - `TERADATA` → `driverLocation: "/Volumes/30636_azuredl_prd/adl/adlcontainer-stl/3rd-party/terajdbc4.jar"`, `driverClassName: "com.ncr.teradata.TeraDriver"`
   - For `SNOWFLAKE`, `POSTGRESQL`, `TRINO`, `GENERIC` → do not set driver fields (handled by Databricks built-in drivers)
3. **SQL file location?** → Ask for the ADLS path to the SQL file (e.g., `abfss://adl@datalakeeastus2prd.dfs.core.windows.net/jdbc/sql/app/query.sql`). This is mandatory for all JDBC sources.
4. **Secret scope name?** → Suggest default from env-config (`dl-eastus2-dev-sec-kv-scope`). Ask user to confirm or provide their own.
5. **Secret key name?** → Ask user to provide the Databricks secret key name for this database connection.
6. **(If SNOWFLAKE)** → Ask for `sfDatabaseName`, `sfSchemaName`, `sfWarehouse` in one prompt.

7. **Bind parameters?** → Ask: "Does the SQL query have bind parameters?" (Yes/No)
   - If **Yes**, show this example and ask user to provide their parameter SQL:
   ```json
   "parameters": [
     {
       "index": 1,
       "sourceType": "SQL",
       "source": "select TO_CHAR(...) AS RESULT1 FROM schema.TABLE WHERE ...",
       "outputType": "STRING",
       "fetchParameterType": "FETCH_ON_NULL",
       "saveValueFromIndex": 2
     },
     {
       "index": 2,
       "sourceType": "SQL",
       "source": "select MAX(BATCH_ID) AS RESULT2 FROM schema.TABLE WHERE ...",
       "outputType": "STRING",
       "fetchParameterType": "FETCH_ALWAYS"
     }
   ]
   ```
   - `FETCH_ON_NULL`: Runs the SQL only on the very first execution (when no cached value exists).
   - `FETCH_ALWAYS`: Runs the SQL on every job invocation to get the latest value.
   - If **No**, set `"parameters": []`

Apply defaults: `fetchSize: 20000`, `parameters: []`.

**If Kafka — ASK sequentially:**

1. **Bootstrap servers?** → Ask for comma-separated list (e.g., `broker1:9093,broker2:9093`)
2. **Topic name?** → The Kafka topic to subscribe to
3. **Consumer group ID?** → Suggest `xflow_{srcId}` as default
4. **Secret scope and key?** → For SASL authentication
5. **Starting offset?** → Use `ask_user_question`: **latest** (default) | earliest | specific timestamp

Apply defaults: `securityProtocol: "SASL_SSL"`, `saslMechanism: "PLAIN"`, `maxOffsetsPerTrigger: 100000`, `maxBytesPerTrigger: 1000000000`, `pollTimeoutMs: 120000`, `startingOffsets: "LATEST"`.

**If sourceFileFormat is `kafkatext`** (raw message storage): source and target schemas must only contain partition columns (no data columns). `targetFileFormat` must be `"csv"` (the API rejects `"text"`). Do not include a `value` column.

**If File — ASK sequentially:**

1. **Source location?** → ADLS path (must start with `abfss://`). **Note:** The container must be provisioned and accessible to the `appId` — the STL API validates this at submission time.
2. **File format?** → Use `ask_user_question`: CSV | Parquet | JSON | XML | Avro | ORC | Fixed-width
3. **(If CSV)** → Ask: Delimiter? (default `,`) | Has header row? (default `false`)
   - Also ask: "Do you need advanced CSV source properties?" If yes, offer `csvSourceProperties` with options: `delimiter`, `sep`, `quote`, `escape`, `escapeQuotes`, `header`, `multiLine`, `lineSep`, `emptyValue`. Let user select from a dropdown list or enter values manually.
   - Set `csvIgnoreExtraColumnsInd: true` by default.
4. **(If XML)** → Ask: XML row path? (e.g., `root/record`)
5. **(If Fixed-width)** → Ask: Column widths? (comma-separated integers). Generate as a JSON integer array in the config (e.g., `"fixedLengthCounts": [10, 20, 15]`), NOT a string.

Apply defaults: `filesRetentionDays: 7` for ING feeds, `-1` for MGR feeds (user can override). Only include `filesRetentionDays` when the source has a `sourceLocation` — not applicable for Kafka sources without a staging location.

**If DataRouter (httpFileSource) — ASK sequentially:**

Applicable only for DataRouter as source. See constitution Section VI for full field reference.

1. **Source location?** → ADLS prestaging path (`abfss://...`)
2. **Subscriber ID?** → The DataRouter subscriber identifier (integer)
3. **Feed ID?** → The DataRouter/FileGW feed identifier
4. **File filter regex?** → Pattern to match incoming files (e.g., `^DATA_.*\.csv$`)
5. **Duplicate file check?** → Use `ask_user_question`: Yes | No (default)
6. **Source file format?** → CSV, Fixed-width, JSON, etc.
7. **File has header/trailer?** → If yes, add `EXTRACT_HEADER_TRAILER` fileAction with `headerLineCount`, `trailerLineCount`, `excludeEmptyLine: false`, `removeHeaderTrailerInd: false`
8. **Need record count validation?** → If yes, add `RECORD_COUNT_VALIDATION` fileAction
9. **File is compressed?** → If yes, add `COMPRESSION` fileAction with `decompressInd: true`, `openArchiveInd: true`, `compressionArchiveMethod: "gzip"`
10. **Partition from filename?** → If yes, add `DEST_PARTITIONING` fileAction with partition regex
11. Always add `DEST_FILE_PATTERN` fileAction

Apply defaults: `filterBy: "FILE_NAME"`, `tempDirInd: false`, `tempFileRetentionHours: 0`, `filesRetentionDays: 7`.

**If Azure Files — ASK sequentially:**

1. **Source location?** → ADLS prestaging path (`abfss://...`)
2. **Subscriber ID?** → Subscriber identifier
3. **Feed ID?** → Feed identifier
4. **File share name?** → Azure file share name
5. **Storage account name?** → Account name for file share
6. **SAS token vault name?** → Key vault name for SAS token
7. **SAS token secret key?** → Secret key name
8. **Resource path?** → Path within file share (e.g., `lz/inbound`)
9. **File filter regex?** → Pattern to match files
10. **Source file format?** → CSV, Fixed-width, JSON, etc.
11. **File actions?** → Same as DataRouter (header/trailer, partitioning, compression, etc.)

Apply defaults: `filterBy: "FILE_NAME"`, `tempDirInd: false`, `duplicateFileCheckInd: false`, `writeEmptyFileOnTargetInd: false`, `filesRetentionDays: 7`.

<!-- HALT: Wait for user response before continuing to Step 4c -->

---

### Step 4c — Schema

**ASK the user (if not already in $ARGUMENTS):**

> How would you like to define the source schema?
> - **Type column list** — provide as `name:type` pairs (e.g., `customer_id:string, amount:decimal(10,2)`)
> - **Paste JSON** — paste a JSON array of column definitions

After receiving the schema, **validate immediately**:
- Every column has both `columnName` and `columnType`
- All `columnType` values are valid Spark SQL types: string, int, integer, long, bigint, double, float, boolean, date, timestamp, decimal, binary, short, byte
- No duplicate column names
- Decimal columns should have precision and scale — if missing, ask user

If validation fails, show the specific error and ask the user to correct it before continuing.

<!-- HALT: Wait for user response before continuing to Step 4d -->

---

### Step 4d — Pipeline Metadata

**ASK for ALL missing mandatory fields in a single prompt. Skip any already provided in $ARGUMENTS.**

Suggest inferred defaults where possible:
- `srcId` → infer from table/file name (e.g., `customers.orders` → `customer_orders`)
- `appId` → infer from target container name
- `supportTeam` → default `"datalake"`
- `feedType` → default `"ING"`


Fields to collect (ask in one batch):
- `createdBy` — your email (must contain `@`)
- `sourceContact` — source team email (must contain `@`)
- `dataLibrary` — e.g., `DP-DLIB-Brws`, `DP-DLIB-Loc`
- `rimPolicyName` — e.g., `NET-440`, `CUST-100`
- `motsId` — MOTS identifier (always a **string**, e.g., `"19062"`)
- `feedDescription` — (Optional) Human-readable description of the feed

<!-- HALT: Wait for user response before continuing to Step 4e -->

---

### Step 4e — Target Configuration

**ASK the user (if not already in $ARGUMENTS):**

1. **Target location?** → If not provided, ask for the ADLS URI (`abfss://container@account.dfs.core.windows.net/path`)

2. **Write mode?** → Use `ask_user_question`:
   - **append** (default) — add new records, keep existing. Best for streaming/incremental loads.
   - **overwrite** — replace entire dataset. Best for small dimension tables.
   - **overwritePartition** — replace specific partitions. Best for daily batch reloads.
   - **upsert** — insert or update by key. Best for CDC / change data capture.

3. **Target format?** → Use `ask_user_question`:
   - **delta** (default, recommended) — ACID, time-travel, schema evolution (requires Unity Catalog)
   - **parquet** — columnar, good compression
   - **csv** — plain text, interop
   - **database** — write to external database

4. **(If upsert)** → Which columns are primary keys? List the column names.
5. **(If overwritePartition)** → Which columns to partition by? List the column names.
6. **(If database)** → Ask for databaseTarget: connectionType, logonScopeName, logonSecretName, dbTable.
7. **(If csv target)** → Ask for `csvTargetProperties`: `sep`, `quote`, `escape`, `escapeQuotes`, `emptyValue`, `nullValue`, `lineSep`. Let user select from defaults or enter manually.
8. **(If file-based source — httpFileSource or azureFilesSource)** → Ask for `targetFilePattern` (e.g., `"{SRC_FILE_NAME}.parquet"`, `"{SRC_FILE_NAME}_{UNIQUE_ID}.parquet"`).
9. **(If delta target)** → **ALWAYS** collect Unity Catalog details: `catalogName`, `schemaName`. Add `unityCatalog: {writeAsTableInd: true, catalogName: "...", schemaName: "..."}` to the target. **Do NOT include `targetFileFormat`** — when `unityCatalog` is present, delta is implicit. If user already provided catalog/schema in $ARGUMENTS, apply silently.

Apply defaults: Set `writeOneFileInd: true` when source is a database (JDBC) and target is a file format (delta/parquet/csv). Not applicable for other source types. Include `vacuumDaysOld: 7` ONLY when target is delta (i.e., `unityCatalog` is present). Do NOT include for parquet, csv, or database targets.

**NOTE:** `controlColumns` is recommended but not mandatory. Include `controlColumns: {fileNameColumnInd: true, creationTimestampColumnInd: true}` by default.

<!-- HALT: Wait for user response before continuing to Step 4f -->

### Step 4f — Transformations (Intent-Based Questions)

**CRITICAL: All transformations MUST be placed inside `targets[0]` in the generated JSON, NEVER at root level.**

**ASK the user:**

> Do you need any data transformations?
> - **Yes, let me specify** — I'll walk you through the options
> - **No, skip transformations** — no transformations needed
> - **Use recommended defaults** — add `load_timestamp` column only

Use `ask_user_question` with these 3 options.

**If "Yes" — ask these intent-based questions sequentially. Skip any that the user declines.**

**Question 1 — PII / Encryption:**
> Do any columns contain sensitive data (SSN, email, phone, credit card, etc.) that needs encryption?
> - **Yes** — I'll specify which columns
> - **No** — no PII columns

If yes, ask: "Which columns need encryption? (comma-separated)"
For each column, generate a `hashingAndEncrypt` transformation with:
- `encryptIdentity`: `"DL_IDENTITY@ATT.COM"` (default)
- `encryptFormat`: `"ALPHA_NUM"` (default)
- Target column name: `{original_name}_encrypted`
- `onError`: `{ "failRecordInd": true, "replaceFailedValueWith": "NULL" }`

**Question 2 — Date Conversions:**
> Do any columns need date format conversion (e.g., string to date/timestamp)?
> - **Yes** — I'll specify which columns
> - **No** — no date conversions

If yes, ask: "Which columns? For each, what is the source format(s) and target format?"
Generate `dateFormat` transformation with `dateSourceFormats`, `dateTargetFormat`, `dateSourceTimeZone`.

**Question 3 — Derived / Computed Columns:**
> Do you want to add any computed columns?
> - **load_timestamp** — audit timestamp (SYSDATETIME)
> - **data_dt** — partition date column (SYSDATE as yyyyMMdd)
> - **Both** — add both load_timestamp and data_dt
> - **Custom** — I'll specify my own derived columns
> - **None** — no derived columns

Use `ask_user_question` with these options.

**Question 4 — Value Transformations:**
> Do any columns need value cleaning?
> - **Uppercase** — convert columns to uppercase
> - **Lowercase** — convert columns to lowercase
> - **Replace values** — replace patterns or specific values
> - **None** — no value cleaning

Use `ask_user_question` (allowMultiple=true) with these options.
If selected, ask which columns for each transformation type.

**Transformation Reference (use when generating JSON):**

| Type | Required Parameters | Optional |
|------|-------------------|----------|
| `hashingAndEncrypt` | `encryptIdentity`, `encryptFormat` | `padding` (padSide, padWidth, padToLength) |
| `dateFormat` (convert) | `dateSourceFormats`, `dateTargetFormat` | `dateSourceTimeZone` (default `"EST"`) |
| `dateFormat` (generate) | `generatedValue` (`SYSDATE`/`SYSDATETIME`), `dateTargetFormat` | — |
| `regex` | `pattern`, `outputFormat` | — |
| `replace` | `removePatterns`, `replaceWith` | — |
| `uppercase` | (none) | — |
| `lowercase` | (none) | — |
| `epochToTimestamp` | `sourceEpochUnit` | `dateTargetFormat` |
| `addColumn` | `value` | — |
| `concatenate` | `delimiter` | — |
| `substring` | `startPosition`, `length` | — |
| `cast` | `targetType` | — |
| `nullHandling` | `strategy` | `defaultValue` |
| `conditional` | `condition`, `trueTransformation`, `falseTransformation` | — |
| `sql` | `sqlExpression` | — |

Each transformation object must follow this structure:
```json
{
  "targetColumnName": "column_name",
  "sourceColumns": ["source_col1"],
  "transformationSteps": [
    {
      "transformationType": "type_name",
      "transformationParameters": { },
      "description": "What this does",
      "onError": {
        "failRecordInd": true,
        "replaceFailedValueWith": "NULL|CONSTANT|SKIP_RECORD"
      }
    }
  ]
}
```

<!-- HALT: Wait for user response before continuing to Step 4g -->

---

### Step 4g — Validations (Intent-Based Questions)

**ASK the user:**

> Do you want data quality validations on this pipeline?
> - **Yes, let me specify** — I'll walk you through the options
> - **No, skip validations** — no validations
> - **Use recommended defaults** — schema validation + notNull on key columns

Use `ask_user_question` with these 3 options.

**If "Yes" — ask these questions sequentially:**

**Question 1 — Required Fields (notNull):**
> Which columns must NOT be NULL? (comma-separated, or "none")

Generate `notNull` validation with `failureAction: "fail"` for each listed column.

**Question 2 — Schema Validation:**
> Validate that incoming data types match the schema definition?
> - **Yes** (recommended)
> - **No**

If yes, generate: `{ "validationType": "schema", "validationParameters": {"validateDataTypes": true}, "failureAction": "fail" }`

**Question 3 — Duplicate File Check:**
> Check for duplicate source files?
> - **Yes** — specify lookback window in days (default: 30)
> - **No**

If yes, ask for days, then generate: `{ "validationType": "duplicateFileCheck", "validationParameters": {"daysBack": N}, "failureAction": "fail" }`

**Question 4 — Uniqueness / Primary Key:**
> Any columns that must be unique (primary keys)?
> - **Yes** — I'll specify which columns
> - **No**

If yes, ask which columns, then generate `primaryKey` validation with `failureAction: "fail"`.

**Question 5 — Pattern Matching:**
> Any columns with format constraints (email, phone, regex patterns)?
> - **Email validation** — validate email format
> - **Phone validation** — validate phone format
> - **Regex pattern** — custom regex validation
> - **None**

Use `ask_user_question` (allowMultiple=true). For each selected, ask which columns.

**Question 6 — Range Checks:**
> Any numeric columns with min/max bounds? (or "none")

If yes, ask which columns and their min/max values. Generate `numericRange` validation.

**Validation Reference (use when generating JSON):**

| Type | Required Parameters | Optional |
|------|-------------------|----------|
| `schema` | `validateDataTypes` | — |
| `notNull` | `sourceColumns` | — |
| `notEmpty` | `sourceColumns` | — |
| `primaryKey` | `sourceColumns` | — |
| `unique` | `sourceColumns` | `scope` |
| `regex` | `pattern`, `sourceColumns` | — |
| `numericRange` | `sourceColumns` | `minValue`, `maxValue` |
| `length` | `sourceColumns` | `minLength`, `maxLength` |
| `allowedValues` | `allowedValues`, `sourceColumns` | `caseSensitive` |
| `dateFormat` | `dateFormat`, `sourceColumns` | — |
| `dateRange` | `sourceColumns` | `minDate`, `maxDate` |
| `email` | `sourceColumns` | — |
| `phone` | `sourceColumns` | `country` |
| `foreignKey` | `referenceTable`, `referenceColumns`, `sourceColumns` | — |
| `count` | — | `minCount`, `maxCount` |
| `duplicateFileCheck` | `daysBack` | — |
| `duplicateCount` | `columns` | `maxDuplicates` |
| `sql` | `sqlExpression` | — |
| `custom` | `functionName`, `parameters` | — |

Each validation object must follow this structure:
```json
{
  "validationType": "type_name",
  "sourceColumns": ["col1", "col2"],
  "validationParameters": { },
  "failureAction": "fail|warn|skip"
}
```

<!-- HALT: Wait for user response before continuing to Step 4h -->

---

### Step 4h — Global Transformation

**CRITICAL: `globalTransformation` MUST be placed inside `targets[0]` in the generated JSON, NEVER at root level.**

**ASK the user:**

> Do not apply global data cleaning to all records? (recommended)
> - **Yes, use defaults** — trim spaces + standardize nulls (NA/NULL/""→Null)
> - **Yes, customize** — let me specify what to clean
> - **No** — skip global transformation

Use `ask_user_question` with these 3 options.

**If "Yes, use defaults":**
```json
{
  "trimSpacesInd": true,
  "replaceValues": [
    { "existingValues": ["", "NA", "NULL", "reserved:NULL", "N/A", "null"], "newValue": "Null" }
  ]
}
```

**If "Yes, customize" — ask:**

1. **Trim spaces?** → Yes (default) / No
2. **Remove quote characters?** → If yes, set `removeStartCharacters: "\""` and `removeEndCharacters: "\""`
3. **Standardize null values?** → If yes, ask which values to treat as null (default: `["", "NA", "NULL", "reserved:NULL", "N/A"]`)
4. **Custom value replacements?** → Any other `existingValues → newValue` mappings

<!-- HALT: Wait for user response before continuing to Step 4i -->

---

### Step 4i — Error Handling

**CRITICAL: `errorHandling` MUST be placed inside `targets[0]` in the generated JSON, NEVER at root level. Include `errorTableLocation` for error audit trail.**

**ASK the user:**

> How should pipeline failures be handled?
> - **Strict** — fail on any error (threshold=0), create bad file for debugging
> - **Standard** (default) — fail on any error, skip malformed records, create bad file
> - **Lenient** — allow up to 5% error rate, skip malformed, no reject
> - **Custom** — let me specify thresholds and behavior

Use `ask_user_question` with these 4 options.

**Preset mappings:**

| Preset | `fileFailureThresholdPercentage` | `skipMalformedRecsInd` | `onFailure.badFileInd` | `onFailure.moveToRejectInd` |
|--------|--------------------------------|----------------------|----------------------|---------------------------|
| Strict | 0 | false | true | false |
| Standard | 0 | true | true | false |
| Lenient | 5 | true | true | false |

**If "Custom":**
1. Error threshold percentage? (0-100, 0 = fail on any error)
2. Skip malformed records? Yes/No
3. Move failed files to reject location? Yes/No → if yes, ask for reject ADLS path
4. Create bad file for debugging? Yes/No
5. Retry failed files? Yes/No

<!-- HALT: Wait for user response before continuing to Step 4i2 -->

---

### Step 4i2 — Job Configuration

**Source-type-aware logic:**

- **If source is File (ADLS Path)**: Ask the user — "Do you want to schedule this job or run it in continuous mode?"
  - If **continuous mode**: Add `jobConfiguration` with `jobInvocationConfig.continuousProcessing.activeInd: true` and `checkTimePattern: ""`. Do NOT omit `jobConfiguration` — the API requires it.
  - If **scheduled**: Ask for cron schedule and add `jobConfiguration`.
- **If source is JDBC, DataRouter, Azure Files, or Kafka**: Always ask for the cron schedule. For Kafka, if user requests continuous mode, add `continuousProcessing.activeInd: true` instead of a cron schedule.

**ASK the user:**

> What cron schedule should this job run on?
> - Default: `"0 0 1/1 * * ?"` (every hour)
> - Common patterns: `"0 0 6 * * ?"` (daily at 6 AM), `"0 0/30 * * * ?"` (every 30 min)


**For non-Kafka scheduled sources:**
```json
"jobConfiguration": {
  "jobInvocationConfig": {
    "schedule": {
      "type": "databricks",
      "cronSchedule": "{user_cron}",
      "timeZone": "UTC"
    }
  }
}
```

<!-- HALT: Wait for user response before continuing to Step 4j -->

---

### Step 4j — Review & Generate

1. **Display a summary table** of everything collected:

| Section | Value |
|---------|-------|
| Source Type | JDBC (ORACLE) |
| Source Table/Location | customers.orders |
| Schema Columns | 3 (customer_id, order_id, order_type) |
| Target Location | abfss://... |
| Write Mode | append |
| Target Format | delta |
| Transformations | N items (list types) |
| Validations | N items (list types) |
| Global Transform | trim + null standardization |
| Error Handling | Standard |

2. **ASK the user:**

> Ready to generate the XFlow JSON config?
> - **Generate** — output the final JSON
> - **Change something** — go back and modify a section

Use `ask_user_question` with these 2 options.
If "Change something", ask which section to revisit and re-run that step.

3. **On confirmation — generate the complete JSON inline** as a fenced `json` code block directly in the chat. Do NOT save to a file.

**CRITICAL CHECKLIST before output:**
- [ ] `transformations` is inside `targets[0]`, NOT at root
- [ ] `globalTransformation` is inside `targets[0]`, NOT at root
- [ ] `errorHandling` (if present) is inside `targets[0]`, NOT at root
- [ ] `deltaAutoloaderConfiguration` is present (default `[]`)
- [ ] `motsId` is a string value (quoted)
- [ ] `parameters` is present in `jdbcSource` (default `[]`)
- [ ] `saslMechanism` is present in `kafkaSource`
- [ ] `TERADATA` (not `TERRADATA`) if applicable
- [ ] `sourceFileFormat` is only present for file-based sources (not JDBC or Kafka)
- [ ] `writeOneFileInd` is `true` when source is JDBC and target is file-based (delta/parquet/csv); not applicable for other sources
- [ ] `vacuumDaysOld` is ONLY present when `targetFileFormat` is `"delta"` (NOT for parquet, csv, or database)
- [ ] All `@` required in email fields (`createdBy`, `sourceContact`)
- [ ] `targets` is an array `[...]`, not a bare object
- [ ] `targetLocation` starts with `abfss://`
- [ ] `filesRetentionDays` is set for file-based sources

4. **Run constitution compliance check** against all hard-stop rules (Sections I through VII):

**Root-level:** All mandatory fields present (incl. `deltaAutoloaderConfiguration`), emails contain `@`, feedType is valid, targets is array.
**Nesting:** `transformations`, `globalTransformation`, `errorHandling` are inside `targets[]`, NOT at root.
**Source-specific:** JDBC has connectionType + logon fields + sqlFileLocation + parameters. Kafka has servers + topic + group + logon + saslMechanism. File has location + format. DataRouter has subscriberId + feedId + filterRegex + fileActions.
**Schema:** Every column has name + valid type, no duplicates, decimal has precision/scale, partition columns have sequential partitionOrder.
**Target:** Location starts with `abfss://`, valid format + writeMode, upsert has PK/mergeKeys. `vacuumDaysOld` ONLY present when `targetFileFormat` is `"delta"`.
**Transformations:** hashingAndEncrypt has encryptIdentity + encryptFormat, dateFormat has sources or generatedValue, sourceColumns exist in schema.
**Validations:** regex has pattern, duplicateFileCheck has daysBack, sourceColumns exist in schema.
**Error handling:** moveToRejectInd=true requires sourceRejectLocation. errorHandling is inside targets[].
**Security:** No plaintext credentials anywhere.
**Data types:** `motsId` is string, `connectionType` uses `TERADATA` (not `TERRADATA`).

Report compliance result as a table. If any hard-stop violated, explain and suggest fix.

### 5. Post-Generation Recommendations

After generating the config inline, provide brief actionable recommendations:

- **Partition Strategy** — explain why the chosen partition column(s) were selected, estimate partition count
- **Write Mode Rationale** — explain implications (overwrite loses history, upsert requires PK, etc.)
- **Encryption** — list all PII columns and their protection method, if any
- **Performance** — suggest fetchSize/numPartitions adjustments for large JDBC tables, clusterSize for high volume
- **Next Steps** — how to deploy the config, test with a small dataset, set up monitoring

---

## Error Handling

**Hard-Stop Violations**: During the wizard, if any constitution hard-stop would be violated by the user's input, explain the rule immediately at that step and ask the user to provide a compliant value. Do NOT proceed to the next step until the violation is resolved.

**Environment Failure**: If the environment setup in Steps 0-1 fails, report missing configuration and suggest copying and filling `templates/env-config.yaml`.

**User Cancellation**: If the user says "cancel", "stop", or "quit" at any wizard step, confirm cancellation and summarize what was collected so far in case they want to resume later.

---

## Examples

These show what the user types to invoke the wizard. The wizard will then ask follow-up questions for anything not provided.

**Example 1: Minimal input (wizard asks everything)**
```
/scaffold-xflow-orchestrator
```
→ Wizard starts at Step 4a (Source Type) and walks through every step.

**Example 2: Partial input (wizard fills gaps)**
```
/scaffold-xflow-orchestrator Oracle table customers.orders to abfss://customers@datalakeeastus2prd.dfs.core.windows.net/orders. Columns: customer_id string, order_id string, order_type string.
```
→ Wizard skips source type (JDBC) and schema, but asks for: secret key, metadata fields, target write mode, transformations, validations, global transform, error handling.

**Example 3: Detailed input (wizard skips most steps)**
```
/scaffold-xflow-orchestrator JDBC Oracle source BILLING.CUSTOMERS to ADLS Delta.
Columns: customerId long pk, customerName string, email string, phone string.
Encrypt email and phone. Validate notNull on customerId. Standard error handling.
appId: crm, dataLibrary: DP-DLIB-Brws, rimPolicy: NET-440, motsId: "29010", createdBy: us2472@att.com
```
→ Wizard confirms inferred values at Step 4j (Review) and generates immediately.

**Example 4: Kafka minimal**
```
/scaffold-xflow-orchestrator Kafka topic customer_events
```
→ Wizard asks for: bootstrap servers, consumer group, schema, target location, and all remaining sections.

**Example 5: CSV with quality focus**
```
/scaffold-xflow-orchestrator CSV from abfss://raw@datalake.dfs.core.windows.net/billing/invoices. Has header, pipe-delimited.
```
→ Wizard asks for: schema, metadata, target, transformations, validations (where user can specify full data quality rules), error handling.

---

## References

- XFlow System Documentation: `XFlow_System_chunks.json` (43 field/source/transformation/validation/general entries)
- XFlow Pydantic Models: `xflow_models.py` (ColumnSchema, JDBCSource, KafkaSource, Source, Target, XFlowConfig)
- XFlow Transformations: `xflow_transformations.py` (16 transformation types)
- XFlow Validations: `xflow_validations.py` (17 validation types)
- Production Config Examples: `interactive_config_*.json`
- Constitution: `xflow-orchestrator-constitution.md` (hard-stop rules, mandatory patterns, preferred patterns, field reference)
