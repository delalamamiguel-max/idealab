---
description: Scaffold governed experiment design with statistical rigor, lineage tracking, and approval workflows (Experiment Scientist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype experiment-scientist --json ` and parse for ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/experiment-scientist/templates/env-config.yaml` for metric thresholds, review gates, and MLflow workspace IDs

### 3. Parse Input
Extract from $ARGUMENTS: experiment goal, primary/secondary metrics, control definition, treatment variants, sample size constraints, data sources, governance tickets. Request clarification if incomplete.

### 4. Validate Constraints
Check proposal against non-negotiables:
- ✘ Refuse designs without control/baseline cohorts
- ✘ Refuse missing power analysis or sample sufficiency evidence
- ✘ Refuse cherry-picked or undefined primary metrics
- ✘ Refuse absent statistical testing plan
- ✘ Refuse missing lineage references (MLflow run IDs, dataset versions, git SHAs)
- ✘ Refuse approvals that bypass Azure DevOps workflow gates
- ✘ Refuse promotions exceeding `metric_tolerance_delta`
Explain violations and recommend compliant remediation.

### 5. Generate Experiment Blueprint
Compose scaffold including:
- Experiment design doc skeleton (hypothesis, cohorts, KPI definitions, guardrails)
- Deterministic data split recipe with stratification guidance
- Cross-validation configuration aligned to problem type (k-fold, time-series, group)
- Statistical evaluation cells (hypothesis tests, confidence interval computation, Bayesian option)
- Fairness assessment checklist with required metrics per protected attribute
- MLflow integration steps (run creation, artifact logging, approval tagging)
- Azure DevOps pipeline hooks for automated validation and approvals
- Audit trail capture (PDF export, config snapshots, notebook archive)

### 6. Add Recommended Enhancements
Suggest optional additions:
- Adaptive experimentation pattern (multi-armed bandit or Bayesian optimization) with safeguards
- Scenario and stress-test simulations for edge cases
- Notification wiring (Teams/email) on experiment completion or threshold breach
- Visualization dashboard pointers (Databricks SQL, Power BI templates)
- Decision log template linking to governance artifacts

### 7. Validate and Report

## Error Handling
- Hard-stop triggered: Block scaffold and cite specific constitution clause; provide remediation checklist
- Insufficient inputs: Request hypothesis, metrics, control/treatment descriptions, sample targets; share example command
- Tooling gap: Flag missing MLflow workspace or Azure DevOps pipeline and reference env-config onboarding steps
- Governance conflict: Notify user to reopen approval ticket and attach refreshed experiment design doc

## Examples
- **Example 1**: `/scaffold-experiment Launch churn uplift test comparing gradient boosted model vs baseline rules`
- **Example 2**: `/scaffold-experiment Design pricing elasticity experiment with regional segmentation and fairness guardrails`
- **Example 3**: `/scaffold-experiment Prepare adaptive A/B test for new recommendation model with Azure DevOps approvals`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/experiment-scientist/templates/env-config.yaml`
