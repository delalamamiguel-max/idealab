# Key Vault Config Steward Constitution

## Purpose

Defines the guardrails for producing a reusable configuration layer that sources secrets from Azure Key Vault with typed fallbacks and operational observability baked in.

## I. Hard-Stop Rules (Non-Negotiable)

The agent **must refuse** or immediately correct any implementation that:

- ✘ **Reads secrets directly from env files**: Do not bypass Key Vault when a managed secret exists.
- ✘ **Stores secrets in code**: Never embed connection strings, tokens, or certs in source files, notebooks, or logs.
- ✘ **Omits Pydantic typing**: Do not deliver configuration objects without explicit Pydantic models and validators.
- ✘ **Suppresses Key Vault errors**: Do not swallow retrieval exceptions; surface actionable errors with context IDs.
- ✘ **Skips environment fallback policy**: Do not ignore ordered fallbacks (`Key Vault → environment variables → local .env`) when specified.
- ✘ **Disables auditing**: Do not remove Key Vault diagnostic logging or access policy telemetry hooks.
- ✘ **Uses insecure client auth**: Do not authenticate with shared keys or static secrets when Managed Identity is available.
- ✘ **Returns raw dicts**: Do not expose untyped dictionaries in place of validated config objects.
- ✘ **Accepts missing critical secrets**: Do not proceed when required secret names resolve to `None` without explicit overrides.
- ✘ **Commits tenant-specific URIs**: Do not hardcode tenant IDs, vault URIs, or subscription IDs in reusable templates.

## II. Mandatory Patterns (Must Apply)

The Agent **must include** the following structures in generated artifacts:

### Secret Acquisition
- ✔ **DefaultAzureCredential usage**: Instantiate `DefaultAzureCredential` with the managed identity client ID parameterized via environment (e.g., `managed_identity_client_id` in Python, `ManagedIdentityClientId` in .NET).
- ✔ **Key Vault client wiring**: Use `SecretClient(vault_url, credential)` with retry policies (exponential backoff, 3 attempts).
- ✔ **Fallback cascade**: Implement ordered fallback loader that checks Key Vault first, then environment variables, then optional local `.env`.
- ✔ **Secret name registry**: Centralize secret identifiers in a `SecretKeys` enum or mapping to prevent drift.

### Configuration Modeling
- ✔ **Pydantic BaseSettings**: Define `AppConfig(BaseSettings)` wrapping secrets, connection pools, logging toggles, and TTLs.
- ✔ **Type-safe overrides**: Support environment overrides via `model_validate` and `.model_dump()` with `by_alias=True`.
- ✔ **Validation hooks**: Enforce connector-specific validation (e.g., `sqlalchemy_url`, `redis_url`, `timeout_seconds`).
- ✔ **Redaction helper**: Provide utility to redact sensitive fields during logging (`ConfigForLogging`).

### Operational Controls
- ✔ **Structured logging**: Emit JSON logs with `service`, `environment`, `vault_uri`, and `request_id` metadata.
- ✔ **Telemetry hooks**: Publish secret fetch metrics to Azure Monitor/App Insights (`secret_fetch_latency_ms`, `fallback_path`).
- ✔ **Rotation awareness**: Expose `refresh()` method that rehydrates secrets and invalidates cached connectors.
- ✔ **Unit tests**: Include tests covering Key Vault success, fallback path, missing secret refusal, and typed validation errors.

## III. Preferred Patterns (Recommended)

The Agent **should adopt** these practices unless the user overrides them:

### Developer Experience
- ➜ **Scaffolded examples**: Ship `examples/` showing FastAPI, Azure Functions, and worker usage of `AppConfig`.
- ➜ **CLI health check**: Provide `python -m app_config.check` command that verifies vault reachability and required secrets.
- ➜ **.env.sample sync**: Generate `.env.sample` with placeholder keys aligned to `SecretKeys` registry.

### Reliability
- ➜ **Circuit breaker**: Wrap Key Vault calls with short-circuit logic to avoid cascading failures.
- ➜ **Backoff tuning**: Surface retry configuration via settings to honor latency budgets.
- ➜ **Secrets cache TTL**: Cache secrets in-memory with configurable TTL, invalidating on rotation events.

### Compliance
- ➜ **Access policy linting**: Include script/check that validates consuming principal has `get/list` rights only.
- ➜ **Change log template**: Generate markdown template for documenting secret additions/removals per release.
- ➜ **Documentation link**: Reference AT&T Key Vault governance wiki in README or docstring comments.

## IV. Quality Standards

### Testing Requirements
- 🔍 **Coverage targets**: Maintain ≥85% test coverage on loaders, credential wiring, and validation utilities.
- 🔍 **Scenario breadth**: Exercise Key Vault success paths, fallback permutations, token acquisition failures, rotation refresh, and redaction helpers.
- 🔍 **Contract tests**: Mock Azure SDK interfaces to assert retry configuration, exponential backoff intervals, and telemetry emission payloads.

### Documentation Standards
- 📝 **Runbook completeness**: Provide operational runbooks with vault onboarding steps, secret naming conventions, and escalation paths for fetch failures.
- 📝 **Change logs**: Record every secret addition, rename, or deprecation alongside associated service owners and approval tickets.
- 📝 **Usage blueprints**: Publish integration snippets for FastAPI startup, Azure Functions dependency injection, and Airflow DAG operators.

### Security & Compliance
- 🛡️ **Config drift checks**: Schedule automated scans verifying vault firewall rules, RBAC assignments, and diagnostic settings.
- 🛡️ **PII classification**: Flag secrets containing regulated data classes and enforce masked outputs in all logs.
- 🛡️ **Retention policy**: Align secret backup and purge cadence with corporate retention schedules and legal holds.

## V. Enforcement Mechanisms

### Automated Validation
- 🤖 **Static analysis**: Lint for hardcoded URIs, missing Pydantic validators, and plaintext secrets before merge.
- 🤖 **Policy gates**: Block deployments lacking telemetry plumbing or structured logging configuration via CI pipelines.
- 🤖 **Security scans**: Integrate secret scanners and Azure Policy compliance checks in PR workflows.

### Manual Review Protocols
- 👥 **Dual approval**: Require security and platform architect sign-off for new vault integrations or fallback overrides.
- 👥 **Quarterly audits**: Review secret inventories, access logs, and rotation metrics with governance councils.
- 👥 **Post-incident retros**: Document root causes, compensating controls, and constitution updates after any credential-related incident.

---

**Version**: 1.0.0
**Last Updated**: 2025-10-24
