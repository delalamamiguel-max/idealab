# Databricks Notebook Best Practices

> Aligned with **Code Reviewer Constitution §1 (Cross-cutting) & §6 (Databricks Notebooks)**

---

## 1. Notebook Header Block (Mandatory)

The first cell of every notebook must be a metadata/documentation cell.

```python
# Databricks notebook source
# ──────────────────────────────────────────────────────────────
# NOTEBOOK        : load_fact_sales_incremental
# DESCRIPTION     : Incremental merge of FACT_SALES from bronze → silver layer
# SOURCE_SYSTEMS  : bronze.raw_sales (Auto Loader from S3)
# TARGET_TABLES   : silver.fact_sales
# SLA_PRIORITY    : P1 — must complete by 06:00 UTC
# AUTHOR          : <team>
# CREATED         : 2026-01-15
# ──────────────────────────────────────────────────────────────
```

---

## 2. No Manual Cell Execution Order (✘ Hard-Stop)

Notebooks must run top-to-bottom as a single unit. Never rely on users running cells in a specific non-linear order.

```python
# ✘ BAD — relies on user running "Cell 5" before "Cell 2"
# Cell 2:
df_transformed = transform(df_raw)  # df_raw defined in Cell 5?!

# ✔ GOOD — linear top-to-bottom flow:
# Cell 1: Config & parameters
# Cell 2: Read source
# Cell 3: Transform
# Cell 4: Write target
# Cell 5: Validation
```

**Rule**: If your notebook breaks when run via `dbutils.notebook.run()` or a Databricks Job, it's broken.

---

## 3. Parameterization via Widgets (✔ Mandatory)

All runtime inputs must come from widgets or job parameters — never hardcoded in notebook cells.

```python
# ✔ GOOD — parameterized via widgets
dbutils.widgets.text("batch_date", "", "Batch Date (YYYY-MM-DD)")
dbutils.widgets.dropdown("environment", "dev", ["dev", "uat", "prod"], "Environment")

batch_date  = dbutils.widgets.get("batch_date")
environment = dbutils.widgets.get("environment")

# Validate inputs early
assert batch_date, "batch_date widget must be provided"
assert environment in ("dev", "uat", "prod"), f"Invalid environment: {environment}"
```

---

## 4. No Driver OOM (✘ Hard-Stop)

Never call `collect()`, `toPandas()`, or `display()` on unbounded datasets.

```python
# ✘ BAD — pulls entire dataset to driver, OOM guaranteed on large tables
pdf = spark.table("bronze.raw_sales").toPandas()

# ✘ ALSO BAD — collect on millions of rows
all_rows = spark.table("bronze.raw_sales").collect()

# ✔ GOOD — keep data distributed, use Spark operations
df = spark.table("bronze.raw_sales").filter(f"sale_date = '{batch_date}'")
df.write.mode("overwrite").saveAsTable("silver.fact_sales_staging")

# ✔ GOOD — if you MUST bring to driver, apply limit or aggregation first
sample = spark.table("bronze.raw_sales").limit(100).toPandas()  # bounded
summary = spark.table("bronze.raw_sales").groupBy("region").count().toPandas()  # small result
```

---

## 5. Checkpoints & Watermarks for Streaming (✔ Mandatory)

All streaming workloads must use checkpoints and watermarks. No exceptions.

```python
# ✔ GOOD — structured streaming with checkpoint and watermark
(
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", f"/mnt/checkpoints/{environment}/raw_sales/schema")
    .load(f"/mnt/landing/{environment}/sales/")
    .withWatermark("event_time", "2 hours")
    .writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", f"/mnt/checkpoints/{environment}/raw_sales/checkpoint")
    .trigger(availableNow=True)
    .toTable("bronze.raw_sales")
)
```

**Why**: Without checkpoints, a restart reprocesses everything from scratch. Without watermarks, late-arriving data causes unbounded state growth and eventual OOM.

---

## 6. Separation of Concerns (✔ Mandatory)

Config, transformations, and shared utilities must be clearly separated.

