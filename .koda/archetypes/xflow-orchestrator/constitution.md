 # XFlow Orchestrator Constitution

## Purpose

This constitution defines the foundational principles and hard-stop rules for the XFlow Orchestrator archetype. It governs the generation, validation, refactoring, and management of XFlow JSON pipeline configurations used to ingest data from JDBC, Kafka, File, HTTP, and Azure Files sources into ADLS/Delta targets on Databricks.

---

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** output that violates these rules:

### Root-Level Structure
- ✘ **No missing mandatory root fields**: Every config must include `srcId`, `appId`, `createdBy`, `dataLibrary`, `rimPolicyName`, `sourceContact`, `motsId`, `source`, `targets`, and `deltaAutoloaderConfiguration` (default `[]`)
- ✘ **No targets as single object**: The `targets` field must always be a JSON array `[]`, never a single object `{}`
- ✘ **No invalid feedType**: `feedType` must be `"ING"` (ingestion) or `"MGR"` (migration) only
- ✘ **No invalid email fields**: `createdBy`, `sourceContact`, and `modifiedBy` must contain `@`

### Nesting Structure
- ✘ **No transformations at root level**: `transformations` must always be placed inside `targets[]` objects, never at the root level of the config
- ✘ **No globalTransformation at root level**: `globalTransformation` must always be placed inside `targets[]` objects, never at the root level
- ✘ **No errorHandling at root level**: `errorHandling` must always be placed inside `targets[]` objects as an `errorHandling` object containing `fileFailureThresholdPercentage`, optional `errorTableLocation`, optional `skipMalformedRecsInd`, and optional `onFailure`

### Credential Security
- ✘ **No plaintext credentials**: Do not embed passwords, connection strings, API keys, or tokens anywhere in config JSON
- ✘ **No credentials outside secret scopes**: All credentials must use Databricks secret scopes via `logonScopeName` + `logonSecretName`; never use environment variables or plain-text files
- ✘ **No decrypted data persistence**: Never configure a pipeline that decrypts sensitive data and writes it to ADLS; decryption must only occur in memory

### Schema Rules
- ✘ **No schema columns without name and type**: Every entry in a `schema` array must have both `columnName` (string) and `columnType` (valid Spark SQL type)
- ✘ **No invalid column types**: `columnType` must be one of: `string`, `int`, `integer`, `long`, `bigint`, `double`, `float`, `boolean`, `date`, `timestamp`, `decimal`, `binary`, `short`, `byte`
- ✘ **No duplicate column names**: Column names within a single schema array must be unique
- ✘ **No partition columns without partitionOrder**: Any column designated as a partition column in the target schema must have a `partitionOrder` integer value (sequential starting from 1)

### JDBC Source Rules
- ✘ **No JDBC without required fields**: A `jdbcSource` must include `connectionType`, `logonScopeName`, `logonSecretName`, `parameters` (default `[]`), and `sqlFileLocation` (path to SQL file in ADLS)
- ✘ **No invalid connectionType**: Must be one of: `ORACLE`, `SQL_SERVER`, `MY_SQL`, `VERTICA`, `TERADATA`, `SNOWFLAKE`, `TRINO`, `POSTGRESQL`, `GENERIC`
- ✘ **No Snowflake without extra fields**: If `connectionType` is `SNOWFLAKE`, config must also include `sfDatabaseName`, `sfSchemaName`, and `sfWarehouse`
- ✘ **No JDBC without driver fields for known types**: If `connectionType` is `ORACLE`, `SQL_SERVER`, `MY_SQL`, `VERTICA`, or `TERADATA`, the `jdbcSource` must include `driverLocation` and `driverClassName` with values matching the driver defaults in `env-config.yaml`

