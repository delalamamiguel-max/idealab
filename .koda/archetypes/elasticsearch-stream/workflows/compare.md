---
description: Compare Elasticsearch streaming approaches and index strategies (Elasticsearch Stream)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype elasticsearch-stream --json ` and parse for ES_ENDPOINT, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/elasticsearch-stream/templates/env-config.yaml` for comparison framework

### 3. Parse Input
Extract from $ARGUMENTS: comparison type, candidate approaches, evaluation criteria. Request clarification if incomplete.

### 4. Generate Comparison Framework
Evaluate streaming approaches, indexing strategies, performance optimization techniques.

### 5. Create Comparison Matrix
Generate comparison with throughput, latency, resource usage, cost.

### 6. Add Recommendations
Recommend approach with justification and implementation guidance.

### 7. Validate and Report
Generate report. Report completion.

## Error Handling
**Insufficient Context**: Request workload characteristics and requirements.
**Performance Trade-offs**: Document latency vs throughput considerations.

## Examples
**Example 1**: `/compare-elasticsearch-stream Bulk vs single document indexing` - Output: Strategy comparison with performance analysis
**Example 2**: `/compare-elasticsearch-stream Index lifecycle management policies` - Output: ILM policy comparison

## References
