---
description: Intelligent debug orchestrator - detects archetype and routes to specialist
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
- Error messages or stack traces
- Code context or file paths
- Symptoms and expected behavior
- Technology keywords

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
- Match error patterns against archetype metadata
- Analyze technology keywords and file patterns
- Score confidence based on error signatures
- Return ranked debug contexts

**Error Pattern Matching:**
Discovery script checks:
- Technology-specific error codes (SQL, HTTP, Spark)
- Stack trace patterns (py4j, org.apache.spark, etc.)
- File extensions (.sql, .py, .sh, .tsx)
- Framework-specific errors (Airflow, React, Terraform)


### 4. Route to Specialist

Based on discovery script output:

**High Confidence (score ≥30)**:
```
✓ Detected: {archetype_display_name}
  Category: {category_name}
  Error Type: {error_category}
  Score: {score}
  Routing to: /{workflow}

Executing specialized debug workflow...
```

**Medium Confidence (score 15-29)**:
```
🤔 Debug Context Detected

Archetype: {archetype_display_name} (score: {score})
Category: {category_name}
Error Pattern: {pattern_matched}

Proceed with /{workflow}? [Y/n]

Alternatives:
1. {alternative_1} (score: {score_1})
2. {alternative_2} (score: {score_2})
```

**Low Confidence (score <15)**:
```
⚠️ Unable to confidently detect error context

Your error: "{user_input}"

Suggested category: {category_name}
See archetypes: {category_index_link}

Provide more context:
- Full error message or stack trace
- Technology/framework being used
- File path or code snippet
- When the error occurs

Or specify archetype explicitly
```

### 5. Execute Specialist Workflow

**Use the `workflow` field from discover-archetype.py output directly.**
Example: `/{workflow} $ARGUMENTS`

For workflow mappings, see: `manifest.yaml` files in each archetype

### 6. Provide Immediate Guidance

While routing, offer quick diagnostic steps:

**For Error Messages:**
```
💡 Quick Diagnostic Steps:
1. Check error message for specific codes/patterns
2. Review recent changes that might have caused it
3. Check logs for additional context
4. Verify environment configuration

Routing to specialist for detailed debugging...
```

**For Performance Issues:**
```
💡 Performance Diagnostic Steps:
1. Check resource utilization (CPU, memory, disk)
2. Review query plans or execution logs
3. Look for bottlenecks in data flow
4. Monitor network I/O

Routing to specialist for performance analysis...
```

### 7. Handle Multi-Component Errors

If error spans multiple components:

```
🔗 Multi-Component Error Detected

Error affects multiple components:
1. {component_1} - {archetype_1}
2. {component_2} - {archetype_2}

Recommended approach:
→ Start with root cause component: {primary_component}
→ Then check downstream: {secondary_components}

Or use /solution-debug for integrated troubleshooting
```

## Error Handling

**Insufficient Information**: Request full error message, stack trace, and context.

**Ambiguous Errors**: Suggest enabling debug logging or adding instrumentation.

**No Clear Pattern**: Provide general debugging workflow and ask for technology specifics.

## Examples

**Example 1: SQL Error**
```
User: /debug SQL compilation error: invalid identifier 'customer_id'

Discovery: SQL Query Crafter (score: 25)
Error Pattern: SQL syntax/compilation
Action: Route to /debug-sql-query-crafter
```

**Example 2: Spark Error**
```
User: /debug py4j.protocol.Py4JJavaError: An error occurred while calling

Discovery: Transformation Alchemist (score: 22)
Error Pattern: PySpark/Java interop
Action: Route to /debug-transformation-alchemist
```

**Example 3: API Error**
```
User: /debug FastAPI returning 500 error on POST /users

Discovery: Integration Specialist (score: 20)
Error Pattern: HTTP 500, API endpoint
Action: Route to /debug-integration-specialist
```

**Example 4: Deployment Error**
```
User: /debug AKS pod failing with ImagePullBackOff

Discovery: AKS DevOps Deployment (score: 23)
Error Pattern: Kubernetes pod error
Action: Route to /debug-aks-devops-deployment
```

**Example 5: Model Training Error**
```
User: /debug XGBoost training fails with memory error

Discovery: Gradient Boosted Trees (score: 18)
Category: Machine Learning Models
Action: Route to /debug-gradient-boosted-trees
```

## References

- **Category Index**: [Category Index](../../../INDEX.md)
- **Routing Config**: [../../templates/archetype manifest.yaml files](../../../solution/templates/archetype manifest.yaml files)
- **Discovery Script**: `../../scripts/discover-archetype.py`
- **Related**: [/scaffold](./scaffold.md), [/compare](./compare.md), [/document](./document.md), [/refactor](./refactor.md), [/test](./test.md)
- **Solution**: [/solution-debug](../../../solution/.windsurf/workflows/solution-debug.md)