### Kafka Source Rules
- ✘ **No Kafka without required fields**: A `kafkaSource` must include `bootstrapServers`, `subscribe`, `groupId`, `logonScopeName`, `logonSecretName`, `saslMechanism` (default `"PLAIN"`), and `securityProtocol` (default `"SASL_SSL"`)
- ✘ **No Kafka without sourceFileFormat**: Kafka sources that parse messages into structured columns MUST include `sourceFileFormat` (e.g., `"csv"`, `"json"`, `"avro"`) in the source section. Omitting it causes silent API rejection
- ✘ **No kafkatext schema mismatch**: If `sourceFileFormat` is `"kafkatext"`, source and target schemas must only contain partition columns (the raw message is stored as-is). `targetFileFormat` must be `"csv"` (not `"text"` — the API rejects `"text"` as an invalid target format)
- ✘ **No Kafka continuous processing without explicit config**: Continuous processing Kafka feeds MUST include `jobConfiguration` with `jobInvocationConfig.continuousProcessing.activeInd: true`. Do NOT omit `jobConfiguration` entirely

### File Source Rules
- ✘ **No file source without location and format**: A file-based source must have `sourceLocation` and `sourceFileFormat`
- ✘ **No inaccessible sourceLocation**: `sourceLocation` must be an ADLS path (`abfss://`) under a container that is provisioned and accessible to the `appId`. The STL API validates container access at config submission time
- ✘ **No filesRetentionDays without sourceLocation**: `filesRetentionDays` must only be included when the source has a `sourceLocation`. Not applicable for Kafka sources without a staging location
- ✘ **No invalid sourceFileFormat**: Must be one of: `parquet`, `orc`, `avro`, `csv`, `fixed`, `xml`, `json`, `kafkatext`. This field is only applicable for file-based sources (not JDBC, Kafka, or database sources)
- ✘ **No sourceFileFormat for JDBC sources**: JDBC sources must not include `sourceFileFormat` field (Kafka sources MUST include it — see Kafka Source Rules)
- ✘ **No fixed-width without lengths**: If `sourceFileFormat` is `"fixed"`, `fixedLengthCounts` must be specified as a JSON array of integers (e.g., `[10, 20, 15]`), NOT a comma-separated string
- ✘ **No XML without row path**: If `sourceFileFormat` is `"xml"`, `xmlRowPath` must be specified

### HTTP/Azure Files Source Rules
- ✘ **No Azure Files without pull config**: An `azureFilesSource` must include `sourcePullConfig` with `azureFileShare` containing `fileShareName`, `accountName`, `sasTokenVaultName`, `sasTokenSecretKey`, and `resourcePath`

### Target Rules
- ✘ **No target without location**: Every target must have `targetLocation` starting with `abfss://`
- ✘ **No invalid writeMode**: Must be one of: `append`, `overwrite`, `overwritePartition`, `upsert`
- ✘ **No upsert without primary keys**: If `writeMode` is `"upsert"`, the target schema must contain at least one column with `pk: true` or `mergeKeys` must be specified
- ✘ **No overwritePartition without partitions**: If `writeMode` is `"overwritePartition"`, at least one schema column must have `partitionOrder`
- ✘ **No database target without config**: If `targetFileFormat` is `"database"`, a `databaseTarget` section must be present
- ✘ **No invalid targetFileFormat**: Must be one of: `parquet`, `csv`, `database` (case-insensitive matching accepted but lowercase recommended). For delta targets, do NOT set `targetFileFormat` — use `unityCatalog` instead
- ✘ **No delta without Unity Catalog**: Delta targets MUST include a `unityCatalog` object with `writeAsTableInd: true`, `catalogName`, and `schemaName`. When `unityCatalog` is present, `targetFileFormat` must be omitted (delta is implicit). This pattern is confirmed across all 64 Unity Catalog production configs
- ✘ **No vacuumDaysOld for non-delta targets**: `vacuumDaysOld` is only supported for delta targets (when `unityCatalog` is present). Must NOT be included for `parquet`, `csv`, or `database` targets

### Transformation Rules
- ✘ **No hashingAndEncrypt without encryption params**: Must include `encryptIdentity` and `encryptFormat` in `transformationParameters`
- ✘ **No dateFormat without format params**: Must include either `dateSourceFormats` (for conversion) or `generatedValue` (for generation like `SYSDATE`/`SYSDATETIME`)
- ✘ **No regex without pattern**: Must include `pattern` and `outputFormat` in `transformationParameters`
- ✘ **No replace without patterns**: Must include `removePatterns` and `replaceWith` in `transformationParameters`
- ✘ **No epochToTimestamp without unit**: Must include `sourceEpochUnit` (`"seconds"` or `"milliseconds"`)
- ✘ **No transformation referencing nonexistent columns**: `sourceColumns` in a transformation must exist in the source schema (except for `addColumn` type)

