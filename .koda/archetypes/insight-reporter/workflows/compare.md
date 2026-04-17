---
description: Compare reporting approaches for stakeholder alignment, compliance, and communication effectiveness (Insight Reporter)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype insight-reporter --json ` and ensure ENV_VALID. Stop if false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/insight-reporter/templates/env-config.yaml` for KPI standards, accessibility requirements, and publishing options

### 3. Parse Input
Extract from $ARGUMENTS: candidate reporting formats (Power BI dashboard, narrative brief, automated digest), audiences, cadence, KPIs, governance needs, localization/accessibility constraints. Request representative artifacts if missing.

### 4. Establish Comparison Criteria
Assess alternatives on:
- Metric reconciliation depth and data lineage transparency
- Methodology clarity and segmentation support
- Accessibility compliance (WCAG, localization)
- Privacy safeguards (PII handling, aggregation)
- Business impact storytelling and risk coverage
- Model vs baseline comparison fidelity
- Automation capabilities (refresh, alerts, publishing)
- Approval workflow alignment and reviewer effort
- Stakeholder engagement effectiveness (interactivity, readability)
- Operational overhead and maintainability

### 5. Evaluate Options
For each approach:
- Score against criteria with supporting evidence
- Highlight hard-stop violations (missing reconciliation, accessibility gaps, PII exposure)
- Note advantages and limitations for different audiences
- Estimate remediation work to reach compliance

### 6. Recommend Strategy
Provide ranked recommendation:
- Preferred reporting mix with rationale tied to guardrails and stakeholder needs
- Complementary deliverables (dashboard + narrative) if required
- Remediation roadmap for viable alternatives
- Governance implications (approval cadence, documentation updates)

### 7. Summarize Decision

## Error Handling
- Missing inputs: Request sample reports, KPI definitions, accessibility constraints; provide example command clarifying expectations
- Hard-stop triggered: Exclude option and cite constitution clause with remediation advice
- Conflicting priorities: Facilitate alignment on engagement vs compliance vs effort trade-offs
- Tooling gap: Flag need for localization, accessibility, or automated publishing resources and reference env-config onboarding

## Examples
- **Example 1**: `/compare-insight Decide between Power BI dashboard and narrated PDF for fraud operations`
- **Example 2**: `/compare-insight Evaluate automated email digest vs executive brief for churn KPIs`
- **Example 3**: `/compare-insight Choose storytelling approach for regulatory transparency report`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/insight-reporter/templates/env-config.yaml`
