# pipeline builder Constitution

## Purpose

This constitution defines the foundational principles and hard-stop rules for the pipeline builder archetype.


## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** output that violates these rules:

- ✘ **No unbounded collect**: Do not call `collect()` on a DataFrame with unknown or unbounded row count
- ✘ **No unsafe overwrite**: Do not execute `df.write.mode("overwrite")` without partition predicate or Delta `replaceWhere` clause
- ✘ **No plaintext credentials**: Do not write plaintext credentials, API tokens or connection strings
- ✘ **Bad records path required**: Do not omit `.option("badRecordsPath", ...)` on any read from semi-structured files (CSV, JSON, Avro, XML)
- ✘ **Unique temp names**: Do not create temp view or table without unique, deterministic name containing `${runtime_uuid}` or `${lineage_id}` placeholders

## II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify these patterns:

- ✔ **Retry logic**: Wrap external I/O in retry logic (`maxRetries ≥ 3`, exponential back-off)
- ✔ **Logging**: Log `record_count_in`, `record_count_out`, and `sha256(concat_ws("|", key_columns))` after each major transformation
- ✔ **Idempotent writes**: Use idempotent write semantics (Delta MERGE or overwriteDynamic on partitioned tables)
- ✔ **Quality metrics**: Compute row-level quality metrics with Great Expectations or Deequ and fail job when thresholds exceeded
- ✔ **External configs**: Make all configurable values (paths, thresholds, cluster sizing) live in external configuration (YAML/JSON, environment variables via `os.environ`, or Databricks Widgets); no literals in code

## III. Preferred Patterns (Recommended)

The LLM **should adopt** these patterns unless user overrides:

- ➜ **Push filters early**: Apply `where`, `filter` before joins or aggregations
- ➜ **Broadcast sizing**: Broadcast joins only when broadcast side is < 10 MiB
- ➜ **Select over withColumn**: Use `select` with aliases over `withColumn` chains for readability and optimizer push-down
- ➜ **Cache management**: Cache only when dataframe reuse count > 2 and unpersist as soon as last use
- ➜ **Function size**: Name functions in `snake_case` (Python) / `camelCase` (Scala) and limit to ≤75 LOC each
- ➜ **Typed literals**: Prefer typed lit values (`F.lit(0).cast("int")`) over raw literals

---

**Version**: 1.0.0
**Last Updated**: 2025-10-07
