---
description: Produce feature documentation packets with contracts, lineage, and steward-ready summaries (Feature Architect)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype feature-architect --json ` and confirm ENV_VALID. Stop if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/feature-architect/templates/env-config.yaml` for templates, storage locations, and glossary links

### 3. Parse Input
Extract from $ARGUMENTS: feature set name, audience (data scientists, stewards, auditors), required artifacts (contract, quality report, lineage), release cadence, confidentiality tags. Request feature store entry and test outputs if absent.

### 4. Assemble Core Artifacts
Ensure package includes:
- Feature contract detailing types, ranges, owner, purpose, KPIs, TTL
- Source validation summary and freshness SLA evidence
- Temporal integrity explanation (join patterns, leakage prevention)
- Quality test results and skew monitoring status
- Privacy controls documentation (hashing/tokenization proofs)
- Feature store registration metadata with version history
- Lineage graph or Purview export showing dependencies
- Unit test and CI pipeline status, including links to Azure DevOps runs

### 5. Format Deliverables
Produce tailored outputs:
- Steward review packet (contract, quality metrics, lineage screenshots)
- Consumer quick-start guide (how to query, feature importance references)
- Governance archive (PDF/HTML complete dossier stored in MLflow/artifact repo)
- Business glossary update referencing KPIs and domain definitions

### 6. Compliance Checks
- Verify documentation excludes raw PII and sensitive values
- Ensure accessibility (alt text, contrast) in visuals
- Confirm storage in governed repository with retention metadata
- Notify owners and subscribers of new/updated feature release

### 7. Guardrail Validation

## Error Handling
- Missing evidence: Request quality reports, lineage exports, feature store IDs; provide sample command listing required inputs
- Hard-stop unmet: Refuse documentation until contracts, privacy controls, or versioning restored
- Storage conflict: Redirect to approved artifact repositories per env-config guidance
- Audience mismatch: Ask for targeted recipients to tailor messaging appropriately

## Examples
- **Example 1**: `/document-feature Publish steward dossier for churn aggregation features`
- **Example 2**: `/document-feature Create consumer guide for real-time fraud features`
- **Example 3**: `/document-feature Archive quality and lineage proof for marketing propensity features`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/feature-architect/templates/env-config.yaml`
