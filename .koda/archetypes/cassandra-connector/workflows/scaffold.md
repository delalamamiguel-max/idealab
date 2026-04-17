---
description: Generate Cassandra connector configuration with SSL, pooling, and health monitoring (Cassandra Connector)
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
-- Load `${ARCHETYPES_BASEDIR}/cassandra-connector/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: target keyspace, datacenter topology, SSL requirements, consistency level, pooling needs, health-check requirements. Request clarification if incomplete.

### 4. Generate Connector Configuration
Create connector components: CassandraDbConfig (cluster endpoints, auth, SSL/TLS, timeouts), CassandraConnector (session management, pooling, load balancing policies), CassandraService interface and implementation (CRUD, batch, accessor operations), Spring configuration properties (cassandra-config prefix binding), health-check endpoint (session liveness probe).

### 5. Generate Security Configuration
Implement Key Vault integration for credentials, SSL/TLS truststore setup (OpenSSL or JDK), address translation if NAT/VPN is required.

### 6. Generate Observability
Implement health-check endpoint, connection metrics, latency tracking, alert rule definitions.

### 7. Add Recommendations
Include connection pooling best practices, consistency level guidance for multi-DC, TTL strategies, retry and speculative execution tuning.

### 8. Validate and Report
// turbo
Generate connector configuration. Report completion.

## Error Handling
**Connection Issues**: Validate Cassandra cluster reachability, credentials, and SSL certificate chain.
**Pool Exhaustion**: Review pooling settings and connection lifecycle management.

## Examples
**Example 1**: `/scaffold-cassandra-connector Create SSL-enabled connector for prod cluster with LOCAL_QUORUM` - Output: Complete connector with SSL, pooling, and health check
**Example 2**: `/scaffold-cassandra-connector Generate multi-keyspace connector with token-aware routing` - Output: Multi-session connector with advanced load balancing

## References
Original: `prompts/scaffold_prompt.md` | Constitution: `${ARCHETYPES_BASEDIR}/cassandra-connector/cassandra-connector-constitution.md`
