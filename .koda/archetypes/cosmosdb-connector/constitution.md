# Cosmos DB Connector Constitution

## Purpose

This constitution defines the foundational principles and hard-stop rules for the **Cosmos DB Connector** archetype, which generates production-ready Azure Cosmos DB client libraries and connectors for Spring Boot applications with auto-configuration, retry logic, and comprehensive query support.

**Scope:** Cosmos DB client libraries, Spring Boot auto-configuration, connection management, query services (sync/async), retry mechanisms, and Maven/Gradle-based packaging. The agent must not introduce UI, frontend, or unrelated backend services.

**Source**: Created from analysis of Azure Cosmos DB connector patterns and AT&T archetype collection standards

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** or correct any code or design that violates these rules:

### Security
- ✘ **No hardcoded secrets**: Do not include Cosmos DB keys, connection strings, or credentials directly in code
- ✘ **No plaintext credentials in properties**: Credentials must be externalized via Azure Key Vault or environment variables
- ✘ **No logging of secrets**: Do not log connection strings, secret keys, or sensitive query parameters
- ✘ **No PII exposure in logs**: Do not log document contents, partition keys, or query results containing PII
- ✘ **No SQL injection**: Do not construct queries with string concatenation; use parameterized queries with `SqlQuerySpec`
- ✘ **No exposed error details**: Production errors must not leak internal paths, connection strings, or stack traces

### Configuration & Connection Management
- ✘ **No missing auto-configuration**: Must provide Spring Boot auto-configuration with `@EnableConfigurationProperties`
- ✘ **No connection leaks**: Must properly manage `CosmosClient` and `CosmosAsyncClient` lifecycle as Spring beans
- ✘ **No missing refresh scope**: Configuration beans must support `@RefreshScope` for dynamic updates
- ✘ **No hardcoded database names**: Database and container names must be configurable via properties
- ✘ **No missing consistency level**: Must specify consistency level (EVENTUAL, BOUNDED_STALENESS, SESSION, etc.)
- ✘ **No unbounded connection pools**: Must configure `maxConnectionPool` and `idleConnectionTimeout`

### Query & Data Operations
- ✘ **No unbounded queries**: All queries must support pagination with configurable page size
- ✘ **No missing retry logic**: Must implement retry mechanisms for transient failures (ReadTimeoutException, CosmosException)
- ✘ **No silent error swallowing**: All exceptions must be logged with structured diagnostics before retry or propagation
- ✘ **No missing partition key**: All item operations (read, create, upsert, patch) must specify partition key
- ✘ **No improper bulk operations**: Bulk operations must validate item count and handle partial failures

### Code Quality
- ✘ **No incompatible dependency versions**: Verify Azure Cosmos SDK compatibility with Spring Boot version
- ✘ **No missing null checks**: All Cosmos responses must be null-checked before accessing properties
- ✘ **No improper exception handling**: Must distinguish between retriable (429, timeout) and non-retriable (404, 409) errors
- ✘ **No missing metrics**: Must support query metrics logging when enabled

## II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify these patterns:

### Project Structure (Maven/Gradle)
- ✔ **Build tool support**: Support both Maven and Gradle build configurations
- ✔ **Maven packaging**: Use `<packaging>jar</packaging>` for library artifacts
- ✔ **Gradle packaging**: Use `java-library` plugin for library artifacts
- ✔ **Proper artifact naming**: Follow convention `{org}-cosmos-connector` or `{org}-cosmos-client`
- ✔ **Sonar configuration**: Include Sonar properties for code coverage and quality gates
- ✔ **Test framework**: Use JUnit 5 (jupiter-engine) and Spock for testing
- ✔ **Gradle wrapper**: Include Gradle wrapper for Gradle projects (gradlew, gradlew.bat)

### Spring Boot Auto-Configuration
- ✔ **Configuration properties class**: Create `@ConfigurationProperties` class for Cosmos settings
- ✔ **Properties map support**: Support multiple Cosmos database connections via map-based configuration
- ✔ **Auto-configuration class**: Provide `@Configuration` class with `@ConditionalOnProperty` guard
- ✔ **Bean registration**: Register `CosmosClient`, `CosmosAsyncClient`, `CosmosDatabase`, `CosmosAsyncDatabase` as beans
- ✔ **Refresh scope**: Apply `@RefreshScope` to configuration beans for runtime updates
- ✔ **Connection mode**: Support both direct mode and gateway mode configuration

### Configuration Properties Pattern
```java
@ConfigurationProperties(prefix = "cosmos.config")
public class CosmosPropertiesMap {
    private Map<String, Map<String, String>> config;
    // getters/setters
}

public class CosmosProperties {
    private String hostName;
    private String secretKey;
    private String databaseName;
    private String preferredRegion;
    private String consistencyLevel = "BOUNDED_STALENESS";
    private Long idleConnectionTimeout = 1000L;
    private Integer maxConnectionPool = 50;
    private Boolean directModeEnabled = true;
    private String agentSuffix;
    private Boolean contentResponseOnWriteEnabled = false;
}
```

