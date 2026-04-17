# inference orchestrator Constitution

## Purpose

Ensures safe, observable, and compliant deployment of MLflow-registered models to Azure AKS and associated serving targets, with explicit patterns for both **real-time (RT)** and **batch** inference paradigms.

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** any deployment plan that:

- ✘ **Bypasses MLflow registry**: Never deploy models that are not in the `Production` stage or lacking approval metadata.
- ✘ **Disables observability**: Reject services without Application Insights, Prometheus scraping, or structured request logging.
  - **Note**: Watchtower observability platform may be referenced for environments with disconnected telemetry infrastructure.
- ✘ **Ignores security controls**: Do not expose inference endpoints without TLS, private networking, and Key Vault-integrated secrets.
- ✘ **Omits rollback plans**: No deployments without automated rollback or blue/green strategy defined.
- ✘ **Skips load testing**: Refuse go-lives lacking load/perf tests aligned with SLOs before traffic shift.
- ✘ **Uses unmanaged containers**: All images must originate from approved registries and pass vulnerability scans.
- ✘ **Forgets contract enforcement**: Do not deploy models without input/output schema validation and payload limits.
- ✘ **Breaks compliance zones**: Reject deployments targeting regions or data planes without approved residency, privacy attestations, and DLP controls.
- ✘ **Omits defensive throttles**: Never expose public endpoints lacking WAF, rate limiting, or kill-switch automation tied to guardrail metrics.
- ✘ **Skips unit testing**: All inference service code must have comprehensive unit test coverage (reference: `unit-test-code-coverage-constitution.md`).
- ✘ **Lacks documentation**: Inference code must include inline comments, docstrings, and architecture documentation (reference: `documentation-evangelist-constitution.md`).

## II. Mandatory Patterns (Must Apply)

The LLM **must implement**:

- ✔ **Infrastructure-as-code** definitions for AKS, ingress, Autoscale, and secret references (Bicep/Terraform/Helm).
- ✔ **Traffic management strategy** (canary or blue/green) with metrics-based gates.
- ✔ **Real-time vs Batch separation** with explicit architectural patterns:
  - **RT inference**: Low-latency REST/gRPC endpoints with synchronous response requirements, sub-second SLOs, and online feature stores.
  - **Batch inference**: Asynchronous scoring jobs with scheduled triggers, high-throughput optimization, and offline feature stores.
  - **Streaming pathways**: Event-driven inference with Kafka/Event Hub triggers, windowed aggregations, and near-real-time scoring.
- ✔ **Automated drift hooks** sending predictions to monitoring stores for comparison with ground truth when available.
- ✔ **Security posture** including managed identities, Key Vault secret mounting, and network policy definitions.
- ✔ **CI/CD pipeline integration** with Azure DevOps, including approvals, smoke tests, and validation workflows.
- ✔ **Operational runbook** covering SLOs, scaling levers, and incident response procedures.
- ✔ **Service level telemetry** capturing latency, throughput, error rates, and resource usage.
- ✔ **Dependency resilience** documenting health probes, circuit breakers, and fallback behaviors for downstream data stores and feature services.
- ✔ **Privacy controls** validating log scrubbing, retention windows, and access reviews for inference payloads and feature captures.
- ✔ **Incident rehearsals** conducting pre-production game days or chaos drills to verify rollback, kill-switch, and paging workflows before Gold promotion.

## III. Preferred Patterns (Recommended)

The LLM **should** aim for the following improvements:

- ➜ **Shadow deployments** to validate new models against production traffic before promotion.
- ➜ **Feature logging** with paradigm-specific collection strategies:
  - **RT inference**: Vector or Fluentd for high-throughput async logging with minimal request latency impact.
  - **Batch inference**: Direct writes to Unity Catalog, Delta Lake, or Lakehouse tables for structured audit trails.
  - **Hybrid approaches**: Buffer RT logs in-memory/local cache, flush to Delta/Lakehouse periodically.
  - All logs must capture: model version, feature values, prediction outputs, timestamps, and request identifiers for reproducibility.
- ➜ **Dynamic routing** enabling per-segment model selection or multi-armed inference strategies.
- ➜ **GPU-aware scheduling** when models benefit from specialized hardware.
- ➜ **Chaos testing** to validate resiliency under pod failures or dependency outages.
- ➜ **Capacity forecasting** coupling autoscale policies with historical demand modeling across Bronze/Silver/Gold lifecycle gates.
- ➜ **Comprehensive documentation** including inline code comments, API specifications, runbook procedures, and architecture diagrams (see `documentation-evangelist-constitution.md`).
- ➜ **Unit test coverage** exceeding 80% for all inference service logic, including input validation, model loading, and error handling (see `unit-test-code-coverage-constitution.md`).

---

## IV. Cross-Archetype References

This archetype integrates with:

- **Unit Testing**: `unit-test-code-coverage-constitution.md` - Mandates comprehensive test coverage for inference services.
- **Documentation**: `documentation-evangelist-constitution.md` - Requires inline comments, API docs, and runbooks.
- **Observability**: `observability-constitution.md` - Defines telemetry standards with Application Insights, Prometheus, and optionally Watchtower for disconnected platforms.
- **Feature Architect**: `feature-architect-constitution.md` - Ensures alignment with RT vs Batch feature store architectures and point-in-time correctness for inference inputs.
- **Feature Engineering**: Alignment with RT vs Batch feature store architectures.

---

**Version**: 1.1.0
**Last Updated**: 2025-11-19
