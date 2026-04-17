---
description: Validate experiment readiness with statistical tests, fairness diagnostics, and governance checks (Experiment Scientist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype experiment-scientist --json ` and confirm ENV_VALID. Abort if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/experiment-scientist/templates/env-config.yaml` for metric tolerances, approval gates, and fairness library versions

### 3. Parse Input
Extract from $ARGUMENTS: experiment artifact path, metrics to validate, cohorts, expected thresholds, governance ticket IDs. Request supplementary config if missing.

### 4. Assemble Test Suite
Plan validation coverage:
- Power and sample adequacy verification scripts
- Statistical test execution (t-test, MWU, chi-square, Bayesian posterior)
- KPI calculations compared to baseline with confidence intervals
- Fairness metrics per protected group and mitigation evidence
- MLflow lineage completeness checks (datasets, run ids, git SHAs)
- Azure DevOps approval status and pipeline log review
- Metric drift comparison to `metric_tolerance_delta`

### 5. Execute Tests
Outline commands/notebooks to run:
- Automated notebooks or pipelines with deterministic seeds
- Papermill/NBQA runs to ensure clean execution
- MLflow validation logs capturing outcomes and artifacts
- Export of validation report (PDF/HTML) with sign-off section

### 6. Evaluate Results
Summarize outcomes:
- Pass/fail per validation dimension with evidence links
- Highlight any breached hard-stop (control missing, stats absent, lineage gaps)
- Provide remediation actions and retest requirements
- Update decision log with validation status

### 7. Final Guardrail Check

## Error Handling
- Missing artifacts: Request experiment notebook path, MLflow run, fairness report; include sample command listing required attachments
- Failing hard-stop: Block promotion, cite constitution clause, outline remediation tasks before retest
- Tooling mismatch: Note absent statistical libraries or fairness packages and point to env-config installation notes
- Governance mismatch: If approval gates not ready, instruct to reconfigure Azure DevOps policies prior to promotion

## Examples
- **Example 1**: `/test-experiment Validate uplift experiment prior to Azure DevOps promotion`
- **Example 2**: `/test-experiment Run fairness and KPI conformance checks for credit risk challenger`
- **Example 3**: `/test-experiment Execute statistical validation suite for adaptive pricing experiment`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/experiment-scientist/templates/env-config.yaml`
