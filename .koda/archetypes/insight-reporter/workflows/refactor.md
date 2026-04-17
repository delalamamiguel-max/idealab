---
description: Refactor performance reporting to restore metric trust, accessibility, and balanced storytelling (Insight Reporter)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype insight-reporter --json ` and confirm ENV_VALID. Abort if false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/insight-reporter/templates/env-config.yaml` for KPI definitions, accessibility standards, and publishing pipelines

### 3. Parse Input
Extract from $ARGUMENTS: report asset path, issues identified (metric mismatch, PII exposure, accessibility gaps), target audience, required turnaround. Request dashboards, datasets, and approval logs if missing.

### 4. Diagnose Current Report
Review for:
- Unreconciled metrics vs authoritative sources
- Missing methodology or segmentation disclosures
- PII or sensitive data in visuals/tables
- Accessibility violations (contrast, alt text, font size)
- Misleading axes or omitted negative outcomes
- Absent approvals or stale reviewer sign-offs
- Incomplete business impact narrative or risk coverage
- Inconsistent model vs baseline comparisons

### 5. Execute Refactor
Recommend updates:
- Implement reconciliation scripts and annotate source-of-truth references
- Add methodology section detailing filters, cohort definitions, segmentation logic
- Mask or aggregate sensitive data to meet privacy standards
- Apply accessible color palettes, alt text, and typography updates
- Rebuild charts with honest axes and include downside metrics
- Refresh approval workflow metadata and audit logs
- Expand business impact narrative to include risks and required actions
- Recompute diagnostics (residuals, calibration) and embed results

### 6. Enhance Sustainability
Suggest improvements:
- Parameterize report generation for automated cadence
- Add monitoring alerts to flag KPI deltas or stale data
- Introduce multilingual or localized storytelling where relevant
- Update reusable templates stored in shared repository
- Automate PPT export or snapshot archival for executives

### 7. Validate and Publish

## Error Handling
- Persistent hard-stop: Refuse publication until metric reconciliation, privacy, or accessibility fulfilled
- Missing artifacts: Request dataset pointers, dashboard export, approval log; share example command to clarify inputs
- Tooling limitations: Flag absence of accessibility tooling or publishing workspace; reference env-config onboarding
- Governance blockers: Escalate if approvals missing or policy thresholds breached

## Examples
- **Example 1**: `/refactor-insight Fix executive churn report failing accessibility audit`
- **Example 2**: `/refactor-insight Reconcile revenue impact metrics for personalization dashboard`
- **Example 3**: `/refactor-insight Remove PII exposure in fraud monitoring report`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/insight-reporter/templates/env-config.yaml`
