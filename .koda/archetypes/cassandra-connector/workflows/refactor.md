---
description: Refactor Cassandra connector for performance, reliability, and driver modernization (Cassandra Connector)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Set ARCHETYPES_BASEDIR [⋯]
 
**SUCCESS CRITERIA**:
- Search for directory: "00-core-orchestration"
- Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory
 
**HALT IF**:
- Directory "00-core-orchestration" is not found
- `${ARCHETYPES_BASEDIR}` is not set (workflow will halt if this variable is not present in the environment)
 
// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Environment Setup
// turbo
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype cassandra-connector --json ` and parse for CASSANDRA_CONTACT_POINTS, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- Read `${ARCHETYPES_BASEDIR}/cassandra-connector/cassandra-connector-constitution.md` for hard-stop rules
- Load `${ARCHETYPES_BASEDIR}/cassandra-connector/templates/env-config.yaml` for best practices

### 3. Parse Input
Extract from $ARGUMENTS: connector location, refactoring goals (driver upgrade, pooling optimization, error handling improvement, multi-keyspace support). Request clarification if incomplete.

### 4. Analyze Current State
Assess driver version compatibility, connection pooling efficiency, load balancing policy layering, error handling coverage, session lifecycle management, SSL configuration modernization needs.

### 5. Generate Refactoring Plan
Create improvements for: DataStax driver version upgrade path (3.x to 4.x migration), connection pooling tuning, load balancing policy optimization (DCAware + TokenAware + LatencyAware layering), structured exception handling with correlation IDs, session management (singleton vs multi-keyspace), health-check hardening.

### 6. Implement Refactorings
Generate optimized connector with enhanced reliability, modernized driver usage, and improved observability.

### 7. Validate and Report
// turbo
Generate report. Report completion.

## Error Handling
**Breaking Changes**: Plan DataStax driver migration with API compatibility checks.
**Performance Regression**: Benchmark connection setup time and query latency before and after changes.

## Examples
**Example 1**: `/refactor-cassandra-connector Upgrade from DataStax driver 3.x to 4.x` - Output: Migration plan with API mapping and configuration translation
**Example 2**: `/refactor-cassandra-connector Optimize connection pooling for high-throughput writes` - Output: Tuned pooling configuration with benchmark guidance

## References
Original: `prompts/refactor_prompt.md` | Constitution: `${ARCHETYPES_BASEDIR}/cassandra-connector/cassandra-connector-constitution.md`
