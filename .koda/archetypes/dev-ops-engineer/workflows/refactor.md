---
description: Refactor data pipeline deployment to reinforce telemetry, alerting, and lifecycle compliance (Dev Ops Engineer)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype dev-ops-engineer --json ` and parse for CI_TOOL, ORCHESTRATOR, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/dev-ops-engineer/templates/env-config.yaml` for best practices

### 3. Parse Input
Extract from $ARGUMENTS: pipeline location (DAG, workflow, CI/CD config), refactoring goals (observability, reliability, governance, performance), specific issues (missing monitoring, poor error handling, secret exposure). Request clarification if incomplete.

### 4. Analyze Current State

Assess deployment: observability (metrics coverage, structured logging, trace correlation, alert configurations), reliability (retry policies, timeout settings, rollback procedures, error handling), governance (quality gates, security scanning, audit logging, ownership documentation), performance (resource utilization, execution efficiency, DORA metrics), cost efficiency (resource optimization, idle time reduction, efficiency scoring).

Identify refactoring opportunities and technical debt.

### 5. Generate Refactoring Plan

Create improvements: Observability Enhancements (add comprehensive metrics emission, implement structured logging with trace correlation, configure SLO monitoring with error budgets, set up dashboards and alert rules), Reliability Improvements (implement retry policies with exponential backoff, add timeout configurations, enhance error handling, create automated rollback procedures, add health check probes), Governance Strengthening (add data quality validation gates, implement security scanning, enhance audit logging, document ownership and escalation, add policy gates), Performance Optimizations (optimize resource allocation, improve parallelization, reduce idle time, implement cost monitoring).

### 6. Implement Refactorings

Generate refactored code: updated CI/CD pipeline with enhanced gates, refactored orchestration with reliability controls, improved configuration management, enhanced observability integration, updated documentation and runbooks.

Include migration guide with validation strategy.

### 7. Validate and Report


Generate refactoring report with before/after comparison, reliability improvements, governance enhancements, performance gains. Report completion.

## Error Handling

**Breaking Changes**: Provide backward-compatible migration path with phased rollout.

**Performance Regression**: Benchmark before and after refactoring.

**Compliance Gaps**: Ensure all changes meet policy requirements.

## Examples

**Example 1**: `/refactor-dev-ops Add comprehensive observability to analytics pipeline` - Output: Refactored pipeline with DORA metrics and SLO monitoring

**Example 2**: `/refactor-dev-ops Implement automated rollback for customer data DAG` - Output: Enhanced DAG with rollback triggers and validation

**Example 3**: `/refactor-dev-ops Add quality gates to production deployment pipeline` - Output: Hardened CI/CD with data validation and security scanning

## References

