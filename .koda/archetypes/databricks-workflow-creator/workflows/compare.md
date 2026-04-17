---
description: Compare Databricks workflow approaches, DLT strategies, and orchestration patterns (Databricks Workflow Creator)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype databricks-workflow-creator --json ` and parse for DATABRICKS_HOST, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/databricks-workflow-creator/templates/env-config.yaml` for comparison framework

### 3. Parse Input
Extract from $ARGUMENTS: comparison type (DLT vs notebooks, batch vs streaming, orchestration tools), candidate approaches, evaluation criteria (cost, performance, maintainability, governance), use case requirements. Request clarification if incomplete.

### 4. Generate Comparison Framework

Based on comparison type, evaluate: DLT vs Notebooks (declarative vs imperative, expectation enforcement, schema evolution, operational complexity, debugging capability), batch vs streaming (latency requirements, cost implications, complexity, use case fit, checkpoint management), cluster strategies (job clusters vs all-purpose, serverless vs classic, spot vs on-demand, autoscaling policies), orchestration approaches (Databricks workflows vs Airflow, task dependencies, retry strategies, monitoring capabilities).

### 5. Create Comparison Matrix

Generate detailed comparison with quantitative metrics (cost analysis per approach, performance benchmarks, complexity ratings), qualitative assessments (governance posture, operational overhead, team capability requirements), trade-off analysis, use case recommendations.

Include cost projections and DBU consumption estimates.

### 6. Add Recommendations

Recommend approach with justification: requirements alignment, cost-benefit analysis, governance fit, operational feasibility, migration path if changing approaches.

Provide implementation roadmap and success metrics.

### 7. Validate and Report


Generate comparison report with decision matrix, cost analysis, recommendations. Report completion.

## Error Handling

**Insufficient Data**: Request workload characteristics and usage patterns.

**Unclear Requirements**: Facilitate requirements gathering with stakeholders.

**Cost Uncertainty**: Provide DBU consumption models and projections.

## Examples

**Example 1**: `/compare-databricks-workflow DLT vs notebook-based pipeline for customer data` - Output: Strategy comparison with governance and cost analysis

**Example 2**: `/compare-databricks-workflow Batch vs streaming for real-time analytics` - Output: Latency-cost trade-off analysis with recommendations

**Example 3**: `/compare-databricks-workflow Job clusters vs serverless compute` - Output: Cost and performance comparison with sizing guidance

## References

Original: `prompts/compare_prompt.md` | Constitution: (pre-loaded above)
