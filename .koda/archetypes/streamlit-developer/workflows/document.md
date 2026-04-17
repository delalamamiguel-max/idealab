---
description: Generate comprehensive documentation for Streamlit application including setup, architecture, and usage (Streamlit Developer)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype streamlit-developer --json ` and parse for ENV_VALID.

### 2. Load Configuration
- The constitution rules are already loaded in context above.

### 3. Parse Input
Extract from $ARGUMENTS: project path, target audience (users/developers), deployment details.

### 4. Analyze Project
- Scan `requirements.txt` for dependencies.
- Scan `app.py` and `pages/` for features and flow.
- Scan `.streamlit/secrets.toml.example` for configuration needs.

### 5. Generate Documentation

**README.md**:
- **Title & Description**: Clear overview of the app.
- **Prerequisites**: Python version, Snowflake account, etc.
- **Installation**: `pip install -r requirements.txt`.
- **Configuration**: How to set up `.streamlit/secrets.toml`.
- **Running**: `streamlit run app.py`.
- **Architecture**: Diagram of data flow and component structure.

**User Guide**:
- Screenshots of key workflows.
- Explanation of input parameters.
- Interpretation of outputs/visualizations.

**Developer Guide**:
- Explanation of state management strategy.
- Explanation of caching strategy.
- How to add new pages/components.

### 6. Final Review
- Verify all commands are copy-pasteable and correct.
- Verify no secrets are leaked in documentation.

## Error Handling

**Missing Project Path**: Request the path to the Streamlit application.

**No app.py Found**: Search for main entry point and ask user to confirm.

**Missing Dependencies**: Generate placeholder sections with TODO markers.

## Examples

### Example 1: Full Documentation

```
/document-streamlit-developer "
Generate full docs for sales-dashboard app at ./apps/sales.
Target: both users and developers.
"
```

### Example 2: User Guide Only

```
/document-streamlit-developer "
Create user-facing guide for fraud-detector app.
Focus on workflows and interpretation of results.
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/streamlit-developer/streamlit-developer-constitution.md`
- **Brand Guidelines**: Constitution Section I
- **Related**: scaffold-streamlit-developer, refactor-streamlit-developer
