---
description: Generate integration tests for multi-archetype solution
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

Extract solution components and testing scope.

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

Use discovery script to identify testable components and integration points.

Map to categories for test patterns:

### 4. Generate Test Suite

**Component-Level Tests:**
Route to /test-{archetype} for each component.

**Integration Tests:**
- Data flow validation
- API contract testing
- Event-driven workflows
- Error propagation

**End-to-End Tests:**
- Complete workflow scenarios
- User journey testing
- Performance under load

### 5. Provide Test Execution

```bash
# Run component tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run E2E tests
pytest tests/e2e/

# Run performance tests
locust -f tests/performance/
```

## Examples

**Example: ML Pipeline Testing**
```
Components:
- feature-architect: Feature engineering tests
- gradient-boosted-trees: Model accuracy tests
- inference-orchestrator: API latency tests
- model-ops-steward: Monitoring tests

Integration Tests:
- Feature → Model: Schema compatibility
- Model → Inference: Serialization/deserialization
- Inference → Monitoring: Metrics collection

E2E Test: Complete prediction workflow with monitoring
```

## References

- [Core Test](../../../core/.windsurf/workflows/test.md)
- [Categories](../../../INDEX.md)
