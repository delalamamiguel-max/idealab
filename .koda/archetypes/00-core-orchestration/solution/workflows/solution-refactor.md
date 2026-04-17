---
description: Refactor multi-archetype solution maintaining integration
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

Extract components to refactor and refactoring goals.

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

### 3. Analyze Solution

Use discovery script to identify archetype for each component.

### 4. Generate Refactored Code

**Component-Level Refactoring:**
Route to /refactor-{archetype} for each component.

**Integration-Level Refactoring:**
- Update integration contracts
- Refactor shared utilities
- Consolidate configurations

**Cross-Cutting Concerns:**
- Error handling consistency
- Logging standardization
- Configuration management

### 5. Validate Consistency

Ensure refactored components maintain:
- Contract compatibility
- Performance characteristics
- Test coverage

## Examples

**Example: Data Pipeline Refactoring**
```
Components:
- pipeline-builder: Refactor to idempotent writes
- transformation-alchemist: Optimize Spark code
- pipeline-orchestrator: Improve error handling

Integration: Maintain data contracts, add monitoring
```

## References

- [Core Refactor](../../../core/.windsurf/workflows/refactor.md)
- [Categories](../../../INDEX.md)
