---
description: Debug Terraform CI/CD pipeline failures, policy issues, and state management problems (Terraform CICD Architect)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype terraform-cicd-architect --json ` and parse for TERRAFORM_VERSION, BACKEND_CONFIG, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/terraform-cicd-architect/templates/env-config.yaml` for debugging tools

### 3. Parse Input
Extract from $ARGUMENTS: failure type (plan failure, policy violation, state issues, apply timeout, drift detection), error messages, workspace, environment. Request clarification if incomplete.

### 4. Diagnose Issue

Run diagnostic checks: Plan Failures (validate syntax errors, check provider availability, resolve dependency issues, verify remote state access), Policy Violations (analyze Sentinel/OPA failures, review security scan findings, check compliance violations, validate resource configurations), State Issues (check state locking, verify backend connectivity, validate state integrity, analyze state conflicts), Apply Failures (review resource creation errors, check timeout issues, validate credentials, analyze quota limits), Drift Detection (compare actual vs desired state, identify manual changes, analyze configuration conflicts).

Provide diagnostic report with root cause.

### 5. Generate Fix Recommendations

Provide targeted fixes: for plan failures (fix syntax, update provider versions, resolve state access), for policy violations (remediate security issues, adjust configurations, request exceptions), for state issues (resolve locking, fix backend config, recover state), for apply failures (fix resource configs, adjust timeouts, verify permissions), for drift (revert manual changes, update code to match reality, implement drift prevention).

Include configuration fixes and remediation steps.

### 6. Add Prevention Measures

Recommend improvements: pre-merge validation, automated policy checks, proactive drift monitoring, state backup procedures, change freeze enforcement.

### 7. Validate and Report


Generate debug report with analysis, fixes, prevention measures. Report completion.

## Error Handling

**State Locked**: Provide force-unlock procedures with safety checks.

**Policy Override Needed**: Document exception request process.

**Backend Inaccessible**: Test connectivity and provide troubleshooting.

## Examples

**Example 1**: `/debug-terraform-cicd Terraform plan failing with state lock timeout` - Output: State lock analysis with resolution steps

**Example 2**: `/debug-terraform-cicd Sentinel policy blocking infrastructure change` - Output: Policy violation analysis with remediation or exception path

**Example 3**: `/debug-terraform-cicd Drift detected in production environment` - Output: Drift analysis with reconciliation strategy

## References

