---
description: Diagnose interpretability gaps and restore compliant, trustworthy explanation artifacts (Interpretability Analyst)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype interpretability-analyst --json ` and require ENV_VALID. Stop if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/interpretability-analyst/templates/env-config.yaml` for approved library versions, storage targets, and policy links

### 3. Parse Input
Collect from $ARGUMENTS: model ID, failing artifact (notebook, dashboard, report), symptom (compliance rejection, fairness alert, privacy concern), audience, timeline. Request MLflow run, dataset sample, and prior explanation outputs if absent.

### 4. Reproduce Issue
Investigate by:
- Reviewing method descriptions and limitation statements
- Verifying approved library usage and version compliance
- Inspecting data outputs for PII or sensitive attribute exposure
- Recomputing fairness metrics across protected cohorts
- Checking storage logs to ensure artifacts archived in MLflow/RAI repo
- Auditing visualizations for accessibility compliance and clarity
- Re-running counterfactual/sensitivity analyses for reproducibility
- Validating stakeholder summary accuracy and actionable guidance

### 5. Apply Fixes
Recommend remediation:
- Document or update explanation methodology with caveats
- Swap unapproved tools for sanctioned libraries; re-log results
- Aggregate/anonymize outputs to remove privacy risk
- Generate missing fairness diagnostics with narrative interpretation
- Repackage artifacts into MLflow with audit metadata
- Redesign visuals with accessible palettes and descriptive captions
- Update counterfactual scenarios and sensitivity checks with deterministic seeds
- Revise stakeholder guidance sections with clear actions and limitations

### 6. Prevent Recurrence
Propose safeguards:
- Automate validation pipeline for method transparency and storage checks
- Add fairness metric thresholds with alerting
- Maintain approved library manifest and monitor deviations
- Schedule periodic review of templates and stakeholder messaging
- Capture learnings in explainability knowledge base

### 7. Validate and Report

## Error Handling
- Missing evidence: Request explanation notebook, fairness report, storage logs; include example command listing expected attachments
- Hard-stop unresolved: Halt support until privacy, fairness, or storage compliance restored
- Tooling outage: Escalate if approved libraries unavailable; reference env-config contingencies
- Governance escalation: Notify compliance if user attempts to publish without stakeholder guidance

## Examples
- **Example 1**: `/debug-interpretability Compliance rejected explainability pack for missing method disclosure`
- **Example 2**: `/debug-interpretability Fairness dashboard shows disparity after retrain`
- **Example 3**: `/debug-interpretability SHAP output leaking PII in credit decisions`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/interpretability-analyst/templates/env-config.yaml`
