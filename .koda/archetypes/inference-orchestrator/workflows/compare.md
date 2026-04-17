---
description: Compare deployment strategies, architectures, and rollout plans for MLflow-governed inference services (Inference Orchestrator)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype inference-orchestrator --json ` and ensure ENV_VALID. Stop if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/inference-orchestrator/templates/env-config.yaml` for cluster standards, monitoring defaults, and approval flows

### 3. Parse Input
Extract from $ARGUMENTS: candidate deployment approaches (e.g., AKS, serverless, batch pipeline), traffic profile, security requirements, operational constraints, cost targets, approval deadlines. Request MLflow model references, IaC snippets, and monitoring plans if missing.

### 4. Establish Comparison Criteria
Assess alternatives based on:
- MLflow registry alignment and promotion controls
- Observability coverage (metrics, logs, tracing)
- Security posture (network isolation, TLS, secrets management)
- Rollout strategy (canary, blue/green) and rollback automation
- Load/performance readiness vs SLOs
- Batch and streaming pipeline integration
- Drift logging and monitoring capabilities
- Operational runbook completeness and on-call readiness
- Cost efficiency and scaling flexibility (CPU/GPU, autoscale policies)
- Regulatory/governance compliance and approval complexity

### 5. Evaluate Options
For each approach:
- Score against criteria with evidence and anticipated effort
- Flag hard-stop violations (missing registry, observability, security, rollback)
- Highlight benefits/trade-offs (latency, cost, complexity, compliance)
- Estimate remediation needed to reach production standards

### 6. Recommend Strategy
Deliver ranked recommendation:
- Preferred approach with guardrail compliance rationale
- Remediation roadmap for viable alternatives
- Governance implications (new approvals, documentation)
- Suggested enhancements (shadow traffic, cost dashboards, chaos testing)

### 7. Summarize Decision

## Error Handling
- Missing context: Request deployment artifacts, SLOs, security requirements; provide illustrative command showing inputs
- Hard-stop triggered: Exclude noncompliant option and cite constitution clause with remediation guidance
- Ambiguous priorities: Prompt alignment on latency vs cost vs governance trade-offs
- Tooling gap: Flag required monitoring or IaC investments and point to env-config resources

## Examples
- **Example 1**: `/compare-inference Decide between AKS and Azure Functions for personalization model`
- **Example 2**: `/compare-inference Evaluate blue/green vs canary rollout for fraud API`
- **Example 3**: `/compare-inference Contrast batch scoring orchestration options for credit risk model`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/inference-orchestrator/templates/env-config.yaml`
