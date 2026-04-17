# Cosmos DB Connector Archetype

Production-ready Azure Cosmos DB client library archetype for Spring Boot applications with auto-configuration, retry logic, and comprehensive query support.

## Overview

This archetype generates Spring Boot-compatible Cosmos DB connector libraries that provide:

- **Auto-Configuration**: Spring Boot auto-configuration with `@ConfigurationProperties` support
- **Multi-Database Support**: Connect to multiple Cosmos databases via map-based configuration
- **Sync & Async Operations**: Both synchronous and asynchronous query services
- **Comprehensive CRUD**: Create, read, upsert, patch, delete, and bulk operations
- **Retry Logic**: Configurable retry mechanisms for transient failures
- **Query Safety**: Parameterized queries with `SqlQuerySpec` to prevent injection
- **Metrics & Observability**: Query metrics logging and performance monitoring
- **Spring Integration**: Seamless integration with Spring Boot ecosystem

## Key Features

### 🔧 Configuration Management
- Map-based configuration for multiple database connections
- Support for `@RefreshScope` for runtime configuration updates
- Environment-specific property files
- Azure Key Vault integration for secrets

### 🔄 Retry & Resilience
- Configurable retry count and backoff strategy
- Classification of retriable vs non-retriable exceptions
- Status code-based retry (429 rate limiting, 503 service unavailable)
- Both synchronous and asynchronous retry implementations

### 📊 Query Operations
- Pagination support with configurable page size
- Parameterized queries for SQL injection prevention
- Cross-partition and single-partition query support
- Query metrics and RU consumption tracking

### 🚀 Performance
- Connection pooling with configurable limits
- Direct mode and gateway mode support
- Bulk operations for batch writes
- Async operations for high-throughput scenarios

## Project Structure

```
cosmos-db-connector/
├── cosmos-db-connector-constitution.md    # Archetype constitution (rules & patterns)
├── manifest.yaml                          # Archetype metadata and keywords
├── README.md                              # This file
├── .windsurf/
│   └── workflows/                         # Workflow definitions
│       ├── scaffold-cosmos-db-connector.md
│       ├── debug-cosmos-db-connector.md
│       ├── test-cosmos-db-connector.md
│       ├── refactor-cosmos-db-connector.md
│       ├── compare-cosmos-db-connector.md
│       └── document-cosmos-db-connector.md
├── templates/                             # Code templates
│   ├── config/                           # Spring configuration templates
│   ├── service/                          # Query service templates
│   ├── exception/                        # Exception templates
│   ├── properties/                       # Application properties
│   └── gradle/                           # Gradle build templates
│       ├── build.gradle.template
│       ├── settings.gradle.template
│       └── gradle.properties.template
└── scripts/                               # Validation scripts
    └── validate-cosmos-config.py
```

## Constitution Highlights

### Hard-Stop Rules (Non-Negotiable)

**Security:**
- ✘ No hardcoded secrets or connection strings
- ✘ No SQL injection vulnerabilities
- ✘ No PII exposure in logs or errors

**Configuration:**
- ✘ No missing auto-configuration
- ✘ No connection leaks
- ✘ No unbounded connection pools

**Operations:**
- ✘ No unbounded queries without pagination
- ✘ No missing retry logic for transient failures
- ✘ No silent error swallowing

### Mandatory Patterns

**Spring Boot Integration:**
- ✔ `@ConfigurationProperties` for Cosmos settings
- ✔ `@RefreshScope` for dynamic configuration updates
- ✔ Bean registration for `CosmosClient`, `CosmosDatabase`
- ✔ `@ConditionalOnProperty` guards

**Query Service:**
- ✔ Generic `CosmosQueryService<T>` implementation
- ✔ Sync and async service variants
- ✔ CRUD operations with partition key support
- ✔ Bulk operations with partial failure handling

**Retry Logic:**
- ✔ Configurable retry count and sleep time
- ✔ Exception classification (retriable vs non-retriable)
- ✔ Status code-based retry decisions
- ✔ Exponential backoff strategy

## Configuration Example

### Application Properties

