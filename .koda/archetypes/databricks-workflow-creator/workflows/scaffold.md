---
description: Generate Databricks workflow with Delta Live Tables, governance guardrails, and Unity Catalog integration (Databricks Workflow Creator)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype databricks-workflow-creator --json ` and parse for DATABRICKS_HOST, DATABRICKS_TOKEN, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/databricks-workflow-creator/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: workflow purpose, data sources and targets, transformation logic, schedule requirements, Unity Catalog metadata (catalog, schema, table names), compute requirements. Request clarification if incomplete.

### 4. Generate Workflow Components

Create comprehensive Databricks workflow:

**Job Configuration**: Workflow JSON with tasks and dependencies, cluster configuration with policies and autoscaling, retry policies and timeout settings, max concurrent runs and concurrency guards, alerting and notification setup, parameter passing between tasks.

**Notebooks**: Parameterized notebooks for each task, data ingestion logic with error handling, transformation logic with Delta operations, data quality validation with expectations, Unity Catalog integration, structured logging and monitoring.

**Delta Live Tables**: DLT pipeline definitions (bronze/silver/gold), expectations and quality constraints, streaming or batch mode configuration, schema evolution policies, refresh triggers and schedules.

**Unity Catalog Setup**: Catalog and schema definitions, table registration and metadata, column-level tagging and lineage, access grants and permissions, masking and row-level security policies.

**Secrets Management**: Secret scope references for credentials, managed identity configuration, secure parameter passing, audit logging for secret access.

### 5. Add Quality and Governance

Implement data quality: expectation suites per table layer, schema validation and evolution controls, anomaly detection thresholds, data profiling and monitoring, audit logging and lineage tracking.

Configure cost controls: cluster policies and sizing, DBU budget alerts, spot instance configuration, auto-termination settings, Photon acceleration where applicable.

### 6. Add Recommendations

Include best practices: CI/CD integration with testing, monitoring and alerting setup, disaster recovery and replay procedures, documentation and runbooks, cost optimization strategies, performance tuning guidance.

### 7. Validate and Report


Generate workflow artifacts with deployment instructions. Report completion.

## Error Handling

**Unity Catalog Access**: Verify catalog permissions and service principal grants.

**Cluster Policy Violations**: Adjust configurations to meet policy requirements.

**Secret Scope Missing**: Provide instructions for creating secret scope.

## Examples

**Example 1**: `/scaffold-databricks-workflow Create DLT pipeline for customer data with PII masking` - Output: Complete DLT pipeline with Unity Catalog governance

**Example 2**: `/scaffold-databricks-workflow Generate multi-task workflow for sales analytics` - Output: Workflow with bronze/silver/gold layers and quality checks

**Example 3**: `/scaffold-databricks-workflow Create streaming workflow with Delta expectations` - Output: Streaming DLT pipeline with real-time quality validation

## References

Original: `prompts/scaffold_prompt.md` | Constitution: (pre-loaded above)
