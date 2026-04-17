---
description: Intelligent refactor orchestrator - detects archetype and routes to specialist
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
- Code or system to refactor
- Refactoring goals (performance, maintainability, patterns)
- Constraints and priorities
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
- Match refactoring context against archetypes
- Analyze code patterns and technology
- Return ranked refactoring contexts


### 4. Route to Specialist

Based on discovery script output:

**High Confidence (score ≥30)**:
```
✓ Detected: {archetype_display_name}
  Category: {category_name}
  Refactor Goal: {goal}
  Score: {score}
  Routing to: /{workflow}

Executing specialized refactoring workflow...
```

**Medium Confidence (score 15-29)**:
```
🤔 Refactoring Context Detected

Archetype: {archetype_display_name} (score: {score})
Category: {category_name}

Proceed with /{workflow}? [Y/n]

Alternatives:
1. {alternative_1} (score: {score_1})
2. {alternative_2} (score: {score_2})
```

**Low Confidence (score <15)**:
```
⚠️ Unable to confidently detect refactoring context

Your request: "{user_input}"

Suggested category: {category_name}
See archetypes: {category_index_link}

Clarify:
- What code/system to refactor
- Refactoring goals (performance, readability, patterns)
- Technology stack

Or specify archetype explicitly
```

### 5. Execute Specialist Workflow

**Use the `workflow` field from discover-archetype.py output directly.**

Example: If discover returns `{"workflow": "refactor-sql-query-crafter", ...}`, route to:
```
/refactor-sql-query-crafter $ARGUMENTS
```

The workflow name comes from the archetype's `manifest.yaml`, ensuring consistency.

## Examples

**Example 1: SQL Refactoring**
```
User: /refactor SQL query to use CTEs instead of subqueries

Discovery: SQL Query Crafter (score: 25)
Action: Route to /refactor-sql-query-crafter
```

**Example 2: Spark Refactoring**
```
User: /refactor PySpark code to improve performance

Discovery: Transformation Alchemist (score: 22)
Action: Route to /refactor-transformation-alchemist
```

**Example 3: API Refactoring**
```
User: /refactor REST API to follow OpenAPI standards

Discovery: Integration Specialist (score: 24)
Action: Route to /refactor-integration-specialist
```

**Example 4: Infrastructure Refactoring**
```
User: /refactor Terraform code for better modularity

Discovery: Terraform CICD Architect (score: 21)
Action: Route to /refactor-terraform-cicd-architect
```

## References

- **Category Index**: [Category Index](../../../INDEX.md)
- **Routing Config**: [../../templates/archetype manifest.yaml files](../../../solution/templates/archetype manifest.yaml files)
- **Discovery Script**: `../../scripts/discover-archetype.py`
- **Related**: [/scaffold](./scaffold.md), [/compare](./compare.md), [/debug](./debug.md), [/document](./document.md), [/test](./test.md)
- **Solution**: [/solution-refactor](../../../solution/.windsurf/workflows/solution-refactor.md)
