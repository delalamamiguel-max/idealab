---
description: Compare XFlow configuration approaches, source types, and architecture patterns (XFlow Orchestrator)
---

User input: $ARGUMENTS

## Execution Steps

## Execution Rules (NON-NEGOTIABLE)

**These rules govern HOW this workflow executes. Violating them is a hard-stop.**

1. **ONE question per message.** Each interactive question MUST be its own separate `ask_user_question` call. NEVER combine multiple questions into a single prompt.
2. **NO skipping steps.** Every interactive step MUST be executed in order. The ONLY exception is when the user already provided the information in $ARGUMENTS.
3. **WAIT for user response** before proceeding to the next step. Do not assume defaults unless the workflow explicitly says to apply a default silently.
4. **NEVER output results before collecting all required input.** If the comparison subject or criteria is unclear, ASK before generating.

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
- Load `templates/env-config.yaml` for default values

### 3. Parse Input
Extract from $ARGUMENTS:
- **Comparison subject**: source types, write modes, target formats, transformation strategies, ingestion patterns, encryption approaches, error handling strategies, partitioning strategies, or two specific config files
- **Comparison criteria**: performance, complexity, reliability, cost, data freshness, security, maintainability, scalability, compliance
- **Data characteristics**: volume (rows/day), velocity (batch/streaming/micro-batch), schema complexity (columns, nested types), PII presence, data change rate
- **Constraints**: latency SLA, storage budget, team expertise, compliance requirements (RIM policy, data library), existing infrastructure
- **Two config files**: if comparing two existing configs, provide both file paths

If comparing two config files, read and parse both completely.

### 3b. Interactive Comparison Setup

**If the comparison subject or criteria is not clear from $ARGUMENTS, ASK:**

**Question 1 — Comparison Scope:**
> What should I compare?
> - **Source types** — JDBC vs Kafka vs File for your use case
> - **Write modes** — append vs overwrite vs overwritePartition vs upsert
> - **Architecture** — batch vs streaming vs hybrid patterns
> - **Full analysis** — compare all dimensions for your scenario

Use `ask_user_question` with these 4 options.

<!-- HALT: Wait for user response before continuing to Question 2 -->

**Question 2 — Priorities:**
> What are your top priorities for this comparison?
> - **Performance** — throughput, latency, resource usage
> - **Security** — encryption, credential management, PII protection
> - **Cost** — storage, compute, operational overhead
> - **Simplicity** — ease of setup, maintenance, debugging

Use `ask_user_question` (allowMultiple=true) with these 4 options. Use selected priorities to weight the scoring matrix.

<!-- HALT: Wait for user response before continuing to Step 4 -->

### 4. Generate Alternatives

**For each comparison, generate 2-3 complete XFlow configuration approaches with full JSON snippets showing the key structural differences.**

---

#### Comparison Category 1 — Source Type Comparisons

**1a. Full Extract SQL vs Incremental SQL (via sqlFileLocation)**

| Aspect | Full Extract SQL | Incremental SQL |
|--------|-----------------|----------------|
| **SQL File** | `SELECT * FROM SCHEMA.TABLE` | `SELECT * FROM SCHEMA.TABLE WHERE modified_date > :param` |
| **Use Case** | Small-medium tables, full snapshot | Large tables, incremental loads, complex joins |
| **Data Volume** | Extracts entire table every run | Extracts only changed/new rows via WHERE clause |
| **Maintenance** | Simple SQL file | Requires watermark/parameter management |
| **Flexibility** | Full table only | Full SQL power — joins, filters, aggregations |
| **Performance** | Slower for large tables (full scan) | Faster — only reads delta |
| **Idempotency** | Natural — same result each run | Depends on SQL logic (watermark management) |
| **Parameters** | `"parameters": []` | `"parameters": [{ FETCH_ON_NULL, FETCH_ALWAYS }]` |

