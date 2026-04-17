---
description: Generate SQL scaffold using named CTEs with parameterized filters (SQL Query Crafter)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype sql-query-crafter --json ` and parse for SNOWFLAKE_VERSION, WAREHOUSE, ROLE, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/templates/env-config.yaml` for var.warehouse, var.role, var.date_start, var.date_end, var.max_runtime_secs

### 3. Parse Input
Extract from $ARGUMENTS: input tables with schemas, transformation requirements, business logic, output requirements. Request clarification if incomplete.

### 3.5. Determine Syntax
Determine the target environment syntax:
- If target app is Legacy/Shell based: Use `${VAR}` style.
- If target app is Modern/Python based (e.g. Airflow/dbt): Use `{{var}}` style.
- Default to `{{var}}` if not specified.

### 4. Validate Constraints
Check against hard-stop rules:
- ✘ Refuse SELECT * on large tables without justification
- ✘ Refuse hard-coded literals (dates, table names)
- ✘ Refuse CROSS JOIN without justification
- ✘ Refuse unmasked PII
If violated, explain clearly and suggest compliant alternative.

### 5. Generate SQL Scaffold

Create SQL with: session setup (USE WAREHOUSE/ROLE, ALTER SESSION SET QUERY_TAG), instrumentation markers (\qecho SCRIPT_START/END, STEP:10/20/30), and CTE structure:

```sql
WITH raw_data AS (
  SELECT col1, col2 FROM {{var.source_table}}
  WHERE date_col >= '{{var.date_start}}' AND date_col <= '{{var.date_end}}'
),
transform AS (
  SELECT key_col, calculated_col FROM raw_data
),
aggregate AS (
  SELECT key_col, SUM(value_col) AS total FROM transform GROUP BY key_col
)
SELECT * FROM aggregate;
```

Apply mandatory patterns: snake_case, explicit columns, parameterized values (use syntax detected in Step 3.5), early filters, fully qualified table names, CTE decomposition, TODO comments. For complex transforms, use temp tables. Add explanation comment block at top.

### 5.5. Validate SQL Identifiers

Run `${ARCHETYPES_BASEDIR}/scripts/python/validate-sql-keywords.py --schema <script_name>.sql --engine snowflake --json` to check table and column names against reserved keywords.

**If violations found**:
- Report identifiers conflicting with SQL reserved keywords or ORM attributes
- Apply safe alternatives automatically:
  - `metadata` → `workflow_metadata`
  - `query` → `search_query`
  - `session` → `user_session`
  - `timestamp` → `event_timestamp`
- Update generated SQL with corrected identifiers
- Add comment noting the change and reason

**Validation Report**:
```
✓ SQL Identifiers: No reserved keyword conflicts
  Tables: customer_data, order_summary
  Columns: customer_id, workflow_metadata, event_timestamp
```

### 6. Add Recommendations

Include inline comments for clustering hints, caching suggestions, and cost estimates where applicable.

### 7. Validate and Report


Generate optional test harness if requested. Report completion with file paths, applied guardrails, next steps, and recommendations.

## Error Handling

**Hard-Stop Violations**: Explain violation, suggest compliant alternative, request reformulation or justification.

**Incomplete Input**: List missing information (table schemas, transformation requirements, output requirements), provide example of well-formed input.

**Environment Failure**: Report missing configuration, list requirements, suggest running setup-env.sh and updating env-config.yaml.

## Examples

**Customer Spend**: `/scaffold Generate SQL to analyze customer spend. Input: customer(id, name, signup_dt), orders(id, cust_id, amount, order_dt). Calculate total spend per customer between {{var.date_start}} and {{var.date_end}}. Flag VIP customers with spend > $500.`
Output: CTEs for filtering, joining, and aggregating with VIP flag.

**Time-Series**: `/scaffold Create SQL for daily sales rollup. Input: transactions(id, product_id, sale_amount, sale_timestamp). Output daily totals by product for last 30 days with 7-day moving average.`
Output: CTEs for date filtering, grouping, and window function.

**SCD Type 2**: `/scaffold Generate SCD Type 2 merge logic. Source: customer_updates(id, name, email, updated_at). Target: customer_history(id, name, email, valid_from, valid_to, is_current).`
Output: CTEs for change detection and MERGE statement scaffold.

## References

Original: `prompts/01_scaffold_prompt.md` | Constitution: `../../sql-query-crafter-constitution.md`
