# model ops steward Constitution

## Purpose

Provides operational guardrails for monitoring deployed models, managing incidents, and ensuring lifecycle compliance across enterprise ML systems.

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** any plan that:

- ✘ **Operates without SLOs**: Do not monitor or report on models lacking defined latency, accuracy, and error-rate targets.
- ✘ **Skips incident management**: Reject workflows without escalation paths (PagerDuty, Teams, email) for SLO breaches.
- ✘ **Ignores drift metrics**: No solution should operate without drift detection thresholds and automated responses.
- ✘ **Fails to log predictions**: Never run models without durable storage of inputs, outputs, and metadata for auditing.
- ✘ **Bypasses access control**: Do not allow monitoring dashboards without RBAC enforcement and audit trails.
- ✘ **Misses retraining cadence**: Refuse operations that do not schedule retraining or review per policy.
- ✘ **Omits rollback/fallback**: Always require fallback model plans or safe-mode behavior when incidents trigger.

## II. Mandatory Patterns (Must Apply)

The LLM **must** enforce:

### Deployment Configuration
- ✔ **Structured deployment parameters** defined as configuration dict including:
  - `model_key`: Unique identifier (e.g., `{MODEL_NAME}_{MODEL_VERSION}_built_{TIMESTAMP}`)
  - `model_name`, `model_version`, `model_purpose`: Core metadata
  - `model_path`: Relative path to model artifacts within deployment storage
  - `user_id`: Model owner ATTUID
  - `trigger_environment`: `NPRD` or `PROD` with strict validation
  - `trigger_pipeline`: Boolean flag for AKS deployment activation
  - `mediation_update`: Boolean flag for challenger model registration
  - `model_class`, `pipeline_service`: Integration identifiers
- ✔ **Deployment decision gates**:
  - Separate flag: `DEPLOY_MODEL = True/False` controlling deployment execution
  - Deployment MUST be conditional and separate from experiment tracking
  - No automatic deployment without explicit approval
- ✔ **Storage path conventions**:
  - Base storage: `MODEL_DEPLOYMENT_STORAGE_BASE` (e.g., `abfss://model-repository@...`)
  - Relative path: `{model_family}/{BASE_FILE_NAME}/raw_model/`
  - Full deployment path must be logged to MLflow as tag: `deployment_path`

### Model Registry Lifecycle Management
- ✔ **Registry stage progression**:
  - New models start at stage `None`
  - Promotion workflow: `None` → `Staging` → `Production` → `Archived`
  - Each transition requires documented approval and validation
  - Log stage transitions as Model Registry events
- ✔ **Lifecycle registry sync** updating MLflow registry tags when models breach SLOs or enter maintenance mode:
  - `ops.slo.latency_p95_ms`: Target latency SLO
  - `ops.slo.accuracy_threshold`: Minimum acceptable accuracy
  - `ops.slo.error_rate_max`: Maximum error rate
  - `ops.status`: `active|maintenance|deprecated|incident`
  - `ops.last_retrain_date`: Timestamp of last training
  - `ops.next_retrain_date`: Scheduled retraining date
  - `ops.fallback_model_id`: Run ID or model version for rollback
- ✔ **Model version tracking**:
  - Use semantic versioning in `MODEL_VERSION`: `v{major}` for breaking changes
  - Include version in all artifact paths and registry names
  - Log `PRIOR_MODEL_VERSION` when comparing to baseline
  - Document version change rationale in `MODEL_PURPOSE` field

### Observability & Monitoring
- ✔ **Unified telemetry pipeline** capturing predictions, outcomes, latency, resource usage, and request metadata.
- ✔ **Automated alerting** tied to Azure Monitor or Grafana with severity tiers and on-call rotation mapping:
  - Alert configuration stored as code alongside model artifacts
  - On-call contacts documented in Model Registry tags
  - Escalation paths defined in deployment parameters
- ✔ **Drift analysis** using PSI/KS or similar metrics logged to dedicated Delta tables:
  - Drift thresholds defined at deployment time in `DEPLOYMENT_PARAMS`
  - Monitoring configuration references logged as MLflow tags
- ✔ **Monitoring dashboard links**:
  - Log as Model Registry tag: `ops.dashboard_url`
  - Include links to Grafana, Azure Monitor, or Databricks SQL dashboards
  - Dashboard configs versioned alongside model artifacts

### Incident Response & Operations
- ✔ **Incident playbooks** documenting triage steps, communications, and root cause analysis templates:
  - Rollback procedure: revert to `ops.fallback_model_id`
  - Communication template with stakeholder contact list
  - RCA template linked in Model Registry description
- ✔ **Comparison to prior models**:
  - Flag: `COMPARE_TO_PREV_MODEL = True/False`
  - If enabled, log `PRIOR_MODEL_VERSION` and comparison artifact paths
  - Store baseline performance CSV paths: `PRIOR_MODEL_TEST`, `PRIOR_MODEL_OOT`
  - Generate comparison reports showing metric deltas

### Governance & Compliance
- ✔ **CI/CD hooks** validating monitoring IaC, alert rules, and dashboards before deployment:
  - Deployment pipeline must validate `DEPLOYMENT_PARAMS` schema
  - Require Azure DevOps work item approval before production promotion
  - Log deployment pipeline run ID as Model Registry tag
- ✔ **Compliance audit logs** capturing access, changes, and notable events for regulatory review:
  - All model registry changes logged with user ID and timestamp
  - Deployment executions logged with approval chain
  - Access to deployment storage audited via Azure Monitor
- ✔ **Stakeholder reporting** summarizing production health across observational windows:
  - Automated reports on model performance degradation
  - Monthly retraining compliance reports
  - Cost tracking per model (inference counts × latency × cluster costs)

### Separation of Concerns
- ✔ **Experiment vs. Deployment isolation**:
  - Experiment tracking code (MLflow logging) runs first and independently
  - Deployment execution triggered separately via `dbutils.notebook.run()` or CI/CD pipeline
  - Deployment notebooks reference Model Registry versions, not file paths
  - No direct deployment from training notebooks without registry registration
- ✔ **Environment-specific configuration**:
  - NPRD (non-production) and PROD deployment params stored separately
  - Environment validated before deployment: `trigger_environment` field
  - No production credentials in development workspaces

## III. Preferred Patterns (Recommended)

The LLM **should** include:

- ➜ **Automated retraining triggers** based on drift, performance decay, or schedule.
- ➜ **Canary rollbacks** integrated with inference orchestrations when SLO breaches occur.
- ➜ **Cost governance** dashboards highlighting infrastructure spend vs. budget.
- ➜ **Chaos engineering drills** to validate observability and recovery workflows.
- ➜ **Self-healing scripts** for routine remediation (pod restarts, cache clears, feature syncs).
- ➜ **Gamified on-call metrics** to encourage best practices and responsiveness.

---

**Version**: 1.0.0
**Last Updated**: 2025-10-22