```json
// Approach A: Full Extract SQL
"jdbcSource": {
  "connectionType": "ORACLE",
  "logonScopeName": "dl-eastus2-dev-sec-kv-scope",
  "logonSecretName": "logon-oracle-dev",
  "sqlFileLocation": "abfss://sql@datalakeeastus2prd.dfs.core.windows.net/billing/customers_full.sql",
  "fetchSize": 20000,
  "parameters": []
}

// Approach B: Incremental SQL with bind parameters
"jdbcSource": {
  "connectionType": "ORACLE",
  "logonScopeName": "dl-eastus2-dev-sec-kv-scope",
  "logonSecretName": "logon-oracle-dev",
  "sqlFileLocation": "abfss://sql@datalakeeastus2prd.dfs.core.windows.net/billing/customers_incremental.sql",
  "fetchSize": 20000,
  "parameters": [
    { "index": 1, "sourceType": "SQL", "source": "SELECT MAX(modified_date) FROM BILLING.CUSTOMERS", "outputType": "STRING", "fetchParameterType": "FETCH_ALWAYS" }
  ]
}
```

**Decision criteria**: Use full extract SQL for tables < 1M rows or when full snapshot is needed. Use incremental SQL with parameters for tables > 1M rows or when only changed/new records are needed.

---

**1b. JDBC vs File Source**

| Aspect | JDBC Source | File Source |
|--------|-----------|------------|
| **Config** | `"jdbcSource": { ... }` | `"sourceLocation": "abfss://...", "sourceFileFormat": "csv"` |
| **Use Case** | Direct database extraction | File-based ingestion (CSV, Parquet, JSON, etc.) |
| **Latency** | Near real-time (minutes) | Batch (depends on file delivery schedule) |
| **Schema** | From database DDL or explicit | Must be explicitly defined |
| **Authentication** | Secret scope for DB credentials | ADLS access (managed identity or SAS token) |
| **Error Handling** | Connection retries, query timeouts | File validation, malformed record handling |
| **Data Quality** | Database enforces constraints | Must add validations in config |
| **Scalability** | Limited by DB connection pool | Scales with file count and size |

**Decision criteria**: Use JDBC when data lives in a database and you need fresh extracts. Use File source when data is delivered as files (vendor feeds, exports, ETL outputs).

---

**1c. Kafka Streaming vs Batch File Ingestion**

| Aspect | Kafka Source | File Source (Batch) |
|--------|-------------|-------------------|
| **Config** | `"kafkaSource": { "bootstrapServers": "...", "subscribe": "topic" }` | `"sourceLocation": "abfss://...", "sourceFileFormat": "csv"` |
| **Latency** | Sub-second to seconds | Minutes to hours |
| **Data Freshness** | Real-time | Depends on file delivery schedule |
| **Complexity** | High — consumer groups, offsets, SASL | Low — file path and format |
| **Cost** | Higher — always-on cluster, Kafka infra | Lower — scheduled jobs |
| **Reliability** | Offset management, exactly-once semantics | File-level retry, duplicate file check |
| **Schema** | Typically kafkatext (raw) or JSON | Explicit schema definition |
| **Monitoring** | Consumer lag, offset tracking | File arrival, record counts |
| **writeMode** | Always `append` | Any (append, overwrite, overwritePartition, upsert) |

```json
// Approach A: Kafka
"source": {
  "kafkaSource": {
    "bootstrapServers": "broker1:9093,broker2:9093",
    "subscribe": "order_events",
    "groupId": "xflow_orders",
    "logonScopeName": "dl-kafka-scope",
    "logonSecretName": "kafka-credentials",
    "securityProtocol": "SASL_SSL",
    "startingOffsets": "latest",
    "maxOffsetsPerTrigger": 100000
  },
  "sourceFileFormat": "kafkatext",
  "schema": [{"columnName": "event_date", "columnType": "string", "partitionOrder": 1}]
}

// Approach B: File (CSV)
"source": {
  "sourceLocation": "abfss://raw@storage.dfs.core.windows.net/orders/",
  "sourceFileFormat": "csv",
  "csvDelimiter": ",",
  "csvIgnoreHeaderInd": true,
  "schema": [
    {"columnName": "order_id", "columnType": "long", "pk": true},
    {"columnName": "customer_id", "columnType": "long"},
    {"columnName": "amount", "columnType": "decimal", "precision": 12, "scale": 2},
    {"columnName": "order_date", "columnType": "string"}
  ]
}
```

