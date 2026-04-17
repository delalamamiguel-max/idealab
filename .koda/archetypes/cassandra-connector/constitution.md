
# Cassandra Connector Archetype Constitution

## Purpose
Establish standard, secure, and performant practices for Java Spring Boot applications that connect to Apache Cassandra clusters using the DataStax driver, with governed configuration for SSL/TLS, connection pooling, load balancing, consistency levels, health monitoring, query safety, and operational governance.

## I. Hard-Stop Rules (Non-Negotiable)

### Security & Credentials
- ✘ Cassandra credentials (username, password) MUST be sourced from Azure Key Vault or an equivalent secret manager; plain-text credentials in source or config files are prohibited.
- ✘ SSL/TLS MUST be enabled for all non-local Cassandra connections with TLS 1.2 or higher; TLS 1.0 and TLS 1.1 are prohibited. Unencrypted traffic to remote clusters is prohibited.
- ✘ Truststore passwords MUST NOT be committed to version control or hardcoded in application code.
- ✘ Cassandra node IPs MUST NOT be hardcoded in Java source files; they MUST be externalized via Spring configuration properties.
- ✘ `CassandraDbConfig.toString()` and all log statements MUST NOT include passwords, truststore passwords, or any secret material. *(Source: OWASP Logging Cheat Sheet, CWE-532)*

