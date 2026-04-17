---
description: Refactor Streamlit application for performance, maintainability, and brand compliance (Streamlit Developer)
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
Extract from $ARGUMENTS: code to refactor, goals (performance, cleanup, modularization, branding), constraints.

### 4. Analyze Codebase
- Identify monolithic scripts (> 500 lines).
- Identify repeated code blocks.
- Identify uncached data loading.
- Identify hardcoded styles or secrets.
- Identify deprecated Streamlit commands.

### 5. Apply Refactoring Strategies

**Modularization**:
- Extract reusable UI parts into `src/components/`.
- Extract data logic into `src/utils/`.
- Move pages to `pages/` directory if using single-script multi-page pattern.

**Performance Optimization**:
- Apply `@st.cache_data` to data fetching functions.
- Apply `@st.cache_resource` to database connections and ML models.
- Optimize Pandas operations (vectorization).

**State Management**:
- Centralize state initialization.
- Use callbacks for widget interactions where appropriate.

**Brand Compliance**:
- Update `.streamlit/config.toml` to match AT&T colors.
- Replace custom CSS with standard Streamlit theming where possible.

### 6. Generate Refactored Code
- Provide the updated file structure and code content.
- Ensure all imports are correct.
- Ensure `requirements.txt` is updated if new libraries are used.

### 7. Final Review
- Verify functionality is preserved.
- Verify code is cleaner and more maintainable.

## Error Handling

**No Code Provided**: Request specific files or code to refactor.

**Monolithic Single File**: Recommend phased extraction starting with data layer, then UI components.

**Missing Dependencies**: Update requirements.txt with any new libraries needed.

## Examples

### Example 1: Performance Refactor

```
/refactor-streamlit-developer "
Add caching to data_loader.py functions.
Current issue: page reloads trigger full data refresh.
"
```

### Example 2: Modularization

```
/refactor-streamlit-developer "
Extract sidebar navigation and chart components from app.py (800 lines).
Goal: Better maintainability and reusability.
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/streamlit-developer/streamlit-developer-constitution.md`
- **Caching**: Constitution Section II - Application Architecture
- **Related**: scaffold-streamlit-developer, debug-streamlit-developer