### Query Service Patterns
- ✔ **Generic service**: Implement `CosmosQueryService<T>` with type parameter support
- ✔ **Sync and async services**: Provide both synchronous and asynchronous query services
- ✔ **CRUD operations**: Implement create, read, upsert, patch, delete operations
- ✔ **Bulk operations**: Support bulk patch and bulk upsert with `CosmosBulkOperations`
- ✔ **Parameterized queries**: Use `SqlQuerySpec` with `SqlParameter` for safe queries
- ✔ **Pagination support**: All list operations must support page size and continuation tokens
- ✔ **Query metrics**: Expose query metrics when `cosmos.print.metrics=true`

### Retry Logic Patterns
- ✔ **Configurable retry**: Support `cosmos.retry.enabled`, `cosmos.retry.count`, `cosmos.retry.sleep.time`
- ✔ **Sync and async retry**: Implement both synchronous and asynchronous retry mechanisms
- ✔ **Exception classification**: Classify exceptions as retriable vs non-retriable
- ✔ **Status code retry**: Support retry based on HTTP status codes (429, 503, etc.)
- ✔ **Backoff strategy**: Implement sleep/wait between retry attempts
- ✔ **Retry exhaustion**: Log and propagate exceptions after retry exhaustion

### Retry Configuration Pattern
```java
@Value("${cosmos.retry.enabled:false}")
private boolean cosmosRetryEnabled;

@Value("${cosmos.retry.count:3}")
private int cosmosRetryCount;

@Value("${cosmos.retry.sleep.time:100}")
private Long cosmosRetryWaitTime;

@Value("${cosmos.sync.retry.enabled:false}")
private boolean cosmosSyncRetryEnabled;

@Value("#{'${cosmos.retryable.exceptions}'.split(',')}")
private List<String> cosmosRetriableExceptions;

@Value("#{'${cosmos.retry.status.code:0}'.split(',')}")
private List<Integer> cosmosRetryStatusCode;
```

### Error Handling Patterns
- ✔ **Custom exception**: Define `CosmosQueryException` with status code support
- ✔ **Exception wrapping**: Wrap Cosmos SDK exceptions with context and trace information
- ✔ **Structured logging**: Use SLF4J with structured log messages including operation type, retry count
- ✔ **404 handling**: Special handling for 404 errors with optional fallback to create operation
- ✔ **Optimistic concurrency**: Support eTag-based updates with conflict detection

### Testing Patterns
- ✔ **Unit tests**: Spock tests for configuration and service logic
- ✔ **Mock Cosmos client**: Mock `CosmosContainer` and `CosmosDatabase` for unit tests
- ✔ **Integration tests**: Optional integration tests with Cosmos emulator
- ✔ **Coverage targets**: Exclude config, exception, and model classes from coverage requirements

## III. Preferred Patterns (Recommended)

The LLM **should adopt** these patterns unless user overrides:

### Code Quality
- ➜ **Javadoc comments**: Document all public APIs with parameter descriptions and return types
- ➜ **Method naming**: Use descriptive names like `readAllData`, `createCosmosItem`, `patchUpdate`
- ➜ **Generic type support**: Support both `Map` and typed object operations
- ➜ **Builder pattern**: Consider builder pattern for complex query construction

### Performance
- ➜ **Connection pooling**: Configure appropriate pool sizes based on expected load
- ➜ **Async operations**: Prefer async operations for high-throughput scenarios
- ➜ **Batch operations**: Use bulk operations for multiple item updates
- ➜ **Query optimization**: Enable query metrics to identify slow queries
- ➜ **Preferred regions**: Configure preferred regions for multi-region deployments

### Observability
- ➜ **Metrics logging**: Log request units (RU) consumption for cost monitoring
- ➜ **Query metrics**: Log query execution time, RU charge, and result count
- ➜ **Correlation IDs**: Include correlation/trace IDs in log messages
- ➜ **Operation tracking**: Log operation type, container name, and partition key

### Configuration
- ➜ **Environment-based config**: Support different configurations per environment
- ➜ **Sensible defaults**: Provide reasonable defaults for all optional properties
- ➜ **Validation**: Validate required properties at startup with clear error messages
- ➜ **Documentation**: Document all configuration properties in README

### API Design
- ➜ **Overloaded methods**: Provide overloaded methods with and without retry count parameter
- ➜ **Consistent return types**: Return boolean for write operations, List/Object for read operations
- ➜ **Null safety**: Return empty collections instead of null for list operations

## IV. Configuration Properties Reference

### Required Properties
```properties
cosmos.config.{key}.hostName=https://{account}.documents.azure.com:443/
cosmos.config.{key}.secretKey=${COSMOS_SECRET_KEY}
cosmos.config.{key}.databaseName={DATABASE_NAME}
```

