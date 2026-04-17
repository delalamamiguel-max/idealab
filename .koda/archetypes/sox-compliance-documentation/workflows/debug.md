---
description: Diagnose SOX compliance failures and provide remediation paths (SOX Compliance)
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
- Read `${ARCHETYPES_BASEDIR}/sox-compliance/sox-compliance-constitution.md` for validation rules
- Identify hard-stop rules and escalation triggers

### 3. Parse Input
Extract from $ARGUMENTS: failure type, affected commits/tickets, error messages, evidence gaps. Request clarification if incomplete.

### 4. Diagnose Traceability Failures
If traceability issue:
- Identify commits without iTrack references
- Check commit message format/convention
- Verify iTrack ticket exists and is valid
- Verify CR/CANA linkage in iTrack
- Remediation: Add proper commit references, link tickets to CR

### 5. Diagnose Commit Integrity Failures
If commit integrity issue:
- Identify Fix Version mismatches
- Identify Status mismatches (not Accepted/Test Complete)
- Identify invalid or closed CR references
- Identify out-of-scope commits
- Remediation: Update ticket Fix Version, move to correct status, revert out-of-scope commits

### 6. Diagnose SAST Failures
If SAST coverage issue:
- Identify components without SAST scan
- Identify components with failing SAST
- Identify high-severity open findings
- Remediation: Run SAST scans, fix findings, or exclude from release

### 7. Diagnose Release Branch Issues
If branch hygiene issue:
- Identify future release commits in branch
- Identify missing EM tickets for post-pre-deployment changes
- Remediation: Revert commits, create EM ticket, cherry-pick correctly

### 8. Diagnose Security Failures
If secrets/logging issue:
- Identify exposed secrets (location, type)
- Identify PCI/RPI/SPI in logs
- Remediation: Remove secrets, use secure vault, mask sensitive data in logs

### 9. Diagnose Work Item Status Failures
If status issue:
- Identify US not in Accepted status
- Identify Non-US not in Test Complete status
- Remediation: Complete testing, update status, obtain acceptance

### 10. Diagnose Evidence Gaps
If interface evidence issue:
- Identify missing producer/consumer evidence
- Identify missing flow execution evidence
- Identify missing timestamps or parity proof
- Remediation: Collect required evidence, capture new screenshots with timestamps

### 11. Generate Remediation Plan
Create prioritized remediation plan:
- Critical (hard-stop violations): Immediate action required
- High (escalation triggers): Action before release
- Medium (gaps): Address before attestation

### 12. Report Findings
// turbo
Generate debug report with: root cause, affected items, remediation steps, timeline.

## Error Handling
**Multiple Failures**: Prioritize by severity (hard-stop first).
**Unclear Root Cause**: Request additional context from user.

## Examples
**Example 1**: `/debug-sox-compliance SAST coverage failing for oce-enrichmentms` - Output: SAST diagnosis with remediation steps
**Example 2**: `/debug-sox-compliance Commits missing iTrack references` - Output: Traceability fix guide

## References
- SOX Compliance Constitution: `${ARCHETYPES_BASEDIR}/sox-compliance/sox-compliance-constitution.md`
- Wiki: https://wiki.web.att.com/pages/viewpage.action?pageId=2524256762
