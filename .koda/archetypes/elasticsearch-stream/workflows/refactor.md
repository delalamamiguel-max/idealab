---
description: Refactor Elasticsearch streaming pipeline for performance and reliability (Elasticsearch Stream)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype elasticsearch-stream --json ` and parse for ES_ENDPOINT, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/elasticsearch-stream/templates/env-config.yaml` for best practices

### 3. Parse Input
Extract from $ARGUMENTS: pipeline location, refactoring goals. Request clarification if incomplete.

### 4. Analyze Current State
Assess performance, reliability, error handling, monitoring coverage.

### 5. Generate Refactoring Plan
Create improvements for indexing performance, error handling, monitoring, scalability.

### 6. Implement Refactorings
Generate optimized pipeline with enhanced reliability.

### 7. Validate and Report
Generate report. Report completion.

## Error Handling
**Performance Regression**: Benchmark before and after changes.
**Breaking Changes**: Plan careful migration with validation.

## Examples
**Example 1**: `/refactor-elasticsearch-stream Optimize bulk indexing performance` - Output: Enhanced pipeline with improved throughput
**Example 2**: `/refactor-elasticsearch-stream Add comprehensive error handling` - Output: Robust pipeline with retry logic

## References
