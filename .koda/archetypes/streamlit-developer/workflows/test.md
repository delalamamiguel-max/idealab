---
description: Create automated tests for Streamlit application using pytest and Streamlit AppTest (Streamlit Developer)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype streamlit-developer --json ` and parse for test runner availability (pytest).

### 2. Load Configuration
- The constitution rules are already loaded in context above.

### 3. Parse Input
Extract from $ARGUMENTS: application path, critical flows to test, existing test coverage.

### 4. Design Test Strategy
- **Unit Tests**: Test utility functions and data processing logic in isolation.
- **Integration Tests**: Test component interactions.
- **App Tests**: Use `streamlit.testing.v1.AppTest` to simulate user interactions.

### 5. Generate Test Code

**Unit Tests (`tests/unit/`)**:
- Create tests for `src/utils/` functions.
- Mock external dependencies (Snowflake, APIs).

**App Tests (`tests/e2e/`)**:
- Initialize `AppTest.from_file("app.py")`.
- Simulate user inputs (text input, button clicks).
- Assert on output (markdown content, dataframe presence, error messages).

Example:
```python
from streamlit.testing.v1 import AppTest

def test_app_loads():
    at = AppTest.from_file("app.py").run()
    assert not at.exception

def test_user_interaction():
    at = AppTest.from_file("app.py").run()
    at.text_input[0].set_value("test").run()
    assert "Processed: test" in at.markdown[0].value
```

### 6. Run Tests
- Execute `pytest tests/`.
- Report pass/fail status.

### 7. Final Review
- Ensure tests cover critical paths.
- Ensure tests are deterministic.

## Error Handling

**Missing pytest**: Add pytest to requirements.txt and install dependencies.

**AppTest Import Error**: Verify Streamlit version >= 1.18.0 for testing support.

**Test Failures**: Report failure details with suggestions for fixes.

## Examples

### Example 1: Full Test Suite

```
/test-streamlit-developer "
Create comprehensive tests for sales-dashboard app.
Critical flows: data loading, filtering, export.
"
```

### Example 2: Targeted Tests

```
/test-streamlit-developer "
Add tests for the new chart component in src/components/charts.py.
Focus on edge cases and error handling.
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/streamlit-developer/streamlit-developer-constitution.md`
- **Testing Guide**: Streamlit AppTest documentation
- **Related**: debug-streamlit-developer, scaffold-streamlit-developer
