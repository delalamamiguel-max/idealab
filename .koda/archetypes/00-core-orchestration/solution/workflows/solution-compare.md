---
description: Compare multi-archetype solution architectures and approaches
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

Extract solution requirements and comparison criteria.

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

### 3. Identify Solution Patterns

Map requirements to common patterns (see `manifest.yaml` files in each archetype):
- ML Training Pipeline
- Data Platform
- Application with Knowledge Graph
- DevOps CI/CD Pipeline

### 4. Generate Alternative Solutions

For each pattern, identify component archetypes using discovery script.

### 5. Create Comparison Matrix

Compare solutions across dimensions:
- **Performance**: Throughput, latency
- **Cost**: Infrastructure, operational
- **Complexity**: Implementation, maintenance
- **Reliability**: SLAs, failure modes
- **Scalability**: Growth potential

### 6. Provide Recommendations

Based on comparison matrix and requirements, recommend optimal solution.

## Examples

**Example: Data Platform Comparison**
```
Solution A (Batch): pipeline-builder + transformation-alchemist + sql-query-crafter
Solution B (Streaming): elasticsearch-stream + transformation-alchemist + databricks-workflow-creator

Comparison: Performance (B wins), Cost (A wins), Complexity (A wins)
Recommendation: Solution A for initial implementation, migrate to B as scale increases
```

## References

- [Solution Patterns](../../templates/archetype manifest.yaml files)
- [Categories](../../../INDEX.md)
