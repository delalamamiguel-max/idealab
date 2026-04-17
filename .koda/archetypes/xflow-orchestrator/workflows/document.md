---
description: Generate comprehensive documentation for XFlow JSON configurations (XFlow Orchestrator)
---

User input: $ARGUMENTS

## Execution Steps

## Execution Rules (NON-NEGOTIABLE)

**These rules govern HOW this workflow executes. Violating them is a hard-stop.**

1. **ONE question per message.** Each interactive question MUST be its own separate `ask_user_question` call. NEVER combine multiple questions into a single prompt.
2. **NO skipping steps.** Every interactive question in Step 3b MUST be asked in order. The ONLY exception is when the user already provided the information in $ARGUMENTS.
3. **WAIT for user response** before proceeding to the next question. Do not assume defaults unless the workflow explicitly says to apply a default silently.
4. **NEVER generate documentation before collecting all required input.** If audience, scope, or format is unclear, ASK before generating.

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
- **Config file path**: path to the XFlow JSON config to document — read and parse the file completely
- **Target audience** (determines depth and terminology):
  - `developer` — technical detail, config field explanations, code-level references
  - `operations` — deployment, monitoring, troubleshooting, runbook focus
  - `data-steward` — data lineage, schema, PII, compliance, data quality focus
  - `management` — executive summary, data flow, SLA, cost, risk
  - `all` — comprehensive documentation for all audiences (default)
- **Documentation scope** (one or more):
  - `full` — all 12 sections (default)
  - `overview` — pipeline identity and data flow only
  - `schema` — schema reference with column details
  - `transformations` — transformation guide with business logic
  - `validations` — validation rules and data quality
  - `runbook` — operational runbook with deployment and troubleshooting
  - `security` — PII handling, encryption, compliance
  - `lineage` — data lineage from source to target
  - `changelog` — document changes between two config versions
- **Output format**: Markdown (default), Confluence wiki, or JIRA-compatible
- **Second config file**: if `changelog` scope, provide the previous version for diff

If a config file is referenced, read and parse it. Request clarification if no config file is provided.

### 3b. Interactive Documentation Setup

**If audience, scope, or format is not specified in $ARGUMENTS, ASK these questions:**

**Question 1 — Target Audience:**
> Who is the target audience for this documentation?
> - **Developer** — technical details, config field explanations, code references
> - **Operations** — deployment, monitoring, troubleshooting, runbook
> - **Data steward** — lineage, schema, PII, compliance, data quality
> - **All audiences** — comprehensive documentation for everyone

Use `ask_user_question` with these 4 options.

<!-- HALT: Wait for user response before continuing to Question 2 -->

**Question 2 — Documentation Scope:**
> What scope of documentation do you need?
> - **Full** — all 12 sections (pipeline identity, source, target, schema, transformations, validations, security, lineage, runbook, etc.)
> - **Overview** — pipeline identity + source/target summary only
> - **Runbook** — operational guide with deployment, monitoring, and troubleshooting
> - **Schema + Lineage** — schema reference, column details, and data lineage

Use `ask_user_question` with these 4 options.

<!-- HALT: Wait for user response before continuing to Question 3 -->

**Question 3 — Output Format:**
> What output format?
> - **Markdown** (default) — standard markdown document
> - **Confluence** — Confluence wiki format with macros
> - **Inline** — output directly in chat

Use `ask_user_question` with these 3 options.

<!-- HALT: Wait for user response before continuing to Step 4 -->

### 4. Analyze Config Structure

**Parse the XFlow JSON config and extract EVERY detail for documentation:**

---

**4a. Pipeline Identity:**

