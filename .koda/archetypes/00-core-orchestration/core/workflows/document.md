---
description: Intelligent document orchestrator - detects archetype and routes to specialist
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
- What to document (code, API, architecture, workflow)
- Documentation scope and audience
- Output format preferences
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
- Match documentation context against archetypes
- Analyze technology and domain keywords
- Return ranked documentation contexts


### 4. Route to Specialist

Based on discovery script output:

**High Confidence (score ≥30)**:
```
✓ Detected: {archetype_display_name}
  Category: {category_name}
  Doc Type: {documentation_type}
  Score: {score}
  Routing to: /{workflow}

Executing specialized documentation workflow...
```

**Medium Confidence (score 15-29)**:
```
🤔 Documentation Context Detected

Archetype: {archetype_display_name} (score: {score})
Category: {category_name}

Proceed with /{workflow}? [Y/n]

Alternatives:
1. {alternative_1} (score: {score_1})
2. {alternative_2} (score: {score_2})
```

**Low Confidence (score <15)**:
```
⚠️ Unable to confidently detect documentation context

Your request: "{user_input}"

Suggested category: {category_name}
See archetypes: {category_index_link}

Clarify:
- What system/code to document
- Target audience (developers, users, operators)
- Documentation type (API, architecture, user guide)

Or specify archetype explicitly
```

### 5. Execute Specialist Workflow

**Use the `workflow` field from discover-archetype.py output directly.**

Example: If discover returns `{"workflow": "document-sql-query-crafter", ...}`, route to:
```
/document-sql-query-crafter $ARGUMENTS
```

The workflow name comes from the archetype's `manifest.yaml`, ensuring consistency.

## Examples

**Example 1: SQL Documentation**
```
User: /document SQL query for monthly sales aggregation

Discovery: SQL Query Crafter (score: 22)
Action: Route to /document-sql-query-crafter
```

**Example 2: API Documentation**
```
User: /document REST API endpoints for user management

Discovery: Integration Specialist (score: 25)
Action: Route to /document-integration-specialist
```

**Example 3: ML Model Documentation**
```
User: /document XGBoost classification model

Discovery: Gradient Boosted Trees (score: 20)
Action: Route to /document-gradient-boosted-trees
```

**Example 4: Release Notes**
```
User: /document Create release notes for v2.0

Discovery: Software Release Notes (score: 28)
Action: Route to /document-software-release-notes
```

## References

- **Category Index**: [Category Index](../../../INDEX.md)
- **Routing Config**: [../../templates/archetype manifest.yaml files](../../../solution/templates/archetype manifest.yaml files)
- **Discovery Script**: `../../scripts/discover-archetype.py`
- **Related**: [/scaffold](./scaffold.md), [/compare](./compare.md), [/debug](./debug.md), [/refactor](./refactor.md), [/test](./test.md)
- **Solution**: [/solution-document](../../../solution/.windsurf/workflows/solution-document.md)