### Validation Rules
- ✘ **No regex validation without pattern**: A `regex` validation must include `pattern` in `validationParameters`
- ✘ **No duplicateFileCheck without daysBack**: Must include `daysBack` in `validationParameters`
- ✘ **No validation referencing nonexistent columns**: `sourceColumns` in a validation must exist in the schema

### Error Handling Rules
- ✘ **No moveToReject without location**: If `onFailure.moveToRejectInd` is `true`, `sourceRejectLocation` must be specified

---

## II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify these patterns:

### Structural
- ✔ **Valid JSON**: All generated configs must be syntactically valid JSON
- ✔ **Pydantic-compatible structure**: Config must pass structural checks for required fields, valid enums, and cross-field dependencies as defined in `xflow_models.py`

### Schema
- ✔ **Source schema required**: Every source must have a `schema` array with at least one column
- ✔ **Target schema required**: Every target must have a `schema` array
- ✔ **Schema consistency**: Target schema should contain all source columns plus any derived columns; source schema should not contain derived columns

### Target Configuration
- ✔ **Target error handling placement**: If `errorHandling` is needed, it must be placed inside the target object with `fileFailureThresholdPercentage` (default `0`), optional `errorTableLocation` (e.g., `abfss://{appId}-stg@{storageAccount}.dfs.core.windows.net/{srcId}_stlerror`), and optional `onFailure` sub-object
- ✔ **Write mode alignment**: `writeMode` must match the data pattern:
  - `append` — streaming, incremental loads, log data
  - `overwrite` — small dimension/lookup tables only
  - `overwritePartition` — daily/batch partition reloads
  - `upsert` — CDC, change data capture, row-level updates

### Column Types
- ✔ **Valid Spark SQL types**: All `columnType` values must be valid: `string`, `int`, `integer`, `long`, `bigint`, `double`, `float`, `boolean`, `date`, `timestamp`, `decimal`, `binary`, `short`, `byte`
- ✔ **Decimal precision**: If `columnType` is `decimal`, `precision` and `scale` should be specified

### Transformations
- ✔ **Derived column coverage**: Any column present in the target schema but absent from the source schema must have a corresponding entry in `transformations` with appropriate `addColumn`, `dateFormat` (with `generatedValue`), or other derivation logic
- ✔ **Encrypted column flag**: If a column has a `hashingAndEncrypt` transformation, the target schema column should have `"encrypted": true`
- ✔ **Transformation structure**: Each transformation must have `targetColumnName`, `sourceColumns` (array), and `transformationSteps` (array with at least one step containing `transformationType` and optionally `transformationParameters`, `description`, `onError`)

### Global Transformation
- ✔ **Default trimSpacesInd**: `globalTransformation.trimSpacesInd` should default to `false` unless explicitly overridden
- ✔ **globalTransformation placement**: `globalTransformation` must be placed inside the `targets[]` object, alongside `schema` and `transformations`

### Error Handling
- ✔ **onError for transformations**: Non-critical transformations should include `onError` with `failRecordInd` and `replaceFailedValueWith` settings
- ✔ **errorHandling placement**: `errorHandling` must be placed inside the `targets[]` object

---

## III. Preferred Patterns (Recommended)

The LLM **should adopt** these patterns unless user overrides:

### Target Defaults
- ◉ **Delta target format**: Default `targetFileFormat` to `"delta"` for ACID properties, time-travel, and schema evolution
- ◉ **Vacuum policy**: Include `vacuumDaysOld: 7` ONLY for Delta targets (`targetFileFormat: "delta"`) to manage storage. Do NOT include for parquet, csv, or database targets
- ◉ **Remove target metadata**: Set `removeTargetMetadataFilesInd: false` (default)

