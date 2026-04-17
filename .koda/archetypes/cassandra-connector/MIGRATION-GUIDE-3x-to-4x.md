# DataStax Java Driver Migration Guide: 3.x → 4.x

> **Target Audience**: Teams migrating the `oce-cassandra-connector` from DataStax Java Driver 3.7.1 to 4.17.x  
> **Estimated Effort**: 2-4 weeks (depending on codebase size and test coverage)  
> **Risk Level**: Medium-High (breaking API changes, configuration overhaul, behavioral differences)

---

## Executive Summary

The DataStax Java Driver 4.x series represents a complete rewrite with:
- **Configuration-driven design** (HOCON/JSON files replace builder pattern)
- **Async-first API** (`CompletionStage<AsyncResultSet>` replaces blocking `ResultSet`)
- **Reactive Streams support** (optional, for backpressure-aware streaming)
- **Improved performance** (reduced allocations, better connection pooling)
- **Breaking changes** in core APIs (`Cluster` → `CqlSession`, `MappingManager` → `Mapper`)

**Key Decision**: Driver 3.x is in **maintenance mode** (security fixes only). Migration to 4.x is recommended for long-term support.

---

## Phase 1: Pre-Migration Assessment

### 1.1 Inventory Current Usage
Run these checks on the `oce-cassandra-connector` codebase:

```bash
# Find all Cluster.builder() usages
grep -r "Cluster\.builder()" src/

# Find all Session usages
grep -r "import com.datastax.driver.core.Session" src/

# Find all MappingManager usages
grep -r "MappingManager" src/

# Find all PoolingOptions usages
grep -r "PoolingOptions" src/

# Find all LoadBalancingPolicy usages
grep -r "LoadBalancingPolicy" src/
```

### 1.2 Identify Breaking Changes in Your Codebase

| Current 3.x Code | Impact | 4.x Equivalent |
|------------------|--------|----------------|
| `Cluster.builder()` | **High** | `CqlSession.builder()` |
| `Session session = cluster.connect()` | **High** | `CqlSession session = CqlSession.builder().build()` |
| `MappingManager` | **High** | `@Mapper` interface + `MapperBuilder` |
| `DCAwareRoundRobinPolicy` | **Medium** | Config file: `basic.load-balancing-policy.local-datacenter` |
| `PoolingOptions` | **Medium** | Config file: `advanced.connection.pool.*` |
| `SSLOptions` | **Medium** | Config file: `advanced.ssl-engine-factory` |
| `QueryOptions.setConsistencyLevel()` | **Medium** | Config file: `basic.request.consistency` |
| `ResultSet.all()` | **Low** | `resultSet.all()` (same, but returns `List<Row>` not `PagingIterable`) |

### 1.3 Compatibility Matrix

| Component | 3.x Version | 4.x Version | Notes |
|-----------|-------------|-------------|-------|
| Cassandra | 2.1+ | 2.1.5+ | 4.x drops support for Cassandra 2.0 |
| Java | 8+ | 8+ | 4.x recommends Java 11+ for production |
| Spring Boot | 2.x | 2.x / 3.x | Spring Boot 3.x requires driver 4.x |
| Netty | 4.0.x | 4.1.x | Bundled, no action needed |

---

## Phase 2: Dependency Migration

### 2.1 Update `pom.xml`

**Before (Driver 3.x)**:
```xml
<dependency>
    <groupId>com.datastax.cassandra</groupId>
    <artifactId>cassandra-driver-core</artifactId>
    <version>3.7.1</version>
</dependency>
<dependency>
    <groupId>com.datastax.cassandra</groupId>
    <artifactId>cassandra-driver-mapping</artifactId>
    <version>3.7.1</version>
</dependency>
```

**After (Driver 4.x)**:
```xml
<dependency>
    <groupId>com.datastax.oss</groupId>
    <artifactId>java-driver-core</artifactId>
    <version>4.17.0</version>
</dependency>
<dependency>
    <groupId>com.datastax.oss</groupId>
    <artifactId>java-driver-query-builder</artifactId>
    <version>4.17.0</version>
</dependency>
<dependency>
    <groupId>com.datastax.oss</groupId>
    <artifactId>java-driver-mapper-runtime</artifactId>
    <version>4.17.0</version>
</dependency>
```