### Query & Consistency Safety
- The `consistencyLevel` MUST be explicitly set per keyspace; relying on the driver default (`ONE`) without review is prohibited.
- The Cassandra driver version should be at least 4.17.0; older versions of drivers are not supported. 
- The Cassandra cluster should be at least 5.0.0; older versions are not supported.
- Health-check queries MUST NOT perform full-table scans or unbounded reads.
- All repeated CQL queries MUST use `PreparedStatement`; constructing CQL strings via concatenation or `SimpleStatement` in loops is prohibited. *(Source: [DataStax — Prepared Statements](https://docs.datastax.com/en/developer/java-driver/4.17/manual/core/statements/prepared/))*
- Queries using `ALLOW FILTERING` MUST NOT be deployed to production; they MUST be flagged during code review and replaced with properly modeled tables or materialized views. *(Source: [Apache Cassandra — CQL SELECT](https://cassandra.apache.org/doc/latest/cassandra/cql/dml.html#select))*
- `BatchStatement` MUST NOT span multiple partitions; batch inserts MUST only group mutations targeting the **same partition key**. *(Source: [DataStax — Batching Best Practices](https://docs.datastax.com/en/dse/6.8/cql/cql/cql_using/useBatch.html))*

### Resource Lifecycle
- ✘ Only ONE `CqlSession` instance MUST be created per Cassandra cluster endpoint; creating multiple `CqlSession` objects for the same contact points is prohibited. *(Source: [DataStax — Driver Architecture](https://docs.datastax.com/en/developer/java-driver/4.17/manual/core/))*

## II. Mandatory Patterns (Must Apply)

### Connection & Timeout Configuration
- ✔ Every connection MUST configure `connectTimeoutMillis` and `readTimeoutMillis` with values appropriate for the target environment.
- ✔ A `DCAwareRoundRobinPolicy` MUST be configured with an explicit `localDataCenter` value matching the deployment region.
- ✔ Connection pooling settings (`coreConnectionsPerHost`, `maxConnectionsPerHost`, `poolTimeoutMillis`) MUST be tuned per environment; default driver values MUST NOT be used in production.
- ✔ Heartbeat interval (`heartbeatIntervalSeconds`) MUST be configured to detect stale connections before they cause request failures.

### Lifecycle & Exception Handling
- ✔ A `@PreDestroy` lifecycle hook MUST explicitly close all `CqlSession` objects on application shutdown; logging without closing resources causes connection leaks. *(Source: [DataStax — Session Lifecycle](https://docs.datastax.com/en/developer/java-driver/4.17/manual/core/))*
- ✔ All Cassandra operations MUST be wrapped in structured exception handling using a project-specific exception hierarchy (e.g., `CassandraException` with `CassandraResponseEnum`).
- ✔ A health-check endpoint MUST be implemented to validate Cassandra connectivity and session liveness.

### Retry & Idempotence
- ✔ A retry policy MUST be explicitly configured in `application.conf`; the choice between `DefaultRetryPolicy`, `FallthroughRetryPolicy`, or a custom policy MUST be documented per environment. *(Source: [DataStax — Retries](https://docs.datastax.com/en/developer/java-driver/4.17/manual/core/retries/))*
- ✔ All queries MUST have idempotence explicitly set at the statement level or via configuration. Non-idempotent writes (e.g., counter updates, list appends) MUST be marked `setIdempotent(false)`. *(Source: [DataStax — Retries and Idempotence](https://docs.datastax.com/en/developer/java-driver/4.17/manual/core/retries/))*

### Query Safety
- ✔ All queries that may return more than 5000 rows MUST use the driver's automatic pagination (`setPageSize()`) or manual paging state; unbounded result set retrieval via `results.all()` is prohibited for large datasets. *(Source: [DataStax — Paging](https://docs.datastax.com/en/developer/java-driver/4.17/manual/core/paging/))*
- ✔ Queries MUST specify explicit column names; `SELECT *` is prohibited because schema changes (adding/removing columns) silently break prepared statement metadata and cause runtime errors. *(Source: [DataStax — Prepared Statements Best Practices](https://docs.datastax.com/en/developer/java-driver/4.17/manual/core/statements/prepared/))*

### Observability
- ✔ Cassandra driver metrics (connection pool usage, in-flight requests, request latencies, retries, errors) MUST be exposed via JMX, Micrometer, or a custom metrics registry for production monitoring. *(Source: [DataStax — Metrics](https://docs.datastax.com/en/developer/java-driver/4.17/manual/core/metrics/))*

## III. Preferred Patterns (Recommended)

### Load Balancing & Routing
- ➜ Enable `TokenAwarePolicy` on top of `DCAwareRoundRobinPolicy` to route requests directly to the replica owning the partition key.
- ➜ Enable `LatencyAwarePolicy` to exclude slow-performing nodes from query plans during transient degradation.
- ➜ Configure address translation (`CassAddressTranslator`) when Cassandra nodes are behind NAT or VPN gateways.

### Speculative Execution & Resilience
- ➜ Enable speculative execution (`PercentileSpeculativeExecutionPolicy`) for latency-sensitive read paths to reduce tail latency.
- ➜ Wrap Cassandra operations with a circuit breaker (e.g., Resilience4j, Spring Circuit Breaker) to prevent cascade failures when the cluster is degraded. *(Source: Netflix Hystrix pattern, Resilience4j)*

### Query & Data Patterns
- ➜ Use `MappingManager` with DataStax object-mapper annotations for type-safe CRUD instead of raw CQL strings.
- ➜ Parameterize TTL values per table/entity rather than applying a single global TTL.
- ➜ Use `LOCAL_QUORUM` consistency for cross-datacenter deployments to balance durability and latency.
- ➜ Lightweight transactions (`IF NOT EXISTS`, `IF condition`) should be used only when strong consistency is required (e.g., unique constraints); they incur a ~4x latency penalty due to Paxos consensus rounds. *(Source: [Apache Cassandra — Lightweight Transactions](https://cassandra.apache.org/doc/latest/cassandra/cql/dml.html#insert))*
- ➜ Configure different execution profiles (timeout, consistency, retry policy) for read-heavy vs write-heavy vs batch workloads rather than applying a single global configuration. *(Source: [DataStax — Execution Profiles](https://docs.datastax.com/en/developer/java-driver/4.17/manual/core/configuration/))*

### Performance Optimization
- ➜ Use `executeAsync()` or `Mapper.saveAsync()` for fire-and-forget writes where the caller does not need to wait for acknowledgment, to improve throughput. *(Source: [DataStax — Asynchronous API](https://docs.datastax.com/en/developer/java-driver/4.17/manual/core/async/))*
- ➜ Enable LZ4 or Snappy compression in `application.conf` via `advanced.protocol.compression` to reduce network bandwidth for large payloads. Requires `lz4-java` dependency. *(Source: [DataStax — Compression](https://docs.datastax.com/en/developer/java-driver/4.17/manual/core/compression/))*
- ➜ Execute a lightweight query (e.g., `SELECT release_version FROM system.local`) immediately after session creation to warm up the connection pool and detect configuration issues early. *(Source: [DataStax — Connection Pooling](https://docs.datastax.com/en/developer/java-driver/4.17/manual/core/pooling/))*

### Idempotence & Configuration
- ➜ Set `defaultIdempotence(true)` on the cluster builder so the driver can safely retry idempotent queries.
- ➜ Implement periodic checks for partition sizes (target < 100MB) and tombstone counts (warn at > 1000 per read) via `nodetool tablehistograms` or driver-level tracing. *(Source: [Apache Cassandra — Operations Guide](https://cassandra.apache.org/doc/latest/cassandra/operating/index.html))*

## IV. Anti-Patterns (Must Avoid)
- ✘ **Cluster/Session Per Request**: NEVER create a new `Cluster` or `Session` object per API request. Session creation involves TCP handshake, authentication, and schema metadata exchange — typically 500ms–2s per creation.
- ✘ **Large IN Clauses**: AVOID `IN` clauses with more than ~20 values. The coordinator must contact multiple partitions, creating a single point of contention. Use individual async queries instead.
- ✘ **Secondary Indexes on High-Cardinality Columns**: AVOID secondary indexes on columns with high cardinality (e.g., UUIDs, timestamps). Secondary indexes are local to each node and require scatter-gather queries across all nodes.
- ✘ **Mixing LWT and Non-LWT Writes**: NEVER mix conditional (`IF`) and non-conditional writes to the same partition. This breaks Paxos consistency guarantees and can cause data loss.
- ✘ **Ignoring NoHostAvailableException**: `NoHostAvailableException` MUST trigger immediate alerting — it means the driver cannot reach ANY node. Silently catching this exception masks total cluster failure.
- ✘ **Unlogged Multi-Partition Batches**: NEVER use unlogged batches across partitions as a "performance optimization." Unlogged multi-partition batches provide no atomicity guarantee and add coordinator overhead.

## V. Driver Migration Governance (3.x → 4.x)

The current connector uses **DataStax Java Driver 3.7.1**. Version 3.x is in maintenance mode (security fixes only). Migration to **4.17.x** is recommended. See `MIGRATION-GUIDE-3x-to-4x.md` for detailed migration instructions.

### API Migration Map
| 3.x API | 4.x Equivalent |
|---------|---------------|
| `Cluster.builder()` | `CqlSession.builder()` |
| `Session` | `CqlSession` |
| `MappingManager` | `@Entity` + `@Dao` + `MapperBuilder` |
| `DCAwareRoundRobinPolicy` | Built into default profile (`basic.load-balancing-policy`) |
| `PoolingOptions` | `advanced.connection.pool` in config file |
| `withSSL(SSLOptions)` | `advanced.ssl-engine-factory` in config file |

### Migration Rules
- Driver 4.x moves from programmatic configuration (builder pattern) to file-based configuration (`application.conf` / `application.json`). The migration must preserve all existing parameters.
- Driver 4.x is async-first (`CompletionStage<AsyncResultSet>`). Synchronous methods are convenience wrappers. Plan to adopt the async API for new code paths.
- Plan migration to 4.x within the next major release cycle.

## VI. Operational Governance

- ✔ **Certificate Rotation**: A documented, tested certificate rotation procedure MUST exist for SSL-enabled clusters covering: generate new truststore, deploy to all instances, rolling restart, verify SSL handshake, remove old certificates.
- ✔ **Connection Leak Detection**: Monitor the delta between `open_connections` and `available_connections` in the driver pool. Alert if open connections exceed `maxConnectionsPerHost` for more than 5 minutes.
- ✔ **Schema Change Governance**: Schema changes (DDL: `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE`) MUST NOT be executed through the application connector. Schema migrations MUST use a dedicated migration tool (e.g., `cassandra-migration`, manual CQL scripts with approval).
- ✔ **Multi-DC Failover Testing**: Quarterly failover drills MUST be conducted to verify `DCAwareRoundRobinPolicy` correctly routes traffic to the remote DC when the local DC is unavailable.
- ✔ **Capacity Planning**: Connection pool sizing MUST be reviewed quarterly using the formula: `required_connections = (peak_rps * avg_latency_ms) / (1000 * max_requests_per_connection)`. Alert when pool utilization exceeds 80%.

## VII. Example: Minimum Viable Configuration Map

```java
Map<String, String> dbConfigMap = new HashMap<>();
dbConfigMap.put("clusterName", "prod-cassandra-cluster");
dbConfigMap.put("cassandraNodeIP", "10.0.1.10,10.0.1.11,10.0.1.12");
dbConfigMap.put("port", "9042");
dbConfigMap.put("localDataCenter", "us-east-1");
dbConfigMap.put("usedHostsPerRemoteDc", "2");
dbConfigMap.put("keySpaceName", "my_keyspace");
dbConfigMap.put("userName", "${CASSANDRA_USERNAME}");
dbConfigMap.put("password", "${CASSANDRA_PASSWORD}");
dbConfigMap.put("sslEnabled", "true");
dbConfigMap.put("digiCertEnabled", "false");
dbConfigMap.put("trustStoreLocation", "/opt/certs/cassandra-truststore.jks");
dbConfigMap.put("trustStorePwd", "${TRUSTSTORE_PASSWORD}");
dbConfigMap.put("connectTimeoutMillis", "5000");
dbConfigMap.put("readTimeoutMillis", "12000");
dbConfigMap.put("heartbeatIntervalSeconds", "30");
dbConfigMap.put("consistencyLocalQuorumEnabled", "true");
dbConfigMap.put("useConnectionPooling", "true");
dbConfigMap.put("coreConnectionsPerHost", "2");
dbConfigMap.put("maxConnectionsPerHost", "8");
dbConfigMap.put("poolTimeoutMillis", "5000");
```

## VIII. Source References

| # | Source | URL |
|---|--------|-----|
| 1 | DataStax Java Driver 4.17 — Manual | https://docs.datastax.com/en/developer/java-driver/4.17/ |
| 2 | DataStax Java Driver 4.17 — Core Driver | https://docs.datastax.com/en/developer/java-driver/4.17/manual/core/ |
| 3 | DataStax Java Driver 4.17 — Prepared Statements | https://docs.datastax.com/en/developer/java-driver/4.17/manual/core/statements/prepared/ |
| 4 | DataStax Java Driver 4.17 — Connection Pooling | https://docs.datastax.com/en/developer/java-driver/4.17/manual/core/pooling/ |
| 5 | DataStax Java Driver 4.17 — Retries | https://docs.datastax.com/en/developer/java-driver/4.17/manual/core/retries/ |
| 6 | DataStax Java Driver 4.17 — Metrics | https://docs.datastax.com/en/developer/java-driver/4.17/manual/core/metrics/ |
| 7 | DataStax Java Driver 4.17 — Compression | https://docs.datastax.com/en/developer/java-driver/4.17/manual/core/compression/ |
| 8 | DataStax Java Driver 4.17 — Configuration | https://docs.datastax.com/en/developer/java-driver/4.17/manual/core/configuration/ |
| 9 | DataStax Java Driver 4.17 — Paging | https://docs.datastax.com/en/developer/java-driver/4.17/manual/core/paging/ |
| 10 | DataStax Java Driver 4.17 — Async API | https://docs.datastax.com/en/developer/java-driver/4.17/manual/core/async/ |
| 11 | DataStax Java Driver 4.17 — Upgrade Guide | https://docs.datastax.com/en/developer/java-driver/4.17/upgrade_guide/ |
| 12 | Apache Cassandra — CQL Reference | https://cassandra.apache.org/doc/latest/cassandra/cql/ |
| 13 | Apache Cassandra — Operations Guide | https://cassandra.apache.org/doc/latest/cassandra/operating/index.html |
| 14 | OWASP — Logging Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html |

## IX. Version
- 2.1.0

## X. Last Updated
- 2026-02-18

## XI. Related Documents
- [Migration Guide: Driver 3.x → 4.x](./MIGRATION-GUIDE-3x-to-4x.md)
