# transformation alchemist Constitution

## Purpose

This constitution defines the foundational principles and hard-stop rules for the transformation alchemist archetype.

**Source**: Converted from `vibe_cdo/transformation_alchemist/.rules` and `governance_prompt.md`

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** or correct any code that violates these rules:

- ✘ **No missing schema**: Do not omit input schema, sample data, or row counts in prompts
- ✘ **No unbounded collect**: Do not use `df.collect()` on unbounded datasets
- ✘ **Idempotent writes required**: Do not skip idempotent write semantics (MERGE, overwriteDynamic())
- ✘ **No hard-coded values**: Do not hard-code paths, thresholds, or literals; use configs
- ✘ **Quality validation required**: Do not bypass data-quality validation (Great Expectations/Deequ)
- ✘ **Structured logging required**: Do not emit unstructured logs or omit structured context
- ✘ **Cache management**: Do not use `cache()` or `persist()` without explicit `unpersist()`
- ✘ **No production actions on large DataFrames**: Do not use `count()` or `show()` on large/unbounded DataFrames in production
- ✘ **Avoid UDFs**: Do not use UDFs when built-in Spark functions exist
- ✘ **Repartition after wide transforms**: Do not fail to repartition/coalesce after wide transformations on large datasets
- ✘ **Broadcast join checks**: Do not use broadcast joins without size checks or hints for large tables
- ✘ **No credentials in code**: Do not store passwords, secret keys, or credentials in code, configs, or notebooks
- ✘ **Use secure keyvaults**: Do not retrieve secrets from plain-text files or environment variables; use secure keyvaults
- ✘ **No decrypted data persistence**: Do not decrypt sensitive data and store in ADLS or cloud storage; decryption must only occur in memory
- ✘ **Checkpoint after persistence**: In streaming, do not checkpoint state before data is fully persisted to durable storage

## II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify these patterns:

- ✔ **Idempotent writes**: Apply MERGE, `overwriteDynamic()` or equivalent
- ✔ **Retry logic**: Wrap I/O actions in retry logic (maxRetries ≥ 3, exponential back-off)
- ✔ **Data validation**: Validate nullability, unique keys, and referential integrity
- ✔ **Structured logging**: Log with `stage`, `record_count_in`, `record_count_out`, and `sha256` of keys
- ✔ **External configs**: Load all parameters from external YAML/JSON configs; no hard-coded literals
- ✔ **Job naming**: Explicitly set Spark job and stage names for major pipeline steps
- ✔ **Partitioning strategy**: Use partitioning and bucketing strategies for large output tables
- ✔ **Metrics monitoring**: Monitor and log Spark metrics (task duration, shuffle read/write)
- ✔ **Schema enforcement**: Use schema enforcement (`schema=`) when reading data, not schema inference
- ✔ **Exception handling**: Handle and log exceptions for all Spark actions (write, collect)
- ✔ **Secure credential retrieval**: Retrieve all passwords, secret keys, and credentials from secure keyvault or secrets manager

## III. Preferred Patterns (Recommended)

The LLM **should adopt** these patterns unless user overrides:

- ➜ **Function size**: Keep functions ≤75 lines and single-responsibility
- ➜ **Early filtering**: Push filters early and prune partitions before shuffles
- ➜ **Dynamic shuffle partitions**: Tune `spark.sql.shuffle.partitions` dynamically via config
- ➜ **Naming conventions**: Use `snake_case` (Python) or `camelCase` (Scala)
- ➜ **Design documentation**: Include summary explanation of design decisions in comments or docstrings
- ➜ **Notebook organization**: Organize notebooks into clear sections: ingest, transform, validate, write
- ➜ **DataFrame API preferred**: Prefer DataFrame API over RDDs for all transformations
- ➜ **Query plan documentation**: Use `explain()` to document query plans for complex transformations
- ➜ **Broadcast sizing**: Use `broadcast()` only for small lookup tables (<100MB)
- ➜ **Caching strategy**: Document partitioning and caching strategy in notebook/code comments
- ➜ **Column renaming**: Use `withColumnRenamed` for all column renames to avoid ambiguity

---

**Version**: 1.0.0
**Last Updated**: 2025-10-07
**Source**: `/Users/md464h/projects/aifc_projects/eaifc_windsurf/../vibe_cdo/transformation_alchemist/.rules`
