# Databricks Developer Workflow Constitution

## Purpose

Codifies the guardrails for **local IDE development, Databricks CLI operations, notebook deployment workflows, and developer-initiated job execution** when building and testing Databricks notebooks from Koda or other local development environments.

**Scope**: This archetype covers the **developer workflow and CLI deployment mechanics**. For **job configuration standards, cluster specifications, and production workflow design**, refer to the `databricks-workflow-creator` constitution which is the authoritative source.

**Clear Separation of Concerns**:
- **This Archetype (developer-workflow)**: CLI commands, dynamic ATTUID resolution, notebook push operations, local validation, deployment scripts
- **workflow-creator Archetype**: Job JSON structure, cluster configuration, retry policies, notifications, Unity Catalog integration, quality gates

**Source**: Developer experience runbook, Databricks CLI best practices, notebook deployment patterns, local-to-remote workflow standards.

---

## I. Hard-Stop Rules (Non-Negotiable)

### 1.1 Authentication & Security
- ✘ **NEVER** hardcode authentication tokens, workspace URLs, or credentials in scripts, notebooks, or CLI commands.
- ✘ **NEVER** commit `.databrickscfg` files containing tokens to version control.
- ✔ **ALWAYS** use Databricks CLI profiles with OAuth or service principal authentication.
- ✔ **ALWAYS** store sensitive configuration in environment variables or secure credential stores (Key Vault, system keychain).

### 1.2 Workspace Safety
- ✘ **NEVER** push directly to production workspace paths without validation and approval.
- ✘ **NEVER** overwrite shared notebooks without backing up or version control.
- ✘ **NEVER** execute jobs that modify production data from local development commands without explicit confirmation.
- ✔ **ALWAYS** use workspace-specific prefixes (dev/staging/prod) in notebook paths.
- ✔ **ALWAYS** validate workspace context before deployment operations.

### 1.3 CLI Operations
- ✘ **NEVER** deploy notebooks without syntax validation and pre-commit checks.
- ✘ **NEVER** create jobs that violate `databricks-workflow-creator` constitution standards (see Section VIII for cross-reference).
- ✘ **NEVER** execute `databricks workspace delete` without explicit confirmation and backup.
- ✔ **ALWAYS** validate CLI tool versions meet minimum requirements before operations.
- ✔ **ALWAYS** verify workspace connection and permissions before bulk operations.

### 1.4 Job Execution
- ✘ **NEVER** start job runs without monitoring and timeout configurations.
- ✘ **NEVER** ignore job failures or skip error log collection.
- ✔ **ALWAYS** monitor job run status with proper timeout and failure handling.
- ✔ **ALWAYS** collect and display run logs for failed executions.

**Refusal Template**:
```
❌ Hard-Stop breach detected ({rule_id}). Required: authenticated CLI profile, workspace validation, syntax checks, and job monitoring before execution.
```

---

## II. Mandatory Patterns (Must Apply)

### 2.1 CLI Configuration Management
- Maintain separate CLI profiles for each environment (dev, staging, prod).
- Use `databricks auth profiles` command to list and validate available profiles.
- Set `DATABRICKS_CONFIG_PROFILE` environment variable to control active profile.
- Validate workspace connectivity before operations: `databricks workspace list --profile <profile>`.
- **ATTUID Resolution**: Use `$USER` or `$(whoami)` to dynamically construct workspace paths:
  - Environment variable: `$USER` returns your ATTUID (e.g., `eh163e`)
  - Shell command: `$(whoami)` also returns ATTUID
  - Workspace path pattern: `/Users/${USER}@att.com/` (e.g., `/Users/eh163e@att.com/`)

### 2.2 Notebook Development Workflow

There are **two primary approaches** for deploying notebooks to Databricks:

#### Approach 1: Git-Based Workflow (Recommended for Production)
```bash
# Notebook lives in Git, job references repository
1. Validate notebook syntax locally (linting, imports check)
2. Commit and push to Git repository branch
3. Create/update job definition following databricks-workflow-creator standards:
   - See workflow-creator Section 3.1 for git_source configuration
   - See workflow-creator Section 5.1 for complete job template
   - Job JSON must conform to all workflow-creator mandatory patterns
4. Execute job run: `databricks jobs run-now --job-id <id> --profile dev`
5. Monitor run status: `databricks runs get --run-id <id> --profile dev`
6. Collect logs on failure: `databricks runs get-output --run-id <id> --profile dev`
```

