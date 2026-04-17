---
description: Refactor Databricks deployment scripts for security, reliability, and alignment with workflow standards
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Assess Current State

Extract from $ARGUMENTS:
- Scripts or configurations to refactor
- Current issues or compliance gaps
- Target improvements (security, reliability, standards)

Review existing deployment scripts for:
- Hardcoded credentials or tokens
- Static workspace paths (not using dynamic ATTUID)
- Missing error handling
- Non-compliance with workflow-creator job standards

### 2. Check Hard-Stop Compliance

Validate against constitution hard-stop rules:

**Authentication & Security:**
- No hardcoded tokens or credentials
- No `.databrickscfg` files in version control
- Using OAuth or service principal authentication

**Workspace Safety:**
- Not pushing directly to production without validation
- Workspace prefixes (dev/staging/prod) in paths
- Validation before deployment operations

**CLI Operations:**
- Syntax validation before notebook push
- Job configs meet workflow-creator standards
- No delete operations without confirmation/backup

### 3. Generate Refactoring Plan

Identify changes needed:

**Security Improvements:**
- Replace hardcoded values with environment variables
- Implement credential scanning in pre-commit
- Add authentication validation step

**Reliability Improvements:**
- Add error handling with meaningful messages
- Implement retry logic for transient failures
- Add timeout handling for long operations

**Standards Alignment:**
- Update job configs to workflow-creator template
- Implement dynamic ATTUID resolution
- Add proper monitoring and logging

### 4. Apply Refactoring

**For Deployment Scripts:**
- Replace static paths with `$(whoami)` or `$USER`
- Add pre-flight validation checks
- Implement proper error handling with exit codes
- Add logging for audit trail

**For Job Configurations:**
- Update to use databricks-workflow-creator enterprise template
- Add required fields (notifications, retry, cluster config)
- Validate against workflow-creator checklist

**For Monitoring Scripts:**
- Implement exponential backoff polling
- Add proper state handling for all lifecycle states
- Include log collection on failure

### 5. Validate Refactored Code

Run validation checks:
- Syntax validation for all scripts
- Credential scanning for leaked secrets
- Test deployment in dev environment
- Verify job configuration against standards

### 6. Update Documentation

Ensure documentation reflects changes:
- Update README with new usage patterns
- Document environment variable requirements
- Add troubleshooting section for common issues

## Error Handling

**Legacy Dependencies**: Document breaking changes and provide migration path.

**Permission Changes**: Coordinate with workspace admin for any new permission requirements.

**CI/CD Updates**: Ensure pipeline configurations are updated to match new scripts.

## Examples

### Example 1: Security Hardening

```
/refactor-databricks-developer-workflow "
Our deployment script has hardcoded workspace URLs and paths.
Need to make it environment-agnostic and secure.
Script: scripts/deploy_notebook.sh
"
```

### Example 2: Standards Compliance

```
/refactor-databricks-developer-workflow "
Job configuration was created manually and doesn't follow workflow-creator standards.
Need to update to enterprise template with proper retry and notifications.
Job config: configs/my_job.json
"
```

### Example 3: Reliability Improvement

```
/refactor-databricks-developer-workflow "
Deployment scripts fail silently and don't handle errors properly.
Need to add proper error handling, logging, and retry logic.
Scripts: scripts/*.sh
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/databricks-developer-workflow/databricks-developer-workflow-constitution.md`
- **Job Standards**: `${ARCHETYPES_BASEDIR}/databricks-workflow-creator/databricks-workflow-creator-constitution.md`
- **Script Standards**: Delegate to automation-scripter for complex script refactoring