### Source Defaults
- ◉ **JDBC fetch size**: Set `fetchSize: 20000` for JDBC sources
- ◉ **JDBC driver auto-population**: When `connectionType` is selected, auto-populate `driverLocation` and `driverClassName` from `jdbc_driver_defaults` in `env-config.yaml`:
  - `ORACLE` → `ojdbc8.jar` / `oracle.jdbc.OracleDriver`
  - `SQL_SERVER` → `mssql-jdbc-8.2.2.jre8.jar` / `com.microsoft.sqlserver.jdbc.SQLServerDriver`
  - `MY_SQL` → `mssql-jdbc-8.2.2.jre8.jar` / `com.mysql.cj.jdbc.Driver`
  - `VERTICA` → `vertica-jdbc-9.2.1-0.jar` / `com.vertica.jdbc.Driver`
  - `TERADATA` → `terajdbc4.jar` / `com.ncr.teradata.TeraDriver`
- ◉ **JDBC parameters default**: Always include `"parameters": []` in `jdbcSource`. When the SQL query file has bind parameters, populate with `FETCH_ON_NULL` (first run) and `FETCH_ALWAYS` (subsequent runs) entries
- ◉ **CSV defaults**: Set `csvDelimiter: ","`, `csvIgnoreHeaderInd: false` for CSV sources
- ◉ **Kafka security**: Default `securityProtocol` to `"SASL_SSL"` for Kafka sources
- ◉ **Kafka rate limiting**: Include `maxOffsetsPerTrigger: 100000`, `maxBytesPerTrigger: 1000000000`, and `pollTimeoutMs: 120000` as defaults for Kafka sources
- ◉ **Kafka SASL**: Include `saslMechanism: "PLAIN"` for all Kafka sources
- ◉ **File retention**: Set `filesRetentionDays: 7` for ING feeds, `-1` for MGR feeds (user can override)
- ◉ **CSV source properties**: For CSV sources, optionally include `csvSourceProperties` object with keys: `delimiter`, `sep`, `quote`, `escape`, `escapeQuotes`, `header`, `multiLine`, `lineSep`, `emptyValue`
- ◉ **CSV ignore extra columns**: Set `csvIgnoreExtraColumnsInd: true` for CSV sources to handle trailing columns not in schema

### Global Transformation
- ◉ **Null standardization**: Include `replaceValues` to standardize null representations: `["", "NA", "NULL", "reserved:NULL"] → "Null"`
- ◉ **Quote removal**: For CSV sources, include `removeStartCharacters` and `removeEndCharacters` for quote marks

### Naming and Metadata
- ◉ **Descriptive naming**: Use `snake_case` for `srcId` values (e.g., `customer_orders`)
- ◉ **Feed type**: Default `feedType` to `"ING"`; use `"MGR"` only for migration feeds
- ◉ **Support team**: Default `supportTeam` to `"datalake"`

### Error Handling
- ◉ **Bad file tracking**: Set `onFailure.badFileInd: true` for debugging
- ◉ **Skip malformed**: Set `skipMalformedRecsInd: true` for file sources
- ◉ **Reject location**: Configure `sourceRejectLocation` for data quality monitoring
- ◉ **Error table location**: Set `errorTableLocation` in `errorHandling` to `abfss://{appId}-stg@{storageAccount}.dfs.core.windows.net/{srcId}_stlerror`
- ◉ **Control columns**: Include `controlColumns` with `fileNameColumnInd: true` and `creationTimestampColumnInd: true` on targets (recommended but not mandatory)

### Performance
- ◉ **Write one file**: Set `writeOneFileInd: true` for all JDBC sources
- ◉ **Cluster sizing**: Use `clusterSize: "low"` (1 workers) for small tables, `"medium"` (2 workers) for standard, `"high"` (5 workers) for large

### Target Configuration
- ◉ **CSV target properties**: For CSV targets, include `csvTargetProperties` object with keys: `sep`, `quote`, `escape`, `escapeQuotes`, `emptyValue`, `nullValue`, `lineSep`, `ignoreLeadingWhiteSpace`, `ignoreTrailingWhiteSpace`, `multiline`
- ◉ **Target file pattern**: For file-based sources (httpFileSource, azureFilesSource), include `targetFilePattern` (e.g., `"{SRC_FILE_NAME}.parquet"`, `"{SRC_FILE_NAME}_{UNIQUE_ID}.parquet"`)
- ◉ **Unity Catalog**: When `targetFileFormat` is `"delta"`, ask for `unityCatalog` configuration with `catalogName`, `schemaName`, and `writeAsTableInd: true`
- ◉ **Feed description**: Include `feedDescription` at root level for human-readable feed documentation

