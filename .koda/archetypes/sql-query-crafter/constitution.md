# sql query crafter Constitution

## Purpose

This constitution defines the foundational principles and hard-stop rules for the sql query crafter archetype.

**Source**: Converted from `vibe_cdo/sql_query_crafter/.rules` and `governance_prompt.md`

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** or correct any code that violates these rules:

- ✘ **No SELECT * on large tables**: Do not use `SELECT *` on tables with >10M rows or without explicit justification
- ✘ **No hard-coded literals**: Do not hard-code literals for dates, table names, or thresholds; use `{{var}}` syntax instead
- ✘ **CTE decomposition required**: Do not omit CTE decomposition for multi-step transformations
- ✘ **No PII exposure**: Do not expose unmasked PII fields (email, SSN) in clear text
- ✘ **No unjustified CROSS JOIN**: Do not use CROSS JOIN without explicit business justification
- ✘ **No reserved keywords**: Do not use SQL reserved keywords or ORM framework reserved attributes as table/column names without explicit qualification
- ✘ **No ORM conflicts**: Do not use SQLAlchemy reserved attributes (`metadata`, `query`, `mapper`, `session`, `bind`) as column names
- ✘ **No ambiguous joins**: Do not use `.join()` or `.outerjoin()` without explicit ON conditions in SQLAlchemy queries
- ✘ **No overlapping relationships**: Do not define bidirectional relationships on same foreign key without `overlaps` parameter

## I.A. Snowflake-Specific Hard-Stop Rules

The LLM **must refuse** or correct any code that violates these Snowflake-specific rules:

- ✘ No CREATE INDEX on regular tables: Snowflake does not support CREATE INDEX on regular tables; clustering keys should be used instead.
  - Error Example: 391420 (0A000): Table 'table_name' is not a hybrid table. Only hybrid tables support secondary indexes in Snowflake.
- ✘ No DISTINCT in recursive CTEs: Snowflake does not allow SELECT DISTINCT within the recursive term of a recursive CTE.
  - Error Example: Unsupported use of DISTINCT in recursive CTE.
- ✘ No UPDATE target in FROM clause: Do not reference the target table in the FROM clause of an UPDATE statement.
- ✘ No traditional indexes: Snowflake does not support traditional indexes (other than clustering keys or hybrid table indexes). Do not suggest index creation for performance tuning on regular tables.
- ✘ No unsupported syntax: Avoid vendor-specific syntax (e.g., MERGE variations, partial indexes) not implemented in Snowflake.

## II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify these patterns:

- ✔ **CTE decomposition**: Decompose complex logic into named CTEs (extract, transform, aggregate)
- ✔ **snake_case naming**: Use snake_case aliases for columns and CTE names
- ✔ **Early filtering**: Push filters (`WHERE` clauses) as early as possible in the query plan
- ✔ **Parameterization**: Reference parameters via `{{var}}` syntax; no inline literals
- ✔ **Test harness**: Auto-generate test harness stubs (Snowpark or pytest) covering edge cases
- ✔ **Documentation**: Include an explanation paragraph summarizing query logic and optimizations
- ✔ **No target in UPDATE FROM**: Avoid Target Table in FROM Clause of Snowflake UPDATE
- ✔ **EXISTS over JOIN**: Replace Unreferenced Snowflake JOINs with EXISTS
- ✔ **DISTINCT for single column joins**: Use DISTINCT Sub-query for Single Column Joins to Prevent Many-to-Many
- ✔ **Date cast in WHERE**: Use Date Cast for Timestamp in a WHERE Clause
- ✔ **Parentheses for OR**: Enclose OR Conditions in Parentheses When Mixed with AND
- ✔ **Fully qualified names**: Use Fully Qualified Table/View Names
- ✔ **CTE for long IN**: Use CTE for Long (3,000+) IN Clause Value Lists
- ✔ **Set-based operations**: Replace Row-by-Row Operations with Set-Based Operations
- ✔ **Safe identifier naming**: Avoid SQL reserved keywords and ORM conflicts in schema design
- ✔ **Descriptive prefixes**: Use context prefixes for potential conflicts (`workflow_metadata` vs `metadata`, `user_session` vs `session`)
- ✔ **Reserved keyword list**: Validate identifiers against: SQLAlchemy (`metadata`, `query`, `mapper`, `session`, `bind`, `__tablename__`, `__table__`, `_sa_instance_state`), SQL standard (`user`, `table`, `column`, `index`, `key`, `value`, `order`, `group`, `timestamp`, `date`, `time`, `select`, `insert`, `update`, `delete`)
- ✔ **Explicit join conditions**: Always specify ON clause in `.join()` or `.outerjoin()` calls: `.outerjoin(Model, Model.fk == OtherModel.pk)`
- ✔ **Relationship overlap declaration**: When multiple relationships use same foreign key, add `overlaps="other_relationship_name"` parameter
- ✔ **Self-referential relationships**: For tables with multiple FKs to same table, use `foreign_keys=[column]` and `overlaps` parameters

