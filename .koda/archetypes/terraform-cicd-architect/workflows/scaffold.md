---
description: Generate Terraform CI/CD pipeline with policy compliance, drift detection, and audit controls (Terraform CICD Architect)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype terraform-cicd-architect --json ` and parse for TERRAFORM_VERSION, BACKEND_CONFIG, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/terraform-cicd-architect/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: infrastructure scope, Terraform modules, environments (dev/staging/prod), backend configuration, policy requirements, approval workflow. Request clarification if incomplete.

### 4. Generate CI/CD Pipeline

Create comprehensive pipeline: Validation Stage (terraform fmt check, terraform validate, tflint for best practices, provider version validation), Security Stage (tfsec/Checkov security scanning, CIS/SOC2 compliance checks, Sentinel/OPA policy evaluation, secret scanning), Planning Stage (terraform plan with detailed output, cost estimation and anomaly detection, plan artifact immutable storage, provenance metadata capture), Policy Gates (hard-mandatory policy violations block, compliance score calculation, automated policy evaluation, manual review for warnings), Approval Stage (manual approval with change record, RFC and CAB linkage, risk rating and backout plan, on-call acknowledgement), Apply Stage (terraform apply with state locking, drift detection schedule, structured apply logs with metadata, success/failure notifications), Drift Monitoring (scheduled terraform plan checks, drift status dashboard, alert on configuration drift, auto-remediation options).

### 5. Generate State Management Configuration

Implement state controls: remote backend with locking (S3/Azure/GCS configuration), state encryption at rest, state access audit logging, backup and recovery procedures, state versioning and history.

### 6. Add Recommendations

Include best practices: module composition strategy, version pinning approach, testing with Terratest, ChatOps integration, cost optimization, disaster recovery procedures.

### 7. Validate and Report


Generate complete CI/CD pipeline with documentation. Report completion.

## Error Handling

**State Locking Missing**: Configure remote backend with locking support.

**Policy Violations**: Document and remediate hard-mandatory failures.

**Missing Approval Workflow**: Create RFC and CAB integration.

## Examples

**Example 1**: `/scaffold-terraform-cicd Create pipeline for AKS infrastructure with Sentinel policies` - Output: Complete CI/CD with policy gates and drift detection

**Example 2**: `/scaffold-terraform-cicd Generate multi-environment Terraform workflow with approvals` - Output: Pipeline with staging gates and production approval

**Example 3**: `/scaffold-terraform-cicd Build pipeline with cost estimation and compliance checks` - Output: Governance-ready pipeline with cost controls

## References

