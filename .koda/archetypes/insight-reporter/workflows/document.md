---
description: Package reconciled performance narratives, visuals, and approvals for stakeholder distribution (Insight Reporter)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype insight-reporter --json ` and confirm ENV_VALID. Stop if false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/insight-reporter/templates/env-config.yaml` for templates, publishing channels, and accessibility checklists

### 3. Parse Input
Extract from $ARGUMENTS: model/system, reporting cadence, audience segments, required deliverables (dashboard export, narrative brief, PPT), privacy classification, approval workflow. Request KPI reconciliation outputs and segmentation specs if missing.

### 4. Assemble Core Content
Ensure package includes:
- Metric reconciliation summary with variance tables vs authoritative sources
- Methodology section detailing filters, cohorts, segmentation logic
- Segmentation deep dives with statistical context
- Performance trend visuals over `rolling_window_days`
- Model vs baseline comparison charts and narratives
- Business impact summary quantifying revenue/cost/CX effects and risks
- Accessibility compliance documentation (contrast checks, alt text inventory)
- Approval log with reviewer sign-offs and timestamps
- Publishing metadata (refresh schedule, distribution list)

### 5. Format Deliverables
Produce tailored outputs:
- Executive brief with concise narrative and action list
- Operational dashboard export (Power BI PBIX, Databricks SQL link)
- Compliance dossier highlighting privacy considerations and approvals
- Optional PPT deck generated from template with key visuals and notes

### 6. Quality Review
- Verify PII removed or aggregated per policy
- Ensure visuals meet accessibility standards
- Confirm narrative balances wins and risks
- Store artifacts in governed repository with retention metadata
- Notify stakeholders and schedule next update

### 7. Final Guardrail Check

## Error Handling
- Missing components: Request reconciliation workbook, accessibility audit results, approval roster; provide sample command to clarify expectations
- Hard-stop unmet: Refuse publication until reconciliation, accessibility, or approval requirements satisfied
- Storage conflict: Direct to approved repositories per env-config guidance
- Audience ambiguity: Request segmentation details to tailor outputs appropriately

## Examples
- **Example 1**: `/document-insight Publish monthly executive summary for churn model`
- **Example 2**: `/document-insight Prepare compliance packet for Responsible AI review`
- **Example 3**: `/document-insight Deliver weekly operations digest for fraud analysts`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/insight-reporter/templates/env-config.yaml`
