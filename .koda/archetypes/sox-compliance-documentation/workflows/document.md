---
description: Generate audit-ready SOX compliance documentation package (SOX Compliance)
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
// turbo
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype sox-compliance --json` and parse for ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- Read `${ARCHETYPES_BASEDIR}/sox-compliance/sox-compliance-constitution.md` for documentation requirements
- Identify required artifacts per interface

### 3. Parse Input
Extract from $ARGUMENTS: release scope, interfaces, evidence locations, audit requirements. Request clarification if incomplete.

### 4. Generate Release Attestation Document
Create release attestation summary:
- Release identifier and date
- Components included
- CR/CANA references
- Traceability summary
- Security attestation decision (Go/No-Go)

### 5. Generate Traceability Report
Document end-to-end traceability:
- Commit list with iTrack references
- iTrack tickets with CR/CANA mapping
- Bidirectional verification results
- Any exceptions with documentation

### 6. Generate SAST Coverage Report
Document security testing:
- Component list with SAST status
- Veracode scan results summary
- High-severity findings (should be 0)
- Remediation actions taken

### 7. Generate Branch Hygiene Report
Document release branch integrity:
- Commits included in release
- Out-of-scope commits reverted
- EM tickets for post-pre-deployment changes
- Cherry-pick/revert validation

### 8. Generate Security Compliance Report
Document security controls:
- Secrets scanning results
- Logger compliance (no PCI/RPI/SPI)
- Configuration review results
- Remediation actions

### 9. Generate Work Item Status Report
Document release readiness:
- User Stories status (Accepted)
- Non-US items status (Test Complete)
- Test plan/results attestation
- Product acceptance documentation

### 10. Generate Interface Evidence Package
Per interface, document:
- Producer logic evidence (code/config)
- Consumer logic evidence (code/config)
- Flow execution evidence (Prod/Non-Prod)
- Timestamps on captures
- Change integrity evidence
- Parity proof (if Non-Prod used)
- Traceability chain

### 11. Generate Audit Summary
Create executive summary for auditors:
- Release overview
- Compliance status per category
- Evidence artifacts index
- Attestation signatures required
- Go/No-Go decision with rationale

### 12. Package Documentation
// turbo
Assemble documentation package. Generate index/table of contents. Report completion.

## Error Handling
**Missing Evidence**: Flag gaps and request collection.
**Incomplete Attestation**: Block until all requirements met.

## Examples
**Example 1**: `/document-sox-compliance Generate attestation package for REL-2025.02` - Output: Complete audit-ready documentation
**Example 2**: `/document-sox-compliance Create interface evidence doc for OCE-to-Telegence` - Output: Interface-specific evidence package

## References
- SOX Compliance Constitution: `${ARCHETYPES_BASEDIR}/sox-compliance/sox-compliance-constitution.md`
- Wiki: https://wiki.web.att.com/pages/viewpage.action?pageId=2524256762
