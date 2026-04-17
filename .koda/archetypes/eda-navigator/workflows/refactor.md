---
description: Refactor EDA notebook workflow to enforce governance, reproducibility, and collaborative audit trail (EDA Navigator)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype eda-navigator --json ` and parse for ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/eda-navigator/templates/env-config.yaml` for cluster policies, visualization stack, and governance settings

### 3. Parse Input
Extract from $ARGUMENTS: notebook file path, refactoring goals (provenance, sampling, audit trail, visualization, reproducibility). Request clarification if incomplete.

### 4. Analyze Existing Notebook
Scan for:
- Missing provenance metadata
- Unrestricted queries
- Local result storage
- Missing audit trail
- Deprecated visual libraries
- Missing cluster policies
- Silenced warnings

### 5. Generate Refactored Notebook
Apply:
- Header template
- Data quality checkpoints
- Sampling logic
- Profiling cells
- Collaboration metadata
- Reproducible seeds
- Structured logging
- Accessibility compliance

### 6. Add Recommendations
- Interactive widgets
- Reusable modules
- Insight summary cell
- Time-series controls
- Version control
- Dashboard hooks
- Unit tests

### 7. Validate and Report

## Error Handling
- Hard-stop violation persists: Block refactor until provenance metadata, audit logs, or approved visuals are restored; cite constitution clause
- Missing context: Request notebook path, target cohorts, or governance objectives and return a sample command with required fields
- Tooling mismatch: Surface missing Great Expectations or widget libraries and point to env-config for installation and policy alignment
- Reviewer gaps: Alert if collaboration metadata lacks reviewer/approval info and provide remediation template

## Examples
- **Example 1**: `/refactor-eda Harden legacy product analytics notebook for governance board review` → Adds metadata cells, replaces matplotlib with approved stack, reinstates audit log hooks
- **Example 2**: `/refactor-eda Update sales insights notebook to enforce sampling widgets and MLflow logging` → Introduces parameter widgets, structured logging, reproducible seeds
- **Example 3**: `/refactor-eda Modernize experimentation notebook with accessible visuals and reviewer workflow` → Replaces deprecated visuals, adds collaboration cell, documents approvals

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/eda-navigator/templates/env-config.yaml`
