---
description: Harden existing artifacts to meet the security baseline
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

### 2. Run Gap Analysis
- Run `${ARCHETYPES_BASEDIR}/security-guardian/scripts/validate-security-guardian.py --path <repo-root>` (from $ARGUMENTS or current directory)
- Record all reported gaps: missing files, empty files, unfilled placeholders

### 3. Fill Evidence Pack Gaps
For each gap identified:
- **Missing file**: copy from `${ARCHETYPES_BASEDIR}/security-guardian/templates/` and populate all required fields
- **Empty or placeholder-only file**: complete all required fields, assign owners, set review dates
- **Missing security gate/cadence**: update `security/evidence/security-test-matrix.md` with test category, cadence, ownership, evidence location
- **Missing or wrong owner**: assign a named individual (not a team) for each artifact

### 4. Remove Secrets from Committed Material
- Scan codebase for hardcoded credentials, API keys, tokens
- Remove found secrets; replace with environment variable references or vault lookups
- Rewrite git history for any previously committed secrets

### 5. Enforce Log/Telemetry Redaction
- Open `security/evidence/secure-by-default-checklist.md`
- Confirm log redaction rules are listed for all PII/sensitive fields
- Add any missing redaction rules with evidence references

### 6. Document Remaining Exceptions
For any gap that cannot be immediately resolved:
- Add entry to `security/evidence/risk-profile.md` with: owner, expiry date, compensating controls, approval record

### 7. Re-run Validator and Confirm
- Re-run `validate-security-guardian.py` and confirm all required artifacts are present and complete
- Commit updated evidence pack: `fix(security): harden evidence pack to meet security baseline`

## Error Handling

- If constitution file is missing, halt and report.
- If `validate-security-guardian.py` exits with errors, address each reported gap before re-running.
- Log all changes made with before/after evidence.

## Examples

1. `refactor-security-guardian "Harden payments-api security evidence pack for Q2 audit"`
2. `refactor-security-guardian "Remove hardcoded secrets and update secure-by-default checklist"`
3. `refactor-security-guardian "Add missing owners and review dates to all security evidence artifacts"`

## References

- [security-guardian-constitution.md](${ARCHETYPES_BASEDIR}/security-guardian/security-guardian-constitution.md)
- [templates/](${ARCHETYPES_BASEDIR}/security-guardian/templates/)