| Field | Value | Documentation Purpose |
|-------|-------|----------------------|
| `srcId` | Source identifier | Pipeline name, used in titles and references |
| `appId` | Application ID | Application context, ADLS path component |
| `createdBy` | Creator email | Owner, contact for questions |
| `feedType` | ING or MGR | Feed classification (ingestion vs migration) |
| `dataLibrary` | Data library code | Data classification, governance tier |
| `rimPolicyName` | RIM policy | Retention and information management policy |
| `motsId` | MOTS ID | Application registry identifier |
| `supportTeam` | Support team name | Operational support contact |
| `sourceContact` | Source team email | Data source team contact |
| `bypassSoftlimit` | Boolean | Whether soft limits are bypassed |
| `createdDate` | Date | When config was created |
| `modifiedBy` | Email | Last modifier |
| `modifiedDate` | Date | Last modification date |

---

**4b. Source Configuration Analysis:**

**For JDBC Sources:**
| Field | Value | Documentation |
|-------|-------|---------------|
| `connectionType` | ORACLE/SQL_SERVER/etc. | Database platform |
| `logonScopeName` | Secret scope name | Authentication method (document scope, NOT secret) |
| `logonSecretName` | Secret key name | Credential reference (document key name, NOT value) |
| `sqlFileLocation` | ADLS path | SQL file location in ADLS (mandatory for all JDBC sources) |
| `fetchSize` | Integer | Rows per batch (performance tuning) |
| `numPartitions` | Integer | Parallel extraction threads |
| `dbTablePartitioning` | Object | Parallel read configuration |
| Snowflake: `sfDatabaseName`, `sfSchemaName`, `sfWarehouse` | Strings | Snowflake-specific connection details |

**For Kafka Sources:**
| Field | Value | Documentation |
|-------|-------|---------------|
| `bootstrapServers` | Broker addresses | Kafka cluster endpoints |
| `subscribe` | Topic name | Kafka topic being consumed |
| `groupId` | Consumer group | Consumer group for offset management |
| `securityProtocol` | SASL_SSL/etc. | Security protocol |
| `saslMechanism` | PLAIN/etc. | SASL mechanism |
| `startingOffsets` | latest/earliest | Initial offset strategy |
| `maxOffsetsPerTrigger` | Integer | Rate limiting |
| `failOnDataLoss` | Boolean | Data loss handling |
| `pollTimeoutMs` | Integer | Poll timeout |

**For File Sources:**
| Field | Value | Documentation |
|-------|-------|---------------|
| `sourceLocation` | ADLS path | File source location |
| `sourceFileFormat` | csv/parquet/json/etc. | File format |
| `csvDelimiter` | Character | CSV delimiter |
| `csvIgnoreHeaderInd` | Boolean | Header handling |
| `csvIgnoreExtraColumnsInd` | Boolean | Extra column handling |
| `jsonMultiline` | Boolean | Multi-line JSON handling |
| `xmlRowPath` | XPath | XML row path |
| `fixedLengthCounts` | Array | Fixed-width column lengths |
| `fileRetentionDays` | Integer | File retention period |
| `fileEncryption` | Object | File-level encryption |
| `fileCompression` | String | File compression type |

**For HTTP File Sources:**
| Field | Value | Documentation |
|-------|-------|---------------|
| `feedId` | String | FileGW feed identifier |
| `filterBy` | FILE_NAME/etc. | File filter method |
| `filterRegex` | Pattern | File name filter pattern |
| `fileActions` | Array | File processing actions (document each action type and parameters) |
| `writeEmptyFileOnTargetInd` | Boolean | Empty file handling |
| `tempDirInd` | Boolean | Temporary directory usage |
| `duplicateFileCheckInd` | Boolean | Duplicate file detection |

**For Azure Files Sources:**
| Field | Value | Documentation |
|-------|-------|---------------|
| `sourcePullConfig.pullFrequencyMin` | Integer | Pull frequency in minutes |
| `sourcePullConfig.startWindowHrs` | Time | Pull window start |
| `sourcePullConfig.endWindowHrs` | Time | Pull window end |
| `azureFileShare.fileShareName` | String | Azure File Share name |
| `azureFileShare.accountName` | String | Storage account |
| `azureFileShare.resourcePath` | String | File path within share |

---

**4c. Schema Analysis:**

