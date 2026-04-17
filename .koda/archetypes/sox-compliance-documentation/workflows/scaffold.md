---
description: Generate SOX compliance validation checklist and evidence package template (SOX Compliance)
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
- Read `${ARCHETYPES_BASEDIR}/sox-compliance/sox-compliance-constitution.md` for validation rules and hard-stop conditions
- Identify applicable validation checks based on release scope

### 3. Parse Input
Extract from $ARGUMENTS: release branch name, production baseline branch, iTrack ticket IDs, CR/CANA references, interface scope. Request clarification if incomplete.

### 4. Generate Compliance Checklist
Create comprehensive SOX compliance validation checklist:
- End-to-End Traceability (Commits → iTrack → CR/CANA)
- Code Commit Integrity (Fix Version, Status, CR scope)
- SAST Coverage (100% Veracode)
- Release Branch Hygiene (in-scope commits only)
- Logger Data Handling (no PCI/RPI/SPI)
- Credential Exposure Prevention (no secrets)
- Work Item Status Validation (Accepted/Test Complete)

### 5. Generate Evidence Package Template
Create interface integration evidence template:
- Producer logic evidence (code/config)
- Consumer logic evidence (code/config)
- Flow execution evidence (Prod ≤72h or Non-Prod + parity)
- Timestamp requirements
- Change integrity evidence
- Traceability chain (iTrack → US → CR → CANA)

### 6. Generate Validation Scripts
Create scripts/commands for:
- Commit extraction (release branch vs baseline)
- iTrack ticket validation
- SAST coverage check
- Secrets scanning
- Logger statement review

### 7. Add Recommendations
Include: audit best practices, evidence collection tips, remediation guidance, escalation triggers.

### 8. Validate and Report
// turbo
Generate checklist and evidence package template. Report completion.

## Error Handling
**Missing Release Info**: Request release branch and baseline details.
**Missing Ticket References**: Flag commits without iTrack references.

## Examples
**Example 1**: `/scaffold-sox-compliance Generate checklist for REL-2025.02 release` - Output: Complete SOX compliance checklist and evidence template
**Example 2**: `/scaffold-sox-compliance Create evidence package for OCE-to-Telegence interface` - Output: Interface-specific evidence collection template

## References
- SOX Compliance Constitution: `${ARCHETYPES_BASEDIR}/sox-compliance/sox-compliance-constitution.md`
- Wiki: https://wiki.web.att.com/pages/viewpage.action?pageId=2524256762
