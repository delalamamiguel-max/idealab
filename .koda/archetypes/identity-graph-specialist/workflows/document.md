---
description: Generate documentation for a Identity Graph Specialist project (Identity Graph Specialist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Set ARCHETYPES_BASEDIR [⋯]
 
**SUCCESS CRITERIA**:
- Search for directory: "00-core-orchestration"
- Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory
 
**HALT IF**:
- Directory "00-core-orchestration" is not found
- `${ARCHETYPES_BASEDIR}` is not set (workflow will halt if this variable is not present in the environment)
 
// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype identity-graph-specialist --json ` and confirm ENV_VALID. Halt if false.

### 2. Load Configuration
- Read `${ARCHETYPES_BASEDIR}/identity-graph-specialist/identity-graph-specialist-constitution.md` for guardrails and required artifacts
- Load `${ARCHETYPES_BASEDIR}/identity-graph-specialist/templates/env-config.yaml` for tool versions and configuration

### 3. Inventory Identity Graph Assets
Enumerate from the codebase:
- All source system connectors and entity types ingested
- All blocking key definitions
- All similarity measure configurations
- All confidence tier thresholds
- All survivorship rules
- All access control policies

### 4. Document Match Strategy
Ensure `docs/MATCH_STRATEGY.md` contains:
- Source systems and their entity types
- Blocking key definitions with rationale for each
- Similarity measures used (Jaccard, Cosine, Levenshtein, etc.) and their normalisation
- Composite confidence score formula
- Confidence tier thresholds: Exact / High / Medium / Low with acceptance criteria
- Survivorship rules with source system precedence per field

### 5. Document PII Inventory and Protection
- List all PII fields across node labels and relationship types
- Document encryption method applied to each PII field
- Document masking rules for each external data path (API, export, reporting)
- Include access control matrix: role → permitted operations per node label

### 6. Document Golden Record Schema
- Golden record node label and all properties
- Source record → golden record relationship types
- Audit trail relationship structure (created_by, updated_by, merged_from)
- Retention policy: window duration and archival/deletion process

### 7. Document Data Governance
- Data lineage: source → blocking → matching → golden record flow diagram
- Retention schedule per record type
- Audit trail access procedure for compliance reviews

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `document-identity-graph-specialist "Generate complete match strategy documentation for customer MDM system"`
2. `document-identity-graph-specialist "Document PII inventory and protection controls for healthcare identity graph"`
3. `document-identity-graph-specialist "Create data governance documentation including retention policy and audit trail"`

## References

- [identity-graph-specialist-constitution.md](${ARCHETYPES_BASEDIR}/identity-graph-specialist/identity-graph-specialist-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/identity-graph-specialist/templates/env-config.yaml)
