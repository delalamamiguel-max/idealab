---
description: Validate Terraform CI/CD pipeline for security, policy compliance, and governance readiness (Terraform CICD Architect)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype terraform-cicd-architect --json ` and parse for TERRAFORM_VERSION, PYTEST_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/terraform-cicd-architect/templates/env-config.yaml` for test specifications

### 3. Parse Input
Extract from $ARGUMENTS: pipeline location, test scope (unit, integration, policy, security, compliance), acceptance criteria, test environment. Request clarification if incomplete.

### 4. Analyze Test Requirements

Identify testable components: pipeline stages (fmt, validate, plan, apply), policy enforcement (Sentinel/OPA rules, security scanning, compliance checks), state management (remote backend, locking, encryption, backup), approval workflow (RFC linkage, CAB integration, change governance), drift detection (scheduled checks, alert configuration, remediation).

Define test scenarios: unit tests (terraform validate, module testing, policy rule testing), integration tests (end-to-end pipeline execution, state management validation, drift detection testing), security tests (tfsec/Checkov validation, secret scanning, compliance scanning), policy tests (Sentinel/OPA rule execution, hard-mandatory violations, warning handling), compliance tests (RFC linkage validation, approval workflow testing, audit log verification).

### 5. Generate Test Suite

Create comprehensive test suite with unit tests (terraform fmt/validate, tflint validation, module unit tests with Terratest), integration tests (full pipeline execution, multi-environment deployment, state operations validation), security tests (security scanning with multiple tools, vulnerability assessment, CIS compliance validation), policy tests (policy engine validation, violation handling, exception testing), compliance tests (approval gate validation, RFC linkage tests, audit trail verification), drift tests (drift detection validation, alert testing, auto-remediation validation).

Include test fixtures, mock resources, test workspaces.

### 6. Add Recommendations

Include testing best practices: automated testing in CI/CD, test infrastructure isolation, policy testing in PRs, continuous compliance validation, drift monitoring, test coverage tracking.

Provide test execution commands.

### 7. Validate and Report


Execute test suite: `pytest tests/ --junitxml=results.xml --cov --cov-report=html`

Generate test report with pass/fail summary, policy validation, security scan results, compliance checks. Report completion.

## Error Handling

**Test Infrastructure Missing**: Provide setup instructions for test workspaces.

**Policy Validation Fails**: Document violations and remediation steps.

**State Access Issues**: Configure test backend or use mock state.

## Examples

**Example 1**: `/test-terraform-cicd Validate AKS infrastructure pipeline with policies` - Output: Complete test suite with policy and security validation

**Example 2**: `/test-terraform-cicd Test multi-environment Terraform workflow` - Output: Integration tests with state management and approvals

**Example 3**: `/test-terraform-cicd Validate drift detection and remediation` - Output: Drift monitoring test suite with alert validation

## References

