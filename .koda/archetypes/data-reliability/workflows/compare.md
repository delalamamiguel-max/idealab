---
description: Compare data reliability strategies, monitoring platforms, and quality frameworks (Data Reliability)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-reliability --json ` and parse for MONITORING_ENDPOINT, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/data-reliability/templates/env-config.yaml` for comparison framework

### 3. Parse Input
Extract from $ARGUMENTS: comparison type (monitoring tools, quality frameworks, SLO approaches, incident management), candidate options, evaluation criteria. Request clarification if incomplete.

### 4. Generate Comparison Framework
Evaluate: monitoring platforms (Datadog vs Monte Carlo vs custom), quality frameworks (Great Expectations vs Deequ vs custom), SLO approaches (availability-focused vs freshness-focused vs balanced), incident management (PagerDuty vs Opsgenie vs custom runbooks).

### 5. Create Comparison Matrix
Generate with metrics (coverage, cost, integration complexity), assessments (feature completeness, vendor support, customization), trade-off analysis, recommendations.

### 6. Add Recommendations
Recommend with justification: reliability requirements, cost-benefit, operational feasibility, integration effort, long-term scalability.

### 7. Validate and Report
Generate comparison report. Report completion.

## Error Handling
**Insufficient Context**: Request reliability requirements and scale.
**Unclear Requirements**: Facilitate requirements gathering.

## Examples
**Example 1**: `/compare-data-reliability Great Expectations vs Deequ for data quality` - Output: Framework comparison with integration analysis
**Example 2**: `/compare-data-reliability SLO strategies for multi-tier data platform` - Output: Strategy comparison with error budget models

## References
