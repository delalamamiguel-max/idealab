---
description: Validate reporting packages for metric accuracy, accessibility, and governance readiness (Insight Reporter)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype insight-reporter --json ` and confirm ENV_VALID. Abort if false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/insight-reporter/templates/env-config.yaml` for KPI registries, accessibility checklists, and publishing requirements

### 3. Parse Input
Extract from $ARGUMENTS: report/dashboard ID, target audience, KPIs covered, threshold tolerances, approval workflow, publishing channel. Request dataset snapshots and reconciliation specs if missing.

### 4. Define Test Suite
Plan validations:
- Metric reconciliation vs authoritative data sources (SQL queries, Databricks tables)
- Methodology disclosure completeness (filters, cohorts, segmentation)
- Segmentation accuracy with statistical context
- Accessibility audit (contrast ratios, alt text, keyboard navigation)
- Privacy check ensuring no PII leakage
- Narrative balance confirming risks and negative outcomes included
- Model vs baseline comparison accuracy
- Automation pipeline status (refresh schedules, data freshness)
- Approval workflow readiness (reviewer assignments, sign-off logs)

### 5. Execute Tests
Outline tooling:
- Reconciliation scripts with variance thresholds
- Accessibility tooling (axe CLI, Power BI accessibility analyzer)
- Automated screenshot review with captions and alt text verification
- Template linting for narrative sections
- Approval pipeline dry run in Azure DevOps or Power BI deployment pipelines

### 6. Review Results
Summarize pass/fail outcomes:
- Flag any hard-stop violation blocking publication
- Provide remediation plan with owners and timeline
- Update reporting log with validation status and expiration
- Notify stakeholders of pending approvals or risks

### 7. Guardrail Verification

## Error Handling
- Missing inputs: Request KPI queries, accessibility checklist, approval roster; include example command for context
- Hard-stop breaches: Block release, cite constitution clause, detail remediation before retest
- Tooling limitations: Flag need for accessibility analyzer or reconciliation workspace; reference env-config support
- Approval delays: Escalate to reviewers if SLA risk detected

## Examples
- **Example 1**: `/test-insight Certify quarterly executive narrative for credit risk model`
- **Example 2**: `/test-insight Validate Power BI dashboard accessibility prior to launch`
- **Example 3**: `/test-insight Check automated marketing performance digest before publication`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/insight-reporter/templates/env-config.yaml`
