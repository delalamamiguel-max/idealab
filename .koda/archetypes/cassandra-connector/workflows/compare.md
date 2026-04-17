---
description: Compare Cassandra connector strategies, driver versions, and configuration approaches (Cassandra Connector)
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
- Load `${ARCHETYPES_BASEDIR}/cassandra-connector/templates/env-config.yaml` for comparison framework

### 3. Parse Input
Extract from $ARGUMENTS: comparison type (driver versions, consistency levels, pooling strategies, load balancing policies, SSL providers), candidate approaches, evaluation criteria. Request clarification if incomplete.

### 4. Generate Comparison Framework
Evaluate candidate approaches across: DataStax driver 3.x vs 4.x (API changes, performance, feature set), consistency levels (ONE vs LOCAL_QUORUM vs QUORUM — latency vs durability trade-offs), load balancing stacks (DCAware only vs DCAware+TokenAware vs DCAware+LatencyAware+TokenAware), SSL providers (JDK SSL vs OpenSSL via Netty — performance and compatibility), connection pooling strategies (conservative vs aggressive tuning).

### 5. Create Comparison Matrix
Generate comparison with: latency impact, throughput, resource consumption, operational complexity, failure behavior, migration effort.

### 6. Add Recommendations
Recommend approach with justification, migration path, and rollback strategy.

### 7. Validate and Report
// turbo
Generate report. Report completion.

## Error Handling
**Insufficient Context**: Request workload characteristics (read/write ratio, partition size, DC topology).
**Performance Trade-offs**: Document latency vs consistency vs availability triangle impacts.

## Examples
**Example 1**: `/compare-cassandra-connector DataStax driver 3.x vs 4.x migration` - Output: Feature comparison with migration effort analysis
**Example 2**: `/compare-cassandra-connector LOCAL_QUORUM vs LOCAL_ONE for read-heavy workload` - Output: Consistency level comparison with latency benchmarks

## References
Original: `prompts/compare_prompt.md` | Constitution: `${ARCHETYPES_BASEDIR}/cassandra-connector/cassandra-connector-constitution.md`
