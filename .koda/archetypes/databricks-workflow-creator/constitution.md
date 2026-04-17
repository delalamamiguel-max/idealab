# Databricks Workflow Creator Constitution

## Purpose

Codifies the guardrails for authoring and operating Databricks workflows, Delta Live Tables pipelines, and Unity Catalog governed assets with enterprise-grade reliability, security, and observability.

**Source**: Lakehouse platform runbook, Unity Catalog governance policy, workflow reliability SLO charter, production job templates.

---

## I. Hard-Stop Rules (Non-Negotiable)

### 1.1 Data Governance
- ✘ **NEVER** write to Unity Catalog tables without explicit catalog/schema ownership metadata.
- ✘ **NEVER** bypass masking or row-level security for protected domains.
- ✔ **ALWAYS** tag assets with lineage (producer, consumer, SLA) before publishing.

### 1.2 Job Reliability
- ✘ **NEVER** deploy workflows lacking retry policy, timeout, and alerting.
- ✘ **NEVER** schedule overlapping runs of the same pipeline without concurrency guard.
- ✔ **ALWAYS** provide upstream/downstream dependencies and termination behavior.

### 1.3 Secrets & Credentials
- ✘ **NEVER** embed tokens, passwords, or connection strings in notebooks, JSON, or CLI parameters.
- ✔ **ALWAYS** load secrets from Databricks secrets scopes using `{{secrets/scope-name/key-name}}` syntax.
- ✔ **ALWAYS** use managed identities or service principals for external resource access.

### 1.4 Quality Gates
- ✘ **NEVER** promote bronze/silver/gold tables without expectation suites passing.
- ✔ **ALWAYS** enforce schema evolution policy (additive only by default) and anomaly thresholds.

### 1.5 Audit Logging
- ✘ **NEVER** disable diagnostic logging or truncate logs under 90-day retention.
- ✔ **ALWAYS** emit structured job events (job_id, run_id, status, duration, SLA).

**Refusal Template**:
```
❌ Hard-Stop breach detected ({rule_id}). Provide expectation suites, secret scope references, retry policies, and audit logging hooks.
```

---

## II. Mandatory Patterns (Must Apply)

### 2.1 Workflow Configuration
- Declare `max_concurrent_runs`, `timeout_seconds`, and `email_notifications` at job level.
- Define task-level `notification_settings` with `no_alert_for_skipped_runs`, `no_alert_for_canceled_runs`, and `alert_on_last_attempt`.
- Use `job_cluster_key` references to reusable `job_clusters` array for consistent cluster configurations.
- Set `queue.enabled: true` for job queuing when cluster capacity is limited.
- Specify `run_as.user_name` for proper authorization and audit trails.

### 2.2 Delta Expectations
- Register Delta expectations per layer and propagate expectation drift metrics to monitoring tables.

### 2.3 Unity Catalog Governance
- Assign grants via service principals, not personal tokens.
- Populate table comments with SLA, owner, and refresh cadence.

### 2.4 Observability Hooks
- Stream run status to Event Hubs/Kafka for incident correlation.
- Publish metrics (success rate, runtime percentile, failed tasks) into scorecard JSON.

### 2.5 DR & Replay Strategy
- Provide replay notebooks or workflows for bronze reprocessing.
- Document checkpoint and watermark handling for streaming tasks.

### 2.6 Cluster Configuration & Cost Controls
- Pin `policy_id` (e.g., `"001AE0617D43CEA2"`) in `job_clusters.new_cluster` configuration.
- Specify `node_type_id`, `num_workers`, and `azure_attributes.availability` for predictable capacity.
- Configure proxy settings in `spark_conf` for enterprise network isolation:
  - `spark.executor.extraJavaOptions` with `-Dhttp.proxyHost`, `-Dhttp.proxyPort`, `-Dhttp.nonProxyHosts`
  - `spark.driver.extraJavaOptions` with matching proxy configurations
  - `spark.databricks.pyspark.iptable.outbound.whitelisted.ports` for allowed outbound connections
- Enable Delta optimizations: `spark.databricks.delta.optimizeWrite.enabled`, `spark.databricks.delta.autoCompact.enabled`.
- Reference metastore configs via secrets: `javax.jdo.option.ConnectionPassword: "{{secrets/scope/key}}"`.
- Set `data_security_mode: "SINGLE_USER"` for Unity Catalog compatibility.
- Configure `init_scripts` array for custom library installations or environment setup.
- Tag clusters with `tags` object for cost allocation and workload classification.
- Enable `enable_elastic_disk: true` for automatic disk expansion.

---