For EACH column in source and target schemas, extract:
| Attribute | Source | Target | Notes |
|-----------|--------|--------|-------|
| `columnName` | Name | Name | Note if renamed (e.g., email → email_encrypted) |
| `columnType` | Type | Type | Note if type changed (e.g., string → date) |
| `pk` | Boolean | Boolean | Primary key indicator |
| `precision` | Integer | Integer | Decimal precision |
| `scale` | Integer | Integer | Decimal scale |
| `partitionOrder` | — | Integer | Partition column order |
| `encrypted` | — | Boolean | Encryption flag |
| Derived? | — | Yes/No | Whether column exists only in target |
| Transformation | — | Type | What transformation produces this column |

---

**4d. Target Configuration Analysis:**

For EACH target:
| Field | Value | Documentation |
|-------|-------|---------------|
| `targetLocation` | ADLS URI | Where data is written |
| `targetFileFormat` | delta/parquet/csv/database | Output format |
| `writeMode` | append/overwrite/overwritePartition/upsert | Write strategy |
| `overwriteType` | DEFAULT/DYNAMIC | Overwrite behavior |
| `vacuumDaysOld` | Integer | Data retention (Delta) |
| `writeOneFileInd` | Boolean | Single file output (true for JDBC sources and file as target, not applicable for other sources) |
| `processOneFileInd` | Boolean | Single file processing |
| `controlColumns` | Object | Lineage columns |
| `mergeKeys` | Array | Upsert merge keys |
| `partitionBy` | Array | Partition columns |
| `databaseTarget` | Object | Database target config (if applicable) |

---

**4e. Transformation Analysis:**

For EACH transformation:
| Attribute | Value | Documentation |
|-----------|-------|---------------|
| `targetColumnName` | Column name | Output column |
| `sourceColumns` | Array | Input column(s) |
| `transformationType` | Type name | What it does |
| `transformationParameters` | Object | Configuration details |
| `description` | String | Business purpose |
| `onError` | Object | Error handling strategy |
| Business justification | Inferred | Why this transformation exists |

Document each transformation type with plain-language explanation:
- `hashingAndEncrypt` → "Encrypts {column} using Voltage with identity {encryptIdentity} and format {encryptFormat} for PII protection"
- `dateFormat` (conversion) → "Converts {column} from {dateSourceFormats} to {dateTargetFormat}"
- `dateFormat` (generation) → "Generates {column} using {generatedValue} in format {dateTargetFormat}"
- `regex` → "Extracts pattern {pattern} from {column} and reformats as {outputFormat}"
- `replace` → "Replaces values matching {removePatterns} with {replaceWith} in {column}"
- `uppercase`/`lowercase` → "Normalizes {column} to {upper/lower}case"
- `epochToTimestamp` → "Converts Unix {sourceEpochUnit} timestamp in {column} to {dateTargetFormat}"
- `addColumn` → "Adds derived column {column} with value {value}"
- `concatenate` → "Concatenates {sourceColumns} with delimiter '{delimiter}' into {column}"
- `substring` → "Extracts characters {startPosition} to {startPosition+length} from {column}"
- `cast` → "Casts {column} from {sourceType} to {targetType}"

---

**4f. Validation Analysis:**

For EACH validation:
| Attribute | Value | Documentation |
|-----------|-------|---------------|
| `validationType` | Type name | What it checks |
| `sourceColumns` | Array | Columns validated |
| `validationParameters` | Object | Check parameters |
| `failureAction` | fail/warn/skip | What happens on failure |
| Business purpose | Inferred | Why this validation exists |

