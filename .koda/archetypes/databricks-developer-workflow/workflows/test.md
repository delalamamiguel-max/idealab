---
description: Validate Databricks developer workflow scripts and configurations for compliance and reliability
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Identify Test Scope

Extract from $ARGUMENTS:
- Scripts or configurations to test
- Test scope (full validation, security audit, functionality)
- Target environment for testing

### 2. Run Environment Prerequisites Test

Validate development environment setup:
- Databricks CLI version check (≥ 0.213.0)
- Authentication profiles exist and valid
- Required tools available (jq, python3, git)
- Environment variables properly set

### 3. Run Security Compliance Test

Check for hard-stop rule violations:

**Credential Security:**
- No hardcoded tokens in scripts
- No `.databrickscfg` in version control
- Sensitive data in environment variables only

**Workspace Safety:**
- Workspace prefixes used (dev/staging/prod)
- No direct production path references in dev scripts
- Delete operations have backup steps

### 4. Run Script Functionality Test

For each deployment script:
- Syntax validation (shellcheck for bash, python -m py_compile for Python)
- Error handling verification (proper exit codes)
- Dynamic ATTUID resolution test
- Dry-run capability (if applicable)

### 5. Run Job Configuration Test

If job configurations exist, validate against workflow-creator standards:
- Required fields present (name, tasks, clusters)
- Notification configuration
- Retry policies defined
- Cluster configuration within limits

**Delegate deep validation to**: `/test-databricks-workflow-creator`

### 6. Run Integration Test

Test end-to-end workflow in dev environment:
- CLI connectivity verification
- Notebook push to test path
- Job creation (if applicable)
- Run monitoring script execution

### 7. Generate Test Report

Produce validation report covering:
- Environment prerequisites status
- Security compliance status
- Script functionality results
- Job configuration compliance
- Integration test results
- Overall pass/fail with recommendations

## Error Handling

**CLI Not Available**: Provide installation instructions.

**Authentication Failure**: Guide through profile setup.

**Test Environment Unavailable**: Skip integration tests, report partial results.

## Examples

### Example 1: Full Validation

```
/test-databricks-developer-workflow "
Validate all deployment scripts and configurations.
Scripts directory: ./scripts/
Job configs: ./configs/
"
```

### Example 2: Security Audit

```
/test-databricks-developer-workflow "
Security-focused audit of deployment scripts.
Check for credential leakage and compliance.
Scripts: scripts/deploy_*.sh
"
```

### Example 3: Pre-Deployment Check

```
/test-databricks-developer-workflow "
Quick validation before deploying to staging.
Focus on functionality and configuration.
Environment: staging
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/databricks-developer-workflow/databricks-developer-workflow-constitution.md`
- **Quality Standards**: Constitution Section IV
- **Environment Checklist**: Constitution Section 5.3