## III. Preferred Patterns (Recommended)

### 3.1 Infrastructure as Code
- Manage workflows via Terraform/Databricks provider or the Databricks CLI release pipelines.
- Integrate with Git via `git_source` configuration:
  - `git_url`: Repository URL (e.g., GitHub, Azure Repos)
  - `git_provider`: Provider type ("gitHub", "azureDevOpsServices", etc.)
  - `git_branch`: Branch name for source code
- Use `notebook_task.source: "GIT"` to reference notebooks from version control.
- Parameterize notebooks with `base_parameters` object for environment-specific configs.

### 3.2 Reusable Notebook Patterns
- Parameterize notebook inputs, avoid hard-coded paths, and separate validation routines.

### 3.3 Cluster Utilization
- Favor serverless or job clusters (automated clusters) which automatically terminate after job completion.
- **Job clusters do NOT support `autotermination_minutes`** - they auto-terminate by design; only use this for interactive/shared clusters.
- **Prefer `autoscale.min_workers: 1`** for cost optimization, scaling up as needed (max_workers: 4-8 typical).
- **Default `runtime_engine: "STANDARD"`** unless Photon is explicitly required for performance.
- Prefer spot instance pools where policy allows and capture fallback strategy.
- Benchmark Photon acceleration and adaptive query execution to minimize DBU cost only when performance requirements justify the cost.

### 3.4 DataFrame Caching Strategies
- Use DataFrame caching strategically to optimize iterative or multi-pass operations.
- Apply `.cache()` or `.persist(StorageLevel.MEMORY_AND_DISK)` to DataFrames reused across multiple actions.
- Clear caches with `.unpersist()` when no longer needed to free memory.
- **Warning**: Excessive caching without unpersist can cause OOM errors.
- Avoid caching very large DataFrames that exceed cluster memory (monitor Spark UI storage tab).
- For graph workloads processing >800M relationships, prefer staged UC table writes over in-memory caching.
- Use broadcast joins for small lookup tables instead of caching both sides.
- Document caching strategy in notebook comments with memory estimates.

### 3.5 Dry Runs & Shadow Tests
- Execute dry-run workflows in staging prior to production promotion.

### 3.6 CI Validation
- Enforce unit tests (pytest, pyspark), lint checks, and data expectation validation pre-merge.
- Validate job JSON schema and required fields before deployment.
- Test library dependencies in isolated environments before production deployment.
- Configure task-level `libraries` array for Python packages:
  ```json
  "libraries": [
    {"pypi": {"package": "kafka-python"}},
    {"pypi": {"package": "great-expectations"}}
  ]
  ```

---

## IV. Quality Standards

- **Success Rate**: ≥ 99% rolling 30 days.
- **Median Runtime**: ≤ 20 minutes for scheduled pipelines.
- **Expectation Coverage**: ≥ 95% tables with active expectation suites.
- **Incident MTTR**: ≤ 60 minutes from alert to resolution.

---

## V. Enterprise Job Template

### 5.1 Standard Job Structure
All production jobs must follow this structure:

```json
{
  "name": "PROJECT_ENV_WORKLOAD_NAME",
  "email_notifications": {
    "on_failure": ["${USER_ATTUID}@att.com"],
    "no_alert_for_skipped_runs": false
  },
  "webhook_notifications": {},
  "timeout_seconds": 3600,
  "max_concurrent_runs": 1,
  "queue": {
    "enabled": true
  },
  "tags": {
    "project": "project-name",
    "environment": "prod",
    "owner": "team-name"
  },
  "run_as": {
    "user_name": "${USER_ATTUID}@att.com"
  },
  "git_source": {
    "git_url": "https://github.com/org/repo.git",
    "git_provider": "gitHub",
    "git_branch": "main"
  },
  "tasks": [
    {
      "task_key": "task_name",
      "run_if": "ALL_SUCCESS",
      "notebook_task": {
        "notebook_path": "path/to/notebook",
        "base_parameters": {
          "env": "prod",
          "catalog": "catalog_name"
        },
        "source": "GIT"
      },
      "job_cluster_key": "job_cluster",
      "libraries": [
        {"pypi": {"package": "package-name"}}
      ],
      "timeout_seconds": 1800,
      "email_notifications": {
        "on_failure": ["${USER_ATTUID}@att.com"]
      },
      "notification_settings": {
        "no_alert_for_skipped_runs": true,
        "no_alert_for_canceled_runs": false,
        "alert_on_last_attempt": false
      }
    }
  ],
  "job_clusters": [
    {
      "job_cluster_key": "job_cluster",
      "new_cluster": {
        "spark_version": "14.3.x-scala2.12",
        "node_type_id": "Standard_DS3_v2",
        "autoscale": {
          "min_workers": 1,
          "max_workers": 4
        },
        "policy_id": "POLICY_ID_HERE",
        "data_security_mode": "SINGLE_USER",
        "runtime_engine": "STANDARD",
        "enable_elastic_disk": true,
        "spark_conf": {
          "spark.databricks.delta.optimizeWrite.enabled": "true",
          "spark.databricks.delta.autoCompact.enabled": "true",
          "spark.executor.extraJavaOptions": "-Dhttp.proxyHost=proxy.local -Dhttp.proxyPort=3128",
          "spark.driver.extraJavaOptions": "-Dhttp.proxyHost=proxy.local -Dhttp.proxyPort=3128"
        },
        "spark_env_vars": {
          "ENV_VAR": "{{secrets/scope/key}}"
        },
        "init_scripts": [
          {"workspace": {"destination": "/init/script"}}
        ],
        "azure_attributes": {
          "availability": "ON_DEMAND_AZURE",
          "first_on_demand": 1
        }
      }
    }
  ]
}
```

