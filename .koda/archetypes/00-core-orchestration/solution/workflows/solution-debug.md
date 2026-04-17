---
description: Debug multi-archetype solution with cross-component issues
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

**SUCCESS CRITERIA**:
- Search for directory: "00-core-orchestration"
- Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory

**HALT IF**:
- Directory "00-core-orchestration" is not found
- `${ARCHETYPES_BASEDIR}` is not set

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Parse Input

Extract error description, affected components, and solution architecture.

### 2. Infer Context from User's Assets

**Before calling discover-archetype.py, analyze the user's context to augment queries.**

**If user references a PROJECT or DIRECTORY:**
```
Analyze directory structure to infer composition:
- Look for package.json, requirements.txt, pom.xml → Application type
- Look for .tf, terraform/ → Infrastructure as Code
- Look for .py + mlflow/, model/ → ML/Data Science
- Look for Dockerfile, helm/, k8s/ → Container/Kubernetes
- Look for .sql, dbt_project.yml → Data Engineering
- Look for airflow/, dags/ → Orchestration
- Look for manifest.yaml + constitution.md → Archetype

Generate context description:
"Project composition: {inferred_type} with {key_technologies}"
```

**If user references a FILE:**
```
Analyze file to infer purpose and framework from imports/content.

Generate context description:
"File type: {extension}, Purpose: {inferred_purpose}, Framework: {detected_framework}"
```

**Build Augmented Query:**
```
${AUGMENTED_QUERY} = "${CONTEXT_DESCRIPTION}. User request: $ARGUMENTS"
```

### 3. Analyze Problem Across Components

**Root Cause Analysis:**
Use discovery script to identify affected archetypes for each component.

**Data Flow Tracing:**
- Track data from source to error point
- Identify transformation stages
- Check integration points

**Dependency Analysis:**
- Verify component versions
- Check configuration consistency
- Validate contracts between components

### 4. Generate Fixes

**Component-Level Fixes:**
Route to specific /debug-{archetype} workflows for each affected component.

**Integration-Level Fixes:**
- Update contracts
- Add error handling
- Implement circuit breakers

### 5. Add Recommendations

**Prevention:**
- Monitoring improvements
- Test coverage gaps
- Documentation updates

## Examples

**Example: Data Pipeline Failure**
```
Error: Data quality check failing after Spark transformation

Analysis:
- Component 1: transformation-alchemist (Spark) - Schema mismatch
- Component 2: quality-guardian - Validation rules outdated

Fix:
1. /debug-spark - Fix schema in transformation
2. /debug-quality - Update validation rules
3. Add integration test for schema compatibility
```

## References

- [Core Debug](../../../core/.windsurf/workflows/debug.md)
- [Categories](../../../INDEX.md)
