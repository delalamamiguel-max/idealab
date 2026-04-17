---
description: Generate documentation for Elasticsearch streaming pipeline (Elasticsearch Stream)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype elasticsearch-stream --json ` and parse for ES_ENDPOINT, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/elasticsearch-stream/templates/env-config.yaml` for documentation templates

### 3. Parse Input
Extract from $ARGUMENTS: pipeline location, target audience, documentation scope. Request clarification if incomplete.

### 4. Analyze Pipeline
Extract configuration, mappings, performance metrics, monitoring setup.

### 5. Generate Documentation Package
Create: Pipeline Architecture, Operations Runbook, Performance Guide, Troubleshooting Documentation.

### 6. Add Recommendations
Include maintenance procedures, optimization strategies, disaster recovery.

### 7. Validate and Report
Generate documentation. Report completion.

## Error Handling
**Incomplete Information**: Request pipeline configuration and metrics.
**Missing Diagrams**: Generate from pipeline architecture.

## Examples
**Example 1**: `/document-elasticsearch-stream Create streaming documentation package` - Output: Complete docs with architecture and runbooks
**Example 2**: `/document-elasticsearch-stream Generate operations guide` - Output: Ops guide with monitoring and troubleshooting

## References
Original: `prompts/document_prompt.md` | Constitution: (pre-loaded above)
