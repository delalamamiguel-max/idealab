---
description: Diagnose reporting defects and restore metric trust, accessibility, and governance compliance (Insight Reporter)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype insight-reporter --json ` and require ENV_VALID. Stop if false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/insight-reporter/templates/env-config.yaml` for KPI registry, accessibility standards, and publishing workflows

### 3. Parse Input
Collect from $ARGUMENTS: report/dashboard identifier, failure symptom (metric mismatch, approval rejection, accessibility bug), impacted audience, timestamp, upstream data sources. Request reconciliation logs, dataset extracts, and approval notes if missing.

### 4. Reproduce Issue
Investigate by:
- Re-running reconciliation scripts vs authoritative KPI sources
- Inspecting methodology, filters, and segmentation logic for omissions
- Scanning visuals/tables for exposed PII or sensitive data
- Running accessibility audit (contrast, alt text, keyboard navigation)
- Checking chart scales and axis integrity
- Reviewing approval tracker for missing sign-offs
- Evaluating narrative balance for hidden risks or SLO misses
- Confirming automation pipelines executed successfully

### 5. Apply Fixes
Recommend remediation:
- Correct data joins or aggregations and document data provenance
- Restore methodology disclosures and cohort definitions
- Sanitize outputs to remove PII or aggregate sensitive fields
- Update visual styles to meet WCAG standards; add alt text and captions
- Rebuild charts with full axes and annotate caveats
- Re-trigger approvals with refreshed evidence and logs
- Expand narrative to include negative outcomes and action items
- Repair automated publishing pipeline or schedule rerun

### 6. Prevent Recurrence
Propose safeguards:
- Add reconciliation health checks with alerting
- Embed accessibility linting in CI pipeline
- Version control story templates and require peer review
- Schedule stakeholder validation steps prior to publication
- Maintain lessons learned in reporting knowledge base

### 7. Validate and Report

## Error Handling
- Missing data: Request KPI source exports, dashboard snapshots, approval notes; provide example command clarifying expectations
- Hard-stop unresolved: Refuse release until reconciliation, accessibility, or approval guardrails satisfied
- Tooling outage: Escalate if Power BI or monitoring services unavailable; reference env-config contingency plans
- Confidentiality breach: Alert security/compliance if PII exposure discovered

## Examples
- **Example 1**: `/debug-insight Metrics in monthly churn brief do not match finance KPIs`
- **Example 2**: `/debug-insight Accessibility audit failed Power BI dashboard`
- **Example 3**: `/debug-insight Compliance rejected report for missing risk narrative`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/insight-reporter/templates/env-config.yaml`
