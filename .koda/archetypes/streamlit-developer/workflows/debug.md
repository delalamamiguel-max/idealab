---
description: Debug Streamlit application errors including runtime exceptions, state issues, and performance bottlenecks (Streamlit Developer)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype streamlit-developer --json ` and parse for debugging tools availability.

### 2. Load Configuration
- The constitution rules are already loaded in context above.

### 3. Parse Input
Extract from $ARGUMENTS: error description, error messages/stack traces, affected pages/components, steps to reproduce, environment. Request clarification if incomplete.

### 4. Categorize Error Type

Analyze error to determine category:

**Runtime Errors**:
- Python exceptions (KeyError, ValueError, etc.)
- Streamlit API misuse (e.g., calling widget outside of script run)
- Data loading failures

**State Management Issues**:
- Session state lost on rerun
- Widget state not persisting
- Infinite rerun loops

**Performance Issues**:
- Slow page loads
- Unnecessary data reloading (caching issues)
- High memory usage

**Layout/UI Issues**:
- Elements overlapping or misaligned
- CSS injection failures
- Theme inconsistencies

### 5. Diagnose and Fix

**For Runtime Errors**:
- Analyze stack trace.
- Check input data types and values.
- Verify API usage against Streamlit documentation.
- **Action**: Propose code fix with error handling (`try-except`).

**For State Management**:
- Check `st.session_state` initialization.
- Verify callback functions.
- Check for key collisions in widgets.
- **Action**: Refactor state logic to ensure persistence.

**For Performance**:
- Check usage of `@st.cache_data` and `@st.cache_resource`.
- Identify expensive computations inside the main script flow.
- **Action**: Move expensive logic to cached functions.

**For Layout/UI**:
- Check `st.columns` and `st.container` usage.
- Verify custom CSS compatibility.
- **Action**: Adjust layout structure or CSS.

### 6. Verify Fix
- Explain how the fix addresses the root cause.
- Ensure no new issues are introduced (e.g., regression).
- Verify compliance with constitution (no hardcoded secrets, brand colors).

## Error Handling

**No Error Message Provided**: Request exact error message and stack trace.

**Cannot Reproduce**: Ask for environment details (Python version, Streamlit version, OS).

**Multiple Issues**: Prioritize by severity - security > runtime > performance > UI.

## Examples

### Example 1: Session State Error

```
/debug-streamlit-developer "
KeyError: 'user_id' in session_state on page reload.
Using st.session_state['user_id'] in callback.
"
```

### Example 2: Performance Issue

```
/debug-streamlit-developer "
Dashboard takes 30+ seconds to load.
Loading data from Snowflake on every page interaction.
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/streamlit-developer/streamlit-developer-constitution.md`
- **State Management**: Constitution Section II - Application Architecture
- **Related**: scaffold-streamlit-developer, refactor-streamlit-developer
