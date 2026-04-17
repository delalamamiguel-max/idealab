---
description: Debug Databricks CLI operations, notebook deployment failures, and job execution issues
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Identify Issue Category

Extract from $ARGUMENTS:
- Error message or symptom
- CLI command that failed
- Environment and profile in use
- Recent changes or operations

**Issue Categories:**
- **Authentication Issues**: Token expired, profile misconfigured, permission denied
- **Deployment Failures**: Notebook push failed, workspace path invalid, overwrite conflicts
- **Job Execution Issues**: Job failed to start, run timeout, cluster unavailable
- **Monitoring Issues**: Unable to get run status, log collection failed

### 2. Run Diagnostic Checks

**For Authentication Issues:**
```bash
# Check CLI version
databricks --version

# List available profiles
databricks auth profiles

# Test workspace connectivity
databricks workspace list --profile <profile> --output JSON
```

**For Deployment Failures:**
```bash
# Validate ATTUID resolution
echo "ATTUID: $(whoami)"
echo "Email: $(whoami)@att.com"

# Check workspace path exists
databricks workspace list /Users/$(whoami)@att.com --profile <profile>

# Validate notebook syntax
python -m py_compile <notebook.py>
```

**For Job Execution Issues:**
```bash
# Get job details
databricks jobs get --job-id <id> --profile <profile>

# Get run details
databricks runs get --run-id <id> --profile <profile>

# Get run output/logs
databricks runs get-output --run-id <id> --profile <profile>
```

### 3. Analyze Root Cause

**Authentication Root Causes:**
- Token expired (re-authenticate with `databricks configure`)
- Wrong profile selected (check DATABRICKS_CONFIG_PROFILE)
- Insufficient permissions (contact workspace admin)

**Deployment Root Causes:**
- Invalid workspace path (check ATTUID format: `user@att.com`)
- Missing parent directory (create with workspace mkdirs)
- Notebook syntax errors (run linter first)
- Permission denied on target path

**Job Execution Root Causes:**
- Cluster not available or terminated
- Notebook path mismatch (workspace vs git source)
- Missing dependencies on cluster
- Job configuration doesn't meet workflow-creator standards

### 4. Generate Fix Recommendations

Based on diagnosis, provide:
- Specific CLI commands to resolve issue
- Configuration changes needed
- Links to relevant constitution sections
- Prevention measures for future

### 5. Apply and Verify Fix

1. Execute recommended fix commands
2. Re-run the original operation
3. Verify success with appropriate checks
4. Document resolution for future reference

## Error Handling

**Cannot Connect to Workspace**: Check network connectivity, VPN status, and workspace URL.

**Permission Denied**: Escalate to workspace admin with specific permission requirements.

**Unknown Error**: Collect full CLI output with `--debug` flag for detailed diagnostics.

## Examples

### Example 1: Authentication Failure

```
/debug-databricks-developer-workflow "
Getting 'PERMISSION_DENIED' when trying to push notebook.
Profile: dev
Command: databricks workspace import ./notebook.py /Users/me@att.com/demos/notebook
"
```

### Example 2: Job Run Failure

```
/debug-databricks-developer-workflow "
Job run failed with 'INTERNAL_ERROR'.
Job ID: 12345
Run ID: 67890
Need to understand what went wrong.
"
```

### Example 3: Notebook Push Error

```
/debug-databricks-developer-workflow "
Notebook push failing with 'path does not exist'.
Trying to push to /Users/myattuid@att.com/demos/test_notebook
Using profile: dev
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/databricks-developer-workflow/databricks-developer-workflow-constitution.md`
- **CLI Reference**: Constitution Section V - CLI Operations Reference
- **Related**: scaffold-databricks-developer-workflow, databricks-workflow-creator