Document each validation type with plain-language explanation:
- `notNull` → "Ensures {columns} are not null — {failureAction} if violated"
- `primaryKey` → "Ensures {columns} are unique (primary key constraint)"
- `schema` → "Validates data types match expected schema"
- `regex` → "Validates {columns} match pattern {pattern}"
- `duplicateFileCheck` → "Checks for duplicate files within last {daysBack} days"
- `numericRange` → "Validates {columns} are between {minValue} and {maxValue}"
- `allowedValues` → "Validates {columns} contain only {allowedValues}"
- `email` → "Validates {columns} are valid email format"
- `length` → "Validates {columns} string length between {minLength} and {maxLength}"
- `dateFormat` → "Validates {columns} match date format {dateFormat}"
- `dateRange` → "Validates {columns} are between {minDate} and {maxDate}"
- `unique` → "Validates {columns} are unique at {scope} level"
- `foreignKey` → "Validates {columns} exist in {referenceTable}.{referenceColumns}"
- `count` → "Validates record count between {minCount} and {maxCount}"
- `duplicateCount` → "Validates {columns} have at most {maxDuplicates} duplicates"

---

**4g. Global Transformation Analysis:**

| Setting | Value | Documentation |
|---------|-------|---------------|
| `trimSpacesInd` | Boolean | Whether leading/trailing spaces are removed from all columns |
| `removeStartCharacters` | String | Characters stripped from start of all values |
| `removeEndCharacters` | String | Characters stripped from end of all values |
| `replaceValues` | Array | Value replacement rules (null standardization) |

For each replaceValues entry:
- "Values {existingValues} are replaced with {newValue} across all columns"

---

**4h. Error Handling Analysis:**

| Setting | Value | Documentation |
|---------|-------|---------------|
| `fileFailureThresholdPercentage` | Integer | Maximum allowed failure percentage (0 = fail on any error) |
| `skipMalformedRecsInd` | Boolean | Whether malformed records are skipped |
| `sourceRejectLocation` | ADLS path | Where rejected records are stored |
| `errorTableLocation` | ADLS path | Where error details are logged |
| `onFailure.moveToRejectInd` | Boolean | Whether failed files are moved to reject location |
| `onFailure.tagObjectInd` | Boolean | Whether failed objects are tagged |
| `onFailure.badFileInd` | Boolean | Whether bad file is created for debugging |
| `onFailure.retryFileInd` | Boolean | Whether failed files are retried |

---

**4i. Constitution Compliance Check:**

Run the config against ALL constitution hard-stop rules and report:
- Total hard-stop rules checked
- Rules passed / failed
- Any violations found (with fix suggestions)
- Mandatory patterns present / missing
- Preferred patterns adopted / skipped

### 5. Generate Documentation

**Generate the complete documentation as a Markdown document with the following 12 sections:**

---

**Section 1 — Executive Summary**
```markdown
# {srcId} — XFlow Pipeline Documentation

## Executive Summary

| Attribute | Value |
|-----------|-------|
| **Pipeline ID** | {srcId} |
| **Application** | {appId} |
| **Owner** | {createdBy} |
| **Source** | {source_type}: {source_detail} |
| **Target** | {target_format} at {target_location} |
| **Write Mode** | {writeMode} |
| **Columns** | {source_count} source → {target_count} target |
| **Transformations** | {transform_count} ({transform_types}) |
| **Validations** | {validation_count} ({validation_types}) |
| **PII Columns** | {pii_count} encrypted |
| **Feed Type** | {feedType} |
| **Data Library** | {dataLibrary} |
| **RIM Policy** | {rimPolicyName} |
| **MOTS ID** | {motsId} |
| **Last Updated** | {modifiedDate or createdDate} |
```

---

**Section 2 — Data Flow Diagram**
```markdown
## Data Flow

┌─────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   SOURCE    │───▶│ TRANSFORMATIONS  │───▶│     TARGET      │
│ {src_type}  │    │ {transform_list} │    │ {target_format} │
│ {src_detail}│    │                  │    │ {target_loc}    │
└─────────────┘    └──────────────────┘    └─────────────────┘
                          │
                   ┌──────┴──────┐
                   │ VALIDATIONS │
                   │ {valid_list}│
                   └─────────────┘

Global: trimSpaces={trimSpacesInd}, nullStandardization={has_replaceValues}
```

---

**Section 3 — Source Configuration**

Full source details with all fields documented. Include:
- Connection method and authentication (scope names only, never secrets)
- Table/topic/file details
- Performance settings (fetchSize, numPartitions, etc.)
- Source-specific configuration

