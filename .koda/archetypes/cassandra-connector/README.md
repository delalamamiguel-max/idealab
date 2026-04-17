# Cassandra Connector Archetype

This archetype governs Java Spring Boot applications that connect to Apache Cassandra clusters via the DataStax driver. It defines the constitution, workflows, and configuration template required to provision compliant connectors with SSL/TLS, connection pooling, load balancing, health monitoring, and structured exception handling.

## Repository Layout
```
cassandra-connector/
├── README.md
├── cassandra-connector-constitution.md
├── MIGRATION-GUIDE-3x-to-4x.md
├── manifest.yaml
├── templates/
│   └── env-config.yaml
├── .windsurf/
│   └── workflows/
│       ├── compare-cassandra-connector.md
│       ├── debug-cassandra-connector.md
│       ├── document-cassandra-connector.md
│       ├── refactor-cassandra-connector.md
│       ├── scaffold-cassandra-connector.md
│       └── test-cassandra-connector.md
└── scripts/
    └── README.md
```

## Quick Start
1. **Validate the environment**
   ```bash
   python ../../00-core-orchestration/scripts/validate_env.py --archetype cassandra-connector --json
   ```
2. **Review the constitution**
   - Read `cassandra-connector-constitution.md` for hard-stop rules around credential management, SSL enforcement, consistency levels, and connection pooling governance.
3. **Capture intake inputs**
   - Copy `templates/env-config.yaml` and fill in cluster contact points, keyspace, authentication secrets, SSL settings, pooling parameters, load balancing policy, observability hooks, and quality gates.
4. **Select a workflow**
   - `/scaffold-cassandra-connector` — bootstrap a governed Cassandra connector with SSL, pooling, and health monitoring.
   - `/refactor-cassandra-connector` — modernize driver version, optimize pooling, or improve error handling.
   - `/debug-cassandra-connector` — diagnose connection timeouts, pool exhaustion, SSL failures, or consistency errors.
   - `/test-cassandra-connector` — generate unit, integration, performance, and failover test suites.
   - `/compare-cassandra-connector` — contrast driver versions, consistency levels, or load balancing strategies.
   - `/document-cassandra-connector` — publish architecture, configuration reference, ops runbook, and integration guide.
5. **Extend with scripts (optional)**
   - Drop helper utilities inside `scripts/` for connectivity validation, health probes, truststore rotation, or pool metrics collection.

## Workflow Expectations
- Every engagement must reference the constitution, a populated `templates/env-config.yaml`, and cite the Cassandra connector configuration contract.
- Workflows must enforce Key Vault–backed credentials, SSL/TLS for non-local connections, explicit consistency levels, and tuned connection pooling before a connector is approved.
- Observability outputs (health endpoints, Grafana dashboards, Log Analytics queries, alert rules) are mandatory deliverables for debug/test workflows.

## Templates
- `templates/env-config.yaml` is the single intake artifact for cluster endpoints, authentication, SSL, pooling, load balancing, observability rules, quality gates, and smoke tests.

## Scripts
- See `scripts/README.md` for guidelines. Keep utilities idempotent, load configuration from the template, and emit structured logs for guardrail ingestion.

## Key Components Governed
| Component | Description |
|-----------|-------------|
| `CassandraConnector` | Session lifecycle, cluster builder, SSL, pooling, load balancing |
| `CassandraDbConfig` | 30+ configuration parameters for a single keyspace connection |
| `CassandraConfig` | Spring `@ConfigurationProperties` binding for multi-keyspace setups |
| `CassandraService` | Generic CRUD interface (put, get, query, remove, batchInsert) |
| `CassandraServiceImpl` | DataStax MappingManager-based implementation with structured exceptions |
| `CassandraHealthCheck` | Session liveness probe with configurable health-check query |

## Driver Migration: 3.x → 4.17.x

The DataStax Java Driver 3.x series is in **maintenance mode** (security fixes only). This archetype now targets **Driver 4.17.x** as the recommended version.

### Why Migrate?
- **Performance**: 10-20% latency reduction, reduced allocations
- **Configuration**: File-based config (`application.conf`) replaces builder pattern
- **Async-First**: Native `CompletionStage` support, reactive streams
- **Long-term Support**: Active development, new features, security patches

### Migration Resources
- **Comprehensive Guide**: See [`MIGRATION-GUIDE-3x-to-4x.md`](./MIGRATION-GUIDE-3x-to-4x.md) for:
  - Phase-by-phase migration plan (10 phases)
  - Dependency updates (`pom.xml` changes)
  - Configuration migration (builder → `application.conf`)
  - Code migration (API changes, async patterns, object mapper)
  - Testing strategy and deployment plan
  - Known issues and workarounds
  - Side-by-side API comparison

### Quick Migration Checklist
- [ ] Update dependencies: `com.datastax.cassandra` → `com.datastax.oss` (4.17.0)
- [ ] Create `application.conf` with cluster settings
- [ ] Replace `Cluster.builder()` → `CqlSession.builder()`
- [ ] Migrate `MappingManager` → `@Mapper` + `@Dao` interfaces
- [ ] Update exception handling (`NoHostAvailableException` → `AllNodesFailedException`)
- [ ] Test with embedded Cassandra
- [ ] Deploy to staging with canary rollout

### Constitution Updates
All DataStax driver links in the constitution now point to **4.17 documentation**. The constitution includes:
- Driver 4.x API migration map
- Configuration-driven design patterns
- Async-first API guidance

## Related References
- Router governance: `reference/workflows/00-core-orchestration/solution/router.md`
- Connector source: `https://github.com/ATT-DP1/apm0011159-oce3-oce-cassandra-connector`