**Note**: Group ID changed from `com.datastax.cassandra` to `com.datastax.oss`.

### 2.2 Add Annotation Processor (for Mapper)

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.11.0</version>
            <configuration>
                <annotationProcessorPaths>
                    <path>
                        <groupId>com.datastax.oss</groupId>
                        <artifactId>java-driver-mapper-processor</artifactId>
                        <version>4.17.0</version>
                    </path>
                </annotationProcessorPaths>
            </configuration>
        </plugin>
    </plugins>
</build>
```

---

## Phase 3: Configuration Migration

### 3.1 Create `application.conf` (HOCON Format)

Driver 4.x uses **Typesafe Config** (HOCON) for configuration. Create `src/main/resources/application.conf`:

```hocon
datastax-java-driver {
  # Basic settings
  basic {
    contact-points = ["10.0.1.10:9042", "10.0.1.11:9042", "10.0.1.12:9042"]
    load-balancing-policy {
      local-datacenter = "us-east-1"
      class = DefaultLoadBalancingPolicy
    }
    request {
      timeout = 12 seconds
      consistency = LOCAL_QUORUM
      page-size = 5000
    }
    session-keyspace = my_keyspace
  }

  # Advanced settings
  advanced {
    connection {
      init-query-timeout = 5 seconds
      set-keyspace-timeout = 5 seconds
      pool {
        local {
          size = 2
        }
        remote {
          size = 1
        }
      }
      max-requests-per-connection = 1024
      max-orphan-requests = 256
    }

    reconnection-policy {
      class = ExponentialReconnectionPolicy
      base-delay = 1 second
      max-delay = 60 seconds
    }

    retry-policy {
      class = DefaultRetryPolicy
    }

    speculative-execution-policy {
      class = ConstantSpeculativeExecutionPolicy
      max-executions = 3
      delay = 100 milliseconds
    }

    ssl-engine-factory {
      class = DefaultSslEngineFactory
      truststore-path = "/opt/certs/cassandra-truststore.jks"
      truststore-password = "${TRUSTSTORE_PASSWORD}"
      hostname-validation = false
    }

    auth-provider {
      class = PlainTextAuthProvider
      username = "${CASSANDRA_USERNAME}"
      password = "${CASSANDRA_PASSWORD}"
    }

    heartbeat {
      interval = 30 seconds
      timeout = 5 seconds
    }

    metrics {
      session.enabled = [connected-nodes, cql-requests, bytes-sent, bytes-received]
      node.enabled = [pool.open-connections, pool.available-streams, bytes-sent, bytes-received]
    }
  }
}
```

### 3.2 Map 3.x Config to 4.x Config

| 3.x Builder Method | 4.x Config Path | Example |
|--------------------|-----------------|---------|
| `.addContactPoint()` | `basic.contact-points` | `["10.0.1.10:9042"]` |
| `.withPort()` | Embedded in contact-points | `"10.0.1.10:9042"` |
| `.withLoadBalancingPolicy(DCAwareRoundRobinPolicy)` | `basic.load-balancing-policy.local-datacenter` | `"us-east-1"` |
| `.withQueryOptions(consistencyLevel)` | `basic.request.consistency` | `LOCAL_QUORUM` |
| `.withSocketOptions(connectTimeout, readTimeout)` | `advanced.connection.init-query-timeout`, `basic.request.timeout` | `5 seconds`, `12 seconds` |
| `.withPoolingOptions(coreConnections, maxConnections)` | `advanced.connection.pool.local.size` | `2` |
| `.withSSL(sslOptions)` | `advanced.ssl-engine-factory.*` | See above |
| `.withAuthProvider(username, password)` | `advanced.auth-provider.*` | See above |
| `.withReconnectionPolicy()` | `advanced.reconnection-policy.*` | See above |
| `.withRetryPolicy()` | `advanced.retry-policy.class` | `DefaultRetryPolicy` |
| `.withSpeculativeExecutionPolicy()` | `advanced.speculative-execution-policy.*` | See above |

### 3.3 Environment Variable Substitution

Driver 4.x supports `${VAR_NAME}` syntax for environment variables in `application.conf`:

```hocon
advanced.auth-provider {
  username = ${CASSANDRA_USERNAME}
  password = ${CASSANDRA_PASSWORD}
}
```

---

## Phase 4: Code Migration

### 4.1 Session Creation

**Before (3.x)**:
```java
Cluster cluster = Cluster.builder()
    .addContactPoint("10.0.1.10")
    .withPort(9042)
    .withCredentials("user", "pass")
    .build();
