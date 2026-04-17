---
description: Refactor Databricks workflow to enforce governance, reproducibility, and cost optimization (Databricks Workflow Creator)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype databricks-workflow-creator --json ` and parse for DATABRICKS_HOST, DATABRICKS_TOKEN, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/databricks-workflow-creator/templates/env-config.yaml` for best practices

### 3. Parse Input
Extract from $ARGUMENTS: workflow location (job ID, notebooks, DLT pipelines), refactoring goals (governance, performance, cost, reliability), specific issues (hard-coded secrets, missing retries, inefficient queries). Request clarification if incomplete.

### 4. Analyze Current State

Assess workflow: governance compliance (Unity Catalog integration, secret management, audit logging, lineage tracking), reliability (retry policies, timeout settings, error handling, monitoring), performance (query optimization, cluster sizing, caching strategies), cost efficiency (DBU usage, cluster utilization, spot instances, auto-termination), code quality (parameterization, reusability, documentation).

Identify refactoring opportunities.

### 5. Generate Refactoring Plan

Create improvements: governance enhancements (migrate to Unity Catalog, externalize secrets, add expectation suites, implement lineage tracking), reliability improvements (add retry policies and timeouts, enhance error handling, implement monitoring, add health checks), performance optimizations (optimize Spark queries, right-size clusters, enable Photon, implement caching, optimize partitioning), cost optimizations (configure spot instances, implement auto-termination, optimize cluster policies, reduce DBU waste), code quality (parameterize notebooks, create reusable functions, add documentation, implement testing).

### 6. Implement Refactorings

Generate refactored code: updated workflow JSON with governance controls, refactored notebooks with best practices, improved DLT pipeline definitions, optimized cluster configurations, enhanced monitoring and alerting, updated documentation.

Include migration guide with testing strategy.

### 7. Validate and Report


Generate refactoring report with before/after comparison, cost savings, performance gains, compliance improvements. Report completion.

## Error Handling

**Breaking Changes**: Provide backward-compatible migration path.

**Data Loss Risk**: Implement validation and rollback procedures.

**Performance Regression**: Benchmark before and after refactoring.

## Examples

**Example 1**: `/refactor-databricks-workflow Migrate legacy workflow to Unity Catalog governance` - Output: Refactored workflow with Unity Catalog integration

**Example 2**: `/refactor-databricks-workflow Optimize cost for expensive data pipeline` - Output: Cost-optimized workflow with 40% DBU reduction

**Example 3**: `/refactor-databricks-workflow Add reliability controls to production DLT pipeline` - Output: Hardened pipeline with retries, monitoring, and expectations

## References

Original: `prompts/refactor_prompt.md` | Constitution: (pre-loaded above)
