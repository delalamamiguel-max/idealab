# Scripts Directory

Use this folder for helpers that keep Elasticsearch streaming engagements deterministic and auditable.

Suggested utilities:
- **register-ilm-policy.sh** — Apply lifecycle policies defined in `templates/env-config.yaml` to target indices.
- **validate-index-template.py** — Compare local index templates with the Elasticsearch cluster and flag drift.
- **replay-dead-letter.py** — Rehydrate DLQ payloads back into EventHub after fixes.
- **monitor-eventhub-lag.sh** — Emit lag metrics and trigger alerts when backlog thresholds are exceeded.

Guidelines:
- Load EventHub, Elasticsearch, and observability settings from `../templates/env-config.yaml` and local `templates/env-config.local.yaml` variables.
- Never log secrets; rely on Key Vault or managed identities for auth.
- Emit structured logs (`timestamp`, `workspace`, `index_prefix`, `action`, `result`) so guardrail scripts can ingest them.
- Keep scripts idempotent and parameterized (flags for hub name, index prefix, ILM policy, etc.).
