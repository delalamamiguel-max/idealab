---
description: Document data sourcing workflow for catalog, lineage, sampling, and PII guardrail coverage (Data Sourcing Specialist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-sourcing-specialist --json ` and parse for ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/data-sourcing-specialist/templates/env-config.yaml` for catalog/table patterns

### 3. Parse Input
Extract from $ARGUMENTS: workflow file path, documentation goals (catalog, lineage, sampling, PII). Request clarification if incomplete.

### 4. Document Workflow
Summarize:
- Guardrail coverage
- Catalog compliance
- Lineage registration
- Sampling enforcement
- PII controls
- Glossary links
- Recommendations for improvement

## Error Handling
- Missing source details: Request workflow path, steward contacts, catalog IDs; provide template snippet to complete submission
- Guardrail gaps uncovered: Document missing controls (e.g., absent sampling policy) and insert remediation tasks before publishing docs
- Tooling issues: Flag inability to reach documentation repository or metadata APIs and reference env-config remediation steps
- Audit artefact failure: Require updated lineage diagrams or approval logs when attachments fail validation checksum

## Examples
- **Example 1**: `/document-data-sourcing Publish certified view ingestion workflow` → Produces catalog-ready summary with guardrail annotations and glossary links
- **Example 2**: `/document-data-sourcing Capture audit notes for finance regulatory extract` → Generates compliance narrative, retention details, stewardship contacts
- **Example 3**: `/document-data-sourcing Create playbook entry for marketing sandbox loader` → Delivers templated doc with lineage diagram references and sampling caps

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/data-sourcing-specialist/templates/env-config.yaml`
