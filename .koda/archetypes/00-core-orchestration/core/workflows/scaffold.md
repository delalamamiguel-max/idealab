---
description: Intelligent scaffold orchestrator - detects archetype and routes to specialist
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
- Technology keywords
- File types mentioned
- Explicit archetype names
- Current file context (if available)

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
- Match keywords against all available archetypes in this distribution
- Score confidence for each potential match
- Return ranked suggestions with workflow routing

### 4. Route to Specialist

Based on discovery script output:

**High Confidence (score ≥30)**:
```
✓ Detected: {display_name}
  Confidence: {score}
  Routing to: /{workflow}

Executing specialized workflow...
```

Use the `workflow` field from discover output directly (e.g., `scaffold-sql-query-crafter`).

**Medium Confidence (score 15-29)**:
```
🤔 Archetype Detection

Detected: {display_name} (score: {score})

Proceed with /{workflow}? [Y/n]
```

Run with `--top 3` to show alternatives:
```bash
python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/discover-archetype.py --query "$ARGUMENTS" --json --top 3
```

**Low Confidence (score <15)**:
```
⚠️ Unable to confidently detect archetype

Your request: "{user_input}"
Score: {score}

Please provide more context about:
- Technology stack (SQL, Spark, Python, etc.)
- File types or formats
- Specific keywords from your domain

Or specify archetype explicitly: /scaffold-{archetype-name}
```

### 4. Execute Specialist Workflow

**Use the `workflow` field from discover-archetype.py output directly.**

Example: If discover returns `{"workflow": "scaffold-sql-query-crafter", ...}`, route to:
```
/scaffold-sql-query-crafter $ARGUMENTS
```

The workflow name comes from the archetype's `manifest.yaml`, ensuring consistency.

### 6. Handle Multi-Archetype Scenarios

If discovery detects multiple archetypes (confidence distributed across >3 archetypes):

```
🔗 Multi-Archetype Solution Detected

Your request may require multiple components:
1. {archetype_1} ({category_1}) - {confidence_1}%
2. {archetype_2} ({category_2}) - {confidence_2}%
3. {archetype_3} ({category_3}) - {confidence_3}%

Recommended approach:
→ /solution-scaffold {your request}

This will:
- Generate all components with integration points
- Create dependency graph
- Provide testing framework

Or scaffold individually:
1. /scaffold-{archetype-1} [component 1 description]
2. /scaffold-{archetype-2} [component 2 description]
3. /scaffold-{archetype-3} [component 3 description]
```

### 7. Learn from Feedback

If routing was incorrect:
- Note the keywords that led to mismatch
- Suggest reporting for metadata refinement
- Provide option to specify archetype directly

## Error Handling

**Discovery Script Failure**:
```
⚠️ Automated discovery unavailable

Falling back to manual category selection.

Please select a category:
1. Machine Learning Models - ML training algorithms
2. ML Operations & Lifecycle - Experiment, feature, inference
3. Data Engineering - Pipelines, SQL, Spark
4. Data Governance & Quality - Validation, security
5. Infrastructure & DevOps - Deployment, automation
6. Application Development - Apps, APIs
7. Graph & Analytics - Graph algorithms, reporting
8. Software Quality & Maintenance - Testing, security
9. Documentation & Requirements - Docs, stories

Or view all: {master_index_link}
```

**No Match Found**:
```
❓ No Archetype Match

Your request: "{user_input}"

No archetypes matched with sufficient confidence.

Options:
1. Browse categories: {master_index_link}
2. Refine your request with more keywords
3. Use explicit workflow: /scaffold-{archetype-slug}

Example refined requests:
- "Create SQL query with CTEs" → SQL Query Crafter
- "Build PySpark DataFrame transformation" → Transformation Alchemist
- "Deploy API with authentication" → Integration Specialist
```

## Examples

**Example 1: Clear Single Archetype**
```
User: /scaffold Create SQL query with CTEs for customer monthly analysis

Discovery Result:
- Archetype: SQL Query Crafter
- Category: Data Engineering
- Confidence: 95%

Action: Route to /scaffold-sql-query-crafter
```

**Example 2: ML Model Request**
```
User: /scaffold Train XGBoost model for classification

Discovery Result:
- Archetype: Gradient Boosted Trees
- Category: Machine Learning Models
- Confidence: 85%

Action: Route to /scaffold-gradient-boosted-trees
```

**Example 3: Infrastructure Request**
```
User: /scaffold AKS deployment with Helm charts

Discovery Result:
- Archetype: AKS DevOps Deployment
- Category: Infrastructure & DevOps
- Confidence: 90%

Action: Route to /scaffold-aks-devops-deployment
```

**Example 4: Ambiguous Request**
```
User: /scaffold Build data pipeline

Discovery Result:
- Could be: Pipeline Builder, Transformation Alchemist, or Pipeline Orchestrator
- Confidence: 60% distributed

Action: Show alternatives and request clarification
Options:
1. Pipeline Builder - Data ingestion with merge/overwrite
2. Transformation Alchemist - PySpark/Scala transformations
3. Pipeline Orchestrator - Airflow/TWS orchestration

Which best describes your needs?
```

**Example 5: Multi-Category Solution**
```
User: /scaffold Complete data platform with ML capabilities

Discovery Result:
- Multiple categories detected:
  * Data Engineering: 30%
  * ML Operations: 25%
  * Infrastructure: 20%
- Suggests: Multi-archetype solution

Action: Route to /solution-scaffold
```

## References

- **Category Index**: [Category Index](../../../INDEX.md)
- **Manifest Files**: Each archetype has a `manifest.yaml` at its root for discovery
- **Discovery Script**: `../../scripts/discover-archetype.py`
- **Related Orchestrators**: 
  - [/compare](./compare.md) - Compare approaches
  - [/debug](./debug.md) - Debug issues
  - [/document](./document.md) - Generate documentation
  - [/refactor](./refactor.md) - Improve code
  - [/test](./test.md) - Validate implementation
- **Solution Orchestrator**: [/solution-scaffold](../../../solution/.windsurf/workflows/solution-scaffold.md)
