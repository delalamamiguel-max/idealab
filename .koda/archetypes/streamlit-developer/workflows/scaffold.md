---
description: Generate ready-to-deploy data application with Streamlit following AT&T brand guidelines (Streamlit Developer)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype streamlit-developer --json ` and parse for PYTHON_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.

### 3. Parse Input
Extract from $ARGUMENTS: project name, description, features needed, data source (Snowflake/CSV/API), authentication requirement, CI/CD requirement, telemetry requirement. Request clarification if incomplete.

### 4. Validate Constraints
Check against hard-stop rules:
- ✘ Refuse if database credentials would be hardcoded
- ✘ Refuse if non-ATT fonts specified
- ✘ Refuse if AT&T Blue not dominant color
- ✘ Refuse if missing input validation requirements
- ✘ Refuse if accessibility requirements omitted
If violated, explain clearly and suggest compliant alternative.

### 5. Generate Project Structure

Create complete project with structure: Streamlit app, pages, components, utils, configuration.

**Project Structure**:
```
project_name/
├── .streamlit/
│   ├── config.toml             # Theme configuration
│   └── secrets.toml.example    # Secrets template
├── pages/                      # Multi-page app pages
├── src/
│   ├── components/             # Reusable UI components
│   └── utils/                  # Helper functions and data loaders
├── app.py                      # Main entry point
├── requirements.txt            # Python dependencies
└── README.md                   # Documentation
```

### 6. Implement Core Features
- **Theme**: Configure `.streamlit/config.toml` with AT&T colors.
- **Navigation**: Implement sidebar navigation if multi-page.
- **Data Connection**: Create `src/utils/data_loader.py` with `@st.cache_data` and Snowflake connection (if requested).
- **Authentication**: Implement basic auth or integrate with SSO if requested.
- **Components**: Create reusable components in `src/components/`.

### 7. Add Documentation
- Create `README.md` with setup instructions, environment variable requirements, and run commands.
- Add docstrings to all functions.

### 8. Final Review
- Verify no secrets are hardcoded.
- Verify brand colors are used.
- Verify error handling is in place.

## Error Handling

**Missing App Name**: Request application name before scaffolding.

**Invalid Data Source**: Validate connection parameters and provide setup guidance.

**Dependency Conflicts**: Resolve version conflicts in requirements.txt automatically.

## Examples

### Example 1: Data Dashboard

```
/scaffold-streamlit-developer "
Create analytics dashboard for sales data.
Data source: Snowflake, need charts and filters.
Multi-page with authentication.
"
```

### Example 2: ML Model Demo

```
/scaffold-streamlit-developer "
Build demo app for fraud detection model.
Upload CSV, show predictions with confidence scores.
Single page, no auth needed.
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/streamlit-developer/streamlit-developer-constitution.md`
- **Brand Guidelines**: Constitution Section I
- **Related**: debug-streamlit-developer, refactor-streamlit-developer
