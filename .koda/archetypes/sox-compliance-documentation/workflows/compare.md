---
description: Compare SOX compliance status between releases or approaches (SOX Compliance)
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
- Read `${ARCHETYPES_BASEDIR}/sox-compliance/sox-compliance-constitution.md` for comparison criteria
- Identify validation checks to compare

### 3. Parse Input
Extract from $ARGUMENTS: releases/approaches to compare, comparison scope, specific checks to focus on. Request clarification if incomplete.

### 4. Compare Traceability
Compare between releases:
- Traceability completeness (% commits with valid references)
- CR/CANA linkage coverage
- Bidirectional verification results

### 5. Compare Commit Integrity
Compare between releases:
- Fix Version accuracy rate
- Status compliance rate
- Out-of-scope commit count
- Remediation effort required

### 6. Compare SAST Coverage
Compare between releases:
- SAST coverage percentage
- High-severity findings count
- Time to remediation
- Components excluded

### 7. Compare Branch Hygiene
Compare between releases:
- Revert count
- EM ticket count for post-pre-deployment
- Cherry-pick accuracy

### 8. Compare Security Compliance
Compare between releases:
- Secrets exposure incidents
- PCI/RPI/SPI logging violations
- Remediation actions required

### 9. Compare Work Item Status
Compare between releases:
- Acceptance rate for User Stories
- Test Complete rate for Non-US
- Blocked items count

### 10. Compare Evidence Quality
Compare between releases:
- Evidence package completeness
- Timestamp coverage
- Parity proof quality (if Non-Prod used)

### 11. Generate Comparison Matrix
Create side-by-side comparison:
| Check | Release A | Release B | Delta |
|-------|-----------|-----------|-------|
| Traceability | % | % | +/- |
| SAST Coverage | % | % | +/- |
| Secrets Found | # | # | +/- |
| Evidence Complete | Y/N | Y/N | - |

### 12. Generate Recommendations
Based on comparison:
- Areas of improvement
- Regression warnings
- Best practices to adopt
- Process refinements

### 13. Report Comparison
// turbo
Generate comparison report with matrix, trends, and recommendations.

## Error Handling
**Missing Data**: Flag gaps in comparison data.
**Incompatible Releases**: Note differences in scope/methodology.

## Examples
**Example 1**: `/compare-sox-compliance Compare REL-2025.01 vs REL-2025.02` - Output: Compliance comparison matrix
**Example 2**: `/compare-sox-compliance Compare SAST coverage trend across last 3 releases` - Output: SAST trend analysis

## References
- SOX Compliance Constitution: `${ARCHETYPES_BASEDIR}/sox-compliance/sox-compliance-constitution.md`
- Wiki: https://wiki.web.att.com/pages/viewpage.action?pageId=2524256762