```
Recommended notebook structure:
├── config/
│   └── pipeline_config        # Widget definitions, env settings, table names
├── transforms/
│   ├── bronze_to_silver       # Raw → cleaned
│   └── silver_to_gold         # Cleaned → aggregated
├── utils/
│   ├── schema_validation      # Reusable schema checks
│   └── audit_helpers          # load_ts, batch_id injection
└── orchestrator               # Top-level notebook that calls the above
```

```python
# orchestrator notebook
# ✔ GOOD — clean composition
dbutils.notebook.run("./config/pipeline_config", timeout_seconds=60, arguments={"environment": environment})
dbutils.notebook.run("./transforms/bronze_to_silver", timeout_seconds=600, arguments={"batch_date": batch_date})
dbutils.notebook.run("./transforms/silver_to_gold", timeout_seconds=600, arguments={"batch_date": batch_date})
```

For truly shared logic, move it to a **Wheel package** or **Databricks Repos library**.

```python
# ✔ GOOD — shared logic in a library, not copy-pasted across notebooks
from etl_common.audit import add_audit_columns
from etl_common.validation import validate_schema

df = spark.table("bronze.raw_sales")
df = validate_schema(df, expected_schema)
df = add_audit_columns(df, batch_id=batch_id)
```

---

## 7. Audit Columns (✔ Mandatory)

Every write to a target table must include operational metadata.

```python
from pyspark.sql import functions as F

def add_audit_columns(df, batch_id: str):
    """Inject mandatory audit columns.

    Why: Every row must be traceable to its source batch for debugging and lineage.
    """
    return (
        df
        .withColumn("load_ts", F.current_timestamp())
        .withColumn("batch_id", F.lit(batch_id))
        .withColumn("source_file", F.input_file_name())
    )
```

---

## 8. Idempotent Writes (✔ Mandatory)

Use Delta Lake MERGE or replaceWhere for idempotent writes. Never blind append if reruns are possible.

```python
# ✘ BAD — rerun appends duplicates
df.write.mode("append").saveAsTable("silver.fact_sales")

# ✔ GOOD — idempotent overwrite for a partition
df.write.mode("overwrite") \
    .option("replaceWhere", f"sale_date = '{batch_date}'") \
    .saveAsTable("silver.fact_sales")

# ✔ ALSO GOOD — MERGE for upsert semantics
from delta.tables import DeltaTable

target = DeltaTable.forName(spark, "silver.fact_sales")
target.alias("tgt").merge(
    df.alias("src"),
    "tgt.cust_id = src.cust_id AND tgt.sale_date = src.sale_date"
).whenMatchedUpdateAll() \
 .whenNotMatchedInsertAll() \
 .execute()
```

---

## 9. Error Handling & Logging (✔ Mandatory)

Use structured logging. Never silence exceptions. Provide run-level context.

```python
import logging

logger = logging.getLogger("etl.load_fact_sales")
logger.setLevel(logging.INFO)

run_id = dbutils.widgets.get("run_id") if dbutils.widgets.get("run_id") else str(spark.sparkContext.applicationId)

logger.info(f"[{run_id}] Starting bronze → silver transformation | batch_date={batch_date}")

try:
    df = spark.table("bronze.raw_sales").filter(f"sale_date = '{batch_date}'")
    record_count = df.count()
    logger.info(f"[{run_id}] Records to process: {record_count}")

    if record_count == 0:
        logger.warning(f"[{run_id}] Zero records for batch_date={batch_date}. Exiting gracefully.")
        dbutils.notebook.exit("NO_DATA")

    # ... transform and load ...

    logger.info(f"[{run_id}] Successfully loaded {record_count} records into silver.fact_sales")
    dbutils.notebook.exit(f"SUCCESS:{record_count}")

except Exception as exc:
    logger.error(f"[{run_id}] Pipeline failed: {exc}", exc_info=True)
    raise
```

---

## 10. No Hardcoded Secrets (✘ Hard-Stop)

Use Databricks Secrets, not inline credentials.

```python
# ✘ BAD
storage_account_key = "xYz123SuperSecret..."

# ✔ GOOD — Databricks Secret Scope
storage_account_key = dbutils.secrets.get(scope="etl-secrets", key="storage-account-key")
```

