---
description: Refactor SQL query to apply best practices and patterns (SQL Query Crafter)
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
Extract from $ARGUMENTS: existing SQL file path or inline SQL code, refactoring goals (CTEs, parameterization, performance, etc.), constraints. Request clarification if incomplete.

### 4. Analyze Existing Code
Load and analyze existing SQL:
- Identify hard-stop rule violations (SELECT *, hard-coded literals, CROSS JOIN, unmasked PII)
- Identify missing mandatory patterns (CTEs, snake_case, parameterization, early filters)
- Identify opportunities for preferred patterns (clustering hints, caching, cost optimization)
- Calculate technical debt score based on violations

Report findings:
```
Analysis Results:
✘ Hard-Stop Violations: [count] found
  - Line 5: Hard-coded date literal '2024-01-01'
  - Line 8: SELECT * without justification
✔ Mandatory Patterns Missing: [count]
  - CTE decomposition not used
  - Parameterization missing
➜ Preferred Patterns: [count] opportunities
  - Clustering hints could improve performance
  - Early filter pushdown possible
```

### 5. Generate Refactored SQL

Create refactored SQL applying:

**Hard-Stop Fixes**:
- Replace SELECT * with explicit column list
- Replace hard-coded literals with parameters (using target-appropriate syntax like {{var}} or ${VAR})
- Replace comma-joins with explicit JOIN syntax
- Add PII masking where needed
- Remove or justify CROSS JOINs

**Mandatory Patterns**:
- Decompose into named CTEs (extract, transform, aggregate)
- Apply snake_case to all aliases and CTE names
- Push filters early (WHERE clauses in extract CTE)
- Use fully qualified table names (database.schema.table)
- Add parameterization via {{var}} or ${VAR} syntax
- Include explanation paragraph at top

**Preferred Patterns**:
- Add clustering hints on frequently filtered columns
- Add caching suggestions for large scans
- Annotate with cost estimates
- Provide EXPLAIN plan recommendations
- Add inline TODO comments for future improvements

**Structure**:
```sql
-- Purpose: [Brief description]
-- Refactored: [Date] - Applied CTE decomposition, parameterization, performance hints
-- Expected Runtime: <{{var.max_runtime_secs}}s
-- Estimated Cost: $[X] per TB scanned

-- Session setup
USE WAREHOUSE {{var.warehouse}};
USE ROLE {{var.role}};
ALTER SESSION SET QUERY_TAG = 'refactored_query';

-- Extract: Raw data with early filters
WITH extract AS (
  SELECT 
    customer_id,
    order_date,
    order_amount
  FROM {{var.database}}.{{var.schema}}.{{var.orders_table}}
  WHERE order_date >= '{{var.date_start}}'
    AND order_date <= '{{var.date_end}}'
  -- Clustering hint: Consider clustering on order_date
),

-- Transform: Business logic
transform AS (
  SELECT
    customer_id,
    DATE_TRUNC('month', order_date) AS order_month,
    SUM(order_amount) AS monthly_total
  FROM extract
  GROUP BY customer_id, DATE_TRUNC('month', order_date)
),

-- Aggregate: Final calculations
aggregate AS (
  SELECT
    customer_id,
    order_month,
    monthly_total,
    SUM(monthly_total) OVER (
      PARTITION BY customer_id 
      ORDER BY order_month
    ) AS cumulative_total
  FROM transform
)

SELECT * FROM aggregate
ORDER BY customer_id, order_month;

-- TODO: Consider adding result caching for repeated queries
-- TODO: Monitor query performance and adjust clustering if needed
```

### 6. Add Recommendations

Include inline comments for:
- **Performance**: Clustering keys, caching strategies, partition pruning
- **Cost**: Query cost estimates, optimization opportunities
- **Maintainability**: Modularization suggestions, reusable CTEs
- **Quality**: Data validation checks, edge case handling

Provide summary of improvements:
```
Refactoring Summary:
✅ Fixed 3 hard-stop violations
✅ Applied 5 mandatory patterns
✅ Implemented 4 preferred patterns

Performance Impact:
- Expected runtime reduction: 40% (estimated)
- Cost reduction: 25% (fewer full table scans)
- Maintainability: Significantly improved with CTEs

Next Steps:
1. Test refactored query with sample data
2. Compare EXPLAIN plans (before/after)
3. Monitor performance in production
4. Consider adding to shared SQL template library
```

### 7. Validate and Report


Generate optional test cases comparing original vs refactored output. Report completion with file paths, applied improvements, performance estimates, next steps.

## Error Handling

**Hard-Stop Violations in Original**: Explain each violation clearly, show before/after comparison, highlight compliance with constitution.

**Incomplete Input**: List missing information (SQL file path or code, refactoring goals, constraints), provide well-formed example.

**Environment Failure**: Report missing Snowflake configuration, suggest running validate-env.sh and updating env-config.yaml.

## Examples

**Example 1: CTE Decomposition**
```
/refactor-sql Refactor sales_rolling.sql to use CTEs instead of subqueries

Input SQL:
SELECT c.id, c.name, (SELECT SUM(amt) FROM orders WHERE cust_id = c.id) AS total
FROM customer c;

Output: Refactored with extract and transform CTEs, parameterized dates, clustering hints
```

**Example 2: Parameterization**
```
/refactor-sql Remove hard-coded dates from customer_analysis.sql and add parameters

Input SQL:
SELECT * FROM orders WHERE order_date BETWEEN '2024-01-01' AND '2024-01-31';

Output: Refactored with {{var.date_start}}/{{var.date_end}}, explicit columns, early filters
```

**Example 3: Performance Optimization**
```
/refactor-sql Optimize slow query in monthly_sales.sql with clustering and caching

Input SQL:
SELECT customer_id, SUM(amount) FROM large_orders GROUP BY customer_id;

Output: Refactored with CTEs, clustering hints on frequently filtered columns, cost annotations
```

## References

Original: `vibe_cdo/sql_query_crafter/prompts/02_refactor_prompt.md` | Constitution: `../../sql-query-crafter-constitution.md`