### Optional Properties with Defaults
```properties
cosmos.config.{key}.preferredRegion=East US 2
cosmos.config.{key}.consistencyLevel=BOUNDED_STALENESS
cosmos.config.{key}.idleConnectionTimeout=1000
cosmos.config.{key}.maxConnectionPool=50
cosmos.config.{key}.directModeEnabled=true
cosmos.config.{key}.agentSuffix=CosmosDB
cosmos.config.{key}.contentResponseOnWriteEnabled=false

cosmos.autoconfig.enabled=true
cosmos.print.metrics=false
cosmos.retry.enabled=false
cosmos.retry.count=3
cosmos.retry.sleep.time=100
cosmos.sync.retry.enabled=false
cosmos.sync.retry.count=3
cosmos.retryable.exceptions=io.netty.handler.timeout.ReadTimeoutException,com.azure.cosmos.CosmosException
cosmos.retry.status.code=429,503
```

## V. Cosmos SDK Best Practices

### Connection Management
- Use singleton `CosmosClient` instances (managed by Spring)
- Close clients gracefully on application shutdown
- Configure connection mode based on network topology (direct for Azure VMs, gateway for on-premises)

### Query Patterns
- Always specify partition key for single-item operations
- Use cross-partition queries sparingly (high RU cost)
- Implement pagination for large result sets
- Use `SELECT *` only when all properties are needed

### Write Operations
- Use `upsert` when unsure if item exists
- Use `patch` for partial updates to minimize RU consumption
- Use bulk operations for batch writes (>10 items)
- Implement optimistic concurrency with eTags for conflict-sensitive updates

### Error Handling
- Retry on 429 (rate limiting) with exponential backoff
- Retry on transient network errors (ReadTimeoutException)
- Do not retry on 404 (not found) or 409 (conflict) unless intentional
- Log all retry attempts with context for debugging

## VI. Maven Dependencies Reference

### Required Dependencies
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-autoconfigure</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-configuration-processor</artifactId>
    <optional>true</optional>
</dependency>
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-cosmos</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.data</groupId>
    <artifactId>spring-data-commons</artifactId>
</dependency>
<dependency>
    <groupId>com.fasterxml.jackson.datatype</groupId>
    <artifactId>jackson-datatype-jsr310</artifactId>
</dependency>
```

### Optional Dependencies
```xml
<dependency>
    <groupId>com.azure.spring</groupId>
    <artifactId>spring-cloud-azure-appconfiguration-config</artifactId>
</dependency>
<dependency>
    <groupId>commons-codec</groupId>
    <artifactId>commons-codec</artifactId>
</dependency>
```

### Test Dependencies
```xml
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter-engine</artifactId>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.spockframework</groupId>
    <artifactId>spock-spring</artifactId>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>
```

## VII. Jenkins Pipeline Integration

### Pipeline Requirements
- ✔ Use shared library: `oce-jenkins-shared-lib@release/{version}`
- ✔ Configure notification email distribution lists
- ✔ Call `pl_idp_library(ovrParams)` for standardized build/test/deploy
- ✔ Ensure pipeline runs unit tests, builds JAR, and publishes to artifact repository

### Example Jenkinsfile
```groovy
library "oce-jenkins-shared-lib@release/2.9.0"

def ovrParams = [
    ALWAYS_NOTIFY_Q_IDS           : "",
    ALWAYS_NOTIFY_EMAIL_IDS       : "DL-TeamEmail@list.att.com"
]

pl_idp_library(ovrParams)
```

## VIII. Archetype-Specific Patterns

### Multi-Database Support
- Support multiple Cosmos database connections via map-based configuration
- Each database connection identified by unique key
- Beans registered as `Map<String, CosmosDatabase>` and `Map<String, CosmosAsyncDatabase>`

### Utility Classes
- ✔ **CosmosServiceUtil**: Centralize metrics printing and common operations
- ✔ **CosmosCommonDateUtil**: Date/time utilities for Cosmos queries
- ✔ **CosmosRetry**: Async retry executor with configurable backoff
- ✔ **CosmosAsyncRetry**: Async retry implementation for non-blocking operations

### Service Layer Pattern
```java
@Service
public class CosmosQueryService<T> {
    // Inject configuration
    @Value("${cosmos.retry.enabled:false}")
    private boolean cosmosRetryEnabled;
    
    // Inject utility services
    @Autowired
    CosmosServiceUtil cosmosServiceUtil;
    
    // Generic CRUD operations
    public <T> boolean createItem(CosmosContainer container, T item);
    public <T> List<T> readAllDataObject(CosmosContainer container, String query, Class<T> clazz);
    public <T> boolean upsertCosmosItem(CosmosContainer container, T item, String eTag);
    public boolean patchUpdate(CosmosContainer container, Map<String, Object> patchData, String id, String partitionKey);
}
```

---

**Version**: 1.0.0  
**Last Updated**: 2026-02-17  
**Source**: Analysis of Azure Cosmos DB connector patterns and AT&T archetype collection standards
