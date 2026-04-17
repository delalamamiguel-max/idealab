---
description: Validate Cassandra connector for connectivity, performance, and fault tolerance (Cassandra Connector)
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
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype cassandra-connector --json ` and parse for CASSANDRA_CONTACT_POINTS, JAVA_VERSION, MVN_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- Read `${ARCHETYPES_BASEDIR}/cassandra-connector/cassandra-connector-constitution.md` for hard-stop rules
- Load `${ARCHETYPES_BASEDIR}/cassandra-connector/templates/env-config.yaml` for test specifications

### 3. Parse Input
Extract from $ARGUMENTS: connector location, test scope (unit, integration, performance, failover), acceptance criteria. Request clarification if incomplete.

### 4. Analyze Test Requirements
Identify testable components: CassandraConnector session creation, SSL handshake, CassandraServiceImpl CRUD operations (put, get, query, remove, batchInsert), MappingManager initialization, health-check endpoint, connection pooling under load, failover behavior.

### 5. Generate Test Suite
Create: unit tests (mock DataStax driver, verify config population, exception hierarchy), integration tests (embedded Cassandra or Testcontainers, end-to-end CRUD), performance tests (connection pool saturation, concurrent read/write throughput), failover tests (node down simulation, DC failover with DCAwareRoundRobinPolicy), SSL tests (valid cert, expired cert, missing truststore).

### 6. Add Recommendations
Include testing best practices: use Testcontainers for reproducible integration tests, baseline connection setup latency, verify health-check under partial cluster failure.

### 7. Validate and Report
// turbo
Execute: `mvn test -Dtest=CassandraConnectorTest,CassandraServiceImplTest -pl . --fail-at-end`
Generate report. Report completion.

## Error Handling
**Test Cluster Unavailable**: Use Testcontainers with `cassandra:3.11` or `cassandra:4.1` Docker image.
**Flaky Timeout Tests**: Use deterministic timeouts and retry-aware assertions.

## Examples
**Example 1**: `/test-cassandra-connector Validate connection pooling under concurrent load` - Output: Load test suite with pool exhaustion scenarios
**Example 2**: `/test-cassandra-connector Test SSL handshake and certificate rotation` - Output: SSL test suite with truststore validation

## References
Original: `prompts/test_prompt.md` | Constitution: `${ARCHETYPES_BASEDIR}/cassandra-connector/cassandra-connector-constitution.md`
