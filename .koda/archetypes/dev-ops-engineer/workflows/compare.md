---
description: Compare deployment strategies, orchestration tools, and observability approaches for data pipelines (Dev Ops Engineer)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype dev-ops-engineer --json ` and parse for CI_TOOL, ORCHESTRATOR, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/dev-ops-engineer/templates/env-config.yaml` for comparison framework

### 3. Parse Input
Extract from $ARGUMENTS: comparison type (orchestration tools, deployment strategies, observability platforms, CI/CD tools), candidate options, evaluation criteria (reliability, cost, complexity, observability), use case requirements. Request clarification if incomplete.

### 4. Generate Comparison Framework

Based on comparison type, evaluate: Orchestration Tools (Airflow vs Databricks vs Azure Data Factory - feature sets, scalability, cost, integration ecosystem, observability), Deployment Strategies (blue-green vs canary vs rolling updates - risk mitigation, resource impact, complexity, rollback speed), Observability Platforms (Datadog vs Prometheus/Grafana vs Azure Monitor - metrics coverage, cost, integration, alerting capabilities), CI/CD Tools (Azure DevOps vs Jenkins vs GitHub Actions - automation capabilities, integration, cost, enterprise features).

### 5. Create Comparison Matrix

Generate detailed comparison with quantitative metrics (cost analysis, performance benchmarks, DORA metrics capability), qualitative assessments (operational complexity, team learning curve, governance fit), trade-off analysis, use case recommendations.

Include DORA metrics tracking capability for each option.

### 6. Add Recommendations

Recommend approach with comprehensive justification: requirements alignment, cost-benefit analysis, operational feasibility, governance compliance, migration path, team capability considerations.

Provide implementation roadmap and success criteria.

### 7. Validate and Report


Generate comparison report with decision matrix, recommendations, implementation guidance. Report completion.

## Error Handling

**Insufficient Data**: Request workload characteristics and usage patterns.

**Unclear Requirements**: Facilitate requirements gathering session.

**Tool Compatibility Issues**: Evaluate integration challenges and workarounds.

## Examples

**Example 1**: `/compare-dev-ops Airflow vs Databricks Workflows for data orchestration` - Output: Tool comparison with cost, reliability, and observability analysis

**Example 2**: `/compare-dev-ops Canary vs blue-green deployment for production pipelines` - Output: Strategy comparison with risk and resource analysis

**Example 3**: `/compare-dev-ops Azure DevOps vs GitHub Actions for pipeline CI/CD` - Output: Platform comparison with governance and integration assessment

## References

