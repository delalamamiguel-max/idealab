---
description: Debug EDA notebook workflow for governance, reproducibility, and collaborative audit trail violations (EDA Navigator)
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
Extract from $ARGUMENTS: notebook file path, debug goals (provenance, sampling, audit trail, visualization, reproducibility). Request clarification if incomplete.

### 4. Analyze Notebook
Check for:
- Missing provenance metadata
- Unrestricted queries
- Local result storage
- Missing audit trail
- Deprecated visual libraries
- Missing cluster policies
- Silenced warnings

### 5. Debug and Fix
- Header template
- Data quality checkpoints
- Sampling logic
- Profiling cells
- Collaboration metadata
- Reproducible seeds
- Structured logging
- Accessibility compliance

### 6. Validate and Report

## Error Handling
- Hard-stop breach confirmed: Halt execution, document violated guardrail (e.g., unrestricted `SELECT *`) and prescribe compliant fix
- Insufficient diagnostics: Request Spark UI logs, notebook revision history, or MLflow run IDs; share example invocation showing expected evidence
- Tool availability: Identify missing visualization approvals or Great Expectations configs, referencing env-config for remediation
- Cluster policy drift: Flag notebooks executed on non-compliant clusters and advise remediation or escalation per governance workflow

## Examples
- **Example 1**: `/debug-eda Investigate notebook that lost provenance metadata after merge` → Restores lineage cells, replays MLflow logs, updates audit trail
- **Example 2**: `/debug-eda Resolve fairness widget failures in collaborative experiment notebook` → Fixes widget config, revalidates sampling logic, documents mitigation
- **Example 3**: `/debug-eda Fix deprecated visualization usage blocking ethics review` → Replaces unapproved library, validates accessibility, logs remediation steps

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/eda-navigator/templates/env-config.yaml`
