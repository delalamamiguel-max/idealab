---
description: Generate Airflow/TWS orchestration workflow with dependencies, retries, and monitoring (Pipeline Orchestrator)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype pipeline-orchestrator --json ` and parse for AIRFLOW_VERSION, ORCHESTRATOR_TYPE, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/pipeline-orchestrator/templates/env-config.yaml` for schedules, connections, alert channels

### 3. Parse Input
Extract from $ARGUMENTS: workflow definition with tasks, dependencies (upstream/downstream), schedule requirements, SLA targets, failure handling. Request clarification if incomplete.

### 4. Validate Constraints
Check against hard-stop rules:
- ✘ Refuse hardcoded credentials or connection strings
- ✘ Refuse missing retry strategies for idempotent tasks
- ✘ Refuse undefined task dependencies
- ✘ Refuse tasks without timeout specifications
If violated, explain clearly and suggest compliant alternative.

### 5. Generate Orchestration Workflow

Create Airflow DAG with structure: imports and configuration, default_args with retries (≥3), email alerts, timeout settings, DAG definition with schedule_interval and tags, task definitions using appropriate operators (BashOperator/PythonOperator/SparkSubmitOperator), dependency declarations using >> or << operators, callback functions for on_failure and on_success, SLA monitoring configuration.

Task patterns: modular task functions with single responsibility (≤75 LOC), parameterized using Variables or Connections, idempotent operations with retry logic, structured logging with dag_run_id and task_instance, resource allocation (pools, queues, priority), timeout and execution_timeout settings.

Monitoring patterns: SLA callbacks for late tasks, email/Slack notifications on failure, metrics emission for observability, task duration tracking, failure cascade prevention.

Apply mandatory patterns: retries ≥3 with exponential backoff, on_failure callbacks for alerts, no hardcoded credentials (use Connections), parameterized schedules and configs, task dependency graph documentation, structured logging with run metadata, timeout specifications for all tasks.

### 6. Add Recommendations

Include comments for: parallelism optimization, resource pool configuration, dynamic task generation, sensor usage for external dependencies, XCom for task communication.

### 7. Validate and Report


Generate optional pytest-airflow test harness. Report completion with file paths, DAG structure, applied guardrails, testing commands, next steps.

## Error Handling

**Hard-Stop Violations**: Explain violation (e.g., missing retries), suggest compliant alternative with retry configuration.

**Incomplete Input**: List missing information (task list, dependencies, schedule), provide well-formed example with task graph.

**Environment Failure**: Report missing Airflow or orchestrator configuration, suggest setup steps.

## Examples

**ETL Pipeline**: `/scaffold-pipeline Create daily ETL pipeline: extract from S3, transform with Spark, load to Snowflake, run at 2am with 4-hour SLA`
Output: Airflow DAG with 3 tasks, dependencies, retry logic, SLA monitoring, email alerts.

**ML Training**: `/scaffold-pipeline Orchestrate ML training: data prep, feature engineering, model training, evaluation, deployment, run weekly`
Output: Airflow DAG with 5 tasks, sequential dependencies, resource pools, failure handling.

**Data Quality**: `/scaffold-pipeline Schedule data quality checks: validate staging tables, run Great Expectations, alert on failures, run hourly`
Output: Airflow DAG with validation tasks, sensor for data arrival, alert callbacks.

## References

Original: `prompts/01_scaffold_prompt.md` | Constitution: (pre-loaded above)