**Decision criteria**: Use Kafka when SLA requires < 1 minute data freshness. Use File source when hourly/daily batch is acceptable and simpler operations are preferred.

---

**1d. HTTP File Source (FileGW) vs Azure Files Source**

| Aspect | HTTP FileGW (Push) | Azure Files (Pull) |
|--------|-------------------|-------------------|
| **Config** | `"httpFileSource": { "feedId": "...", "filterRegex": "..." }` | `"azureFilesSource": { "sourcePullConfig": { ... } }` |
| **Model** | Push — external system sends files to FileGW | Pull — XFlow pulls files from Azure File Share |
| **Scheduling** | Event-driven (file arrival triggers) | Poll-based (pullFrequencyMin) |
| **File Filtering** | filterBy + filterRegex | resourcePath pattern |
| **File Actions** | Rich — EMPTY_FILE_VALIDATION, RECORD_COUNT_VALIDATION, CLEANSE, COMPRESSION, DEST_PARTITIONING | Basic — file matching |
| **Authentication** | FileGW managed | SAS token via secret scope |
| **Use Case** | External vendor/partner file delivery | Internal file share migration, legacy system integration |
| **Complexity** | Medium — FileGW setup required | Medium — Azure File Share + SAS token setup |

**Decision criteria**: Use HTTP FileGW when external partners push files. Use Azure Files when pulling from internal file shares or legacy systems.

---

#### Comparison Category 2 — Write Mode Comparisons

**2a. append vs overwrite**

| Aspect | append | overwrite |
|--------|--------|-----------|
| **Config** | `"writeMode": "append"` | `"writeMode": "overwrite"` |
| **Behavior** | Adds new records to existing data | Replaces ALL existing data |
| **History** | Preserves all historical data | Destroys previous data |
| **Idempotency** | NOT idempotent — re-runs create duplicates | Idempotent — same result each run |
| **Use Case** | Log data, event streams, incremental loads | Small dimension tables, lookup tables |
| **Risk** | Duplicates if job re-runs | Data loss if source is incomplete |
| **Performance** | Fast — write-only, no read | Fast — but must rewrite entire table |
| **Storage** | Grows continuously | Constant size |
| **Constitution** | Recommended for streaming/incremental | Only for small dimension tables |

---

**2b. append vs upsert**

| Aspect | append | upsert (MERGE) |
|--------|--------|----------------|
| **Config** | `"writeMode": "append"` | `"writeMode": "upsert"`, requires `pk: true` or `mergeKeys` |
| **Behavior** | Always inserts new rows | Updates existing rows, inserts new ones |
| **Duplicates** | Can create duplicates on re-run | No duplicates — merge on key |
| **History** | All versions preserved | Only latest version kept |
| **Performance** | Fast — append-only | Slower — read + compare + write |
| **Complexity** | Simple — no key management | Requires primary key definition |
| **Use Case** | Event logs, audit trails, streaming | CDC, master data, slowly changing dimensions |
| **Constitution** | No PK required | Must have `pk: true` columns or `mergeKeys` |

```json
// Approach A: append
"targets": [{
  "writeMode": "append",
  "schema": [
    {"columnName": "customer_id", "columnType": "long"},
    {"columnName": "event_type", "columnType": "string"}
  ]
}]

// Approach B: upsert
"targets": [{
  "writeMode": "upsert",
  "mergeKeys": ["customer_id"],
  "schema": [
    {"columnName": "customer_id", "columnType": "long", "pk": true},
    {"columnName": "customer_name", "columnType": "string"},
    {"columnName": "last_updated", "columnType": "timestamp"}
  ]
}]
```

---

**2c. overwrite vs overwritePartition**

