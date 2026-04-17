---
description: Generate Elasticsearch streaming pipeline with real-time indexing and monitoring (Elasticsearch Stream)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype elasticsearch-stream --json ` and parse for ES_ENDPOINT, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/elasticsearch-stream/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: data source, stream configuration, index mapping, real-time requirements. Request clarification if incomplete.

### 4. Generate Stream Pipeline
Create streaming components: data ingestion (source connectors, stream processing), index configuration (mappings, settings, aliases), bulk indexing (batch sizing, retry logic, error handling), real-time monitoring (throughput, latency, errors).

### 5. Generate Monitoring
Implement dashboards, alerts, performance metrics, error tracking.

### 6. Add Recommendations
Include streaming best practices, performance tuning, disaster recovery.

### 7. Validate and Report
Generate pipeline. Report completion.

## Error Handling
**Connection Issues**: Validate Elasticsearch connectivity and credentials.
**Indexing Failures**: Implement retry logic and dead letter queue.

## Examples
**Example 1**: `/scaffold-elasticsearch-stream Create real-time log indexing pipeline` - Output: Complete streaming pipeline with monitoring
**Example 2**: `/scaffold-elasticsearch-stream Generate event stream to Elasticsearch` - Output: Event streaming with bulk indexing

## References
Original: `prompts/scaffold_prompt.md` | Constitution: (pre-loaded above)