### 5.2 Required Job Fields Checklist
- [ ] `name` follows naming convention: `PROJECT_ENV_WORKLOAD_NAME`
- [ ] `email_notifications` configured with failure alerts
- [ ] `timeout_seconds` set (recommended: 3600 for batch, 0 for streaming)
- [ ] `max_concurrent_runs` defined (typically 1)
- [ ] `queue.enabled` set to true
- [ ] `tags` include project, environment, owner
- [ ] `run_as` specifies service principal (not personal account)
- [ ] `git_source` configured for version control
- [ ] Tasks use `job_cluster_key` (not `new_cluster` or `existing_cluster_id`)
- [ ] Task `notification_settings` configured
- [ ] Job cluster includes `policy_id`
- [ ] Job cluster sets `data_security_mode: "SINGLE_USER"` for UC
- [ ] Job cluster does NOT include `autotermination_minutes` (auto-terminates after job completion)
- [ ] Secrets referenced via `{{secrets/scope/key}}` syntax

---

## VI. Enforcement Mechanisms

- Guardrail script checks JSON definitions for retry/timeout, secret references, and expectations.
- Environment validation ensures CLI tooling, tokens, and workspace context.
- Pipelines must publish metrics and logs to centralized monitoring fabric.

---

## VII. Override Protocol

- Hard-stop overrides require data governance and platform SRE approval with compensating controls.
- Preferred pattern deviations must document rationale in change request and be time-bound.

---

## VIII. Job Execution vs Interactive Execution

**Template References**: 
- 📄 `.cdo-aifc/templates/03-data-engineering/databricks-workflow-creater/autonomous-job-submission-pattern.py`
- 📄 `.cdo-aifc/templates/03-data-engineering/databricks-workflow-creater/proxy-configuration-pattern.py`

Understand the critical differences between job execution and interactive notebook runs to avoid output capture failures.

### Hard-Stop Rules
- ✘ **Never** expect Jobs API to capture cell outputs (`display()`, `print()`, charts)
- ✘ **Never** assume charts or visualizations will be accessible after job completion
- ✘ **Do NOT** rely on interactive cell outputs for reporting in automated workflows

### Mandatory Patterns
- ✔ **Document execution mode**: Clearly indicate whether notebook is for jobs or interactive use
- ✔ **Job-friendly notebooks**: Write results to Unity Catalog tables, return summary via `dbutils.notebook.exit()`
- ✔ **Interactive notebooks**: Use `display()` liberally, export executed notebook as HTML for sharing
- ✔ **Reporting workflows**: Run analysis jobs (write to tables), then separate reporting notebook reads and displays

### Execution Mode Comparison

| Aspect | Job Execution | Interactive Execution |
|--------|--------------|----------------------|
| Cell Outputs | ❌ Not captured by API | ✅ Visible in notebook UI |
| Charts/Plots | ❌ Lost after job completion | ✅ Rendered inline |
| `display()` | ❌ Not accessible via API | ✅ Shows tables/visualizations |
| `print()` | ❌ Not in API response | ✅ Shows in cell output |
| Use Case | ✅ Automation, scheduling | ✅ Analysis, reporting |
| Result Access | Via tables or `notebook.exit()` | Visual in UI, export to HTML |

### Implementation Patterns