Session session = cluster.connect("my_keyspace");
```

**After (4.x)**:
```java
// Option 1: Using application.conf
CqlSession session = CqlSession.builder().build();

// Option 2: Programmatic (not recommended)
CqlSession session = CqlSession.builder()
    .addContactPoint(new InetSocketAddress("10.0.1.10", 9042))
    .withLocalDatacenter("us-east-1")
    .withAuthCredentials("user", "pass")
    .withKeyspace("my_keyspace")
    .build();
```

**Key Changes**:
- `Cluster` + `Session` → single `CqlSession`
- `CqlSession` is `AutoCloseable` — use try-with-resources
- No separate `cluster.connect()` step

### 4.2 Prepared Statements

**Before (3.x)**:
```java
PreparedStatement ps = session.prepare("SELECT * FROM users WHERE id = ?");
BoundStatement bound = ps.bind(userId);
ResultSet rs = session.execute(bound);
```

**After (4.x)**:
```java
PreparedStatement ps = session.prepare("SELECT * FROM users WHERE id = ?");
BoundStatement bound = ps.bind(userId);
ResultSet rs = session.execute(bound);
```

**No change in basic usage**, but:
- `ResultSet` is now `com.datastax.oss.driver.api.core.cql.ResultSet`
- `Row` is now `com.datastax.oss.driver.api.core.cql.Row`
- Column access: `row.getString("name")` → same

### 4.3 Async Queries

**Before (3.x)**:
```java
ResultSetFuture future = session.executeAsync(statement);
ResultSet rs = future.getUninterruptibly();
```

**After (4.x)**:
```java
CompletionStage<AsyncResultSet> futureRs = session.executeAsync(statement);
AsyncResultSet rs = futureRs.toCompletableFuture().join();

// Better: Use async chain
session.executeAsync(statement)
    .thenAccept(rs -> {
        for (Row row : rs.currentPage()) {
            // process row
        }
    });
```

**Key Changes**:
- `ResultSetFuture` → `CompletionStage<AsyncResultSet>`
- `AsyncResultSet` supports pagination via `fetchNextPage()`

### 4.4 Object Mapper Migration

**Before (3.x)**:
```java
MappingManager manager = new MappingManager(session);
Mapper<User> mapper = manager.mapper(User.class);

// CRUD
User user = mapper.get(userId);
mapper.save(user);
mapper.delete(userId);
```

**After (4.x)**:
```java
// 1. Define entity
@Entity
@CqlName("users")
public class User {
    @PartitionKey
    private UUID id;
    private String name;
    // getters/setters
}

// 2. Define DAO interface
@Dao
public interface UserDao {
    @Select
    User findById(UUID id);
    
    @Insert
    void save(User user);
    
    @Delete
    void delete(User user);
}

// 3. Define Mapper interface
@Mapper
public interface AppMapper {
    @DaoFactory
    UserDao userDao(@DaoKeyspace CqlIdentifier keyspace);
}

// 4. Usage
AppMapper mapper = new AppMapperBuilder(session).build();
UserDao userDao = mapper.userDao(CqlIdentifier.fromCql("my_keyspace"));

