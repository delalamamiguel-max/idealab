---
description: Document EDA notebook workflow for governance, reproducibility, and collaborative audit trail coverage (EDA Navigator)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype eda-navigator --json ` and parse for ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/eda-navigator/templates/env-config.yaml` for cluster policies, visualization stack, and governance settings

### 3. Parse Input
Extract from $ARGUMENTS: notebook file path, documentation goals (provenance, sampling, audit trail, visualization, reproducibility). Request clarification if incomplete.

### 4. Document Notebook
Summarize:
- Governance coverage
- Provenance metadata
- Audit trail
- Sampling enforcement
- Visualization stack
- Recommendations for improvement
- Collaboration metadata (authors, reviewers, approvals) with timestamps
- Monitoring commitments (metrics, alerting, recertification cadence)
- Accessibility and visualization compliance status
- Knowledge base links or follow-up tasks for broader teams

### Recommended Summary Table
| Area | Status | Evidence | Follow-up |
|------|--------|----------|-----------|
| Provenance Metadata | ✅ Complete | Notebook cell `00_provenance` | N/A |
| Audit Trail | ⚠️ Needs reviewer sign-off | MLflow run `eda_2025_10_15` | Collect approval from Ops lead |
| Visualization Stack | ✅ Approved | Plotly 5.19 | N/A |
| Accessibility | ⚠️ Pending alt-text review | Dashboard link | Confirm captions with UX |
| Monitoring Plan | ✅ Configured | Alert policy `eda_freshness` | Schedule quarterly review |

## Error Handling
- Missing artifacts: Request notebook path, MLflow run IDs, or reviewer notes; respond with template command showing required inputs
- Policy violation persists: Halt documentation, cite breached rule (e.g., no audit trail) and direct user to refactor/debug workflow
- Tooling/permission issue: Flag inability to access logs or governance portals; recommend escalation per environment config
- Documentation gaps: Note absent glossary, collaborator comments, or monitoring commitments and provide checklist before publishing

## Examples
- **Example 1**: `/document-eda Produce audit packet for customer churn EDA notebook` → Generates summary, governance coverage table, action tracker
- **Example 2**: `/document-eda Capture documentation for cross-functional experiment review` → Highlights collaboration metadata, reviewer feedback, monitoring plan
- **Example 3**: `/document-eda Update knowledge base entry after accessibility remediation` → Logs visual changes, accessibility checks, stakeholder communications

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/eda-navigator/templates/env-config.yaml`
