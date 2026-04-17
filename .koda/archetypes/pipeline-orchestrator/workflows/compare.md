---
description: Compare Airflow/TWS orchestration approaches and patterns (Pipeline Orchestrator)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype pipeline-orchestrator --json ` and parse for AIRFLOW_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/pipeline-orchestrator/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: orchestration problem, comparison criteria (reliability, scalability, complexity), workflow characteristics, constraints. Request clarification if incomplete.

### 4. Generate Alternatives

Create 2-3 orchestration approaches: Airflow (mature, feature-rich), Prefect (modern, Pythonic), Custom scheduler (lightweight). Each with DAG examples, deployment considerations, use cases.

### 5. Generate Comparison Matrix

Compare on: reliability, scalability, complexity, learning curve, community support, operational overhead, cost, monitoring capabilities. Provide scores and analysis.

### 6. Add Recommendations

Recommend approach with justification. Include migration strategy, operational considerations, team training needs, monitoring setup.

### 7. Validate and Report


## Error Handling

**Insufficient Context**: Request workflow complexity, scale, team size, operational requirements.

**Tool Unfamiliarity**: Provide learning resources and migration guides.

**Operational Concerns**: Address deployment, monitoring, and maintenance considerations.

## Examples

**Example 1**: `/compare-pipeline Compare Airflow vs Prefect for data pipeline` - Output: Tool comparison with operational analysis

**Example 2**: `/compare-pipeline TaskFlow API vs traditional operators` - Output: Pattern comparison with code examples

**Example 3**: `/compare-pipeline Compare dynamic vs static DAG generation` - Output: Approach comparison with complexity analysis

## References

