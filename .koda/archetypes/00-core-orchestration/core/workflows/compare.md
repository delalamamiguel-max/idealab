---
description: Intelligent compare orchestrator - detects archetype and routes to specialist
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
- Approaches or implementations to compare
- Comparison criteria (performance, cost, maintainability, complexity)
- Constraints and context
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
- Match keywords against all available archetypes
- Score confidence for comparison context
- Return ranked suggestions


### 4. Route to Specialist

Based on discovery script output:

**High Confidence (score ≥30)**:
```
✓ Detected: {archetype_display_name}
  Category: {category_name}
  Score: {score}
  Routing to: /{workflow}

Executing specialized comparison workflow...
```

**Medium Confidence (score 15-29)**:
```
🤔 Comparison Context Detected

Archetype: {archetype_display_name} (score: {score})
Category: {category_name}

Proceed with /{workflow}? [Y/n]

Alternatives:
1. {alternative_1} (score: {score_1})
2. {alternative_2} (score: {score_2})
```

**Low Confidence (score <15)**:
```
⚠️ Unable to confidently detect comparison context

Your request: "{user_input}"

Suggested category: {category_name}
See archetypes: {category_index_link}

Provide more context about:
- What approaches/tools to compare
- Technology stack
- Comparison criteria (performance, cost, etc.)
```

### 5. Execute Specialist Workflow

**Use the `workflow` field from discover-archetype.py output directly.**
Example: `/{workflow} $ARGUMENTS`

For workflow mappings, see: `manifest.yaml` files in each archetype

### 6. Provide Comparison Guidance

While routing, provide decision-making framework:

**For Technology Choices**:
```
💡 Technology Comparison Framework:
- Evaluate on: performance, cost, learning curve, community support
- Consider: existing skills, infrastructure, long-term maintenance
- Test: proof of concept before committing

Routing to specialist for detailed comparison...
```

**For Architecture Patterns**:
```
💡 Architecture Comparison Framework:
- Evaluate on: scalability, complexity, cost, time to implement
- Consider: team size, growth projections, operational overhead
- Validate: with architecture review and stakeholder input

Routing to specialist for detailed comparison...
```

**For Implementation Approaches**:
```
💡 Implementation Comparison Framework:
- Evaluate on: development time, maintainability, testability
- Consider: team expertise, code standards, future extensibility
- Prototype: critical components before full implementation

Routing to specialist for detailed comparison...
```

### 7. Handle Multi-Archetype Comparisons

If comparing solutions involving multiple archetypes:

**Scenario: Multi-Component Solution**:
```
Detected comparison across multiple components:
- Component 1: [Archetype 1] - [Comparison aspect]
- Component 2: [Archetype 2] - [Comparison aspect]

Recommended approach:
1. Compare each component separately with domain-specific workflows
2. Use /solution-compare for integrated architecture comparison
3. Consider integration points and dependencies

Which component to compare first?
```

### 8. Learn from Feedback

If user corrects the routing or provides additional context:
```
Thank you for the clarification!
Routing to: /compare-[corrected-archetype]

Additional context noted:
- [Context item 1]
- [Context item 2]

(Updating detection patterns for future requests)
```

## Error Handling

**Insufficient Context**: Request problem description, comparison criteria, and constraints.

**Too Many Options**: Suggest narrowing scope or prioritizing key decision factors.

**Unclear Criteria**: Provide standard comparison dimensions (performance, cost, complexity, etc.).

## Examples

**Example 1: SQL Comparison**
```
User: /compare CTE vs subquery for customer aggregation

Discovery: SQL Query Crafter (score: 25)
Action: Route to /compare-sql-query-crafter
```

**Example 2: ML Algorithm Comparison**
```
User: /compare XGBoost vs Random Forest for classification

Discovery: 
- XGBoost → Gradient Boosted Trees (50%)
- Random Forest → Random Forest Model (45%)

Action: Present both options for comparison
```

**Example 3: Infrastructure Comparison**
```
User: /compare Terraform vs ARM templates for AKS deployment

Discovery: 
- Terraform CICD Architect (40%)
- AKS DevOps Deployment (35%)

Action: Clarify focus (IaC tool or deployment strategy)
```

**Example 4: Multi-Archetype Comparison**
```
User: /compare Complete data platform approaches

Discovery: Multiple categories detected
Action: Route to /solution-compare
```

## References

- **Category Index**: [Category Index](../../../INDEX.md)
- **Routing Config**: [../../templates/archetype manifest.yaml files](../../../solution/templates/archetype manifest.yaml files)
- **Discovery Script**: `../../scripts/discover-archetype.py`
- **Related**: [/scaffold](./scaffold.md), [/debug](./debug.md), [/document](./document.md), [/refactor](./refactor.md), [/test](./test.md)
- **Solution**: [/solution-compare](../../../solution/.windsurf/workflows/solution-compare.md)
