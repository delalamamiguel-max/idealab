---
description: Document Responsible AI assessment outcomes, decisions, and monitoring commitments (AI Ethics Advisor)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype ai-ethics-advisor --json ` and parse for DOC_TOOLING, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/ai-ethics-advisor/templates/env-config.yaml` for disclosure templates, approval roles, monitoring thresholds

### 3. Parse Input
Extract from $ARGUMENTS: assessment package location, decision outcome (approve/conditional hold/reject), residual risks, mitigation owners, monitoring commitments, stakeholder audiences. Request clarification if incomplete.

### 4. Structure Documentation
Produce comprehensive record covering:
- Executive summary (model purpose, risk tier, decision outcome)
- Ethical risk register highlights (top risks, mitigations, owners, due dates)
- Fairness evaluation summary (metrics, cohorts, thresholds, mitigation status)
- Explainability overview (artifacts generated, reviewer feedback, limitations)
- Governance sign-off trail (approvers, timestamps, outstanding conditions)
- Monitoring plan (drift/fairness thresholds, alert routing, audit cadence, recertification schedule)
- Privacy and security attestations (consent provenance, data handling, storage controls)
- Stakeholder communication commitments (disclosures, consent language, recourse process)
- Action item tracker (open mitigations, deadlines, responsible roles)

### 5. Embed Evidence Links
- Reference consent registry entries, fairness notebooks, Explainability dashboards, approval tickets, monitoring configs, privacy audits
- Parameterize links as variables where possible to avoid hard-coded environments
- Ensure documents are stored in approved audit repository with correct access controls

### 6. Generate Distribution Package
- Create model card and datasheet appendices referencing the documentation update
- Produce stakeholder-specific summaries (governance board brief, business owner digest, legal compliance memo)
- Include version history and change log for future audits

### 7. Validate and Publish
Publish documentation to governance portal, notify required approvers, and archive snapshots for audit trail.

## Error Handling
- Missing evidence: Request source artifacts or trigger refactor workflow
- Documentation gaps: Flag policy violations and block publication until content completed
- Access issues: Coordinate with data governance/security teams to provision required permissions

## Examples
- `/document-ai-ethics Summarize Responsible AI review for telemarketing model` → Produces executive summary, fairness highlights, monitoring commitments, approval status
- `/document-ai-ethics Create audit packet for facial recognition pilot` → Generates complete documentation bundle with evidence links, privacy attestations, stakeholder notices
- `/document-ai-ethics Update model card after mitigation rollout` → Delivers change log, revised fairness metrics, new monitoring thresholds, communication addendum

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/ai-ethics-advisor/templates/env-config.yaml`