---

**Section 4 — Schema Reference**

```markdown
## Schema Reference

### Source Schema ({source_column_count} columns)

| # | Column Name | Type | PK | Precision | Scale | Notes |
|---|-------------|------|-----|-----------|-------|-------|
| 1 | customer_id | long | ✔ | — | — | Primary key |
| 2 | email | string | — | — | — | PII - encrypted in target |
...

### Target Schema ({target_column_count} columns)

| # | Column Name | Type | PK | Partition | Encrypted | Derived | Source Column | Transformation |
|---|-------------|------|-----|-----------|-----------|---------|---------------|----------------|
| 1 | customer_id | long | ✔ | — | — | — | customer_id | (passthrough) |
| 2 | email_encrypted | string | — | — | ✔ | — | email | hashingAndEncrypt |
| 3 | data_dt | string | — | 1 | — | ✔ | — | dateFormat (SYSDATE) |
...

### Schema Diff (Source → Target)

- **Passthrough columns**: {list of unchanged columns}
- **Renamed columns**: {list of renamed columns with old → new}
- **Type-changed columns**: {list with old type → new type}
- **Derived columns**: {list of columns only in target}
- **Dropped columns**: {list of columns only in source}
- **Encrypted columns**: {list of encrypted columns}
- **Partition columns**: {list with partitionOrder}
```

---

**Section 5 — Target Configuration**

Full target details for each target. Include:
- Target location and format
- Write mode with rationale
- Partition strategy with column order
- Control columns
- Compression and storage settings
- Merge keys (if upsert)
- Database target details (if applicable)

---

**Section 6 — Transformations Guide**

For each transformation, generate:
```markdown
### Transformation: {targetColumnName}

- **Source**: {sourceColumns}
- **Type**: {transformationType}
- **Description**: {description or generated plain-language explanation}
- **Parameters**:
  - {param1}: {value1}
  - {param2}: {value2}
- **Error Handling**: {onError description}
- **Business Purpose**: {inferred or provided justification}
```

---

**Section 7 — Validations Guide**

For each validation:
```markdown
### Validation: {validationType} on {sourceColumns}

- **Purpose**: {plain-language explanation}
- **Columns**: {sourceColumns}
- **Parameters**: {validationParameters}
- **On Failure**: {failureAction} — {impact description}
```

---

**Section 8 — Global Transformations**

Document all global transformation settings with their impact on data.

---

**Section 9 — Error Handling & Recovery**

Document complete error handling configuration:
- Failure threshold and behavior
- Reject file handling
- Bad file creation
- Retry logic
- Recovery procedures

---

**Section 10 — Security & Compliance**

```markdown
## Security & Compliance

### Data Classification
- **Data Library**: {dataLibrary}
- **RIM Policy**: {rimPolicyName}
- **Feed Type**: {feedType}

### PII Protection
| Column | Source Name | Target Name | Encryption Type | Identity | Format |
|--------|-----------|-------------|----------------|----------|--------|
| 1 | email | email_encrypted | hashingAndEncrypt | DL_IDENTITY@ATT.COM | ALPHA_NUM |
...

### Credential Management
- **Secret Scope**: {logonScopeName} (Azure KeyVault)
- **Secret Key**: {logonSecretName} (reference only — no actual secrets in documentation)
- **Authentication**: {connectionType}-specific via Databricks secret scope

### Constitution Compliance
- Hard-stop rules: {passed}/{total} PASS
- Mandatory patterns: {passed}/{total} PASS
- Preferred patterns: {adopted}/{total} adopted
- Violations: {list or "None"}
```

---

**Section 11 — Operational Runbook**

