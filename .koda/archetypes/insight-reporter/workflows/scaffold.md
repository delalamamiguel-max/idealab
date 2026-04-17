---
description: Scaffold stakeholder-ready performance reporting with reconciled metrics and accessible storytelling (Insight Reporter)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype insight-reporter --json ` and ensure ENV_VALID. Halt if false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/insight-reporter/templates/env-config.yaml` for approved data sources, KPI definitions, accessibility standards, and publishing targets

### 3. Parse Input
Extract from $ARGUMENTS: model/system to report, audience (executive, operational, compliance), cadence, KPIs, segmentation requirements, preferred channels (Power BI, Databricks SQL, PPT). Request missing details.

### 4. Validate Constraints
Check plan against hard stops:
- ✘ Reject metrics lacking reconciliation to trusted sources
- ✘ Refuse reports without methodology, filters, or segmentation clarity
- ✘ Block inclusion of PII or unmasked sensitive data
- ✘ Ensure WCAG-compliant visuals (contrast, alt text, font)
- ✘ Prevent misleading charts (axes manipulation) without disclosure
- ✘ Require reviewer approvals before publication
- ✘ Demand balanced narrative covering risks and deficits

### 5. Generate Reporting Blueprint
Provide scaffold including:
- Data reconciliation pipeline comparing telemetry vs business KPI tables
- Segmentation analysis templates with statistical context
- Rolling performance trend visuals aligned to `rolling_window_days`
- Business impact narrative outline quantifying value (revenue, cost, CX)
- Model vs baseline comparison module with key deltas
- Diagnostic visuals (residuals, calibration, cumulative gains)
- Executive summary section respecting `executive_summary_length`
- Accessibility checklist for color palettes, alt text, captions
- Automated publishing workflow to Power BI/Databricks dashboards with approvals

### 6. Add Recommended Enhancements
Suggest optional elements:
- Interactive dashboard design with drill-down and multilingual support
- Scenario simulation visuals for threshold tuning outcomes
- Forecast overlays with confidence bands
- Alert integration (email/Teams) for SLO breaches
- Reusable story templates and PPT export automation

### 7. Validate and Report

## Error Handling
- Hard-stop triggered: Block scaffold, cite violated clause, provide remediation guidance
- Missing inputs: Request KPI definitions, audience profile, cadence, publishing channel; share example command
- Tooling gap: Flag absent dashboard workspace or accessibility resources; reference env-config onboarding
- Data quality concern: Escalate to data owners if reconciliation fails

## Examples
- **Example 1**: `/scaffold-insight Build monthly executive narrative for churn model`
- **Example 2**: `/scaffold-insight Prepare Power BI dashboard for fraud detection performance`
- **Example 3**: `/scaffold-insight Create bilingual operations report for recommendation engine`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/insight-reporter/templates/env-config.yaml`