User user = userDao.findById(userId);
userDao.save(user);
userDao.delete(user);
```

**Key Changes**:
- `MappingManager` → `@Mapper` + `@Dao` interfaces (compile-time code generation)
- More boilerplate, but type-safe and faster
- Requires annotation processor in `pom.xml`

### 4.5 Batch Statements

**Before (3.x)**:
```java
BatchStatement batch = new BatchStatement();
batch.add(statement1);
batch.add(statement2);
session.execute(batch);
```

**After (4.x)**:
```java
BatchStatement batch = BatchStatement.builder(DefaultBatchType.LOGGED)
    .addStatement(statement1)
    .addStatement(statement2)
    .build();
session.execute(batch);
```

**Key Changes**:
- Builder pattern for `BatchStatement`
- Explicit batch type: `LOGGED`, `UNLOGGED`, `COUNTER`

### 4.6 Consistency Level

**Before (3.x)**:
```java
Statement stmt = new SimpleStatement("SELECT ...");
stmt.setConsistencyLevel(ConsistencyLevel.LOCAL_QUORUM);
session.execute(stmt);
```

**After (4.x)**:
```java
SimpleStatement stmt = SimpleStatement.builder("SELECT ...")
    .setConsistencyLevel(DefaultConsistencyLevel.LOCAL_QUORUM)
    .build();
session.execute(stmt);
```

**Key Changes**:
- `ConsistencyLevel` → `DefaultConsistencyLevel`
- Builder pattern for statements

### 4.7 Exception Handling

**Before (3.x)**:
```java
try {
    session.execute(statement);
} catch (NoHostAvailableException e) {
    // handle
} catch (QueryExecutionException e) {
    // handle
}
```

**After (4.x)**:
```java
try {
    session.execute(statement);
} catch (AllNodesFailedException e) {
    // handle (was NoHostAvailableException)
} catch (DriverException e) {
    // handle (base class for all driver exceptions)
}
```

**Key Changes**:
- `NoHostAvailableException` → `AllNodesFailedException`
- `QueryExecutionException` → specific exceptions (`QueryValidationException`, `QueryExecutionException`)

---

## Phase 5: Testing Strategy

### 5.1 Unit Tests

1. **Mock `CqlSession`** using Mockito:
```java
CqlSession session = mock(CqlSession.class);
PreparedStatement ps = mock(PreparedStatement.class);
when(session.prepare(anyString())).thenReturn(ps);
```

2. **Use Embedded Cassandra** (for integration tests):
```xml
<dependency>
    <groupId>com.github.nosan</groupId>
    <artifactId>embedded-cassandra-spring-boot-starter</artifactId>
    <version>4.1.3</version>
    <scope>test</scope>
</dependency>
```

### 5.2 Integration Tests

1. **Verify connection pooling**:
```java
CqlSession session = CqlSession.builder().build();
Metrics metrics = session.getMetrics()
    .orElseThrow(() -> new IllegalStateException("Metrics not enabled"));

// Check pool size
metrics.getNodeMetric(node, DefaultNodeMetric.OPEN_CONNECTIONS);
```

2. **Verify SSL handshake**:
```java
// Enable SSL in application.conf
// Run query and verify no SSLException
session.execute("SELECT release_version FROM system.local");
```

3. **Verify failover**:
```bash
# Simulate node failure
docker stop cassandra-node-1

