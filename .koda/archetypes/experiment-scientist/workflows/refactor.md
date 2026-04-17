---
description: Refactor experiment workflow to restore statistical rigor, lineage completeness, and governance compliance (Experiment Scientist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype experiment-scientist --json ` and confirm ENV_VALID. Abort if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/experiment-scientist/templates/env-config.yaml` for metric thresholds, approval routing, and MLflow workspaces

### 3. Parse Input
Extract from $ARGUMENTS: experiment asset path, observed defects (missing control, weak metrics, absent lineage), desired refactor outcomes, stakeholders. Request supporting notebooks, MLflow run IDs, and Azure DevOps tickets if absent.

### 4. Diagnose Current State
Audit supplied workflow for:
- Missing control cohort or baseline definitions
- Insufficient power/sample calculations or misaligned splits
- Cherry-picked KPIs or undocumented metric changes
- Absent statistical tests or confidence intervals
- Missing MLflow lineage (dataset versions, git SHAs, artifact logs)
- Violations of governance approvals or `metric_tolerance_delta`
- Fairness/bias assessment gaps across regulated cohorts

### 5. Produce Refactored Plan
Recommend targeted changes:
- Rebuild design doc sections with explicit hypotheses and KPI hierarchy
- Introduce deterministic split utilities and cross-validation strategies
- Add statistical evaluation notebooks (t-tests, MWU, Bayesian) with guardrails
- Embed fairness evaluation notebooks and reporting templates
- Wire MLflow logging calls (parameters, metrics, artifacts, approvals)
- Reconnect Azure DevOps pipeline gates and policy checks
- Archive audit-ready artifacts (PDFs, configs, decision logs)

### 6. Prevent Regression
Suggest automation:
- Scheduled power recalculations when traffic shifts
- Scenario simulation jobs validating robustness
- Teams alerts for metric drift or fairness regressions
- Template library updates shared across experiment squads
- Knowledge base entry documenting remediation steps

### 7. Validate and Report

## Error Handling
- Hard-stop persists: Block refactor until control groups, sample sufficiency, and statistical plan restored
- Missing evidence: Request MLflow run URL, dataset catalog entries, or Azure DevOps approval chain; provide example command for context
- Tooling misalignment: Flag absent fairness libraries or MLflow permissions and guide via env-config onboarding
- Governance override attempts: Escalate to approvers and halt changes until formal variance granted

## Examples
- **Example 1**: `/refactor-experiment Tighten promotion gating for personalization uplift test with missing control`
- **Example 2**: `/refactor-experiment Rebuild fairness reporting for credit risk challenger experiment`
- **Example 3**: `/refactor-experiment Reconnect MLflow lineage and Azure DevOps approvals for churn A/B`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/experiment-scientist/templates/env-config.yaml`
