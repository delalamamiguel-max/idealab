---
description: Package collaborative notebook documentation, review evidence, and archival records (Notebook Collaboration Coach)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype notebook-collaboration-coach --json ` and confirm ENV_VALID. Stop if false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/notebook-collaboration-coach/templates/env-config.yaml` for templates, archival locations, and review policies

### 3. Parse Input
Extract from $ARGUMENTS: notebook path, stakeholders (reviewers, auditors, knowledge base), required artifacts (run summary, execution logs, review checklist), cadence, confidentiality level. Request PR link, CI reports, and archival paths if missing.

### 4. Assemble Core Artifacts
Include:
- Notebook overview (purpose, owners, status, linked tickets)
- Execution metadata (timestamp, environment, git SHA, MLflow run ID)
- Summary of results, decisions, and follow-up actions
- Review checklist completion with comment resolution evidence
- CI outputs (Papermill runs, NBQA lint logs, secret scans)
- Jupytext sync verification and paired script link
- Security confirmation (no secrets, sanitized outputs)
- Archival record location with retention metadata
- Knowledge base entry or documentation link

### 5. Tailor Deliverables
Produce audience-specific outputs:
- Reviewer packet (diff highlights, validation results, decision log)
- Operational summary for downstream consumers or runbook inclusion
- Knowledge article or Confluence page summarizing insights and linking to artifacts
- Compliance bundle with audit trail (approvals, execution logs, archival receipts)

### 6. Quality Checks
- Verify notebook and paired script in sync and stored in git
- Ensure outputs sanitized and secrets absent
- Confirm approvals captured and outstanding comments resolved
- Validate archival storage meets policy and access controls applied
- Notify stakeholders and attach documentation to relevant tickets

### 7. Guardrail Verification

## Error Handling
- Missing materials: Request PR link, CI logs, archival location; include example command clarifying expectations
- Hard-stop unmet: Refuse publication until git control, execution validation, or secret removal confirmed
- Storage conflict: Direct artifacts to approved repositories per env-config guidance
- Stakeholder ambiguity: Ask for distribution list to tailor deliverables appropriately

## Examples
- **Example 1**: `/document-notebook Package feature exploration notebook for production handoff`
- **Example 2**: `/document-notebook Archive collaborative fraud analysis session with approvals`
- **Example 3**: `/document-notebook Create knowledge base entry for churn experiment notebook`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/notebook-collaboration-coach/templates/env-config.yaml`
