---
description: Scaffold data reliability framework with SLOs, monitoring, and incident response (Data Reliability)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-reliability --json ` and parse for MONITORING_ENDPOINT, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/data-reliability/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: data product scope, SLO requirements, quality dimensions, monitoring needs, incident response requirements. Request clarification if incomplete.

### 4. Generate Reliability Framework
Create: SLO definitions (availability, freshness, latency, completeness, accuracy targets), error budget calculation (1h and 6h burn rates with gating), golden dashboards (freshness, throughput, failure rate, latency p99, quality scores), data quality rules (null %, distinctness, referential integrity, distribution drift, schema contracts), lineage and dependency maps (upstream impact analysis), incident runbooks (failure mode taxonomy, escalation, post-incident review templates), synthetic probes (delay injection, null testing, partition omission).

### 5. Generate Monitoring Integration
Implement: alerting configuration (severity-1 failure modes, adaptive thresholds, rolling baselines), anomaly detection (seasonality-aware volume and freshness), schema evolution monitoring (contract validation, breaking change detection), lineage integrity checks (provenance capture, dependency validation).

### 6. Add Recommendations
Include: continuous verification procedures, capacity planning, disaster recovery, performance optimization, reliability reviews.

### 7. Validate and Report
Generate framework with documentation. Report completion.

## Error Handling
**Missing SLOs**: Define critical dimension targets before proceeding.
**Silent Data Loss**: Implement detection and alerting immediately.
**Lineage Gaps**: Require provenance capture for regulated datasets.

## Examples
**Example 1**: `/scaffold-data-reliability Create reliability framework for customer data pipeline` - Output: Complete framework with SLOs, monitoring, and runbooks
**Example 2**: `/scaffold-data-reliability Implement data quality rules for analytics tables` - Output: Quality pack with schema contracts and anomaly detection

## References