# Verify app continues to work (may see brief errors)
curl http://localhost:8080/health
```

### 5.3 Performance Testing

Compare 3.x vs 4.x latency:
```java
long start = System.nanoTime();
for (int i = 0; i < 10000; i++) {
    session.execute(preparedStatement.bind(i));
}
long duration = System.nanoTime() - start;
System.out.println("Avg latency: " + (duration / 10000 / 1000) + " µs");
```

**Expected**: 4.x should be 10-20% faster due to reduced allocations.

---

## Phase 6: Deployment Strategy

### 6.1 Blue-Green Deployment

1. **Deploy 4.x version to staging** with full test suite
2. **Run parallel load test** (3.x prod + 4.x staging)
3. **Compare metrics** (latency, error rate, connection pool usage)
4. **Switch 10% traffic** to 4.x (canary)
5. **Monitor for 24 hours**
6. **Gradually increase** to 50%, then 100%

### 6.2 Rollback Plan

Keep 3.x version deployable for 2 weeks post-migration:
```bash
# Rollback command
kubectl set image deployment/cassandra-connector app=cassandra-connector:3.x-stable
```

### 6.3 Monitoring

Add these alerts:
- `AllNodesFailedException` count > 0
- Connection pool exhaustion (`available-streams` = 0)
- Query latency p99 > 500ms
- SSL handshake failures > 1%

---

## Phase 7: Post-Migration Optimization

### 7.1 Enable Metrics

```hocon
advanced.metrics {
  session.enabled = [
    connected-nodes,
    cql-requests,
    cql-client-timeouts,
    bytes-sent,
    bytes-received,
    throttling.errors
  ]
  node.enabled = [
    pool.open-connections,
    pool.available-streams,
    pool.in-flight,
    bytes-sent,
    bytes-received,
    errors.request.unsent,
    errors.request.aborted,
    errors.request.write-timeouts,
    errors.request.read-timeouts,
    errors.request.unavailables,
    errors.request.others
  ]
}
```

### 7.2 Tune Connection Pool

```hocon
advanced.connection.pool {
  local.size = 2  # Start with 2, increase if pool exhaustion occurs
  remote.size = 1
}
```

Monitor `pool.available-streams` metric. If frequently < 100, increase `local.size`.

### 7.3 Enable Request Throttling

```hocon
advanced.throttler {
  class = ConcurrencyLimitingRequestThrottler
  max-concurrent-requests = 10000
  max-queue-size = 100000
}
```

Prevents OOM under extreme load.

---

## Phase 8: Known Issues & Workarounds

### 8.1 Issue: `application.conf` Not Loaded

**Symptom**: Driver uses defaults, ignores config file.

**Cause**: `application.conf` not in classpath root.

**Fix**:
```java
// Explicit config loading
DriverConfigLoader loader = DriverConfigLoader.fromFile(new File("config/application.conf"));
CqlSession session = CqlSession.builder()
    .withConfigLoader(loader)
    .build();
```

### 8.2 Issue: SSL Handshake Failure

**Symptom**: `javax.net.ssl.SSLHandshakeException: PKIX path building failed`

**Cause**: Truststore not loaded or wrong password.

**Fix**:
```hocon
advanced.ssl-engine-factory {
  class = DefaultSslEngineFactory
  truststore-path = "/opt/certs/cassandra-truststore.jks"
  truststore-password = "${TRUSTSTORE_PASSWORD}"
  hostname-validation = false  # Disable if using IP addresses
}
```

### 8.3 Issue: Mapper Annotation Processor Not Running

**Symptom**: `AppMapperBuilder` class not found.

**Cause**: Annotation processor not configured.

**Fix**: Add to `pom.xml`:
```xml
<annotationProcessorPaths>
    <path>
        <groupId>com.datastax.oss</groupId>
        <artifactId>java-driver-mapper-processor</artifactId>
        <version>4.17.0</version>
    </path>