### Location Conventions
- ◉ **Consistent paths**: Use structure `abfss://{appId}@{storageAccount}.dfs.core.windows.net/{srcId}` for targets
- ◉ **Staging paths**: Use `abfss://staging@{storageAccount}.dfs.core.windows.net/{appId}/{srcId}` for sources

---

## IV. Complete Field Reference

### Root-Level Fields
| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `srcId` | ✔ | string | — | Unique source identifier |
| `appId` | ✔ | string | — | Application identifier |
| `createdBy` | ✔ | email | — | Creator email |
| `dataLibrary` | ✔ | string | — | Data library classification (e.g., `DP-DLIB-Brws`) |
| `rimPolicyName` | ✔ | string | — | RIM policy (e.g., `NET-440`) |
| `sourceContact` | ✔ | email | — | Source team contact |
| `motsId` | ✔ | string | — | MOTS identifier (always string, e.g., `"19062"`) |
| `supportTeam` | ➜ | string | `"datalake"` | Support team name |
| `feedType` | ➜ | enum | `"ING"` | `ING` or `MGR` |
| `bypassSoftlimit` | ➜ | bool | `false` | Bypass soft limits |
| `deltaAutoloaderConfiguration` | ✔ | array | `[]` | Delta autoloader settings (empty array if not used) |
| `feedDescription` | ➜ | string | — | Human-readable feed description |

### Source Types
| Source | Key Fields | Use Case |
|--------|-----------|----------|
| `jdbcSource` | connectionType, logonScopeName, logonSecretName, sqlFileLocation, driverLocation, driverClassName, parameters | Database extraction |
| `kafkaSource` | bootstrapServers, subscribe, groupId, securityProtocol, saslMechanism, logonScopeName, logonSecretName, maxOffsetsPerTrigger, maxBytesPerTrigger, pollTimeoutMs | Streaming ingestion |
| File (no wrapper) | sourceLocation, sourceFileFormat, schema | File-based ingestion |
| `httpFileSource` | subscriberId, feedId, filterBy, filterRegex, fileActions, tempDirInd, duplicateFileCheckInd, ruleId, destinationLocation, destinationType | HTTP push via DataRouter/FileGW |
| `azureFilesSource` | sourcePullConfig.azureFileShare.* | Azure File Share pull |

### Transformation Types
| Type | Required Params | Use Case |
|------|----------------|----------|
| `hashingAndEncrypt` | encryptIdentity, encryptFormat | PII protection via Voltage |
| `dateFormat` | dateSourceFormats OR generatedValue, dateTargetFormat | Date conversion/generation |
| `regex` | pattern, outputFormat | Pattern extraction |
| `replace` | removePatterns, replaceWith | Value substitution |
| `uppercase` | (none) | Case normalization |
| `lowercase` | (none) | Case normalization |
| `epochToTimestamp` | sourceEpochUnit, dateTargetFormat | Unix time conversion |
| `addColumn` | value | Derived column (constant, expression) |
| `concatenate` | delimiter | Column concatenation |
| `substring` | startPosition, length | String extraction |
| `cast` | targetType | Type conversion |

### Validation Types
| Type | Required Params | Use Case |
|------|----------------|----------|
| `schema` | validateDataTypes | Schema enforcement |
| `regex` | pattern, sourceColumns | Pattern validation |
| `duplicateFileCheck` | daysBack | Duplicate file detection |
| `notNull` | sourceColumns | Required field checks |
| `primaryKey` | sourceColumns | Uniqueness validation |
| `notEmpty` | sourceColumns | Empty string checks |
| `numericRange` | minValue, maxValue | Range validation |
| `length` | minLength, maxLength | String length checks |
| `allowedValues` | allowedValues | Enum validation |
| `dateFormat` | dateFormat | Date format validation |
| `dateRange` | minDate, maxDate | Date range checks |
| `email` | sourceColumns | Email format validation |
| `unique` | sourceColumns, scope | Uniqueness checks |
| `foreignKey` | referenceTable, referenceColumns | Referential integrity |
| `count` | minCount, maxCount | Record count validation |
| `duplicateCount` | columns, maxDuplicates | Duplicate record checks |

