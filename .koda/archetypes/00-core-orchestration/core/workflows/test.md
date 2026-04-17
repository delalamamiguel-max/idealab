---
description: Intelligent test orchestrator - detects archetype and routes to specialist
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

### 1. Parse User Intent

Extract from $ARGUMENTS:
- Code or system to test
- Test type (unit, integration, performance)
- Coverage goals and scope
- Technology context

### 2. Infer Context from User's Assets

**Before calling discover-archetype.py, analyze the user's context to augment the query.**

**If user references a PROJECT or DIRECTORY:**
```
Analyze directory structure to infer composition:
- Look for package.json, requirements.txt, pom.xml → Application type
- Look for .tf, terraform/ → Infrastructure as Code
- Look for .py + mlflow/, model/ → ML/Data Science
- Look for Dockerfile, helm/, k8s/ → Container/Kubernetes
- Look for .sql, dbt_project.yml → Data Engineering
- Look for airflow/, dags/ → Orchestration
- Look for tests/, pytest.ini → Testing focus
- Look for manifest.yaml + constitution.md → Archetype

Generate context description:
"Project composition: {inferred_type} with {key_technologies}"
```

**If user references a FILE:**
```
Analyze file to infer purpose:
- .py → Python (check imports for framework: fastapi, pyspark, sklearn, etc.)
- .sql → SQL queries
- .tf → Terraform infrastructure
- .tsx/.jsx → React frontend
- .yaml/.yml → Configuration (check content: k8s, airflow, etc.)
- .sh/.bash → Automation scripts
- .md → Documentation

Generate context description:
"File type: {extension}, Purpose: {inferred_purpose}, Framework: {detected_framework}"
```

**If user provides NO asset reference:**
```
Use only $ARGUMENTS as-is (no augmentation)
```

**Build Augmented Query:**
```
${AUGMENTED_QUERY} = "${CONTEXT_DESCRIPTION}. User request: $ARGUMENTS"
```

### 3. Discover Archetype

**Automated Discovery:**
// turbo
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/discover-archetype.py --query "${AUGMENTED_QUERY}" --json`

This will:
- Match testing context against archetypes
- Analyze code and technology patterns
- Return ranked testing contexts


### 4. Route to Specialist

Based on discovery script output:

**High Confidence (score ≥30)**:
```
✓ Detected: {archetype_display_name}
  Category: {category_name}
  Test Type: {test_type}
  Score: {score}
  Routing to: /{workflow}

Executing specialized testing workflow...
```

**Medium Confidence (score 15-29)**:
```
🤔 Testing Context Detected

Archetype: {archetype_display_name} (score: {score})
Category: {category_name}

Proceed with /{workflow}? [Y/n]

Alternatives:
1. {alternative_1} (score: {score_1})
2. {alternative_2} (score: {score_2})
```

**Low Confidence (score <15)**:
```
⚠️ Unable to confidently detect testing context

Your request: "{user_input}"

Suggested category: {category_name}
See archetypes: {category_index_link}

Clarify:
- What to test (code, API, pipeline, model)
- Test type (unit, integration, performance)
- Technology stack

Or specify archetype explicitly
```

### 5. Execute Specialist Workflow

**Use the `workflow` field from discover-archetype.py output directly.**
Example: `/{workflow} $ARGUMENTS`

For workflow mappings, see: `manifest.yaml` files in each archetype

## Examples

**Example 1: SQL Testing**
```
User: /test SQL query for edge cases and performance

Discovery: SQL Query Crafter (93%)
Action: Route to /test-sql-query-crafter
```

**Example 2: API Testing**
```
User: /test REST API endpoints with pytest

Discovery: Integration Specialist (score: 22)
Action: Route to /test-integration-specialist
```

**Example 3: ML Model Testing**
```
User: /test XGBoost model for fairness and accuracy

Discovery: Gradient Boosted Trees (score: 20)
Action: Route to /test-gradient-boosted-trees
```

**Example 4: Unit Test Coverage**
```
User: /test Improve Python unit test coverage to 80%

Discovery: Unit Test Code Coverage (score: 22)
Action: Route to /test-unit-test-code-coverage
```

**Example 5: Load Testing**
```
User: /test Pub/Sub throughput under load

Discovery: Pub/Sub Load Testing (score: 21)
Action: Route to /test-pub-sub-load-testing
```

## References

- **Category Index**: [Category Index](../../../INDEX.md)
- **Routing Config**: [../../templates/archetype manifest.yaml files](../../../solution/templates/archetype manifest.yaml files)
- **Discovery Script**: `../../scripts/discover-archetype.py`
- **Related**: [/scaffold](./scaffold.md), [/compare](./compare.md), [/debug](./debug.md), [/document](./document.md), [/refactor](./refactor.md)
- **Solution**: [/solution-test](../../../solution/.windsurf/workflows/solution-test.md)
