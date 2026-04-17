# Snowflake SQL Best Practices

> Aligned with **Code Reviewer Constitution §1 (Cross-cutting) & §2 (Snowflake SQL)**

---

## 1. Script Header Block (Mandatory)

Every SQL file must open with a comment block establishing lineage, ownership, and operational context.

```sql
-- ──────────────────────────────────────────────────────────────
-- SCRIPT          : load_fact_sales_incremental.sql
-- DESCRIPTION     : Incremental merge of FACT_SALES from staging layer
-- SOURCE_SYSTEMS  : STG.RAW_SALES (S3 ingestion)
-- TARGET_TABLES   : CORE.FACT_SALES
-- SLA_PRIORITY    : P1 — must complete by 06:00 UTC
-- WATERMARK       : load_ts (high-water mark from last successful run)
-- AUTHOR          : <team>
-- CREATED         : 2026-01-15
-- ──────────────────────────────────────────────────────────────
```

---

## 2. No SELECT * (✘ Hard-Stop)

Always enumerate columns explicitly. This protects against silent schema drift and forces conscious selection.

```sql
-- ✘ BAD — breaks if upstream adds/removes columns
SELECT * FROM stg.raw_sales;

-- ✔ GOOD — explicit, prunable, and version-controlled
SELECT
    cust_id,
    product_id,
    sale_amount,
    sale_date,
    load_ts
FROM stg.raw_sales;
```

---

## 3. Deterministic Joins — No Fan-outs (✘ Hard-Stop)

Every join must be deterministic. Accidental cross-joins or many-to-many joins silently inflate row counts.

```sql
-- ✘ BAD — if dim_customer has dupes, this fans out silently
SELECT f.*, d.customer_name
FROM core.fact_sales f
JOIN core.dim_customer d ON f.cust_id = d.cust_id;

-- ✔ GOOD — deduplicate the dimension first, enumerate columns
WITH dim_customer_deduped AS (
    SELECT
        cust_id,
        customer_name,
        ROW_NUMBER() OVER (PARTITION BY cust_id ORDER BY updated_ts DESC) AS rn
    FROM core.dim_customer
)
SELECT
    f.cust_id,
    f.product_id,
    f.sale_amount,
    d.customer_name
FROM core.fact_sales f
JOIN dim_customer_deduped d
    ON f.cust_id = d.cust_id
    AND d.rn = 1;

-- If you truly need a cross-join, annotate it:
SELECT a.col1, b.col2
FROM table_a a
CROSS JOIN table_b b /* CROSS JOIN INTENDED — generating date spine */;
```

---

## 4. Dynamic SQL Injection Prevention (✘ Hard-Stop)

Stored procedures with dynamic SQL must use `IDENTIFIER()` or binding variables—never string concatenation.

```sql
-- ✘ BAD — injectable
CREATE OR REPLACE PROCEDURE truncate_table(table_name STRING)
RETURNS STRING
LANGUAGE SQL
AS
$$
    EXECUTE IMMEDIATE 'TRUNCATE TABLE ' || table_name;
$$;

-- ✔ GOOD — safe identifier reference
CREATE OR REPLACE PROCEDURE truncate_table(table_name STRING)
RETURNS STRING
LANGUAGE SQL
AS
$$
    TRUNCATE TABLE IDENTIFIER(:table_name);
$$;
```

---

## 5. Audit Columns (✔ Mandatory)

Every target table must include operational metadata columns for traceability.

```sql
CREATE TABLE IF NOT EXISTS core.fact_sales (
    cust_id          VARCHAR(50)   NOT NULL,
    product_id       VARCHAR(50)   NOT NULL,
    sale_amount      NUMBER(18,2),
    sale_date        DATE,

    -- Mandatory audit columns
    load_ts          TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()  NOT NULL,
    source_file      VARCHAR(500),
    batch_id         VARCHAR(100)  NOT NULL
);
```

---

## 6. Watermarking / Incremental Logic (✔ Mandatory)

Handle late-arriving data correctly. Never rely on "only process today's data."

```sql
-- Fetch the high-water mark from the control table
SET watermark_ts = (
    SELECT COALESCE(MAX(last_success_ts), '1970-01-01'::TIMESTAMP_NTZ)
    FROM meta.watermarks
    WHERE pipeline_name = 'load_fact_sales'
);

-- Incremental extract using watermark
INSERT INTO core.fact_sales (cust_id, product_id, sale_amount, sale_date, load_ts, source_file, batch_id)
SELECT
    cust_id,
    product_id,
    sale_amount,
    sale_date,
    CURRENT_TIMESTAMP()              AS load_ts,
    METADATA$FILENAME                AS source_file,
    $batch_id                        AS batch_id
FROM stg.raw_sales
WHERE ingestion_ts > $watermark_ts;

-- Update watermark after successful load
UPDATE meta.watermarks
SET last_success_ts = CURRENT_TIMESTAMP()
WHERE pipeline_name = 'load_fact_sales';
```

---

## 7. Performance — Pruning-Friendly Predicates (✔ Mandatory)

Write predicates that align with clustering keys so Snowflake can prune micro-partitions effectively.

```sql
-- ✘ BAD — function on the filter column defeats pruning
SELECT cust_id, sale_amount
FROM core.fact_sales
WHERE DATE(load_ts) = '2026-02-19';

-- ✔ GOOD — range predicate on the raw column, pruning-friendly
SELECT cust_id, sale_amount
FROM core.fact_sales
WHERE load_ts >= '2026-02-19 00:00:00'::TIMESTAMP_NTZ
  AND load_ts <  '2026-02-20 00:00:00'::TIMESTAMP_NTZ;
```