```markdown
## Operational Runbook

### Deployment
1. Validate config: `/test-xflow-orchestrator {config_file}`
2. Deploy to XFlow: {deployment steps}
3. Verify job creation in Databricks workspace
4. Run initial test with limited data

### Monitoring Checklist
- [ ] Job completes within expected time ({maxJobRunningTimeMin} min)
- [ ] Record count matches expected range
- [ ] No validation failures in logs
- [ ] Target data is queryable and correct
- [ ] Partition structure is correct
- [ ] Encrypted columns are properly encrypted

### Common Failure Scenarios

| Scenario | Symptoms | Root Cause | Resolution |
|----------|----------|------------|------------|
| Connection timeout | Job fails at source read | Database unavailable or fetchSize too large | Check DB status, reduce fetchSize |
| Schema mismatch | Job fails at write | Source schema changed | Update source and target schemas |
| Encryption failure | Voltage errors | Wrong encryptIdentity or scope | Verify Voltage config |
| Duplicate files | duplicateFileCheck fails | Same file processed twice | Check file delivery, increase daysBack |
| Partition error | overwritePartition fails | Missing partitionOrder | Add partitionOrder to partition columns |
| OOM error | Executor out of memory | Data too large for cluster | Increase clusterSize or add numPartitions |

### Rollback Procedures
1. If Delta target: Use time-travel to restore previous version
2. If Parquet target: Restore from backup or re-run with previous config
3. If upsert: Merge keys ensure idempotency — safe to re-run

### Contacts
- **Pipeline Owner**: {createdBy}
- **Source Team**: {sourceContact}
- **Support Team**: {supportTeam}
- **MOTS ID**: {motsId}
```

---

**Section 12 — Data Lineage**

```markdown
## Data Lineage

### Source-to-Target Column Mapping

{source_type}:{source_detail}
    │
    ├── customer_id (long) ──────────────────────▶ customer_id (long) [PK]
    ├── email (string) ──── hashingAndEncrypt ───▶ email_encrypted (string) [Encrypted]
    ├── phone (string) ──── hashingAndEncrypt ───▶ phone_encrypted (string) [Encrypted]
    ├── created_date (timestamp) ────────────────▶ created_date (timestamp)
    ├── (generated) ──────── dateFormat(SYSDATE) ▶ data_dt (string) [Partition 1]
    └── (generated) ──────── dateFormat(SYSDATETIME) ▶ load_timestamp (timestamp)

### Data Quality Gates

Source Data → [Global Transform: trim, null standardize] → [Validations: {list}] → [Column Transforms] → Target
```

### 6. Add Recommendations

**Documentation Maintenance:**
- When to update: on any config change, schema change, or transformation change
- Who owns it: {createdBy} or designated documentation owner
- Review cadence: quarterly or on major changes

**Missing Documentation:**
- Flag sections that need business input (transformation rationale, SLA requirements, data dictionary)
- Provide placeholder text for missing business context

**Config Improvements Found:**
- List any constitution violations or missing patterns discovered during documentation
- Suggest running `/refactor-xflow-orchestrator` for improvements

**Monitoring & Alerting:**
- Recommend alerting on job failures, validation failures, and SLA breaches
- Suggest monitoring dashboard for record counts, job duration, error rates

### 7. Validate and Report

// turbo

Generate documentation as Markdown file. Report completion with:
- Sections generated (list of 12)
- Config summary (source type, target format, column count, transformation count, validation count)
- Constitution compliance status
- Any issues found during analysis
- Recommended follow-up actions

## Error Handling

**Insufficient Context**: Request:
1. Config file path
2. Target audience (developer/operations/data-steward/management/all)
3. Documentation scope (full/overview/schema/transformations/validations/runbook/security/lineage)

**Complex Multi-Target Config**: Generate separate target sections for each target, with shared source and transformation sections.

**Missing Business Context**: Flag sections needing business input with `[TODO: Business input needed]` placeholders:
- Transformation business justification
- SLA requirements
- Data dictionary descriptions
- Downstream consumer list

**Changelog Scope**: If comparing two config versions:
1. Read both configs
2. Diff every section (root metadata, source, schema, target, transformations, validations, globalTransformation, error handling)
3. Generate changelog with: field path, old value, new value, impact assessment

## Examples

