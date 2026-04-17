---
description: Generate data pipeline deployment workflow with CI/CD, observability, and governance guardrails (Dev Ops Engineer)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype dev-ops-engineer --json ` and parse for CI_TOOL, ORCHESTRATOR, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/dev-ops-engineer/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: pipeline type (data ingestion, transformation, analytics), orchestration tool (Airflow, Databricks, Azure Data Factory), deployment environments (dev/test/prod), data sources and targets, quality requirements, observability needs. Request clarification if incomplete.

### 4. Generate Pipeline Deployment Workflow

Create comprehensive deployment artifacts: CI/CD Pipeline (build stage with tests and linting, security scanning for vulnerabilities, data quality validation gates, artifact packaging and versioning, environment promotion with approval gates, automated rollback triggers, deployment scorecard generation), Orchestration DAG/Workflow (task definitions with dependencies, retry policies with exponential backoff, timeout configurations, resource allocation, health check probes, structured logging and tracing, ownership and escalation contacts), Configuration Management (externalized configurations per environment, secret management with vault integration, parameter validation, environment-specific overrides), Observability Integration (metrics emission for DORA and pipeline KPIs, structured logging with trace correlation, event taxonomy for audit and lineage, dashboard and alert configurations, SLO definitions with error budgets).

### 5. Generate Governance Controls

Implement policy gates: quality gates (data validation rules, schema evolution checks, freshness and drift monitoring), security gates (secret scanning, vulnerability thresholds, access control validation), compliance gates (audit logging, lineage tracking, change freeze windows), cost gates (resource utilization thresholds, efficiency scoring, budget alerts).

Create rollback and replay procedures with data consistency safeguards.

### 6. Add Recommendations

Include best practices: canary deployment strategies, ephemeral preview environments, continuous cost monitoring, automated incident response, DORA metrics tracking, policy-as-code implementation.

Provide deployment runbook and troubleshooting guide.

### 7. Validate and Report


Generate complete deployment package with documentation. Report completion.

## Error Handling

**Missing Ownership**: Request team assignment and escalation contacts.

**Incomplete SLO**: Define latency, throughput, and success ratio targets.

**Secret Exposure Risk**: Implement vault integration and secret scanning.

## Examples

**Example 1**: `/scaffold-dev-ops Create Airflow DAG deployment for customer data pipeline` - Output: Complete CI/CD workflow with quality gates

**Example 2**: `/scaffold-dev-ops Generate multi-environment deployment for analytics pipeline` - Output: Deployment artifacts with canary and rollback

**Example 3**: `/scaffold-dev-ops Create data pipeline with DORA metrics tracking` - Output: Observability-ready deployment with KPI dashboards

## References