---

## V. Job Configuration Reference

### jobConfiguration
Present in 61% of production configs. Controls scheduling, cluster sizing, and init scripts.

| Field Path | Description |
|------------|-------------|
| `jobConfiguration.jobInvocationConfig.schedule.type` | Schedule type (always `"databricks"`) |
| `jobConfiguration.jobInvocationConfig.schedule.cronSchedule` | Cron expression (e.g., `"0 0 1/1 * * ?"`) |
| `jobConfiguration.jobInvocationConfig.schedule.timeZone` | Time zone (default `"UTC"`) |
| `jobConfiguration.jobInvocationConfig.continuousProcessing.activeInd` | Enable continuous processing |
| `jobConfiguration.jobInvocationConfig.continuousProcessing.checkTimePattern` | Check time pattern |
| `jobConfiguration.clusterConfiguration.numWorkers` | Number of workers |
| `jobConfiguration.clusterConfiguration.nodeTypeId` | Node type |
| `jobConfiguration.clusterConfiguration.initScripts` | Init scripts array |
| `jobConfiguration.clusterConfiguration.sparkConf` | Spark configuration overrides |

**Source-type logic for jobConfiguration:**
- **adlsPath (file) source**: Ask user if they want scheduled or continuous mode. If continuous, include `jobConfiguration` with `continuousProcessing.activeInd: true` (do NOT omit `jobConfiguration`).
- **JDBC source**: Always ask for cron schedule.
- **Kafka source**: Always ask for cron schedule (typically `"0 0 1/1 * * ?"` for hourly). Include `clusterConfiguration.initScripts` with kafka init script. For continuous mode, include `continuousProcessing.activeInd: true` instead of schedule.
- **httpFileSource / azureFilesSource**: Always ask for cron schedule.

---

## VI. httpFileSource / DataRouter Field Reference

Applicable only when source is DataRouter. If not DataRouter, ignore this section.

### httpFileSource Fields
| Field | Required | Description |
|-------|----------|-------------|
| `subscriberId` | ✔ | Subscriber identifier |
| `feedId` | ✔ | Feed identifier |
| `filterBy` | ✔ | Filter type (always `"FILE_NAME"`) |
| `filterRegex` | ✔ | Regex to match incoming files |
| `tempDirInd` | ✔ | Use temp directory (default `false`) |
| `tempFileRetentionHours` | ➜ | Hours to retain temp files (default `0`) |
| `duplicateFileCheckInd` | ✔ | Check for duplicate files |
| `ruleId` | ➜ | Routing rule identifier |
| `destinationLocation` | ➜ | File destination path |
| `destinationType` | ➜ | Destination type |
| `fileActions` | ✔ | Array of file processing actions |

### fileActions Types
| Action Type | Parameters | Description |
|-------------|------------|-------------|
| `DEST_PARTITIONING` | `partitions[].source`, `partitions[].partitionName`, `partitions[].partitionOrder`, `partitions[].partitionValueRegex`, `partitions[].sourceDateFormat`, `partitions[].targetDateFormat` | Partition target by filename regex |
| `DEST_FILE_PATTERN` | `sourceFileNameRegex`, `targetFileNamePattern` | Control target file naming |
| `EXTRACT_HEADER_TRAILER` | `headerLineCount`, `trailerLineCount`, `excludeEmptyLine`, `removeHeaderTrailerInd` | Remove header/trailer lines |
| `RECORD_COUNT_VALIDATION` | `offset`, `source`, `countRegex`, `actionOnFailure` | Validate row count from trailer |
| `COMPRESSION` | `decompressInd`, `openArchiveInd`, `compressionArchiveMethod` | Handle compressed files (gzip, zip) |
| `CLEANSE` | `cleansePatterns[].removePattern`, `cleansePatterns[].replaceWith` | Data cleansing patterns |
| `OPEN_ARCHIVE` | `archiveMethod`, `archiveFilterBy`, `archiveFilterRegex` | Extract files from archives |
| `EMPTY_FILE_VALIDATION` | `onEmpty` | Handle empty files |
| `CREATE_AUDIT` | `auditFileContentConfiguration.*` | Generate audit files |