| Aspect | overwrite | overwritePartition |
|--------|-----------|-------------------|
| **Config** | `"writeMode": "overwrite"` | `"writeMode": "overwritePartition"`, requires partition columns |
| **Behavior** | Replaces entire table | Replaces only affected partitions |
| **Scope** | Full table rewrite | Partition-level rewrite |
| **Performance** | Slower for large tables | Fast — only touches affected partitions |
| **Data Safety** | Risky — all data replaced | Safer — unaffected partitions preserved |
| **Use Case** | Small tables, full refresh | Daily batch loads partitioned by date |
| **Constitution** | Only for small dimension tables | Requires `partitionOrder` on columns |
| **overwriteType** | N/A | `DEFAULT` or `DYNAMIC` |

```json
// Approach A: overwrite
"targets": [{
  "writeMode": "overwrite",
  "schema": [
    {"columnName": "region_code", "columnType": "string"},
    {"columnName": "region_name", "columnType": "string"}
  ]
}]

// Approach B: overwritePartition
"targets": [{
  "writeMode": "overwritePartition",
  "overwriteType": "DYNAMIC",
  "schema": [
    {"columnName": "order_id", "columnType": "long"},
    {"columnName": "amount", "columnType": "decimal", "precision": 12, "scale": 2},
    {"columnName": "data_dt", "columnType": "string", "partitionOrder": 1}
  ]
}]
```

---

**2d. upsert vs overwritePartition**

| Aspect | upsert | overwritePartition |
|--------|--------|-------------------|
| **Granularity** | Row-level merge | Partition-level replace |
| **Key Requirement** | Primary key (pk or mergeKeys) | Partition column (partitionOrder) |
| **Performance** | Slower — row-by-row comparison | Faster — bulk partition swap |
| **Partial Updates** | Yes — update specific columns | No — replaces entire partition |
| **Use Case** | CDC, real-time updates, SCD Type 1 | Daily batch, full partition reload |
| **Complexity** | Higher — merge logic, key management | Lower — partition swap |
| **Re-run Safety** | Idempotent (same key = update) | Idempotent (same partition = replace) |

**Decision criteria**: Use upsert when you need row-level updates and have a natural primary key. Use overwritePartition when you reload entire date partitions daily.

---

#### Comparison Category 3 — Target Format Comparisons

**3a. Delta vs Parquet**

| Aspect | Delta | Parquet |
|--------|-------|---------|
| **Config** | `"targetFileFormat": "delta"` | `"targetFileFormat": "parquet"` |
| **ACID** | Yes — full ACID transactions | No — eventual consistency |
| **Time Travel** | Yes — query previous versions | No |
| **Schema Evolution** | Yes — add/rename columns | Limited |
| **Upsert Support** | Native MERGE | Not supported |
| **Vacuum** | `vacuumDaysOld` for storage management | Manual cleanup |
| **Performance** | Optimized with Z-ORDER, data skipping | Good for read-heavy analytics |
| **Compatibility** | Databricks, Spark, some external tools | Universal — all tools support Parquet |
| **Storage** | Slightly larger (transaction log) | Smaller |
| **Constitution** | Preferred default | Valid alternative |

---

**3b. Delta vs Database Target**

