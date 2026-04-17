---
description: Debug Elasticsearch streaming failures and performance issues (Elasticsearch Stream)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype elasticsearch-stream --json ` and parse for ES_ENDPOINT, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/elasticsearch-stream/templates/env-config.yaml` for debugging tools

### 3. Parse Input
Extract from $ARGUMENTS: failure type, error messages, affected indices. Request clarification if incomplete.

### 4. Diagnose Issue
Check indexing failures, connection issues, mapping conflicts, performance degradation, backpressure.

### 5. Generate Fix Recommendations
Provide fixes for identified issues with configuration adjustments and optimizations.

### 6. Add Prevention Measures
Recommend monitoring improvements, capacity planning, error handling enhancements.

### 7. Validate and Report
Generate debug report. Report completion.

## Error Handling
**Cluster Down**: Escalate and implement failover procedures.
**Mapping Conflicts**: Resolve conflicts and update mappings.

## Examples
**Example 1**: `/debug-elasticsearch-stream Indexing throughput degraded` - Output: Performance analysis with optimization
**Example 2**: `/debug-elasticsearch-stream Mapping conflict errors` - Output: Conflict resolution with mapping updates

## References
Original: `prompts/debug_prompt.md` | Constitution: (pre-loaded above)
