# Elasticsearch Stream Archetype

This archetype governs EventHub-to-Elasticsearch streaming solutions. It defines the constitution, workflows, and configuration template required to provision compliant indexing jobs with observability hooks, ILM policies, and retry guardrails.

## Repository Layout
```
elasticsearch-stream/
├── README.md
├── elasticsearch-stream-constitution.md
├── templates/
│   └── env-config.yaml
├── workflows/
│   ├── compare-elasticsearch-stream.md
│   ├── debug-elasticsearch-stream.md
│   ├── document-elasticsearch-stream.md
│   ├── refactor-elasticsearch-stream.md
│   ├── scaffold-elasticsearch-stream.md
│   └── test-elasticsearch-stream.md
└── scripts/
   ├── README.md
   ├── python/
   │   ├── collect-impact-stats.py
   │   └── python ../../00-core-orchestration/scripts/validate_env.py --archetype elasticsearch-stream
```

## Quick Start
1. **Validate the environment**
   ```bash
 python ../../00-core-orchestration/scripts/validate_env.py -stream --json -stream
   ```
2. **Review the constitution**
   - Read `elasticsearch-stream-constitution.md` for hard-stop rules around query filters, secret handling, payload schemas, and EventHub limits.
3. **Capture intake inputs**
   - Copy `templates/env-config.yaml` and fill in Elasticsearch endpoints, ILM policies, EventHub namespaces, batching strategy, alert routes, and CLI smoke tests.
4. **Select a workflow**
   - `/scaffold-elasticsearch-stream` — bootstrap a governed EventHub→Elasticsearch pipeline.
   - `/refactor-elasticsearch-stream` — improve bulk indexing, retries, and schema evolution.
   - `/debug-elasticsearch-stream` — diagnose throughput drops, mapping conflicts, or EventHub lag.
   - `/test-elasticsearch-stream` — generate performance, failure, and schema validation suites.
   - `/compare-elasticsearch-stream` — contrast ingestion approaches (bulk vs single doc, ILM options).
   - `/document-elasticsearch-stream` — publish architecture, runbooks, and observability coverage.
5. **Extend with scripts (optional)**
   - Drop helper utilities inside `scripts/` for ILM registration, bulk replay tools, or monitoring exports.

## Workflow Expectations
- Every engagement must reference the constitution, a populated `templates/env-config.yaml`, and cite the EventHub payload contract.
- Workflows must enforce Key Vault–backed credentials, filtered queries, bounded batch sizes, and DLQ/alert routes before a job is approved.
- Observability outputs (Kibana dashboards, Log Analytics queries, incident hooks) are mandatory deliverables for debug/test workflows.

## Templates
- `templates/env-config.yaml` is the single intake artifact for endpoints, EventHub settings, retry policies, observability rules, and CLI smoke tests.

## Scripts
- See `scripts/README.md` for guidelines. Keep utilities idempotent, load configuration from the template, and emit structured logs for guardrail ingestion.

## Related References
- Router governance: `reference/workflows/00-core-orchestration/solution/router.md`
- Event backlog diagnostics: `scripts/python/collect-impact-stats.py`