---

## VII. JDBC Parameters Reference

Every `jdbcSource` must include a `parameters` array (default `[]`). When the SQL query file contains bind parameters, populate with parameter entries.

### Parameter Fields
| Field | Type | Description |
|-------|------|-------------|
| `index` | int | Parameter position (1-based) |
| `sourceType` | string | Always `"SQL"` |
| `source` | string | SQL query to fetch the parameter value |
| `outputType` | string | Output type (e.g., `"STRING"`) |
| `fetchParameterType` | enum | `"FETCH_ON_NULL"` (first run only) or `"FETCH_ALWAYS"` (every run) |
| `saveValueFromIndex` | int | Index of another parameter whose value to save for subsequent runs |

### Example
```json
"parameters": [
  {
    "index": 1,
    "sourceType": "SQL",
    "source": "select TO_CHAR(to_date(TO_DATE(SUBSTR(MAX(BATCH_ID),1,8),'YYYYMMDD') - INTERVAL '1' DAY),'yyyymmdd') || 999 AS RESULT1 FROM schema.TABLE_NAME WHERE lower(TABLE_NAME) = 'my_table'",
    "outputType": "STRING",
    "fetchParameterType": "FETCH_ON_NULL",
    "saveValueFromIndex": 2
  },
  {
    "index": 2,
    "sourceType": "SQL",
    "source": "select MAX(BATCH_ID) AS RESULT2 FROM schema.TABLE_NAME WHERE lower(TABLE_NAME) = 'my_table'",
    "outputType": "STRING",
    "fetchParameterType": "FETCH_ALWAYS"
  }
]
```

`FETCH_ON_NULL`: Runs the SQL only when no cached value exists (i.e., the very first execution).
`FETCH_ALWAYS`: Runs the SQL on every job invocation to get the latest value.

---

## VIII. Workflow Execution Discipline

All XFlow Orchestrator workflows (scaffold, compare, debug, document, refactor, test) **must** follow these execution rules. The LLM **must refuse** to deviate from them:

### Interactive Question Rules
- ✘ **No batching questions**: Each interactive question MUST be its own separate `ask_user_question` call. NEVER combine multiple questions into a single prompt
- ✘ **No skipping steps**: Every interactive step defined in a workflow MUST be executed in order. The ONLY exception is when the user already provided the information in the initial arguments
- ✘ **No assumed defaults for interactive steps**: Do not assume a default and skip an interactive step. If the workflow says to ASK the user, the user MUST be asked — even if the likely answer is "none" or "skip"
- ✘ **No premature output**: NEVER generate final output (JSON config, test suite, documentation, comparison matrix, fix application) before all required interactive inputs have been collected

### Sequential Execution Rules
- ✔ **Wait for response**: After each `ask_user_question`, WAIT for the user's response before proceeding to the next step
- ✔ **One step at a time**: Process steps sequentially — do not look ahead or combine future steps
- ✔ **Mandatory stops**: In the scaffold workflow, Steps 4f (Transformations), 4g (Validations), 4h (Global Transformation), and 4i (Error Handling) are MANDATORY wizard stops — the user must be asked even if they choose "skip/none"
- ✔ **Review-each discipline**: When a user selects "Review each fix/change" in debug or refactor workflows, present EACH fix individually with its own `ask_user_question` call — never batch multiple fixes

### Output Rules
- ✔ **Inline by default**: Generate output (JSON, markdown, test suites) inline as fenced code blocks in chat unless the user explicitly requests file creation
- ✔ **No file writes without consent**: Do NOT save generated configs, documentation, or test files to disk unless the user explicitly asks

---

**Version**: 3.2.0
**Last Updated**: 2026-03-02
