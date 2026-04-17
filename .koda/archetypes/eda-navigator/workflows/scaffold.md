---
description: Scaffold an EDA notebook workflow with governance, reproducibility, and collaborative audit trail (EDA Navigator)
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
Extract from $ARGUMENTS: source dataset, objectives, hypotheses, sampling logic, visualization needs, collaboration metadata. Request clarification if incomplete.

### 4. Validate Constraints
Check against hard-stop rules:
- ✘ Refuse missing provenance metadata
- ✘ Refuse unrestricted queries
- ✘ Refuse local result storage
- ✘ Refuse missing audit trail
- ✘ Refuse deprecated visual libraries
- ✘ Refuse missing cluster policies
- ✘ Refuse silenced warnings
If violated, explain and suggest compliant alternatives.

### 5. Generate Notebook Workflow
- Notebook header template (summary, objectives, hypotheses, stakeholders)
- Data quality checkpoints (Great Expectations/nulls/duplicates/range)
- Sampling logic (widgets for date/row/segment)
- Profiling cells (stats, plots, outlier diagnostics)
- Collaboration metadata cell (reviewer comments, open questions)
- Reproducible seeds for sampling/plots
- Structured logging to MLflow/Delta event tables
- Accessibility compliance (high-contrast, alt-text)

### 6. Add Recommendations
- Interactive widgets for exploration
- Reusable helper modules
- Automated insight summary cell
- Time-series controls
- Version-controlled notebooks
- Dashboard publication hooks
- Unit tests for prep functions

### 7. Validate and Report

## Error Handling
- Hard-stop violation: Cite violated rule (e.g., missing `source_dataset` metadata) and provide remediation steps before continuing
- Incomplete input: Request dataset lineage, sampling budget, or governance contacts and show a well-formed invocation
- Environment/tooling gap: Identify missing visualization library policies or cluster policy bindings and reference env-config installation notes
- Deprecated library usage: Flag unsupported plotting packages and suggest approved alternatives from the constitution

## Examples
- **Example 1**: `/scaffold-eda Create governed EDA for customer churn dataset with 5% sampling cap` → Builds notebook with widgets, provenance cells, fairness-aware profiling
- **Example 2**: `/scaffold-eda Spin up exploratory analysis for IoT telemetry with time-slice controls` → Adds time-series widgets, structured logging, audit trail cells
- **Example 3**: `/scaffold-eda Set up collaborative notebook for marketing campaign review` → Emphasizes reviewer metadata, MLflow logging, accessibility-compliant visuals

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/eda-navigator/templates/env-config.yaml`
