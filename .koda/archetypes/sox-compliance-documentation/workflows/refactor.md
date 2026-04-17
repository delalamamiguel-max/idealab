---
description: Update evidence packages and fix compliance gaps to achieve SOX compliance (SOX Compliance)
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
- Read `${ARCHETYPES_BASEDIR}/sox-compliance/sox-compliance-constitution.md` for compliance requirements
- Identify current gaps from previous validation

### 3. Parse Input
Extract from $ARGUMENTS: gaps to address, evidence package location, remediation scope. Request clarification if incomplete.

### 4. Refactor Traceability
If traceability gaps:
- Update commit messages with proper iTrack references (via rebase/amend if allowed)
- Link iTrack tickets to correct CR/CANA
- Update Fix Version on tickets
- Document traceability chain

### 5. Refactor Commit Integrity
If commit integrity issues:
- Update ticket status to Accepted/Test Complete
- Revert out-of-scope commits from release branch
- Cherry-pick correct commits
- Create EM ticket for post-pre-deployment changes

### 6. Refactor SAST Coverage
If SAST gaps:
- Trigger SAST scans for missing components
- Address high-severity findings
- Document SAST pass/fail status
- Exclude unremediated components from release if necessary

### 7. Refactor Release Branch
If branch hygiene issues:
- Revert future release commits
- Ensure only in-scope work in branch
- Document all reverts/additions with EM tickets

### 8. Refactor Security Controls
If secrets/logging issues:
- Remove exposed secrets from code/config
- Move secrets to secure vault (Azure Key Vault)
- Add masking for sensitive data in loggers
- Update log configuration to exclude sensitive payloads

### 9. Refactor Work Item Status
If status issues:
- Complete required testing
- Obtain product acceptance for User Stories
- Update ticket status to required state
- Document test plan/results

### 10. Refactor Evidence Package
If evidence gaps:
- Collect missing producer/consumer logic evidence
- Capture flow execution evidence (Prod ≤72h or Non-Prod + parity)
- Add timestamps to all captures
- Document change integrity (commit metadata, deployment records)
- Complete traceability chain documentation

### 11. Validate Refactored State
Re-run validation checks to confirm:
- All traceability intact
- All commits properly linked
- SAST coverage at 100%
- No secrets exposed
- No PCI/RPI/SPI in logs
- All work items in correct status
- Evidence package complete

### 12. Report Completion
// turbo
Generate refactor report with: changes made, validation results, remaining gaps (if any).

## Error Handling
**Cannot Revert Commits**: Document exception and escalate.
**Cannot Fix SAST**: Exclude component from release with documentation.

## Examples
**Example 1**: `/refactor-sox-compliance Fix traceability gaps for SPTOCE-12345` - Output: Updated traceability with validation
**Example 2**: `/refactor-sox-compliance Complete evidence package for OCE-to-Telegence` - Output: Complete evidence package

## References
- SOX Compliance Constitution: `${ARCHETYPES_BASEDIR}/sox-compliance/sox-compliance-constitution.md`
- Wiki: https://wiki.web.att.com/pages/viewpage.action?pageId=2524256762