```properties
# Enable Cosmos auto-configuration
cosmos.autoconfig.enabled=true

# Database connection (use Key Vault for secrets in production)
cosmos.config.orderIntake.hostName=https://myaccount.documents.azure.com:443/
cosmos.config.orderIntake.secretKey=${COSMOS_SECRET_KEY}
cosmos.config.orderIntake.databaseName=ORDER_INTAKE
cosmos.config.orderIntake.preferredRegion=East US 2
cosmos.config.orderIntake.consistencyLevel=BOUNDED_STALENESS
cosmos.config.orderIntake.maxConnectionPool=50
cosmos.config.orderIntake.idleConnectionTimeout=1000
cosmos.config.orderIntake.directModeEnabled=true

# Retry configuration
cosmos.retry.enabled=true
cosmos.retry.count=3
cosmos.retry.sleep.time=100
cosmos.sync.retry.enabled=true
cosmos.sync.retry.count=3

# Retriable exceptions
cosmos.retryable.exceptions=io.netty.handler.timeout.ReadTimeoutException,com.azure.cosmos.CosmosException
cosmos.retry.status.code=429,503

# Metrics
cosmos.print.metrics=false
```

### Multiple Database Configuration

```properties
# First database
cosmos.config.orderIntake.hostName=https://account1.documents.azure.com:443/
cosmos.config.orderIntake.databaseName=ORDER_INTAKE

# Second database
cosmos.config.taskQueue.hostName=https://account2.documents.azure.com:443/
cosmos.config.taskQueue.databaseName=TASK_QUEUE
```

## Usage Example

### Injecting Cosmos Database

```java
@Service
public class OrderService {
    
    @Autowired
    @Qualifier("cosmosDatabases")
    private Map<String, CosmosDatabase> cosmosDatabases;
    
    @Autowired
    private CosmosQueryService<Order> queryService;
    
    public List<Order> getOrders(String customerId) {
        CosmosDatabase database = cosmosDatabases.get("orderIntake");
        CosmosContainer container = database.getContainer("ORDERS");
        
        String query = "SELECT * FROM c WHERE c.customerId = @customerId";
        Map<String, Object> params = Map.of("customerId", customerId);
        
        return queryService.readAllDataUsingQueryParams(
            container, query, params, Order.class, 100
        );
    }
}
```

### Creating Items

```java
public boolean createOrder(Order order) {
    CosmosContainer container = getContainer("ORDERS");
    return queryService.createItem(container, order);
}
```

### Upserting with Optimistic Concurrency

```java
public boolean updateOrder(Order order, String eTag) {
    CosmosContainer container = getContainer("ORDERS");
    return queryService.upsertCosmosItem(container, order, eTag);
}
```

### Patch Updates

```java
public boolean updateOrderStatus(String orderId, String partitionKey, String status) {
    CosmosContainer container = getContainer("ORDERS");
    Map<String, Object> patchData = Map.of("status", status);
    return queryService.patchUpdate(container, patchData, orderId, partitionKey);
}
```

### Bulk Operations

```java
public List<CosmosBulkOperationResponse<Object>> bulkUpdateOrders(
    List<Map<String, Object>> updates
) {
    CosmosContainer container = getContainer("ORDERS");
    return queryService.bulkPatchUpdate(container, updates);
}
```

## Maven Dependencies

### Required Dependencies

```xml
<dependencies>
    <!-- Spring Boot -->
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
    
    <!-- Azure Cosmos DB -->
    <dependency>
        <groupId>com.azure</groupId>
        <artifactId>azure-cosmos</artifactId>
    </dependency>
    
    <!-- Spring Data -->
    <dependency>
        <groupId>org.springframework.data</groupId>
        <artifactId>spring-data-commons</artifactId>
    </dependency>
    
    <!-- Jackson for JSON -->
    <dependency>
        <groupId>com.fasterxml.jackson.datatype</groupId>
        <artifactId>jackson-datatype-jsr310</artifactId>
    </dependency>
</dependencies>
```

## Testing

### Unit Tests with Spock

```groovy
class CosmosQueryServiceSpec extends Specification {
    
    CosmosQueryService service = new CosmosQueryService()
    CosmosContainer mockContainer = Mock()
    
    def "should create item successfully"() {
        given:
        def item = [id: "123", name: "Test"]
        def response = Mock(CosmosItemResponse)
        response.getStatusCode() >> 201
        
        when:
        mockContainer.createItem(item, _) >> response
        def result = service.createItem(mockContainer, item)
        
        then:
        result == true
    }
}
```

### Integration Tests with Cosmos Emulator

