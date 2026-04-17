---
description: Debug data pipeline deployment failures, orchestration issues, and quality gate violations (Dev Ops Engineer)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype dev-ops-engineer --json ` and parse for CI_TOOL, ORCHESTRATOR, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/dev-ops-engineer/templates/env-config.yaml` for debugging tools

### 3. Parse Input
Extract from $ARGUMENTS: failure type (deployment failure, pipeline error, quality gate violation, performance degradation), error messages and logs, pipeline/job ID, environment, recent changes. Request clarification if incomplete.

### 4. Diagnose Issue

Run diagnostic checks: Deployment Failures (CI/CD pipeline logs, build and test failures, artifact validation errors, deployment gate violations, rollback trigger analysis), Pipeline Execution Failures (orchestration task logs and status, dependency resolution issues, retry exhaustion analysis, resource allocation problems, timeout analysis), Quality Gate Violations (data validation failures, schema evolution conflicts, freshness and drift violations, security scan findings, policy gate breaches), Observability Gaps (missing metrics or logs, trace correlation issues, alert configuration problems, SLO error budget status).

Provide diagnostic report with root cause hypothesis.

### 5. Generate Fix Recommendations

Provide targeted fixes: for deployment failures (fix CI/CD pipeline configuration, resolve artifact issues, update approval workflows), for pipeline failures (adjust retry policies, fix task dependencies, optimize resource allocation), for quality violations (fix data validation rules, resolve schema conflicts, update quality thresholds), for performance issues (optimize pipeline logic, adjust resource allocation, improve parallel execution).

Include configuration fixes and code changes.

### 6. Add Prevention Measures

Recommend improvements: enhanced pre-deployment validation, improved monitoring and alerting, proactive quality checks, automated rollback triggers, better resource management, canary deployment adoption.

### 7. Validate and Report


Generate debug report with issue analysis, fixes, prevention measures. Report completion.

## Error Handling

**Insufficient Logs**: Enable debug logging and collect diagnostic data.

**Multiple Root Causes**: Prioritize fixes by impact and provide sequenced remediation.

**Intermittent Failures**: Set up monitoring to capture transient issues.

## Examples

**Example 1**: `/debug-dev-ops Airflow DAG failing with data quality violations` - Output: Quality gate analysis with threshold adjustments

**Example 2**: `/debug-dev-ops Pipeline deployment timeout in production promotion` - Output: Resource analysis with optimization recommendations

**Example 3**: `/debug-dev-ops Secret scanning gate blocking deployment` - Output: Secret management remediation with vault migration

## References

