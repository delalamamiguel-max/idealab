---
description: Test EDA notebook workflow for governance, reproducibility, and collaborative audit trail compliance (EDA Navigator)
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
Extract from $ARGUMENTS: notebook file path, test goals (provenance, sampling, audit trail, visualization, reproducibility). Request clarification if incomplete.

### 4. Test Notebook
Check for:
- Missing provenance metadata
- Unrestricted queries
- Local result storage
- Missing audit trail
- Deprecated visual libraries
- Missing cluster policies
- Silenced warnings

### 5. Validate and Report

## Error Handling
- Test failure on guardrail: Document failing assertion (e.g., missing audit trail cell) and supply remediation checklist before re-running
- Missing evidence: Request notebook revision link, MLflow run, or widget configuration; provide fully-specified sample command
- Tooling/config mismatch: Identify absent expectations library or visualization policy and reference env-config remediation
- Non-compliant cluster: Flag test executions on clusters without required policies and advise escalation

## Examples
- **Example 1**: `/test-eda Certify finance exploratory notebook prior to leadership review` → Produces pass/fail matrix with remediation items and approvals
- **Example 2**: `/test-eda Validate marketing experiment notebook for provenance and audit trail` → Confirms metadata cells, reviewer logs, sampling widgets
- **Example 3**: `/test-eda Run regression tests on EDA template after visualization stack upgrade` → Ensures approved libraries, accessibility checks, reproducible seeds

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/eda-navigator/templates/env-config.yaml`