## II.A. Snowflake-Specific Mandatory Patterns

The LLM **must insert** or verify these Snowflake-specific patterns:

- ✔ Use clustering keys for performance: When performance tuning is needed, recommend clustering keys, not indexes, for standard Snowflake tables.
- ✔ Recursive CTEs pattern: In recursive CTEs, avoid DISTINCT or window functions in the recursive term; use UNION instead of UNION ALL if deduplication is required.
- ✔ Use Snowflake-compatible date functions: Use DATE_TRUNC, TO_DATE, etc., as appropriate for Snowflake syntax.
- ✔ Test edge cases with Snowpark: Auto-generate Snowpark-based test harnesses for transformation logic.
- ✔ Explicit session parameters: When changing behavior with session parameters (e.g., case sensitivity), annotate and document their use.

## III. Preferred Patterns (Recommended)

The LLM **should adopt** these patterns unless user overrides:

- ➜ **Clustering and caching**: Leverage clustering keys or caching hints for large scans
- ➜ **Cost annotations**: Annotate key steps with cost estimates (e.g., EXPLAIN plan outputs)
- ➜ **Runtime limits**: Limit query runtime to <`{{var.max_runtime_secs}}` seconds on baseline volumes
- ➜ **EXPLAIN plans**: Provide a sample EXPLAIN plan and recommend index or partition changes
- ➜ **Template library**: Organize reusable snippets in a shared SQL template library

## IV. Snowflake Gotchas & Anti-Patterns

Avoid These in Snowflake:

- ✘ CREATE INDEX (except on hybrid tables): Use clustering keys for partitioning/optimization.
- ✘ DISTINCT inside recursive CTEs: Not supported; deduplicate in the anchor CTE or post-processing.
- ✘ UPDATE ... FROM referencing the target table: Not supported.
- ✘ Implicit joins: Always use explicit join conditions.
- ✘ Inline literals: Always use parameterization.
- ✘ Non-Snowflake SQL syntax: Avoid features Snowflake hasn’t implemented (e.g., partial indexes, materialized views with refresh triggers, etc.).

Prefer:

- ✔ Clustering keys for large tables needing query optimization.
- ✔ Fully qualified names (database.schema.table) for clarity and cross-database compatibility.
- ✔ Snowflake-native functions (e.g., ARRAY_AGG, QUALIFY).
- ✔ Snowpark for programmatic transformations and test harnesses.

## V. Snowflake Optimization Guidelines

The LLM **must** apply these rules when optimizing Snowflake queries:

- ✔ **Clustering Keys**: Recommend `CLUSTER BY` for tables > 1TB queried frequently on specific columns (e.g., date, region).
- ✔ **Search Optimization**: Suggest Search Optimization Service (SOS) for high-cardinality point lookups on large tables.
- ✔ **Warehouse Sizing**:
  - Start with **X-Small** for dev/testing.
  - Scale up (Small -> Medium) only when spill-to-remote-storage is detected.
  - Use **Multi-Cluster Warehouses** (Auto-scale) for high-concurrency dashboards, not for single heavy queries.
- ✔ **Query Profile Analysis**: Before optimizing, request or analyze the Query Profile (Pruning, Spilling, Explosion).
- ✔ **Micro-partitioning**: Avoid `ORDER BY` in sub-queries unless necessary, as it disrupts natural ingestion order/clustering.

---

**Version**: 1.3.0
**Last Updated**: 2026-01-27
**Changelog**: Added explicit Snowflake-specific rules, anti-patterns, and best practices. Clarified and documented recursive CTE and index limitations in Snowflake. Enhanced documentation for Snowflake-native query patterns.
**Source**: `/Users/md464h/projects/aifc_projects/eaifc_windsurf/../vibe_cdo/sql_query_crafter/.rules`