---

## 11. Performance Considerations (✔ Mandatory)

- **Partition pruning**: Always filter on partition columns before joins.
- **Cache sparingly**: Only cache DataFrames used more than twice; unpersist after use.
- **Broadcast joins**: Explicitly broadcast small dimension tables.
- **Avoid UDFs**: Prefer native Spark functions. UDFs serialize to Python and kill performance.

```python
# ✔ GOOD — broadcast small dimension
from pyspark.sql.functions import broadcast

df_enriched = df_facts.join(broadcast(df_dim_region), "region_id", "left")

# ✘ BAD — Python UDF where a native function exists
from pyspark.sql.functions import udf
upper_udf = udf(lambda x: x.upper())  # Don't do this

# ✔ GOOD — native Spark function
from pyspark.sql.functions import upper
df = df.withColumn("name_upper", upper("name"))
```

---

## 12. Full Template

```python
# Databricks notebook source
# ──────────────────────────────────────────────────────────────
# NOTEBOOK        : example_bronze_to_silver
# DESCRIPTION     : Template Databricks notebook adhering to code-reviewer constitution
# SOURCE_SYSTEMS  : bronze.<source>
# TARGET_TABLES   : silver.<target>
# SLA_PRIORITY    : P2
# AUTHOR          : <team>
# CREATED         : 2026-02-19
# ──────────────────────────────────────────────────────────────

# COMMAND ----------
# Cell 1: Configuration & Parameters

dbutils.widgets.text("batch_date", "", "Batch Date (YYYY-MM-DD)")
dbutils.widgets.text("run_id", "", "Pipeline Run ID")
dbutils.widgets.dropdown("environment", "dev", ["dev", "uat", "prod"], "Environment")

batch_date  = dbutils.widgets.get("batch_date")
run_id      = dbutils.widgets.get("run_id") or spark.sparkContext.applicationId
environment = dbutils.widgets.get("environment")

assert batch_date, "batch_date is required"

# COMMAND ----------
# Cell 2: Imports & Logger Setup

import logging
from pyspark.sql import functions as F
from delta.tables import DeltaTable

logger = logging.getLogger("etl.example")
logger.setLevel(logging.INFO)
logger.info(f"[{run_id}] Pipeline started | batch_date={batch_date} | env={environment}")

# COMMAND ----------
# Cell 3: Read Source (with partition pruning)

df_raw = (
    spark.table("bronze.source_table")
    .filter(F.col("event_date") == batch_date)
)

record_count = df_raw.count()
logger.info(f"[{run_id}] Source records: {record_count}")

if record_count == 0:
    logger.warning(f"[{run_id}] No data for {batch_date}. Exiting.")
    dbutils.notebook.exit("NO_DATA")

# COMMAND ----------
# Cell 4: Transform

df_transformed = (
    df_raw
    .withColumn("load_ts", F.current_timestamp())
    .withColumn("batch_id", F.lit(run_id))
    .withColumn("source_file", F.input_file_name())
    .select(
        "key_col",
        "value_col",
        "event_date",
        "load_ts",
        "batch_id",
        "source_file",
    )
)

# COMMAND ----------
# Cell 5: Write (idempotent MERGE)

target = DeltaTable.forName(spark, "silver.target_table")
target.alias("tgt").merge(
    df_transformed.alias("src"),
    "tgt.key_col = src.key_col AND tgt.event_date = src.event_date"
).whenMatchedUpdateAll() \
 .whenNotMatchedInsertAll() \
 .execute()

logger.info(f"[{run_id}] MERGE complete | {record_count} records into silver.target_table")

# COMMAND ----------
# Cell 6: Validation

post_count = spark.table("silver.target_table").filter(F.col("event_date") == batch_date).count()
logger.info(f"[{run_id}] Post-load count for {batch_date}: {post_count}")
assert post_count >= record_count, f"Data loss detected: expected >= {record_count}, got {post_count}"

dbutils.notebook.exit(f"SUCCESS:{post_count}")
```
