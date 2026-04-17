# Scripts Directory

Use this folder for helpers that keep Cassandra connector engagements deterministic and auditable.

Suggested utilities:
- **validate-cassandra-connectivity.sh** — Verify reachability of all contact points, port availability, and SSL handshake success.
- **health-check-probe.sh** — Execute the configured health-check query (`SELECT now() FROM system.local`) and report session liveness.
- **rotate-truststore.sh** — Automate JKS truststore rotation: import new certificate, restart connector, validate SSL handshake.
- **pool-metrics-snapshot.sh** — Capture connection pool state (open connections, pending requests, pool exhaustion events) for capacity planning.
- **dc-failover-drill.sh** — Simulate datacenter failover by blackholing remote DC traffic and validating `DCAwareRoundRobinPolicy` behavior.

Guidelines:
- Load cluster endpoints, credentials, and observability settings from `../templates/env-config.yaml` and local `templates/env-config.local.yaml` overrides.
- Never log secrets; rely on Key Vault or managed identities for authentication.
- Emit structured logs (`timestamp`, `cluster`, `keyspace`, `action`, `result`) so guardrail scripts can ingest them.
- Keep scripts idempotent and parameterized (flags for contact points, keyspace, SSL mode, etc.).