**When to use**: Production workflows, team collaboration, version control requirements, CI/CD integration.

**Job Configuration**: All jobs must follow `databricks-workflow-creator` constitution (Section V - Enterprise Job Template).

**Advantages**: 
- Version control integration
- Code review process enforced
- Automated CI/CD deployment
- Notebook changes tracked in Git history
- No manual workspace push required

#### Approach 2: Workspace-Based Workflow (Rapid Development/Testing)
```bash
# Notebook pushed to workspace, job references workspace path
1. Validate notebook syntax locally (linting, imports check)
2. Push notebook to user workspace: `databricks workspace import <local> /Users/{user's ATTUID}/<path> --profile dev`
3. Create/update job definition with workspace path:
   - notebook_task.notebook_path: "/Users/{user's ATTUID}/path/to/notebook"
   - notebook_task.source: "WORKSPACE" (or omit for workspace default)
4. Execute job run: `databricks jobs run-now --job-id <id> --profile dev`
5. Monitor run status: `databricks runs get --run-id <id> --profile dev`
6. Collect logs on failure: `databricks runs get-output --run-id <id> --profile dev`
```

**When to use**: Rapid iteration, ad-hoc testing, personal development, prototyping.

**Advantages**:
- Faster iteration (no Git commit required)
- Immediate testing on cluster
- Personal workspace isolation
- Quick debugging and experimentation

### 2.3 Pre-Deployment Validation
- Lint Python/Scala notebooks before push (pylint, black, scalafmt).
- Validate notebook imports and dependencies are available in target cluster.
- Check for PII, hardcoded credentials, or sensitive data in notebook code.
- Verify notebook references conform to workspace path standards.

### 2.4 Job Configuration Standards

**🔗 Cross-Reference**: `databricks-workflow-creator` Constitution

All jobs created via CLI **MUST** conform to `databricks-workflow-creator` standards:

- **Job Structure**: See workflow-creator Section 5.1 (Enterprise Job Template)
- **Required Fields**: See workflow-creator Section 5.2 (Required Job Fields Checklist)
- **Git Integration**: See workflow-creator Section 3.1 (git_source configuration)
- **Cluster Config**: See workflow-creator Section 2.6 (Cluster Configuration & Cost Controls)
- **Retry/Timeout**: See workflow-creator Section 2.1 (Workflow Configuration)
- **Secrets**: See workflow-creator Section 1.3 (Secrets & Credentials)

**Key Principles for CLI-Created Jobs**:
- Use workflow-creator job template as base
- Modify only `notebook_path` based on deployment approach:
  - **Git-based**: `"source": "GIT"` + relative path in repo
  - **Workspace-based**: `"source": "WORKSPACE"` + absolute workspace path `/Users/${ATTUID}@att.com/...`
- All other job configuration (notifications, retry, cluster config) follows workflow-creator standards

**Deployment Approach Differences**:

| Aspect | Git-Based (Approach 1) | Workspace-Based (Approach 2) |
|--------|------------------------|------------------------------|
| **Notebook Location** | Git repository | Databricks workspace |
| **Job Config** | `git_source` block + relative path | Absolute workspace path |
| **notebook_task.source** | `"GIT"` | `"WORKSPACE"` |
| **notebook_task.notebook_path** | `"notebooks/my_notebook"` (relative) | `"/Users/{ATTUID}@att.com/demos/my_notebook"` (absolute) |
| **Deployment Command** | Git push (no CLI needed) | `databricks workspace import` |
| **Use Case** | Production, team collaboration | Rapid dev, testing |

**📋 Example Job Configs**: Refer to `databricks-workflow-creator` Section 5.1, adapting `notebook_task` based on approach above.

### 2.5 Run Monitoring & Debugging
- Poll run status with exponential backoff (max 60 minutes default).
- Capture `state.life_cycle_state` and `state.result_state` for proper error handling.
- On failure: retrieve full run output including error messages and stack traces.
- Log all run metadata: run_id, job_id, start_time, duration, result_state.

### 2.6 Error Handling
- Wrap all CLI commands in error handling with meaningful error messages.
- Distinguish between transient failures (retry) and permanent failures (abort).
- Provide actionable error messages with troubleshooting steps.
- Log all CLI command outputs for debugging.

---

## III. Preferred Patterns (Recommended)

### 3.1 → Automation Scripts
- Create reusable shell/Python scripts for common deployment workflows.
- Use Makefile or task runner (invoke, just) for standardized commands.
- Parameterize scripts with environment variables for flexibility.
- Example Makefile targets:
  ```makefile
  deploy-notebook: lint validate-auth push-notebook
  run-job: create-job-if-needed run-and-monitor
  ```

### 3.2 → Workspace Organization

**Git-Based (Repos)**:
- Use consistent path structure: `/Repos/{team}/{project}/notebooks/{module}/`
- Reference via `git_source` in job definitions
- Manage via Git commits and branches

**Workspace-Based Paths**:
- **User workspace**: `/Users/{user's ATTUID}@att.com/` for personal development and testing
- **Shared workspace**: `/Shared/{team}/` for team collaboration (use with caution)
- Avoid `/Workspace/` root paths (deprecated)

**Best Practices**:
- Use `$USER` or `$(whoami)` to dynamically construct paths (see Section 2.1)
- Email pattern: `${USER}@att.com` (e.g., `user's ATTUID@att.com`)
- Separate user workspaces from shared team workspaces
- Tag notebooks with metadata: owner, purpose, dependencies
- Maintain notebook documentation with usage examples
- Promote from `/Users/` to `/Repos/` when moving to production

**CLI Examples**: See Section V.1 for complete notebook and job operations commands

### 3.3 → Development Environments
- Use local virtual environments matching Databricks cluster Python version.
- Mirror cluster library dependencies in local `requirements.txt`.
- Test notebooks locally with PySpark before deploying when possible.
- Use notebooks with `%run` magic for shared utilities.

### 3.4 Job Management
- Use descriptive job names: `{project}_{env}_{workflow}_{purpose}`.
- Tag jobs with: project, environment, owner, schedule.
- Version job configurations in Git alongside notebooks.
- Use Terraform or Databricks Asset Bundles for IaC when possible.

### 3.5 CI/CD Integration
- Hook CLI commands into CI/CD pipelines for automated deployment.
- Run validation checks in pre-commit hooks.
- Use GitHub Actions or Azure DevOps with Databricks CLI installed.
- Separate deployment credentials from development credentials.

### 3.6 Interactive Development
- Use `databricks-connect` for local Spark session with remote cluster.
- Develop notebooks in Jupyter/VS Code with Databricks extension.
- Sync notebooks bidirectionally with workspace using `databricks sync`.
- Test small data samples locally before full cluster execution.

---

## IV. Quality Standards

- **Deployment Success Rate**: ≥ 99% successful notebook pushes without errors.
- **Job Creation Time**: ≤ 2 minutes from notebook push to job execution start.
- **Syntax Validation Coverage**: 100% notebooks must pass linting before push.
- **Monitoring Coverage**: 100% job runs must be monitored until completion or timeout.
- **Documentation Coverage**: All custom scripts must have usage examples and README.

---

## V. CLI Operations Reference

### 5.1 Essential CLI Commands

#### Authentication
```bash
# Configure new profile
databricks configure --token --profile dev

# List profiles
databricks auth profiles

# Test connection
databricks workspace list --profile dev --output JSON
```

#### Notebook Operations

**Push to User Workspace** (Approach 2 - Rapid Development):
```bash
# Push notebook to personal workspace (using dynamic ATTUID)
ATTUID=$(whoami)  # Gets 'user's ATTUID' from system
databricks workspace import \
  ./titanic_ingestion.py \
  /Users/${ATTUID}@att.com/demos/titanic_ingestion \
  --format SOURCE \
  --language PYTHON \
  --overwrite \
  --profile dev

# Verify upload
databricks workspace list /Users/${ATTUID}@att.com/demos --profile dev

# Static example (for reference)
databricks workspace import \
  ./titanic_ingestion.py \
  /Users/user's ATTUID@att.com/demos/titanic_ingestion \
  --format SOURCE --language PYTHON --overwrite --profile dev
```

**Pull from Workspace**:
```bash
# Export from user workspace (dynamic)
ATTUID=$(whoami)
databricks workspace export \
  /Users/${ATTUID}@att.com/demos/titanic_ingestion \
  ./titanic_ingestion.py \
  --format SOURCE \
  --profile dev

# Export from Repos path
databricks workspace export \
  /Repos/team/project/my_notebook \
  ./my_notebook.py \
  --format SOURCE \
  --profile dev
```

**List Workspace Directories**:
```bash
# List user workspace (dynamic)
ATTUID=$(whoami)
databricks workspace list /Users/${ATTUID}@att.com --profile dev

# List Repos
databricks workspace list /Repos/team/project --profile dev
```

**Delete Notebook** (with backup!):
```bash
# Backup first (dynamic)
ATTUID=$(whoami)
databricks workspace export /Users/${ATTUID}@att.com/demos/old_notebook ./backup.py --profile dev

# Then delete
databricks workspace delete /Users/${ATTUID}@att.com/demos/old_notebook --profile dev
```

#### Job Operations
```bash
# Create job from JSON
databricks jobs create --json-file job_config.json --profile dev

# Update existing job
databricks jobs reset --job-id 12345 --json-file job_config.json --profile dev

# Run job immediately
databricks jobs run-now --job-id 12345 --profile dev

# List jobs
databricks jobs list --profile dev --output JSON | jq '.jobs[] | {job_id, name}'

# Get job details
databricks jobs get --job-id 12345 --profile dev
```

#### Run Monitoring
```bash
# Get run status
databricks runs get --run-id 67890 --profile dev

# Poll run until completion
run_id=67890
while true; do
  state=$(databricks runs get --run-id $run_id --profile dev | jq -r '.state.life_cycle_state')
  if [[ "$state" == "TERMINATED" || "$state" == "INTERNAL_ERROR" ]]; then
    break
  fi
  echo "Run state: $state"
  sleep 10
done

# Get run output (logs)
databricks runs get-output --run-id 67890 --profile dev

# Cancel running job
databricks runs cancel --run-id 67890 --profile dev
```

#### Cluster Operations (for development)
```bash
# List clusters
databricks clusters list --profile dev

# Get cluster details
databricks clusters get --cluster-id abc-123-def --profile dev

# Start cluster
databricks clusters start --cluster-id abc-123-def --profile dev

# Check cluster status for job
databricks clusters list --profile dev | jq '.clusters[] | select(.cluster_name=="my-dev-cluster")'
```

### 5.2 Common Workflow Scripts

#### Deploy and Run Script (Bash) - Dynamic ATTUID
```bash
#!/bin/bash
set -e

# Get ATTUID dynamically from environment
ATTUID=$(whoami)
USER_EMAIL="${ATTUID}@att.com"

PROFILE="${DATABRICKS_PROFILE:-dev}"
NOTEBOOK_PATH="$1"
NOTEBOOK_NAME=$(basename "$NOTEBOOK_PATH" .py)
WORKSPACE_SUBPATH="${2:-demos}"  # Default to 'demos' if not provided
WORKSPACE_PATH="/Users/${USER_EMAIL}/${WORKSPACE_SUBPATH}/${NOTEBOOK_NAME}"
JOB_ID="$3"

echo "ATTUID: $ATTUID"
echo "Workspace Path: $WORKSPACE_PATH"

echo "Validating notebook..."
python -m py_compile "$NOTEBOOK_PATH"

echo "Pushing to workspace..."
databricks workspace import "$NOTEBOOK_PATH" "$WORKSPACE_PATH" \
  --language PYTHON --format SOURCE --overwrite --profile "$PROFILE"

echo "Verifying push..."
databricks workspace list "/Users/${USER_EMAIL}/${WORKSPACE_SUBPATH}" --profile "$PROFILE"

if [ -n "$JOB_ID" ]; then
  echo "Running job $JOB_ID..."
  run_id=$(databricks jobs run-now --job-id "$JOB_ID" --profile "$PROFILE" | jq -r '.run_id')
  echo "Started run: $run_id"
  
  echo "Monitoring run..."
  databricks runs get --run-id "$run_id" --profile "$PROFILE" --wait
  
  result=$(databricks runs get --run-id "$run_id" --profile "$PROFILE" | jq -r '.state.result_state')
  if [ "$result" != "SUCCESS" ]; then
    echo "Job failed with state: $result"
    databricks runs get-output --run-id "$run_id" --profile "$PROFILE"
    exit 1
  fi
  echo "Job completed successfully"
fi
```

#### Deploy and Run Script (Python)
```python
#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import json

def run_cli_command(command, profile):
    """Run databricks CLI command and return JSON output."""
    full_cmd = f"{command} --profile {profile} --output JSON"
    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"CLI command failed: {result.stderr}")
    return json.loads(result.stdout) if result.stdout else {}

def deploy_and_run(notebook_path, workspace_path, job_id=None, profile="dev"):
    """Deploy notebook and optionally run job."""
    print(f"Deploying {notebook_path} to {workspace_path}...")
    
    # Push notebook
    cmd = f"databricks workspace import {notebook_path} {workspace_path} --language PYTHON --format SOURCE --overwrite"
    subprocess.run(f"{cmd} --profile {profile}", shell=True, check=True)
    print("✓ Notebook deployed")
    
    if job_id:
        print(f"Starting job {job_id}...")
        result = run_cli_command(f"databricks jobs run-now --job-id {job_id}", profile)
        run_id = result["run_id"]
        print(f"Started run: {run_id}")
        
        # Monitor run
        timeout = 3600  # 1 hour
        start_time = time.time()
        while time.time() - start_time < timeout:
            run_status = run_cli_command(f"databricks runs get --run-id {run_id}", profile)
            state = run_status["state"]["life_cycle_state"]
            
            if state in ["TERMINATED", "INTERNAL_ERROR", "SKIPPED"]:
                result_state = run_status["state"].get("result_state", "UNKNOWN")
                if result_state == "SUCCESS":
                    print(f"✓ Job completed successfully")
                    return True
                else:
                    print(f"✗ Job failed with state: {result_state}")
                    output = run_cli_command(f"databricks runs get-output --run-id {run_id}", profile)
                    print(f"Error: {output.get('error', 'No error details')}")
                    return False
            
            print(f"  Run state: {state}")
            time.sleep(10)
        
        print("✗ Job monitoring timeout")
        return False
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: deploy_and_run.py <notebook_path> [workspace_subpath] [job_id] [profile]")
        print("Example: deploy_and_run.py ./titanic_ingestion.py demos 12345 dev")
        sys.exit(1)
    
    # Get ATTUID dynamically
    attuid = os.getenv("USER") or subprocess.check_output(["whoami"], text=True).strip()
    user_email = f"{attuid}@att.com"
    
    notebook = sys.argv[1]
    notebook_name = os.path.splitext(os.path.basename(notebook))[0]
    workspace_subpath = sys.argv[2] if len(sys.argv) > 2 else "demos"
    workspace = f"/Users/{user_email}/{workspace_subpath}/{notebook_name}"
    job = sys.argv[3] if len(sys.argv) > 3 else None
    prof = sys.argv[4] if len(sys.argv) > 4 else os.getenv("DATABRICKS_PROFILE", "dev")
    
    print(f"ATTUID: {attuid}")
    print(f"Workspace Path: {workspace}")
    
    success = deploy_and_run(notebook, workspace, job, prof)
    sys.exit(0 if success else 1)
```

**Usage Examples**:
```bash
# Using bash script (automatically detects ATTUID)
./deploy_and_run.sh ./titanic_ingestion.py demos 12345 dev
# Result: Pushes to /Users/user's ATTUID@att.com/demos/titanic_ingestion

# Using Python script (automatically detects ATTUID)
python deploy_and_run.py ./titanic_ingestion.py demos 12345 dev
# Result: Pushes to /Users/user's ATTUID@att.com/demos/titanic_ingestion

# Manual CLI with dynamic ATTUID
ATTUID=$(whoami)
databricks workspace import \
  ./titanic_ingestion.py \
  /Users/${ATTUID}@att.com/demos/titanic_ingestion \
  --format SOURCE --language PYTHON --overwrite --profile dev

# Verify
databricks workspace list /Users/${ATTUID}@att.com/demos --profile dev
```

### 5.3 Environment Setup Checklist
- [ ] Databricks CLI installed and version ≥ 0.213.0
- [ ] Authentication profiles configured for each environment
- [ ] Workspace connectivity validated
- [ ] Local Python environment matches cluster Python version
- [ ] Required CLI tools installed: jq, python3, git
- [ ] Environment variables set: `DATABRICKS_PROFILE`, `DATABRICKS_HOST` (optional)
- [ ] Pre-commit hooks configured for notebook validation
- [ ] Documentation reviewed for deployment process

---

## VI. Enforcement Mechanisms

- Pre-push validation scripts check notebook syntax and credential scanning.
- Environment validation ensures CLI connectivity and proper authentication.
- Job creation must follow `databricks-workflow-creator` template standards (see Section VIII).
- Monitoring scripts enforce run tracking and log collection requirements.
- CI/CD pipelines validate all deployment steps before production promotion.

---

## VII. Override Protocol

- Hard-stop overrides require security team approval for credential exceptions.
- Production deployment without staging validation requires change management approval.
- Direct production modifications require incident commander authorization.
- CLI version exceptions require platform team assessment and time-bound exception.

---

## VIII. Integration with Other Archetypes

This archetype complements and must align with:

### databricks-workflow-creator (PRIMARY DEPENDENCY)
**Relationship**: `databricks-developer-workflow` handles **HOW** to deploy; `databricks-workflow-creator` defines **WHAT** the job configuration must contain.

**Authority**: `databricks-workflow-creator` is the single source of truth for:
- Job configuration structure and required fields (Section 5.1-5.2)
- Cluster configuration and cost controls (Section 2.6)
- Git integration patterns (Section 3.1)
- Retry policies, timeouts, and notifications (Section 2.1)
- Secrets management and credential handling (Section 1.3)
- Quality gates and Unity Catalog governance (Sections 1.4, 2.3)

**Hard-Stop Alignment**: 
- ✘ **NEVER** create jobs via CLI that violate workflow-creator hard-stop rules (Section I)
- ✔ **ALWAYS** use workflow-creator Enterprise Job Template (Section 5.1) as base for CLI job creation
- ✔ **ALWAYS** validate CLI-created job JSON against workflow-creator Required Fields Checklist (Section 5.2)

**Cross-Reference Pattern**:
```bash
# Step 1: Use workflow-creator job template as base
# Step 2: Adapt notebook_path based on deployment approach (Git vs Workspace)
# Step 3: Validate against workflow-creator checklist
# Step 4: Deploy via databricks CLI
```

**See**: Section 2.4 of this constitution for detailed cross-reference table.

---

### notebook-collaboration-coach
- **Relationship**: Notebooks developed locally must follow collaboration standards before deployment.
- **Cross-Reference**: Version control, review discipline, and reproducibility standards apply.
- **Workflow**: Notebooks pass collaboration standards → Developer workflow deploys them

### automation-scripter
- **Relationship**: Deployment scripts (bash/Python) follow automation-scripter patterns.
- **Cross-Reference**: Script security, idempotency, error handling, and logging standards apply.
- **Examples**: Section V deployment scripts follow automation-scripter constitution patterns

---

**Version**: 1.0.0  
**Last Updated**: 2025-11-04  
**Maintainer**: Developer Experience Team  
**Change Log**: Initial constitution for databricks-developer-workflow archetype covering CLI operations, notebook deployment, and job execution patterns.