</annotationProcessorPaths>
```

Then run `mvn clean compile`.

---

## Phase 9: Migration Checklist

- [ ] Update `pom.xml` dependencies (3.x → 4.x)
- [ ] Add annotation processor for Mapper
- [ ] Create `application.conf` with all settings
- [ ] Migrate `Cluster.builder()` → `CqlSession.builder()`
- [ ] Migrate `MappingManager` → `@Mapper` + `@Dao`
- [ ] Update exception handling (`NoHostAvailableException` → `AllNodesFailedException`)
- [ ] Update imports (`com.datastax.driver.core` → `com.datastax.oss.driver.api.core`)
- [ ] Migrate async code (`ResultSetFuture` → `CompletionStage`)
- [ ] Update unit tests (mock `CqlSession` instead of `Session`)
- [ ] Run integration tests with embedded Cassandra
- [ ] Performance test (compare 3.x vs 4.x latency)
- [ ] Update health check endpoint
- [ ] Enable driver metrics in config
- [ ] Deploy to staging and validate
- [ ] Canary deployment (10% traffic)
- [ ] Monitor for 24 hours
- [ ] Full rollout
- [ ] Update documentation and runbooks

---

## Phase 10: Reference Materials

| Resource | URL |
|----------|-----|
| Driver 4.17 Documentation | https://docs.datastax.com/en/developer/java-driver/4.17/ |
| Upgrade Guide (Official) | https://docs.datastax.com/en/developer/java-driver/4.17/upgrade_guide/ |
| Configuration Reference | https://docs.datastax.com/en/developer/java-driver/4.17/manual/core/configuration/ |
| Mapper Documentation | https://docs.datastax.com/en/developer/java-driver/4.17/manual/mapper/ |
| Migration FAQ | https://docs.datastax.com/en/developer/java-driver/4.17/faq/ |
| GitHub Repository | https://github.com/datastax/java-driver |
| Community Forum | https://community.datastax.com/ |

---

## Appendix A: Side-by-Side Comparison

### A.1 Session Creation

| Aspect | 3.x | 4.x |
|--------|-----|-----|
| **Entry Point** | `Cluster.builder()` | `CqlSession.builder()` |
| **Configuration** | Programmatic (builder methods) | File-based (`application.conf`) |
| **Connection** | `cluster.connect(keyspace)` | `CqlSession.builder().withKeyspace()` |
| **Lifecycle** | Manual `cluster.close()` | `AutoCloseable` (try-with-resources) |

### A.2 Query Execution

| Aspect | 3.x | 4.x |
|--------|-----|-----|
| **Sync** | `session.execute(statement)` | `session.execute(statement)` |
| **Async** | `session.executeAsync()` → `ResultSetFuture` | `session.executeAsync()` → `CompletionStage<AsyncResultSet>` |
| **Reactive** | Not supported | `session.executeReactive()` → `Flux<ReactiveRow>` |

### A.3 Object Mapping

| Aspect | 3.x | 4.x |
|--------|-----|-----|
| **Setup** | `new MappingManager(session)` | `@Mapper` interface + annotation processor |
| **CRUD** | `mapper.get()`, `mapper.save()` | `@Select`, `@Insert`, `@Update`, `@Delete` annotations |
| **Type Safety** | Runtime (reflection) | Compile-time (code generation) |

---

## Appendix B: Quick Reference Card

```java
// ========== SESSION CREATION ==========
// 3.x
Cluster cluster = Cluster.builder().addContactPoint("10.0.1.10").build();
Session session = cluster.connect("my_keyspace");

// 4.x
CqlSession session = CqlSession.builder().build(); // Uses application.conf

// ========== PREPARED STATEMENTS ==========
// 3.x & 4.x (same)
PreparedStatement ps = session.prepare("SELECT * FROM users WHERE id = ?");
BoundStatement bound = ps.bind(userId);
ResultSet rs = session.execute(bound);

// ========== ASYNC QUERIES ==========
// 3.x
ResultSetFuture future = session.executeAsync(statement);
ResultSet rs = future.getUninterruptibly();

// 4.x
CompletionStage<AsyncResultSet> future = session.executeAsync(statement);
AsyncResultSet rs = future.toCompletableFuture().join();

// ========== CONSISTENCY LEVEL ==========
// 3.x
statement.setConsistencyLevel(ConsistencyLevel.LOCAL_QUORUM);

// 4.x
SimpleStatement stmt = SimpleStatement.builder("SELECT ...")
    .setConsistencyLevel(DefaultConsistencyLevel.LOCAL_QUORUM)
    .build();

// ========== EXCEPTION HANDLING ==========
// 3.x
catch (NoHostAvailableException e) { }

// 4.x
catch (AllNodesFailedException e) { }

// ========== CLOSING SESSION ==========
// 3.x
cluster.close();

// 4.x
session.close(); // Or use try-with-resources
```

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-18  
**Maintained By**: OCE Cassandra Connector Team
