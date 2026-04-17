---
description: Validate security evidence artifacts exist and meet minimum shape
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

### 1. Load Configuration
- Read `${ARCHETYPES_BASEDIR}/security-guardian/security-guardian-constitution.md` for guardrails and required artifacts

### 2. Run Automated Validator
- Run `${ARCHETYPES_BASEDIR}/security-guardian/scripts/validate-security-guardian.py --path <repo-root>` (from $ARGUMENTS or current directory)
- Confirm exit code is 0 (success)
- If validator fails, list all reported gaps before proceeding

### 3. Verify All 7 Evidence Artifacts Exist and Are Non-Empty
Confirm each file exists under `security/evidence/` and contains no empty placeholders:
- `security-requirements.md` — project name, compliance framework, owner
- `risk-profile.md` — risk register with owner and review date on each entry
- `threat-model.md` — assets, threats, mitigations, residual risk
- `secure-by-default-checklist.md` — all items marked met/not-met with evidence
- `security-test-matrix.md` — test categories, cadence, ownership, evidence location
- `vulnerability-management.md` — SLA tiers, scanning tools, escalation path
- `security-metrics.md` — metric definitions, targets, current values

### 4. Verify Security Test Matrix Completeness
Open `security/evidence/security-test-matrix.md` and confirm:
- All test categories are represented (SAST, DAST, dependency scan, secrets scan, pen test)
- Each row has: cadence, owner (named individual), evidence location
- Evidence locations are valid and point to existing artifacts

### 5. Verify Risk Profile Currency
- Confirm `security/evidence/risk-profile.md` review date is within the defined cadence
- Check all open exceptions have: owner, expiry date, compensating controls, approval record
- Verify no exception has expired without renewal or resolution

### 6. Verify Secure-by-Default Checklist
- Confirm all items in `security/evidence/secure-by-default-checklist.md` are explicitly met or documented as exceptions
- Check log/telemetry redaction rules are present for PII/sensitive fields

## Error Handling

- If constitution file is missing, halt and report.
- If validator is not found at `scripts/validate-security-guardian.py`, halt and report path.
- Log each validation failure with artifact name and specific missing field.

## Examples

1. `test-security-guardian "Validate security evidence pack for payments-api pre-release"`
2. `test-security-guardian "Check security evidence completeness for Q2 compliance audit"`
3. `test-security-guardian "Verify all security test matrix entries have owners and evidence locations"`

## References

- [security-guardian-constitution.md](${ARCHETYPES_BASEDIR}/security-guardian/security-guardian-constitution.md)
- [templates/](${ARCHETYPES_BASEDIR}/security-guardian/templates/)