#### For Automated Pipelines (Jobs)
```python
# 1. Load and process data
# 2. Write results to Unity Catalog tables
# 3. Return summary via dbutils.notebook.exit()

results_summary = {
    "status": "success",
    "rows_processed": row_count,
    "quality_score": quality_score,
    "output_table": "catalog.schema.results"
}

# Save detailed results
results_df.write.mode("overwrite").saveAsTable("catalog.schema.results")

# Return summary for orchestration
dbutils.notebook.exit(json.dumps(results_summary))
```

#### For Interactive Analysis (Manual Run)
```python
# Use display() freely
display(df)

# Print() shows in cell output
print(f"Quality Score: {score}")

# Charts render inline
plt.figure(figsize=(10, 6))
plt.plot(x, y)
plt.show()

# Export: File → Export → HTML
```

#### For Reporting Workflows
```python
# Hybrid approach:
# 1. Run analysis job (writes to tables)
# 2. Separate reporting notebook reads from tables
# 3. Run reporting notebook interactively
# 4. Export as HTML

results = spark.table("catalog.schema.analysis_results").toPandas()
display(results)  # Interactive mode captures this
```

---

## IX. Corporate Proxy Configuration

**Template Reference**: 📄 `.cdo-aifc/templates/03-data-engineering/databricks-workflow-creater/proxy-configuration-pattern.py`

Many corporate environments require proxy configuration for external API calls, package installations, and Databricks Jobs API access.

### Hard-Stop Rules
- ✘ **Never** hard-code proxy credentials in source code
- ✘ **Never** commit proxy passwords to version control
- ✘ **Do NOT** skip proxy configuration in corporate environments
- ✘ **Never** use proxy for localhost or internal services unnecessarily

### Mandatory Patterns
- ✔ **Configure both protocols**: Set `HTTP_PROXY` and `HTTPS_PROXY` environment variables
- ✔ **Test connectivity**: Validate proxy connection before making API calls
- ✔ **Set NO_PROXY**: Configure bypass list for internal domains
- ✔ **Use secrets**: Store proxy credentials in Databricks secrets, not code
- ✔ **Handle failures**: Implement retry logic for proxy connection issues

### Proxy Configuration Examples

#### Basic Proxy Setup (No Authentication)
```python
import os
import requests

# Set environment variables
os.environ['HTTP_PROXY'] = 'http://cso.proxy.att.com:8080'
os.environ['HTTPS_PROXY'] = 'http://cso.proxy.att.com:8080'

# For requests library
proxies = {
    "http": "http://cso.proxy.att.com:8080",
    "https": "http://cso.proxy.att.com:8080"
}

response = requests.get("https://api.databricks.com/...", proxies=proxies)
```

#### Spark Configuration (Java Options)
Already covered in Section 2.6, but key fields:
```json
"spark_conf": {
  "spark.executor.extraJavaOptions": "-Dhttp.proxyHost=proxy.local -Dhttp.proxyPort=3128",
  "spark.driver.extraJavaOptions": "-Dhttp.proxyHost=proxy.local -Dhttp.proxyPort=3128"
}
```

#### NO_PROXY Configuration
```python
# Domains that should bypass the proxy
NO_PROXY_DOMAINS = [
    "localhost",
    "127.0.0.1",
    "*.internal.company.com",
    "*.azuredatabricks.net"
]

os.environ['NO_PROXY'] = ','.join(NO_PROXY_DOMAINS)
```

#### Databricks API Client with Proxy
```python
class DatabricksAPIClient:
    def __init__(self, workspace_url, api_token, proxy_url=None):
        self.workspace_url = workspace_url
        self.headers = {"Authorization": f"Bearer {api_token}"}
        self.proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
    
    def list_jobs(self):
        url = f"{self.workspace_url}/api/2.0/jobs/list"
        return requests.get(url, headers=self.headers, proxies=self.proxies).json()
```

### Implementation Patterns
The proxy configuration template provides:
1. Basic proxy setup (no authentication)
2. Authenticated proxy configuration
3. Databricks API client with proxy support
4. NO_PROXY/bypass list configuration
5. MLflow tracking with proxy
6. Pip install through proxy
7. Session reuse for better performance
8. Connection validation and testing
9. Troubleshooting common proxy issues

---

**Version**: 2.2.0  
**Last Updated**: 2025-11-23  
**Maintainer**: Lakehouse Reliability Team  
**Changelog**:
- v2.2.0 (2025-11-23): Added job execution vs interactive execution patterns and corporate proxy configuration
- v2.1.0 (2025-11-15): Added DataFrame caching strategies section with OOM warnings and graph workload guidance
- v2.0.0: Added enterprise job template, enhanced cluster configuration patterns, Git integration, and task-level notification patterns from production workloads
