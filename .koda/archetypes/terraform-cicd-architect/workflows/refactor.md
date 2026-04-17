---
description: Refactor Terraform CI/CD pipeline for better security, observability, and compliance (Terraform CICD Architect)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype terraform-cicd-architect --json ` and parse for TERRAFORM_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/terraform-cicd-architect/templates/env-config.yaml` for best practices

### 3. Parse Input
Extract from $ARGUMENTS: pipeline location, refactoring goals (security, observability, compliance, reliability), specific issues (missing policies, poor state management, no drift detection). Request clarification if incomplete.

### 4. Analyze Current State

Assess pipeline: security posture (policy enforcement, secret management, compliance scanning, state encryption), state management (remote backend, locking, backup, access control), observability (structured logging, metrics emission, drift monitoring, change tracking), compliance (RFC linkage, approval workflows, audit trails, change governance), reliability (testing, rollback procedures, error handling, retry logic).

Identify refactoring opportunities and risks.

### 5. Generate Refactoring Plan

Create improvements: Security Enhancements (add Sentinel/OPA policies, implement security scanning, enforce state encryption, secure secret management), State Management (configure remote backend with locking, implement backup procedures, add access controls, enable state versioning), Observability Additions (structured pipeline logs, drift detection scheduling, change tracking metrics, compliance dashboards), Compliance Strengthening (add RFC linkage, implement approval gates, enhance audit logging, enforce change windows), Reliability Improvements (add Terratest integration, implement rollback procedures, enhance error handling, add validation gates).

### 6. Implement Refactorings

Generate refactored pipeline: updated stages with security and compliance, enhanced state management, improved observability, strengthened governance, updated documentation.

Include migration guide with validation strategy.

### 7. Validate and Report


Generate refactoring report with security improvements, compliance gains, observability enhancements. Report completion.

## Error Handling

**Breaking Changes**: Provide backward-compatible migration with phased rollout.

**State Migration**: Plan careful backend migration with backup and validation.

**Policy Changes**: Coordinate with governance team for policy updates.

## Examples

**Example 1**: `/refactor-terraform-cicd Add policy enforcement to existing pipeline` - Output: Enhanced pipeline with Sentinel/OPA gates

**Example 2**: `/refactor-terraform-cicd Implement drift detection for production infrastructure` - Output: Pipeline with scheduled drift monitoring and alerts

**Example 3**: `/refactor-terraform-cicd Add compliance controls to Terraform workflow` - Output: Governance-ready pipeline with RFC and CAB integration

## References

