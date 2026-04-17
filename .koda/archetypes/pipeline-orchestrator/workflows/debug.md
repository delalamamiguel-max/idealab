---
description: Debug Airflow/TWS DAG failures and task errors (Pipeline Orchestrator)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype pipeline-orchestrator --json ` and parse for AIRFLOW_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/pipeline-orchestrator/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: DAG file path, task name, error message (task failed, upstream failed, timeout), symptoms (DAG not running, tasks stuck, wrong execution order), context (DAG run ID, execution date). Request clarification if incomplete.

### 4. Analyze Problem

Identify error category: task failures (Python exceptions, operator errors), dependency issues (upstream failures, circular dependencies), scheduling issues (cron expression errors, catchup problems), resource issues (worker capacity, queue full), configuration issues (connection errors, variable not found).

Analyze Airflow logs, task instance state, and DAG structure. Check against constitution for violations.

Report findings with task name, error type, root cause, and impact on downstream tasks.

### 5. Generate Fix

Create fixed DAG addressing root cause: fix task logic (add error handling, fix operator parameters), fix dependencies (correct task relationships, add sensors), fix scheduling (correct cron, configure catchup), fix resource issues (adjust pool, add retries), fix configuration (update connections, add variables).

Include complete fixed DAG with proper error handling and monitoring.

### 6. Add Recommendations

Include recommendations for prevention (DAG validation, testing, monitoring), testing (unit tests for tasks, integration tests for DAG, backfill testing), monitoring (SLA monitoring, task duration alerts, failure notifications).

Provide summary with root cause, fix, impact on pipeline, and prevention strategies.

### 7. Validate and Report


Generate optional test DAG run. Report completion with root cause, fix, testing recommendations.

## Error Handling

**Insufficient Error Information**: Request Airflow logs, task logs, and DAG run details.

**Cannot Reproduce**: Request Airflow version, configuration, and execution context.

**Multiple Possible Causes**: Provide systematic debugging with log analysis.

## Examples

**Example 1: Task Timeout**
```
/debug-pipeline Task "transform_data" timing out after 1 hour

Root Cause: SLA set too low, task legitimately takes 90 minutes
Fix: Increased SLA to 2 hours, added progress logging, optimized task
```

**Example 2: Upstream Failed**
```
/debug-pipeline All tasks failing with "upstream_failed"

Root Cause: First task has connection error, cascading to all downstream
Fix: Fixed connection configuration, added retry logic, improved error handling
```

**Example 3: DAG Not Scheduling**
```
/debug-pipeline DAG not running on schedule

Root Cause: Invalid cron expression "0 0 * * 8" (day 8 doesn't exist)
Fix: Corrected to "0 0 * * 0" for Sunday, validated cron expression
```

## References

Original: `prompts/03_debug_prompt.md` | Constitution: (pre-loaded above)
