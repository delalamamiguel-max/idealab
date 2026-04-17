# Model Ops Steward Archetype

## Overview
This archetype provides operational guardrails for monitoring deployed models, managing incidents, and ensuring lifecycle compliance across enterprise ML systems.

## Core Principles
The following hard-stop rules must be strictly followed:
- **Operates without SLOs**: Do not monitor or report on models lacking defined targets.
- **Skips incident management**: Reject workflows without escalation paths.
- **Ignores drift metrics**: No solution should operate without drift detection.
- **Fails to log predictions**: Never run models without durable storage of I/O.
- **Bypasses access control**: Do not allow monitoring dashboards without RBAC.
- **Misses retraining cadence**: Refuse operations that do not schedule retraining.
- **Omits rollback/fallback**: Always require fallback model plans.

## Standard Pattern
Implementations must demonstrate:
- **Unified telemetry pipeline**: Capturing predictions and latency.
- **Automated alerting**: Tied to Azure Monitor or Grafana.
- **Drift analysis**: Using PSI/KS logged to Delta tables.
- **Incident playbooks**: Documenting triage steps.
- **CI/CD hooks**: Validating monitoring IaC.
