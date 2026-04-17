---
description: Package interpretability artifacts, fairness evidence, and stakeholder guidance for compliant distribution (Interpretability Analyst)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype interpretability-analyst --json ` and ensure ENV_VALID. Stop if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/interpretability-analyst/templates/env-config.yaml` for templates, storage policies, and communication channels

### 3. Parse Input
Extract from $ARGUMENTS: model version, audiences, required deliverables (model card, fairness report, stakeholder brief), confidentiality level, governance deadlines. Request MLflow run links and prior artifacts if missing.

### 4. Assemble Core Content
Ensure package includes:
- Updated model card (purpose, data, evaluation, ethical considerations, maintenance plan)
- Explainability summary (technique descriptions, limitations, key insights)
- Fairness diagnostics with metrics, mitigation actions, and cohort commentary
- Counterfactual or sensitivity findings with guardrails
- Visualization gallery with accessibility annotations and alt text inventory
- Compliance metadata (author, timestamp, model version, tooling)
- Storage references confirming artifacts logged in MLflow/RAI repository
- Stakeholder-specific guidance outlining actions, caveats, and escalation paths

### 5. Tailor Deliverables
Produce audience-specific outputs:
- Compliance dossier with detailed metrics, policy references, and archival paths
- Business briefing summarizing impact, limitations, and recommended decisions
- Technical appendix with reproducible notebooks/scripts and deterministic seeds
- Optional executive summary deck or one-pager

### 6. Quality Checks
- Verify privacy safeguards (no PII or sensitive individual data in artifacts)
- Confirm accessibility compliance (contrast ratios, alt text, captions)
- Ensure approved libraries used and dependencies documented
- Validate artifacts stored in governed repository with retention metadata
- Trigger approvals and notifications per governance workflow

### 7. Guardrail Verification

## Error Handling
- Missing materials: Request fairness report, explanation notebooks, MLflow run; provide example command to clarify expectations
- Hard-stop unmet: Refuse delivery until transparency, fairness, or storage guardrails fulfilled
- Storage conflict: Direct to approved repositories per env-config guidance
- Audience ambiguity: Ask for stakeholder breakdown to tailor messaging appropriately

## Examples
- **Example 1**: `/document-interpretability Prepare compliance packet for credit decision model review`
- **Example 2**: `/document-interpretability Assemble stakeholder brief for personalization explainability`
- **Example 3**: `/document-interpretability Publish interpretability summary for Responsible AI council`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/interpretability-analyst/templates/env-config.yaml`
