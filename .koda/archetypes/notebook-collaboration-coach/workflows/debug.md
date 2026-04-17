---
description: Diagnose collaborative notebook issues and restore reproducibility, review compliance, and security (Notebook Collaboration Coach)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype notebook-collaboration-coach --json ` and require ENV_VALID. Stop if false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/notebook-collaboration-coach/templates/env-config.yaml` for pairing rules, linting configs, and archival settings

### 3. Parse Input
Collect from $ARGUMENTS: notebook path, failure symptoms (merge conflict, execution drift, review rejection, secret exposure), environment, collaborators, timeline. Request PR link, CI logs, and archival details if absent.

### 4. Reproduce Issue
Investigate by:
- Checking git history and branch status for merge or conflict errors
- Running notebook end-to-end to detect hidden state or missing setup steps
- Validating Jupytext pairing status and diffs between `.ipynb` and script
- Reviewing CI outputs (Papermill, NBQA, linting) for failure messages
- Scanning for embedded secrets or credentials
- Inspecting reviewer comments and unresolved threads
- Examining execution metadata (git SHA, environment capture) for discrepancies
- Verifying archival compliance and storage locations

### 5. Apply Fixes
Recommend remediation:
- Resolve git conflicts and ensure branch protection compliance
- Reorder or modularize cells to eliminate hidden state
- Re-sync Jupytext pairing and adjust workflow to prevent divergence
- Fix CI failures (formatting, linting, execution) and update tests
- Replace secrets with secure references or configs
- Address reviewer feedback and document resolutions in PR
- Capture updated execution metadata and log results
- Archive sanitized notebook outputs per policy

### 6. Prevent Recurrence
Suggest safeguards:
- Add pre-commit hooks for Jupytext sync and linting checks
- Automate Papermill runs on PR and nightly schedules
- Use template-based review checklist to ensure coverage
- Provide contributor guide covering parameterization and environment setup
- Enable notifications for stale reviews or unpaired notebooks

### 7. Validate and Report

## Error Handling
- Missing evidence: Request PR link, CI logs, Jupytext file; provide example command listing requirements
- Hard-stop unresolved: Refuse completion until git control, execution validation, or secret removal confirmed
- Tooling outage: Escalate if NBQA/Papermill infrastructure unavailable; reference env-config contingency plan
- Governance escalation: Notify approvers if review policy breached or compliance deadlines missed

## Examples
- **Example 1**: `/debug-notebook Papermill pipeline failing due to hidden state in feature notebook`
- **Example 2**: `/debug-notebook Secrets detected in marketing analysis notebook`
- **Example 3**: `/debug-notebook Jupytext sync conflicts causing merge failures`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/notebook-collaboration-coach/templates/env-config.yaml`