**Example 1: Full Pipeline Documentation**
```
/document-xflow-orchestrator full — Generate complete documentation for customer_pipeline.json

Output: 12-section Markdown document (25+ pages)
- Executive summary with pipeline identity
- Data flow diagram
- Source: JDBC Oracle BILLING.CUSTOMERS
- Schema: 6 source → 8 target columns (2 encrypted, 2 derived)
- Target: Delta at abfss://crm@storage/customer_orders
- 4 transformations (2 hashingAndEncrypt, 2 dateFormat)
- 4 validations (notNull, primaryKey, email, numericRange)
- Global: trim spaces, null standardization
- Error handling: 5% threshold, bad file tracking
- Security: 2 PII columns encrypted, RIM policy NET-440
- Runbook: deployment, monitoring, failure scenarios
- Lineage: source-to-target column mapping
```

**Example 2: Operational Runbook Only**
```
/document-xflow-orchestrator runbook — Create operational runbook for billing_ingestion.json
Audience: operations

Output: Focused runbook with:
- Deployment steps (validate → deploy → verify → test)
- Monitoring checklist (8 items)
- 6 common failure scenarios with resolution
- Rollback procedures (Delta time-travel)
- Contact information
```

**Example 3: Schema Reference for Data Stewards**
```
/document-xflow-orchestrator schema — Document schema for orders_config.json
Audience: data-steward

Output: Detailed schema reference with:
- Source schema table (12 columns with types, PK, notes)
- Target schema table (15 columns with types, PK, partition, encrypted, derived)
- Schema diff (3 derived columns, 2 encrypted, 1 type change)
- Column-level data lineage
```

**Example 4: Security & Compliance Documentation**
```
/document-xflow-orchestrator security — Document PII handling for sensitive_data_pipeline.json
Audience: data-steward

Output: Security-focused document with:
- Data classification (dataLibrary, rimPolicyName)
- PII column inventory (5 columns: email, phone, SSN, name, address)
- Encryption details per column (identity, format, padding)
- Secret scope configuration
- Constitution compliance check (all hard-stop rules PASS)
```

**Example 5: Changelog Between Versions**
```
/document-xflow-orchestrator changelog — Compare customer_v1.json vs customer_v2.json

Output: Structured changelog:
- Source: full extract SQL → incremental SQL with parameters
- Schema: +2 columns (data_dt, load_timestamp)
- Target: writeMode overwrite → overwritePartition
- Transformations: +2 (hashingAndEncrypt on email, dateFormat for data_dt)
- Validations: +3 (notNull, primaryKey, duplicateFileCheck)
- Global: added replaceValues for null standardization
- Impact: Breaking change (writeMode), requires initial full load
```

**Example 6: Management Summary**
```
/document-xflow-orchestrator overview — Executive summary for quarterly_report_pipeline.json
Audience: management

Output: 1-page summary with:
- Pipeline purpose and data flow
- Key metrics (columns, transformations, validations)
- Security posture (PII protection, compliance)
- Operational status (SLA, error rate, contacts)
```

## References

- XFlow Constitution: `xflow-orchestrator-constitution.md` (Sections I-IV, complete field reference)
- XFlow Field Definitions: `XFlow_System_chunks.json` (field_0001 through field_0026)
- XFlow Source Types: `XFlow_System_chunks.json` (source_0027 through source_0030)
- XFlow Transformation Types: `XFlow_System_chunks.json` (trans_0031 through trans_0037)
- XFlow Validation Types: `XFlow_System_chunks.json` (valid_0038 through valid_0040)
- XFlow Dependencies: `XFlow_System_chunks.json` (general_0041)
- XFlow Defaults: `XFlow_System_chunks.json` (general_0042)
- XFlow Best Practices: `XFlow_System_chunks.json` (general_0043)
- Pydantic Models: `xflow_models.py` (field definitions, validation logic)
- Transformation Models: `xflow_transformations.py` (16 types with descriptions)
- Validation Models: `xflow_validations.py` (17 types with descriptions)
