---
description: Generate Databricks developer workflow scripts with CLI operations, notebook deployment, and job execution patterns
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Gather Requirements

Extract from $ARGUMENTS:
- Deployment approach (Git-based vs Workspace-based)
- Target environment (dev, staging, prod)
- Notebook paths and locations
- Job requirements (if any)
- Monitoring needs

### 2. Validate Environment Prerequisites

Check for required tools and configuration:
- Databricks CLI version ≥ 0.213.0
- Authentication profiles configured
- Environment variables set (DATABRICKS_PROFILE, USER)
- Local Python environment matching cluster version

### 3. Generate CLI Profile Configuration

Create or validate `.databrickscfg` profile:
- Separate profiles for each environment (dev, staging, prod)
- OAuth or service principal authentication (no hardcoded tokens)
- Validate workspace connectivity

### 4. Generate Deployment Scripts

Based on deployment approach:

**For Git-Based Workflow (Production)**:
- Pre-commit validation script (linting, credential scanning)
- Job configuration following databricks-workflow-creator standards
- CI/CD integration hooks

**For Workspace-Based Workflow (Development)**:
- Notebook push script with dynamic ATTUID resolution
- Workspace path validation
- Quick iteration deployment script

### 5. Generate Job Configuration

If job execution required, create job config following databricks-workflow-creator standards:
- Use enterprise job template as base
- Configure notebook_task based on deployment approach
- Set appropriate cluster configuration
- Include retry policies and notifications

**Delegate job structure to**: `/scaffold-databricks-workflow-creator` for complex job configurations

### 6. Generate Monitoring Scripts

Create run monitoring capabilities:
- Poll run status with exponential backoff
- Capture lifecycle and result states
- Log collection on failure
- Timeout handling

### 7. Generate Validation Checks

Create pre-deployment validation:
- Notebook syntax validation (pylint, black)
- Import and dependency checks
- PII and credential scanning
- Workspace path standard conformance

### 8. Assemble Deployment Package

Deliver:
- `scripts/deploy_notebook.sh` - Bash deployment script
- `scripts/deploy_notebook.py` - Python deployment script
- `scripts/monitor_run.sh` - Run monitoring script
- `Makefile` - Standard deployment targets
- `README.md` - Usage documentation
- `.pre-commit-config.yaml` - Validation hooks

## Error Handling

**Missing CLI**: Provide installation instructions for Databricks CLI.

**Authentication Failure**: Guide user through profile configuration.

**Workspace Path Invalid**: Validate ATTUID resolution and path format.

## Examples

### Example 1: Development Workflow Setup

```
/scaffold-databricks-developer-workflow "
Create development workflow for rapid notebook iteration.
Environment: dev
Approach: workspace-based
Notebooks: ./notebooks/data_processing/
"
```

### Example 2: Production Deployment Pipeline

```
/scaffold-databricks-developer-workflow "
Set up CI/CD deployment pipeline for production notebooks.
Environment: prod
Approach: git-based
Repository: team-analytics
Include job configuration and monitoring.
"
```

### Example 3: Full Development Environment

```
/scaffold-databricks-developer-workflow "
Complete developer setup with:
- CLI profiles for all environments
- Notebook push scripts
- Job execution with monitoring
- Pre-commit validation hooks
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/databricks-developer-workflow/databricks-developer-workflow-constitution.md`
- **Job Standards**: `${ARCHETYPES_BASEDIR}/databricks-workflow-creator/databricks-workflow-creator-constitution.md`
- **Related**: databricks-workflow-creator, automation-scripter, notebook-collaboration-coach
