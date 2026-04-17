---
description: Compare EDA notebook workflows for governance, reproducibility, and collaborative audit trail coverage (EDA Navigator)
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
Extract from $ARGUMENTS: notebook file paths, compare goals (provenance, sampling, audit trail, visualization, reproducibility). Request clarification if incomplete.

### 4. Compare Notebooks
Check for:
- Missing provenance metadata
- Unrestricted queries
- Local result storage
- Missing audit trail
- Deprecated visual libraries
- Missing cluster policies
- Silenced warnings

### 5. Report Comparison
Summarize:
- Governance coverage
- Provenance metadata
- Audit trail
- Sampling enforcement
- Visualization stack
- Recommendations for improvement

## Error Handling
- Ambiguous comparison scope: Ask for specific notebooks or governance dimensions; provide structured prompt for clarity
- Hard-stop violation detected: Highlight non-compliant notebook (e.g., unrestricted query) and advise remediation before proceeding
- Missing evidence: Request provenance cells, MLflow logs, or reviewer metadata for each notebook and demonstrate expected inputs
- Tool incompatibility: Note inconsistent visualization stacks or cluster policies and reference env-config for alignment steps

## Examples
- **Example 1**: `/compare-eda Evaluate two exploratory notebooks for audit trail readiness` → Outputs comparison matrix covering provenance, logging, reviewer metadata
- **Example 2**: `/compare-eda Contrast time-series EDA workflows for adherence to sampling guardrails` → Highlights widget coverage, reproducibility, visualization policies
- **Example 3**: `/compare-eda Review legacy vs new collaborative notebook templates` → Compares governance coverage, accessibility, MLflow integration, approval flow

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/eda-navigator/templates/env-config.yaml`
