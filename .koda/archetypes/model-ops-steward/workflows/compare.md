---
description: Compare model operations strategies for SLO coverage, resiliency, and governance fit (Model Ops Steward)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype model-ops-steward --json ` and confirm ENV_VALID. Halt if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/model-ops-steward/templates/env-config.yaml` for telemetry patterns, alerting integrations, and lifecycle policies

### 3. Parse Input
Extract from $ARGUMENTS: candidate operations patterns (centralized vs embedded monitoring, manual vs automated retraining, vendor tools vs in-house), SLO requirements, regulatory obligations, team capacity, budget. Request existing runbooks or dashboards if missing.

### 4. Define Comparison Criteria
Assess alternatives on:
- SLO coverage and enforceability
- Incident response maturity and escalation automation
- Drift detection accuracy and response time
- Telemetry completeness and retention
- RBAC and audit logging strength
- Retraining cadence alignment and automation
- Fallback/rollback robustness
- Integration with MLflow registry and lifecycle governance
- Cost efficiency and tooling maintenance effort
- Scalability across multiple models/teams

### 5. Evaluate Options
For each approach:
- Score against criteria with evidence and historical performance
- Flag hard-stop violations (missing SLOs, lack of drift monitoring, absent logging)
- Highlight strengths/weaknesses (time to detect, cost, complexity)
- Estimate remediation work required to meet guardrails

### 6. Recommend Strategy
Provide recommendation:
- Preferred operations model with rationale tied to guardrails
- Supplemental measures (automated retraining, chaos drills) to close gaps
- Governance impacts (roles, approval workflows, reporting cadence)
- Implementation roadmap with milestones and resource requirements

### 7. Summarize Decision

## Error Handling
- Missing context: Request runbooks, telemetry diagrams, SLO statements; share example command clarifying expectations
- Hard-stop triggered: Exclude option and cite constitution clause with remediation plan
- Conflicting priorities: Facilitate trade-offs between automation cost and response speed
- Tooling constraints: Flag need for additional monitoring or alerting investment; reference env-config resources

## Examples
- **Example 1**: `/compare-model-ops Evaluate managed MLOps platform vs in-house stack`
- **Example 2**: `/compare-model-ops Decide between manual retraining and automated triggers`
- **Example 3**: `/compare-model-ops Contrast centralized monitoring team vs product pod ownership`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/model-ops-steward/templates/env-config.yaml`