| Aspect | Delta (Data Lake) | Database Target |
|--------|------------------|----------------|
| **Config** | `"targetFileFormat": "delta"` | `"targetFileFormat": "database"`, requires `databaseTarget` section |
| **Storage** | ADLS (abfss://) | External database (JDBC) |
| **Cost** | Low — cloud storage | Higher — database compute |
| **Query** | Spark SQL, Databricks SQL | Native database SQL |
| **Use Case** | Analytics, data lake, ML | Operational systems, reporting databases |
| **Scalability** | Massive — petabyte scale | Limited by database capacity |
| **Latency** | Batch | Can be near real-time |
| **Constitution** | Requires `databaseTarget` section with connectionType, credentials |

---

#### Comparison Category 4 — Transformation Strategy Comparisons

**4a. In-Config Transformations vs External SQL File**

| Aspect | In-Config Transformations | sqlFileLocation |
|--------|--------------------------|----------------|
| **Config** | `"transformations": [{ ... }]` | `"sqlFileLocation": "abfss://..."` |
| **Logic Location** | Embedded in XFlow JSON | External SQL file in ADLS |
| **Complexity** | Limited to XFlow transformation types | Full SQL power |
| **Maintenance** | Edit JSON config | Edit SQL file separately |
| **Version Control** | Config versioning | SQL file versioning |
| **Testing** | Test via `/test-xflow-orchestrator` | Test SQL independently |
| **Use Case** | Simple transforms (encrypt, date format, regex) | Complex joins, aggregations, window functions |

---

**4b. hashingAndEncrypt vs No Encryption**

| Aspect | With Encryption | Without Encryption |
|--------|----------------|-------------------|
| **Config** | `"transformationType": "hashingAndEncrypt"` with encryptIdentity, encryptFormat | No transformation on PII columns |
| **Security** | PII protected via Voltage | PII in plaintext |
| **Performance** | ~10-20% overhead per encrypted column | No overhead |
| **Compliance** | Meets data protection requirements | May violate RIM policy |
| **Reversibility** | Decryptable with proper identity | N/A |
| **Constitution** | Required for PII columns | Violation if PII is present |

---

**4c. Global Transformation vs Per-Column Transformations**

| Aspect | Global Transformation | Per-Column Transformations |
|--------|----------------------|--------------------------|
| **Config** | `"globalTransformation": { "trimSpacesInd": true, "replaceValues": [...] }` | Individual transformation entries per column |
| **Scope** | Applied to ALL columns | Applied to specific columns only |
| **Use Case** | Blanket data quality (trim, null standardization) | Targeted transforms (encrypt, date format, regex) |
| **Performance** | Single pass over all data | One pass per transformation |
| **Maintenance** | One config block | Multiple transformation entries |
| **Constitution** | trimSpacesInd: true is mandatory default | Required for derived/encrypted columns |

---

#### Comparison Category 5 — Architecture Pattern Comparisons

**5a. Single Target vs Multi-Target**

| Aspect | Single Target | Multi-Target |
|--------|--------------|-------------|
| **Config** | `"targets": [{ one target }]` | `"targets": [{ target1 }, { target2 }]` |
| **Use Case** | Standard ingestion to one location | Fan-out to multiple formats/locations |
| **Complexity** | Simple | Higher — multiple schemas, write modes |
| **Example** | Raw → Delta | Raw → Delta (analytics) + Raw → Database (operational) |
| **Performance** | Single write | Multiple writes (sequential) |
| **Consistency** | Guaranteed | Must handle partial failures |

**5b. Full Load vs Incremental Load**

| Aspect | Full Load | Incremental Load |
|--------|-----------|-----------------|
| **Source** | `sqlFileLocation` (full `SELECT *`) | `sqlFileLocation` (WHERE clause with parameters) or Kafka |
| **writeMode** | `overwrite` or `overwritePartition` | `append` or `upsert` |
| **Volume** | Entire table each run | Only new/changed records |
| **Cost** | Higher — reads everything | Lower — reads delta only |
| **Complexity** | Simple — no watermark | Requires watermark/offset management |
| **Data Freshness** | Complete snapshot | Depends on load frequency |
| **Recovery** | Easy — just re-run | Complex — must track last successful offset |

**5c. Validation-Heavy vs Validation-Light**

| Aspect | Validation-Heavy | Validation-Light |
|--------|-----------------|-----------------|
| **Config** | 5-10 validations (notNull, primaryKey, numericRange, allowedValues, regex, duplicateFileCheck, schema, email, length) | 0-2 validations (schema, notNull) |
| **Use Case** | Critical data (financial, PII, regulatory) | Non-critical data (logs, events, staging) |
| **Performance** | Slower — multiple validation passes | Faster — minimal overhead |
| **Data Quality** | High — catches issues before write | Low — issues discovered downstream |
| **Error Handling** | Detailed — per-validation failure actions | Basic — fail or succeed |
| **Maintenance** | Higher — must update validations with schema changes | Lower |

### 5. Generate Comparison Matrix

**For every comparison, generate a scored matrix:**

| Dimension | Description | Scoring |
|-----------|-------------|---------|
| **Performance** | Throughput, latency, resource usage | ⭐ (poor) to ⭐⭐⭐⭐⭐ (excellent) |
| **Complexity** | Config size, maintenance burden, learning curve | ⭐ (complex) to ⭐⭐⭐⭐⭐ (simple) |
| **Reliability** | Error handling, idempotency, recovery | ⭐ to ⭐⭐⭐⭐⭐ |
| **Data Freshness** | How current the target data is | ⭐ to ⭐⭐⭐⭐⭐ |
| **Cost** | Compute, storage, network, infrastructure | ⭐ (expensive) to ⭐⭐⭐⭐⭐ (cheap) |
| **Security** | Encryption, credential management, PII handling | ⭐ to ⭐⭐⭐⭐⭐ |
| **Scalability** | Behavior as data volume grows 10x, 100x | ⭐ to ⭐⭐⭐⭐⭐ |
| **Maintainability** | Ease of updates, debugging, documentation | ⭐ to ⭐⭐⭐⭐⭐ |
| **Compliance** | Constitution adherence, RIM policy, data library | ⭐ to ⭐⭐⭐⭐⭐ |

**Example matrix output:**

```
| Dimension       | Approach A (upsert) | Approach B (overwritePartition) |
|-----------------|--------------------|---------------------------------|
| Performance     | ⭐⭐⭐              | ⭐⭐⭐⭐⭐                         |
| Complexity      | ⭐⭐                | ⭐⭐⭐⭐                           |
| Reliability     | ⭐⭐⭐⭐⭐            | ⭐⭐⭐⭐                           |
| Data Freshness  | ⭐⭐⭐⭐⭐            | ⭐⭐⭐                             |
| Cost            | ⭐⭐⭐              | ⭐⭐⭐⭐                           |
| Security        | ⭐⭐⭐⭐             | ⭐⭐⭐⭐                           |
| Scalability     | ⭐⭐⭐              | ⭐⭐⭐⭐⭐                         |
| Maintainability | ⭐⭐⭐              | ⭐⭐⭐⭐                           |
| Compliance      | ⭐⭐⭐⭐             | ⭐⭐⭐⭐                           |
| TOTAL           | 31/45              | 37/45                           |
```

### 6. Add Recommendations

**Provide a clear recommendation with:**

1. **Winner**: Which approach to use and why
2. **When to choose the other**: Specific scenarios where the alternative is better
3. **Implementation guidance**: Key config fields to set for the recommended approach
4. **Migration path**: If switching from current approach to recommended
   - What config fields change
   - Data migration steps (if any)
   - Testing requirements
   - Rollback plan
5. **Constitution compliance**: Confirm both approaches pass hard-stop rules; flag any violations
6. **Config snippet**: Complete JSON snippet for the recommended approach, ready to use
7. **Testing strategy**: How to validate the recommendation with real data

### 7. Validate and Report

// turbo

Report with:
- Recommended approach with confidence level (strong/moderate/conditional)
- Comparison summary table with scores
- Key trade-offs (top 3)
- Complete config snippet for recommended approach
- Migration steps (if applicable)
- Testing recommendations

## Error Handling

**Insufficient Context**: Request:
1. Data volume (rows/day, GB/day)
2. Latency SLA (real-time, hourly, daily)
3. Source characteristics (database type, file format, streaming)
4. Data change pattern (append-only, CDC, full refresh)
5. PII presence and compliance requirements
6. Team expertise level

**Unclear Comparison Subject**: Present the 5 comparison categories and ask which is relevant:
1. Source types (JDBC vs File vs Kafka vs HTTP vs Azure Files)
2. Write modes (append vs overwrite vs overwritePartition vs upsert)
3. Target formats (Delta vs Parquet vs CSV vs Database)
4. Transformation strategies (in-config vs SQL file, encryption vs none)
5. Architecture patterns (single vs multi-target, full vs incremental)

**Both Approaches Violate Constitution**: Explain which hard-stop rules are violated, suggest a third compliant alternative, and show the minimum changes needed for compliance.

**Comparing Two Config Files**: Read both files, diff them section by section (root metadata, source, target, transformations, validations, globalTransformation, error handling), and present a structured comparison.

## Examples

**Example 1: Write Mode for Daily Batch**
```
/compare-xflow-orchestrator Delta upsert vs overwritePartition for daily customer batch load.
500K rows/day, partitioned by data_dt, customer_id is natural PK.

Matrix: overwritePartition scores 37/45 vs upsert 31/45
Recommendation: overwritePartition — simpler, faster at scale, daily full partition reload is natural fit
When to use upsert: If intra-day updates are needed or if only changed rows are available
```

**Example 2: Source Type for Large Oracle Table**
```
/compare-xflow-orchestrator Full extract SQL vs incremental SQL for 50M row Oracle table.
Daily incremental load, last_modified column available.

Matrix: Incremental SQL scores 39/45 vs Full extract SQL 28/45
Recommendation: Incremental SQL with WHERE clause on last_modified and bind parameters
When to use full extract: For initial full load or if table is small enough for full extract
```

**Example 3: Real-time vs Batch for Order Data**
```
/compare-xflow-orchestrator Kafka streaming vs CSV file ingestion for order data.
SLA: 5 minute freshness. 100K orders/day. Team has Kafka experience.

Matrix: Kafka scores 36/45 vs CSV 33/45
Recommendation: Kafka — meets 5-min SLA, team has experience
When to use CSV: If SLA relaxes to hourly or Kafka infrastructure unavailable
```

**Example 4: Encryption Strategy**
```
/compare-xflow-orchestrator hashingAndEncrypt on 5 PII columns vs no encryption for staging table.
Data contains email, phone, SSN. RIM policy: CUST-100.

Matrix: Encryption scores 42/45 vs No encryption 25/45
Recommendation: hashingAndEncrypt — REQUIRED by constitution for PII columns
When to skip: Never for PII — constitution hard-stop rule
```

**Example 5: Two Config File Comparison**
```
/compare-xflow-orchestrator Compare customer_v1.json vs customer_v2.json

Diff:
- Source: v1 uses full extract SQL, v2 uses incremental SQL with parameters
- Target: v1 uses overwrite, v2 uses overwritePartition
- Transformations: v2 adds hashingAndEncrypt on email
- Validations: v2 adds notNull, primaryKey, duplicateFileCheck
- Global: v2 adds null standardization

Recommendation: v2 is superior — incremental load, PII protection, data quality
```

**Example 6: Multi-Target Architecture**
```
/compare-xflow-orchestrator Single Delta target vs Delta + Database dual target for reporting data.
Downstream: Databricks analytics + Power BI via SQL Server.

Matrix: Dual target scores 35/45 vs Single target 38/45
Recommendation: Single Delta target with Databricks SQL endpoint for Power BI
When to use dual: If Power BI cannot connect to Databricks SQL
```

## References

- XFlow Constitution: `xflow-orchestrator-constitution.md` (Sections I-IV, field reference tables)
- XFlow Source Types: `XFlow_System_chunks.json` (source_0027 through source_0030)
- XFlow Write Modes: `XFlow_System_chunks.json` (field_0026)
- XFlow Transformation Types: `XFlow_System_chunks.json` (trans_0031 through trans_0037)
- XFlow Validation Types: `XFlow_System_chunks.json` (valid_0038 through valid_0040)
- XFlow Best Practices: `XFlow_System_chunks.json` (general_0043)
- XFlow Dependencies: `XFlow_System_chunks.json` (general_0041)
- Pydantic Models: `xflow_models.py` (valid enums, field constraints)
- Transformation Models: `xflow_transformations.py` (16 types)
- Validation Models: `xflow_validations.py` (17 types)
