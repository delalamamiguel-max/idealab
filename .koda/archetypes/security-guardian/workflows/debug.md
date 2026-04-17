---
description: Triage security gate failures and remediation workflow
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

### 2. Classify Failing Gate
Identify the gate category from $ARGUMENTS or CI failure log:
- **Secrets exposure**: hardcoded credentials, API keys, tokens found in committed code
- **Dependency risk**: CVE in dependency, SBOM not generated, unpinned versions
- **Missing evidence artifact**: one of the 7 required `security/evidence/` files absent or empty
- **Security test failure**: test category not covered, cadence missed, evidence location missing
- **Policy violation**: secure-by-default checklist item not met, missing owner or review date

### 3. Capture Evidence
Before making any changes, record:
- Failing CI log output or tool report
- Affected artifact references (file path, dependency name, CVE ID)
- Commit SHA and branch name

### 4. Apply Remediation

**Secrets exposure:**
- Remove the secret from code immediately; rotate the credential
- Add the secret path to `.gitignore` or vault configuration
- Rewrite git history if secret was committed (use `git filter-repo`)

**Dependency risk:**
- Update to the patched version; regenerate SBOM
- Pin all dependency versions in the lock file
- Document unresolvable CVEs in `security/evidence/vulnerability-management.md`

**Missing evidence artifact:**
- Run `${ARCHETYPES_BASEDIR}/security-guardian/scripts/validate-security-guardian.py --path <repo-root>` to identify gaps
- Copy missing template from `${ARCHETYPES_BASEDIR}/security-guardian/templates/` and populate required fields

**Security test failure:**
- Update `security/evidence/security-test-matrix.md` with: test category, cadence, ownership, evidence location
- Run outstanding tests and attach evidence

**Policy violation:**
- Open `security/evidence/secure-by-default-checklist.md` and address the failing item
- Update `security/evidence/risk-profile.md` with owner and review date

### 5. Document Exception (if remediation not immediately possible)
If the gate cannot be fixed immediately, record an exception in `security/evidence/risk-profile.md` with:
- Owner (named individual, not team name)
- Duration (expiry date for the exception)
- Compensating controls in place
- Approval record

### 6. Verify Gate Passes
- Re-run the failing security gate or validator
- Confirm exit code is success OR exception is recorded and approved

## Error Handling

- If constitution file is missing, halt and report.
- If `validate-security-guardian.py` is not found, check `scripts/` directory in the archetype.
- Log all remediation steps taken with before/after evidence.

## Examples

1. `debug-security-guardian "GitHub Actions secret scan failing on payments-api commit abc123"`
2. `debug-security-guardian "SBOM missing for data-pipeline service, blocking release gate"`
3. `debug-security-guardian "security-test-matrix.md missing cadence and ownership columns"`

## References

- [security-guardian-constitution.md](${ARCHETYPES_BASEDIR}/security-guardian/security-guardian-constitution.md)
- [templates/](${ARCHETYPES_BASEDIR}/security-guardian/templates/)
