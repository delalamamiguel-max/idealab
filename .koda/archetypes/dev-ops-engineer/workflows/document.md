---
description: Generate documentation for data pipeline deployment workflows and operations (Dev Ops Engineer)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype dev-ops-engineer --json ` and parse for CI_TOOL, ORCHESTRATOR, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/dev-ops-engineer/templates/env-config.yaml` for documentation templates

### 3. Parse Input
Extract from $ARGUMENTS: deployment artifacts location, target audience (engineers, operators, leadership, governance), documentation scope (deployment, operations, troubleshooting, governance). Request clarification if incomplete.

### 4. Analyze Deployment Architecture

Extract deployment information: CI/CD pipeline (stages, gates, tools, configurations), orchestration (DAG/workflow structure, task dependencies, retry policies), environment topology (dev/test/prod configurations, promotion process), observability (metrics, logging, alerting, dashboards), quality gates (validation rules, security checks, policy enforcement), DORA metrics (lead time, change failure rate, MTTR, deployment frequency).

### 5. Generate Documentation Package

Create comprehensive documentation suite: Deployment Guide (pipeline overview and architecture, environment setup and prerequisites, CI/CD pipeline stages and gates, deployment procedures per environment, rollback and recovery procedures, troubleshooting common issues), Operations Runbook (monitoring and alerting configuration, SLO definitions and error budgets, incident response workflows, maintenance procedures, performance tuning guide, cost optimization strategies), Development Guidelines (local development setup, testing procedures, CI/CD integration, code promotion workflow, best practices and standards, governance compliance checklist), Governance Documentation (quality gate definitions and thresholds, security and compliance controls, audit logging and lineage, ownership and escalation contacts, policy gate matrix, exception management process), DORA Metrics Documentation (metric definitions and calculations, baseline and target values, dashboards and reporting, improvement tracking).

Include supporting artifacts: architecture diagrams, pipeline flow charts, runbook checklists, metric dashboards, alert rule documentation.

### 6. Add Recommendations

Include operational best practices: documentation maintenance (update with changes, version control), onboarding procedures (new team members, knowledge transfer), review and improvement cycles, incident post-mortems, continuous optimization.

### 7. Validate and Report


Generate documentation artifacts organized in docs/ directory. Create index with navigation. Report completion.

## Error Handling

**Incomplete Information**: Request additional deployment and operational details.

**Missing Diagrams**: Generate diagrams from configuration and workflow files.

**Outdated Metrics**: Flag discrepancies and update with current values.

## Examples

**Example 1**: `/document-dev-ops Create complete documentation for customer pipeline deployment` - Output: Deployment guide, operations runbook, governance documentation

**Example 2**: `/document-dev-ops Generate operations runbook for analytics DAG` - Output: Comprehensive runbook with monitoring, troubleshooting, and incident response

**Example 3**: `/document-dev-ops Document DORA metrics for production deployments` - Output: Metrics documentation with dashboards and improvement tracking

## References