```java
@SpringBootTest
@TestPropertySource(properties = {
    "cosmos.config.test.hostName=https://localhost:8081",
    "cosmos.config.test.secretKey=C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==",
    "cosmos.config.test.databaseName=TestDB"
})
class CosmosIntegrationTest {
    
    @Autowired
    private Map<String, CosmosDatabase> databases;
    
    @Test
    void testCreateAndRead() {
        // Integration test implementation
    }
}
```

## Workflows

### `/scaffold-cosmos-db-connector`
Generate a new Cosmos DB connector library with:
- Spring Boot auto-configuration
- Query service implementations
- Retry logic
- Configuration properties
- Maven POM with dependencies

### `/debug-cosmos-db-connector`
Debug common issues:
- Connection failures
- Retry exhaustion
- Query performance problems
- Configuration errors

### `/test-cosmos-db-connector`
Generate comprehensive test suite:
- Unit tests for services
- Configuration tests
- Retry logic tests
- Integration tests with emulator

### `/refactor-cosmos-db-connector`
Refactor existing connector:
- Apply retry patterns
- Add missing error handling
- Optimize query performance
- Update to latest SDK version

### `/compare-cosmos-db-connector`
Compare different implementation approaches:
- Sync vs async operations
- Retry strategies
- Connection pooling configurations

### `/document-cosmos-db-connector`
Generate documentation:
- API documentation
- Configuration guide
- Usage examples
- Performance tuning guide

## Best Practices

### Connection Management
- ✓ Use singleton `CosmosClient` instances (Spring-managed)
- ✓ Configure connection mode based on network topology
- ✓ Set appropriate pool sizes for expected load
- ✓ Close clients gracefully on shutdown

### Query Optimization
- ✓ Always specify partition key for single-item operations
- ✓ Use cross-partition queries sparingly (high RU cost)
- ✓ Implement pagination for large result sets
- ✓ Use `SELECT` with specific fields instead of `SELECT *`

### Error Handling
- ✓ Retry on 429 (rate limiting) with exponential backoff
- ✓ Retry on transient network errors
- ✓ Do not retry on 404 or 409 unless intentional
- ✓ Log all retry attempts with context

### Security
- ✓ Store secrets in Azure Key Vault
- ✓ Use managed identities when possible
- ✓ Never log connection strings or secret keys
- ✓ Use parameterized queries to prevent injection

## Performance Tuning

### Connection Pool Sizing
```properties
# For high-throughput scenarios
cosmos.config.{key}.maxConnectionPool=100
cosmos.config.{key}.idleConnectionTimeout=2000

# For low-latency scenarios
cosmos.config.{key}.directModeEnabled=true
cosmos.config.{key}.preferredRegion=East US 2
```

### Query Optimization
- Use indexed properties in WHERE clauses
- Minimize cross-partition queries
- Enable query metrics to identify bottlenecks
- Use bulk operations for batch writes (>10 items)

### Retry Configuration
```properties
# Aggressive retry for transient failures
cosmos.retry.enabled=true
cosmos.retry.count=5
cosmos.retry.sleep.time=200

# Conservative retry for production
cosmos.retry.count=3
cosmos.retry.sleep.time=100
```

## Troubleshooting

### Connection Timeouts
- Increase `idleConnectionTimeout`
- Check network connectivity to Cosmos endpoint
- Verify firewall rules allow outbound HTTPS

### Rate Limiting (429 Errors)
- Enable retry logic with backoff
- Increase provisioned RU/s on container
- Implement client-side throttling

### High RU Consumption
- Enable query metrics logging
- Optimize queries with proper indexing
- Use patch operations instead of full upserts
- Implement caching for frequently accessed data

## Related Archetypes

- **backend-only**: For building complete backend services with Cosmos DB
- **integration-specialist**: For creating REST APIs over Cosmos DB
- **data-pipeline-builder**: For ETL pipelines with Cosmos DB as source/sink
- **observability**: For monitoring Cosmos DB operations

## References

- [Azure Cosmos DB Java SDK Documentation](https://docs.microsoft.com/azure/cosmos-db/sql/sql-api-sdk-java-v4)
- [Spring Boot Auto-Configuration](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.developing-auto-configuration)
- [Cosmos DB Best Practices](https://docs.microsoft.com/azure/cosmos-db/sql/best-practice-java)
- [Constitution Document](./cosmos-db-connector-constitution.md)

---

**Version**: 1.0.0  
**Last Updated**: 2026-02-17  
**Archetype Category**: 06-application-development  
**Maintainer**: AT&T Data Platform Team
