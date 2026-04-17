---
description: Produce experiment documentation packages for reviewers, governance, and knowledge management (Experiment Scientist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype experiment-scientist --json ` and ensure ENV_VALID. Stop if validation fails.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/experiment-scientist/templates/env-config.yaml` for documentation templates, storage paths, and approval routing

### 3. Parse Input
Extract from $ARGUMENTS: experiment identifier, target audience (governance, executives, engineering), required artifacts (design doc, validation report, decision log), confidentiality tags. Request MLflow run links, datasets, and approval IDs if absent.

### 4. Compile Core Artifacts
Ensure package includes:
- Experiment design doc with hypothesis, cohorts, KPI hierarchy, guardrails
- Data sourcing and split description with reproducibility details
- Statistical results (tests performed, p-values, CIs, Bayesian summaries)
- Fairness assessment results with mitigation notes
- MLflow lineage report (run IDs, dataset versions, git SHAs)
- KPI comparisons vs baseline and `metric_tolerance_delta`
- Governance record (Azure DevOps approvals, stakeholder sign-offs)
- Decision log entry summarizing go/no-go outcome and follow-ups

### 5. Format for Audiences
Generate tailored outputs:
- Reviewer bundle (notebooks, PDFs, configuration files)
- Executive summary (bulletized insights within `executive_summary_length` if provided)
- Compliance archive (RAI artifacts, fairness reports, consent documentation)
- Knowledge base article or wiki entry with cross-links to related experiments

### 6. Quality Checks
- Verify accessibility (alt text, high-contrast charts)
- Confirm PII removal and secure storage location
- Ensure artifacts stored in MLflow or designated repository with retention metadata
- Validate approvals logged and notifications sent to stakeholders

### 7. Final Guardrail Validation

## Error Handling
- Missing artifacts: Request design doc, metrics report, fairness outputs; offer example command listing required pieces
- Hard-stop violation: Refuse documentation until statistical tests, fairness metrics, or governance approvals completed
- Storage conflict: Redirect to approved MLflow or document repository per env-config guidance
- Confidentiality breach: Halt and escalate if PII or sensitive data detected in report

## Examples
- **Example 1**: `/document-experiment Package promotion review for churn uplift test`
- **Example 2**: `/document-experiment Create governance packet for adaptive pricing experiment`
- **Example 3**: `/document-experiment Summarize fairness and KPI findings for credit risk challenger`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/experiment-scientist/templates/env-config.yaml`
