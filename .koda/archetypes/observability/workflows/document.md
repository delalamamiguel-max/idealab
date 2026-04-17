---
description: Generate comprehensive documentation for observability implementation and telemetry strategy (Observability)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json` and parse for OTEL_COLLECTOR_ENDPOINT, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/observability/templates/env-config.yaml` for documentation templates

### 3. Parse Input
Extract from $ARGUMENTS: instrumentation location, target audience (developers, SREs, leadership), documentation scope (architecture, usage, troubleshooting, governance). Request clarification if incomplete.

### 4. Analyze Observability Architecture

Extract telemetry information: instrumentation coverage (services instrumented, span creation points, metric emission, log correlation), telemetry pipeline (collector configuration, export destinations, sampling strategy), signal schemas (trace semantics, metric definitions, log structure, resource attributes), observability platform (backend setup, dashboard configurations, alert rules, SLO definitions), compliance controls (PII redaction, metadata requirements, audit logging).

### 5. Generate Documentation Package

Create comprehensive documentation suite: Architecture Documentation (observability overview, telemetry pipeline architecture, instrumentation patterns, signal flow diagrams, backend integration), Developer Guide (instrumentation best practices, adding traces and metrics, structured logging, trace propagation, testing telemetry, troubleshooting common issues), Operations Guide (collector management, dashboard usage, alert response, SLO monitoring, cost optimization, incident investigation with traces), Signal Reference (span semantic conventions, metric definitions and units, log structure and levels, resource attribute catalog, cardinality guidelines), Compliance Documentation (PII redaction implementation, required metadata, audit logging, retention policies, compliance validation).

Include supporting artifacts: architecture diagrams, signal flow visualizations, dashboard screenshots, runbook checklists, cost optimization guides.

### 6. Add Recommendations

Include operational best practices: documentation maintenance, telemetry reviews, cost monitoring, signal quality assessments, continuous improvement, team training.

### 7. Validate and Report


Generate documentation artifacts organized in docs/ directory. Create index with navigation. Report completion.

## Error Handling

**Incomplete Information**: Request additional instrumentation and configuration details.

**Missing Diagrams**: Generate signal flow diagrams from configuration.

**Outdated SLOs**: Update with current definitions and error budgets.

## Examples

**Example 1**: `/document-observability Create complete documentation for order-service observability` - Output: Architecture docs, developer guide, operations runbook

**Example 2**: `/document-observability Generate signal reference for microservices telemetry` - Output: Comprehensive catalog of traces, metrics, and logs

**Example 3**: `/document-observability Document SLO monitoring and incident response` - Output: Operations guide with SLO tracking and runbooks

## References

