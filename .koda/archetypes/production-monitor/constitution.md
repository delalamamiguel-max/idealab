# Production Monitor Constitution

## Purpose

Set up production monitoring with Arize Phoenix and SOX-compliant dashboards.

## I. Hard-Stop Rules

- ✘ **No L4 agents without monitoring**: Never deploy autonomous agents without full observability
- ✘ **No disabled SOX tracing**: Never disable tracing for SOX-scoped agents
- ✘ **No suppressed alerts**: Never suppress critical alerts in production
- ✘ **No missing retention**: Never delete traces before retention period

## II. Mandatory Patterns

- ✔ **Phoenix integration**: Configure Arize Phoenix for all L3+ agents
- ✔ **SLO definition**: Define latency, error rate, and quality SLOs
- ✔ **Drift detection**: Monitor for embedding and response drift
- ✔ **Alert routing**: Route alerts to appropriate channels
- ✔ **Evidence export**: Export traces for SOX compliance

---

## Section III — Preferred Patterns


- ➜ **Cost-per-agent tracking** — Monitor token spend and inference cost per agent instance to enable cost allocation and budget forecasting per team or project.

- ➜ **Anomaly trend dashboards** — Maintain rolling 7-day baselines for key metrics; surface gradual drift before hard thresholds trigger. Grafana or Phoenix visualization recommended.

- ➜ **Runbook auto-generation** — Generate incident response runbooks from SLO definitions automatically; reduces MTTR when alerts fire by providing pre-populated response steps.

---

**Version**: 1.0.0
