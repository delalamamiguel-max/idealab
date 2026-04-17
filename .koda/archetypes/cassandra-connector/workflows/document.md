---
description: Generate documentation for Cassandra connector architecture, operations, and configuration (Cassandra Connector)
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
-- Load `${ARCHETYPES_BASEDIR}/cassandra-connector/templates/env-config.yaml` for documentation templates

### 3. Parse Input
Extract from $ARGUMENTS: connector location, target audience (developers, ops, architects), documentation scope. Request clarification if incomplete.

### 4. Analyze Connector
Extract: cluster topology, keyspace configuration, SSL/TLS setup, pooling parameters, load balancing policy stack, consistency levels, health-check configuration, exception handling patterns.

### 5. Generate Documentation Package
Create: Connector Architecture (class diagram: CassandraConnector, CassandraConfig, CassandraDbConfig, CassandraService, CassandraServiceImpl), Configuration Reference (all 30+ parameters with defaults and recommended values), Operations Runbook (connection troubleshooting, certificate rotation, pool tuning, DC failover procedures), Integration Guide (Spring Boot setup, Maven dependency, configuration properties, health endpoint registration), Performance Tuning Guide (pooling, load balancing, speculative execution, consistency level selection).

### 6. Add Recommendations
Include maintenance procedures, driver upgrade path, disaster recovery, capacity planning.

### 7. Validate and Report
// turbo
Generate documentation. Report completion.

## Error Handling
**Incomplete Information**: Request connector source code location and environment configuration.
**Missing Diagrams**: Generate class and sequence diagrams from connector source.

## Examples
**Example 1**: `/document-cassandra-connector Create full connector documentation package` - Output: Architecture, config reference, ops runbook, and integration guide
**Example 2**: `/document-cassandra-connector Generate operations runbook for multi-DC deployment` - Output: Ops runbook with failover procedures and monitoring setup

## References
Original: `prompts/document_prompt.md` | Constitution: `${ARCHETYPES_BASEDIR}/cassandra-connector/cassandra-connector-constitution.md`
