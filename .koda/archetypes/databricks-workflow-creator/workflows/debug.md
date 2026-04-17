---
description: Debug Databricks workflow failures, DLT pipeline errors, and Unity Catalog issues (Databricks Workflow Creator)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype databricks-workflow-creator --json ` and parse for DATABRICKS_HOST, DATABRICKS_TOKEN, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/databricks-workflow-creator/templates/env-config.yaml` for debugging tools

### 3. Parse Input
Extract from $ARGUMENTS: failure type (job failure, DLT error, cluster issue, permission denied), error messages and stack traces, job/run ID, workflow name, recent changes. Request clarification if incomplete.

### 4. Diagnose Issue

Run diagnostic checks: job execution (check run status and logs, analyze task failures, review cluster events, examine error messages), DLT pipeline (inspect expectation failures, check streaming state, review checkpoint issues, analyze schema evolution errors), Unity Catalog (verify permissions and grants, check table metadata, validate lineage, inspect masking policies), cluster issues (review driver and executor logs, check resource allocation, validate cluster policies, inspect network connectivity), secrets and credentials (verify secret scope access, check managed identity, validate token permissions).

Provide diagnostic report with root cause hypothesis.

### 5. Generate Fix Recommendations

Provide targeted fixes: for expectation failures (adjust thresholds, fix data quality, update constraints), for permission errors (grant required privileges, update service principal, fix RBAC), for cluster failures (adjust resources, fix policies, update configuration), for timeout issues (increase timeout, optimize queries, add partitioning), for streaming errors (reset checkpoints, fix schema, handle duplicates).

Include code fixes and configuration changes.

### 6. Add Prevention Measures

Recommend improvements: enhanced monitoring and alerting, better error handling in notebooks, improved data quality checks, proactive resource management, automated recovery procedures.

### 7. Validate and Report


Generate debug report with issue analysis, fixes, prevention measures. Report completion.

## Error Handling

**Insufficient Logs**: Enable debug logging and collect diagnostic bundles.

**Intermittent Failures**: Set up monitoring to capture transient issues.

**Permission Denied**: Verify service principal permissions and Unity Catalog grants.

## Examples

**Example 1**: `/debug-databricks-workflow DLT pipeline failing with expectation violations` - Output: Expectation analysis with threshold recommendations

**Example 2**: `/debug-databricks-workflow Job timeout after 2 hours in silver layer` - Output: Performance analysis with optimization strategy

**Example 3**: `/debug-databricks-workflow Unity Catalog permission denied on table write` - Output: RBAC analysis with grant commands

## References

Original: `prompts/debug_prompt.md` | Constitution: (pre-loaded above)
