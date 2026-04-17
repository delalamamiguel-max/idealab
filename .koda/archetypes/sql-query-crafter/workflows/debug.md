---
description: Debug SQL query errors and performance issues (SQL Query Crafter)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype sql-query-crafter --json ` and parse for SNOWFLAKE_VERSION, WAREHOUSE, ROLE, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/templates/env-config.yaml` for var.warehouse, var.role, var.max_runtime_secs

### 3. Parse Input
Extract from $ARGUMENTS: SQL file path or inline query, error message (compilation error, runtime error, performance issue), symptoms (query fails, returns wrong results, runs too slow), context (when it started, what changed, expected behavior). Request clarification if incomplete.

### 4. Analyze Problem

**Root Cause Analysis**:

Load SQL and error information, then identify error category:

**Compilation Errors**:
- Syntax errors (missing comma, unclosed parenthesis, invalid keyword)
- Column not found (typo, wrong table alias, missing join)
- Table/view not found (wrong schema, missing qualification)
- Ambiguous column reference (same column in multiple tables)
- Invalid function usage (wrong parameters, unsupported function)

**Runtime Errors**:
- Division by zero
- Data type mismatch
- NULL value violations
- Constraint violations
- Timeout errors

**Logic Errors** (wrong results):
- Incorrect JOIN conditions
- Missing WHERE filters
- Wrong GROUP BY columns
- Incorrect aggregation logic
- Date/time calculation errors

**Performance Issues**:
- Full table scans (missing indexes, no partition pruning)
- Cartesian products (missing JOIN conditions)
- Inefficient subqueries
- No query result caching
- Large data shuffles

Check against constitution rules for common violations.

Report findings:
```
Root Cause Analysis:
Error Type: [Compilation/Runtime/Logic/Performance]
Root Cause: [Specific issue identified]
Location: Line [X], Column [Y]
Impact: [Query fails/Wrong results/Slow performance]

Contributing Factors:
- [Factor 1]
- [Factor 2]

Constitution Violations:
- [Any hard-stop or mandatory pattern violations]
```

### 5. Generate Fix

Create fixed SQL addressing root cause:

**For Compilation Errors**:
- Fix syntax issues
- Correct column/table references
- Add missing qualifications
- Resolve ambiguous references
- Fix function calls

**For Runtime Errors**:
- Add NULL handling (COALESCE, NULLIF)
- Add data type conversions (CAST, TRY_CAST)
- Add defensive checks (CASE WHEN)
- Add error handling

**For Logic Errors**:
- Correct JOIN conditions
- Add missing filters
- Fix GROUP BY logic
- Correct aggregations
- Fix date calculations

**For Performance Issues**:
- Add WHERE clause filters early
- Optimize JOIN order
- Add clustering hints
- Use CTEs to avoid repeated scans
- Add result caching hints

Include explanation:
```sql
-- FIXED: [Brief description of fix]
-- ROOT CAUSE: [What was wrong]
-- SOLUTION: [What was changed]

-- Original problematic code (commented out):
-- SELECT c.id, o.amount
-- FROM customer c, orders o  -- ✘ Cartesian product
-- WHERE c.region = 'US';

-- Fixed code:
SELECT 
    c.customer_id,
    o.order_amount
FROM {{var.database}}.{{var.schema}}.customer c
INNER JOIN {{var.database}}.{{var.schema}}.orders o 
    ON c.customer_id = o.customer_id  -- ✓ Proper JOIN condition
WHERE c.region = '{{var.region}}'
    AND o.order_date >= '{{var.date_start}}';
```

### 6. Add Recommendations

Include recommendations for:

**Prevention**:
- Add data validation checks
- Implement unit tests
- Use query linting tools
- Add monitoring alerts

**Testing**:
- Test with edge cases (NULL values, empty results, large datasets)
- Compare results with original (if logic fix)
- Run EXPLAIN to verify performance

**Monitoring**:
- Set up query performance monitoring
- Add alerting for slow queries
- Track query execution history

Provide summary:
```
Debug Summary:
✅ Root cause identified: [Issue]
✅ Fix applied: [Solution]
✅ Tested: [Test results]

Prevention Strategies:
1. [Strategy 1]
2. [Strategy 2]
3. [Strategy 3]

Next Steps:
1. Deploy fixed query to production
2. Monitor performance for 24 hours
3. Add regression test to prevent recurrence
```

### 7. Validate and Report


Generate optional test cases. Report completion with root cause, fix applied, testing recommendations, monitoring setup.

## Error Handling

**Insufficient Error Information**: Request complete error message, stack trace, or query execution history.

**Cannot Reproduce**: Request environment details, sample data, or execution context.

**Multiple Possible Causes**: Provide systematic debugging steps to isolate root cause.

## Examples

**Example 1: Column Not Found**
```
/debug-sql Fix "column 'customer_name' not found" error in sales_report.sql

Error: SQL compilation error: invalid identifier 'CUSTOMER_NAME'
Root Cause: Column name typo (should be 'cust_name')
Fix: Corrected column reference, added table qualification
```

**Example 2: Performance Issue**
```
/debug-sql Query timing out after 5 minutes in daily_aggregation.sql

Error: Query exceeded maximum execution time
Root Cause: Full table scan on 100M row table, no partition pruning
Fix: Added date filter, clustering hint, result caching
Performance: Reduced from 5min to 15sec
```

**Example 3: Wrong Results**
```
/debug-sql Customer totals are incorrect in monthly_summary.sql

Error: Results don't match expected values
Root Cause: Missing GROUP BY column causing incorrect aggregation
Fix: Added customer_id to GROUP BY, verified logic
Validation: Results now match expected totals
```

## References

Original: `vibe_cdo/sql_query_crafter/prompts/03_debug_prompt.md` | Constitution: `../../sql-query-crafter-constitution.md`