---

## 8. Warehouse Context (✔ Mandatory)

Stored procedures must explicitly set or verify the warehouse before running expensive queries.

```sql
CREATE OR REPLACE PROCEDURE etl.load_fact_sales(batch_id STRING)
RETURNS STRING
LANGUAGE SQL
AS
$$
BEGIN
    -- Why: Prevent accidental execution on an undersized or wrong warehouse
    USE WAREHOUSE ETL_WH_LARGE;

    MERGE INTO core.fact_sales AS tgt
    USING stg.raw_sales AS src
    ON tgt.cust_id = src.cust_id AND tgt.sale_date = src.sale_date
    WHEN MATCHED THEN UPDATE SET
        tgt.sale_amount = src.sale_amount,
        tgt.load_ts     = CURRENT_TIMESTAMP(),
        tgt.batch_id    = :batch_id
    WHEN NOT MATCHED THEN INSERT (cust_id, product_id, sale_amount, sale_date, load_ts, batch_id)
    VALUES (src.cust_id, src.product_id, src.sale_amount, src.sale_date, CURRENT_TIMESTAMP(), :batch_id);

    RETURN 'SUCCESS';
END;
$$;
```

---

## 9. Idempotent MERGE Pattern (✔ Mandatory)

Use `MERGE` instead of `INSERT` to ensure reruns don't create duplicates.

```sql
MERGE INTO core.fact_sales AS tgt
USING (
    SELECT
        cust_id,
        product_id,
        sale_amount,
        sale_date,
        CURRENT_TIMESTAMP()  AS load_ts,
        METADATA$FILENAME    AS source_file,
        $batch_id            AS batch_id
    FROM stg.raw_sales
    WHERE ingestion_ts > $watermark_ts
) AS src
ON  tgt.cust_id   = src.cust_id
AND tgt.sale_date  = src.sale_date

WHEN MATCHED AND tgt.sale_amount <> src.sale_amount THEN UPDATE SET
    tgt.sale_amount = src.sale_amount,
    tgt.load_ts     = src.load_ts,
    tgt.source_file = src.source_file,
    tgt.batch_id    = src.batch_id

WHEN NOT MATCHED THEN INSERT (
    cust_id, product_id, sale_amount, sale_date, load_ts, source_file, batch_id
) VALUES (
    src.cust_id, src.product_id, src.sale_amount, src.sale_date,
    src.load_ts, src.source_file, src.batch_id
);
```

---

## 10. Deterministic ROW_NUMBER (✔ Mandatory)

Always use a tie-breaking secondary sort to avoid non-deterministic ranking.

```sql
-- ✘ BAD — non-deterministic if load_ts ties
ROW_NUMBER() OVER (PARTITION BY cust_id ORDER BY load_ts DESC) AS rn

-- ✔ GOOD — deterministic with secondary key
ROW_NUMBER() OVER (PARTITION BY cust_id ORDER BY load_ts DESC, insert_ts DESC) AS rn
```

---

## 11. No Hardcoded Secrets (✘ Hard-Stop)

Never embed credentials in SQL. Use Snowflake's built-in secret objects or external stages with storage integrations.

```sql
-- ✘ BAD
COPY INTO core.fact_sales
FROM 's3://bucket/path'
CREDENTIALS = (AWS_KEY_ID='AKIA...' AWS_SECRET_KEY='...');

-- ✔ GOOD — use a storage integration
COPY INTO core.fact_sales
FROM @stg.s3_sales_stage
FILE_FORMAT = (FORMAT_NAME = 'stg.csv_format')
PATTERN = '.*sales_.*[.]csv.gz';
```

---

## 12. Full Template

```sql
-- ──────────────────────────────────────────────────────────────
-- SCRIPT          : example_incremental_merge.sql
-- DESCRIPTION     : Template Snowflake SQL adhering to code-reviewer constitution
-- SOURCE_SYSTEMS  : <source>
-- TARGET_TABLES   : <target>
-- SLA_PRIORITY    : P2
-- WATERMARK       : load_ts
-- AUTHOR          : <team>
-- CREATED         : 2026-02-19
-- ──────────────────────────────────────────────────────────────

USE WAREHOUSE ETL_WH_MEDIUM;

-- ── Watermark ────────────────────────────────────────────────
SET watermark_ts = (
    SELECT COALESCE(MAX(last_success_ts), '1970-01-01'::TIMESTAMP_NTZ)
    FROM meta.watermarks
    WHERE pipeline_name = 'example_pipeline'
);

-- ── Incremental Merge ────────────────────────────────────────
MERGE INTO core.target_table AS tgt
USING (
    SELECT
        key_col,
        value_col,
        CURRENT_TIMESTAMP()  AS load_ts,
        METADATA$FILENAME    AS source_file,
        $batch_id            AS batch_id
    FROM stg.source_table
    WHERE ingestion_ts > $watermark_ts
) AS src
ON tgt.key_col = src.key_col

WHEN MATCHED AND tgt.value_col <> src.value_col THEN UPDATE SET
    tgt.value_col   = src.value_col,
    tgt.load_ts     = src.load_ts,
    tgt.source_file = src.source_file,
    tgt.batch_id    = src.batch_id

WHEN NOT MATCHED THEN INSERT (key_col, value_col, load_ts, source_file, batch_id)
VALUES (src.key_col, src.value_col, src.load_ts, src.source_file, src.batch_id);

-- ── Update Watermark ─────────────────────────────────────────
UPDATE meta.watermarks
SET last_success_ts = CURRENT_TIMESTAMP()
WHERE pipeline_name = 'example_pipeline';
```
