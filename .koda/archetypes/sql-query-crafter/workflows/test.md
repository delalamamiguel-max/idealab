---
description: Generate test harness for SQL queries with data validation (SQL Query Crafter)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype sql-query-crafter --json ` and parse for SNOWFLAKE_VERSION, PYTHON_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/templates/env-config.yaml` for test configuration

### 3. Parse Input
Extract from $ARGUMENTS: SQL file path or inline query, testing framework (pytest, Snowpark, custom), coverage goals (query validation, result validation, performance), test data requirements. Request clarification if incomplete.

### 4. Analyze Code

Identify testable components: input parameters ({{var.*}} placeholders), CTEs and subqueries, JOIN conditions, aggregations and calculations, WHERE filters, expected output schema, edge cases (empty results, NULL values, large datasets).

Determine test scenarios: positive cases (valid inputs, expected results), negative cases (invalid inputs, constraint violations), edge cases (boundary values, NULL handling, empty sets), performance cases (execution time, resource usage).

Report test coverage plan with test cases and data requirements.

### 5. Generate Test Suite

Create comprehensive test suite with test framework setup, test data fixtures (sample input tables, expected output data), test cases (query validation tests, result validation tests, schema validation tests, edge case tests, performance tests), helper functions (data comparison, schema validation, performance measurement).

Include complete test code:
```python
import pytest
from snowflake.snowpark import Session
import pandas as pd

@pytest.fixture
def snowflake_session():
    """Create Snowflake session for testing"""
    return Session.builder.configs({
        "account": "test_account",
        "user": "test_user",
        "warehouse": "test_wh"
    }).create()

@pytest.fixture
def sample_data():
    """Create sample test data"""
    return {
        "customers": pd.DataFrame({
            "customer_id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "region": ["US", "EU", "US"]
        }),
        "orders": pd.DataFrame({
            "order_id": [101, 102, 103],
            "customer_id": [1, 1, 2],
            "amount": [100, 200, 150],
            "order_date": ["2024-01-01", "2024-01-02", "2024-01-03"]
        })
    }

def test_query_returns_expected_schema(snowflake_session):
    """Test query returns correct column names and types"""
    result = snowflake_session.sql("SELECT * FROM result_table")
    expected_columns = ["customer_id", "total_amount", "order_count"]
    assert list(result.columns) == expected_columns

def test_query_with_valid_parameters(snowflake_session, sample_data):
    """Test query with valid date range"""
    query = """
    SELECT customer_id, SUM(amount) as total
    FROM orders
    WHERE order_date >= '2024-01-01' AND order_date <= '2024-01-31'
    GROUP BY customer_id
    """
    result = snowflake_session.sql(query).collect()
    assert len(result) > 0
    assert result[0]["TOTAL"] == 300  # Alice's total

def test_query_handles_empty_result(snowflake_session):
    """Test query with no matching records"""
    query = "SELECT * FROM orders WHERE order_date > '2099-12-31'"
    result = snowflake_session.sql(query).collect()
    assert len(result) == 0

def test_query_handles_null_values(snowflake_session):
    """Test query properly handles NULL values"""
    query = "SELECT COALESCE(amount, 0) as amount FROM orders"
    result = snowflake_session.sql(query).collect()
    assert all(r["AMOUNT"] is not None for r in result)

def test_query_performance(snowflake_session):
    """Test query completes within acceptable time"""
    import time
    start = time.time()
    snowflake_session.sql("SELECT * FROM large_table LIMIT 1000").collect()
    duration = time.time() - start
    assert duration < 5.0, f"Query took {duration}s, expected < 5s"
```

### 6. Add Recommendations

Include recommendations for test data management (use test schemas, create reusable fixtures, version control test data), CI/CD integration (run tests on PR, automated regression testing, performance benchmarks), coverage improvements (add more edge cases, test error conditions, validate business rules), monitoring (track test execution time, monitor test flakiness, alert on failures).

Provide summary with test coverage metrics and next steps.

### 7. Validate and Report


Generate test execution report. Report completion with test count, coverage estimate, setup instructions.

## Error Handling

**Insufficient Code Information**: Request complete SQL query or file path.

**No Test Framework Specified**: Suggest pytest with Snowpark as default.

**Missing Test Data**: Provide guidance on creating test fixtures.

## Examples

**Example 1: Query Validation**
```
/test-sql Generate tests for customer_aggregation.sql

Output: Test suite with 8 tests covering schema validation, result validation, NULL handling, empty results
Coverage: 85% of query logic tested
```

**Example 2: Performance Testing**
```
/test-sql Create performance tests for daily_report.sql

Output: Performance test suite with baseline metrics, load testing, timeout validation
Benchmarks: Query completes in <5s for 1M rows
```

**Example 3: Edge Cases**
```
/test-sql Add edge case tests for date_range_query.sql

Output: Tests for boundary dates, invalid dates, NULL dates, timezone handling
Coverage: All edge cases covered
```

## References

Original: `vibe_cdo/sql_query_crafter/prompts/05_test_harness_prompt.md` | Constitution: `../../sql-query-crafter-constitution.md`
