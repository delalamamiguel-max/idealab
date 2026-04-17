---
description: Debug data reliability incidents, SLO breaches, and quality failures (Data Reliability)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-reliability --json ` and parse for MONITORING_ENDPOINT, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/data-reliability/templates/env-config.yaml` for debugging tools

### 3. Parse Input
Extract from $ARGUMENTS: incident type (SLO breach, data loss, freshness delay, quality degradation), affected datasets, time range, error messages. Request clarification if incomplete.

### 4. Diagnose Issue
Check: SLO violations (availability, freshness, latency breaches, error budget burn), data loss (silent drops, partition skips, row count discrepancies), freshness delays (ingestion lag, processing bottlenecks, dependency delays), quality failures (null %, schema violations, referential integrity breaks, distribution drift), lineage breaks (missing provenance, dependency failures).

### 5. Generate Fix Recommendations
Provide fixes: for SLO breaches (optimize pipelines, scale resources, adjust thresholds), for data loss (restore from checkpoints, fix drop logic, add detection), for freshness (optimize processing, parallelize, fix dependencies), for quality (fix validation rules, correct data sources, update schemas), for lineage (restore provenance capture, fix dependencies).

### 6. Add Prevention Measures
Recommend: enhanced monitoring, proactive alerting, capacity planning, synthetic probes, continuous quality validation.

### 7. Validate and Report
Generate incident report with root cause analysis. Report completion.

## Error Handling
**Critical Data Loss**: Escalate immediately and initiate recovery procedures.
**SLO Exhaustion**: Implement emergency response and stakeholder communication.

## Examples
**Example 1**: `/debug-data-reliability Freshness SLO breach for orders table` - Output: Lag analysis with optimization recommendations
**Example 2**: `/debug-data-reliability Silent data loss detected in customer pipeline` - Output: Root cause with recovery procedure

## References
