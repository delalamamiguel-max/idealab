---
description: Compare Streamlit application against architectural standards and best practices (Streamlit Developer)
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
Extract from $ARGUMENTS: project path, specific standards to check (brand, security, performance).

### 4. Perform Analysis

**Brand Compliance**:
- Check `.streamlit/config.toml` for correct hex codes.
- Check for hardcoded colors in code.

**Security**:
- Check for hardcoded secrets.
- Check for SQL injection vulnerabilities.
- Check for unsafe input handling.

**Performance**:
- Check for missing `@st.cache_data` on data loading functions.
- Check for large dataframes being loaded into memory unnecessarily.

**Code Quality**:
- Check for monolithic files.
- Check for proper modularization.

### 5. Generate Report
- **Summary**: Overall compliance score.
- **Violations**: List of specific rule violations (Critical/Warning).
- **Recommendations**: Actionable steps to fix violations.
- **Diff**: Show expected vs actual configuration.

### 6. Final Review
- Ensure report is accurate and constructive.

## Error Handling

**Missing Project Path**: Request path to Streamlit application directory.

**No config.toml**: Flag as critical brand violation, generate template.

**Parse Errors**: Report specific file and line causing issues.

## Examples

### Example 1: Full Compliance Check

```
/compare-streamlit-developer "
Check my-streamlit-app/ for brand, security, and performance compliance.
"
```

### Example 2: Security Focus

```
/compare-streamlit-developer "
Security audit for data-dashboard/ - check for secrets and SQL injection.
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/streamlit-developer/streamlit-developer-constitution.md`
- **Brand Colors**: Constitution Section II - Brand Compliance
- **Related**: scaffold-streamlit-developer, refactor-streamlit-developer
