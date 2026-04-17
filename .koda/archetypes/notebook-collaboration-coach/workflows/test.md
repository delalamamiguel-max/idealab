---
description: Validate collaborative notebook for reproducible execution, policy compliance, and review readiness (Notebook Collaboration Coach)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype notebook-collaboration-coach --json ` and confirm ENV_VALID. Abort if false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/notebook-collaboration-coach/templates/env-config.yaml` for pairing, linting, Papermill, and archival standards

### 3. Parse Input
Extract from $ARGUMENTS: notebook path, target environment, execution pipeline (Papermill/Databricks jobs), reviewer roster, release timeline, compliance requirements. Request Jupytext pair, CI job IDs, and archival path if missing.

### 4. Plan Validation Suite
Include checks for:
- Git compliance (branch protections, recent commits, reviewer assignments)
- Reproducible top-to-bottom execution via Papermill or Databricks job
- Jupytext synchronization and absence of orphaned files
- Linting/formatting (Black, Ruff, isort, NBQA) passes
- Absence of secrets or sensitive data (static scans, manual review)
- Execution metadata capture (git SHA, timestamp, cluster ID, MLflow run)
- Documentation completeness (overview, results, follow-ups)
- Comment resolution status and PR checklist completion
- Archival policy adherence (sanitized output stored in governed location)

### 5. Execute Validation
Outline steps:
- Trigger Papermill/NBQA pipeline and collect results
- Run Jupytext sync check to ensure parity with script version
- Execute linting/formatting commands and store logs
- Run secret scanners (detect-secrets, truffleHog) as configured
- Capture execution metadata and embed in notebook footer or MLflow tags
- Generate validation report summarizing checks and evidence links

### 6. Assess Outcomes
Summarize pass/fail status:
- Highlight hard-stop violations blocking merge/publication
- Provide remediation tasks with owners and target dates
- Update PR or tracking issue with validation status
- Notify reviewers and stakeholders of readiness or outstanding issues

### 7. Guardrail Verification

## Error Handling
- Missing inputs: Request Jupytext pair, CI job link, reviewer roster; provide example command clarifying expectations
- Hard-stop breach: Block move forward, cite constitution clause, detail remediation before retest
- Tooling gap: Flag absent Papermill/NBQA integration or secret scanner; reference env-config onboarding
- Reviewer availability: Escalate if review SLA at risk due to unassigned reviewers

## Examples
- **Example 1**: `/test-notebook Validate Databricks feature exploration notebook before merge`
- **Example 2**: `/test-notebook Run Papermill and linting checks for marketing analytics notebook`
- **Example 3**: `/test-notebook Certify shared VS Code notebook for production handoff`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/notebook-collaboration-coach/templates/env-config.yaml`
