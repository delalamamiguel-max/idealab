---
description: Document Databricks workflow for governance, reproducibility, and collaborative audit trail coverage (Databricks Workflow Creator)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype databricks-workflow-creator --json ` and parse for DATABRICKS_HOST, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/databricks-workflow-creator/templates/env-config.yaml` for documentation templates

### 3. Parse Input
Extract from $ARGUMENTS: workflow identifier (job ID, notebooks, DLT pipeline), target audience (data engineers, data scientists, governance, operations), documentation scope (architecture, operations, development, governance). Request clarification if incomplete.

### 4. Analyze Workflow Architecture

Extract workflow information: job configuration (tasks, dependencies, schedule, clusters), DLT pipeline structure (bronze/silver/gold layers, expectations, schema), Unity Catalog integration (catalogs, schemas, tables, permissions), data lineage (sources, transformations, targets), quality controls (expectations, validation rules, monitoring), cost controls (cluster policies, DBU budgets, optimization).

### 5. Generate Documentation Package

Create comprehensive documentation suite: Architecture Documentation (workflow overview and data flow, layer architecture (bronze/silver/gold), Unity Catalog structure, dependency maps, cluster configurations), Operations Runbook (deployment procedures, monitoring and alerting, troubleshooting guides, incident response, cost management, backup and recovery), Development Guide (local development setup, notebook development best practices, testing procedures, CI/CD integration, governance compliance), Governance Documentation (Unity Catalog permissions, data lineage and provenance, PII handling and masking, audit logging, compliance requirements), Data Quality Documentation (expectation suites by layer, validation rules, anomaly detection, monitoring dashboards, quality SLAs).

Include supporting artifacts: data flow diagrams, lineage visualizations, expectation documentation, cluster configuration details, cost analysis reports.

### 6. Add Recommendations

Include operational best practices: documentation maintenance (update with workflow changes, version control), governance reviews (periodic access audits, lineage validation), cost optimization (regular DBU reviews, cluster tuning), quality monitoring (expectation drift detection, anomaly alerting).

### 7. Validate and Report


Generate documentation artifacts organized in docs/ directory. Create index with navigation. Report completion.

## Error Handling

**Incomplete Metadata**: Request Unity Catalog table comments and lineage details.

**Missing Expectations**: Document data quality gaps and recommend improvements.

**Cost Data Unavailable**: Provide instructions for enabling cost tracking.

## Examples

**Example 1**: `/document-databricks-workflow Create complete documentation for customer_360 DLT pipeline` - Output: Architecture docs, operations runbook, governance documentation

**Example 2**: `/document-databricks-workflow Generate governance documentation for sales_analytics workflow` - Output: Unity Catalog permissions, lineage, compliance mapping

**Example 3**: `/document-databricks-workflow Document troubleshooting guide for order_processing pipeline` - Output: Comprehensive runbook with common issues and resolutions

## References

Original: `prompts/document_prompt.md` | Constitution: (pre-loaded above)
