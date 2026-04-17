---
description: Debug Cassandra connection failures, timeouts, and performance issues (Cassandra Connector)
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
-- Read `${ARCHETYPES_BASEDIR}/cassandra-connector/cassandra-connector-constitution.md` for hard-stop rules
-- Load `${ARCHETYPES_BASEDIR}/cassandra-connector/templates/env-config.yaml` for debugging tools

### 3. Parse Input
Extract from $ARGUMENTS: failure type (connection timeout, read timeout, pool exhaustion, SSL handshake failure, consistency errors), error messages, affected keyspace. Request clarification if incomplete.

### 4. Diagnose Issue
Check connection failures (SSL certificate chain, credential validity, node reachability), timeout issues (connectTimeoutMillis, readTimeoutMillis, heartbeat), pool exhaustion (coreConnectionsPerHost, maxConnectionsPerHost, maxRequestsPerConnection), load balancing misrouting (localDataCenter mismatch, token-aware misconfiguration), consistency errors (quorum not met, insufficient replicas).

### 5. Generate Fix Recommendations
Provide targeted fixes for identified issues with configuration adjustments, pooling tuning, and SSL remediation steps.

### 6. Add Prevention Measures
Recommend health-check improvements, connection pool monitoring, alert thresholds, capacity planning for connection scaling.

### 7. Validate and Report
// turbo
Generate debug report. Report completion.

## Error Handling
**Cluster Unreachable**: Validate network path, firewall rules, and Cassandra node status.
**SSL Handshake Failure**: Verify truststore location, password, certificate expiry, and SSL provider compatibility.

## Examples
**Example 1**: `/debug-cassandra-connector Connection timeouts during peak load` - Output: Pool tuning analysis with connection scaling recommendations
**Example 2**: `/debug-cassandra-connector SSL handshake failures after certificate rotation` - Output: Certificate chain diagnosis with truststore update steps

## References
Original: `prompts/debug_prompt.md` | Constitution: `${ARCHETYPES_BASEDIR}/cassandra-connector/cassandra-connector-constitution.md`
