---
description: Scaffold the security evidence pack for a project
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

### 2. Create Evidence Directory
- Create `security/evidence/` in the target repository root (from $ARGUMENTS or current directory)

### 3. Copy Template Files
Copy all 7 required templates from `${ARCHETYPES_BASEDIR}/security-guardian/templates/` into `security/evidence/`:
- `security-requirements.md`
- `risk-profile.md`
- `threat-model.md`
- `secure-by-default-checklist.md`
- `security-test-matrix.md`
- `vulnerability-management.md`
- `security-metrics.md`

### 4. Populate Evidence Pack
- Open each file and fill in all placeholders (marked `<placeholder>` or `TBD`)
- Required fields per file:
  - `security-requirements.md`: project name, compliance framework, owner
  - `risk-profile.md`: risk register entries, owner, review date
  - `threat-model.md`: assets, threats, mitigations, residual risk
  - `secure-by-default-checklist.md`: check each item as met/not-met with evidence
  - `security-test-matrix.md`: test categories, cadence, ownership, evidence location
  - `vulnerability-management.md`: SLA tiers, scanning tools, escalation path
  - `security-metrics.md`: metric definitions, targets, current values

### 5. Commit to Source Control
- Stage all files under `security/evidence/`
- Confirm no file is empty and no placeholders remain
- Commit with message: `feat(security): add security evidence pack`

## Error Handling

- If constitution file is missing, halt and report.
- If target directory cannot be created, check permissions and retry.
- If any template file is missing from `templates/`, report which file is absent.

## Examples

1. `scaffold-security-guardian "Initialize security evidence pack for payments-api service"`
2. `scaffold-security-guardian "Add security evidence pack to data-pipeline project"`
3. `scaffold-security-guardian "Bootstrap security baseline for new microservice"`

## References

- [security-guardian-constitution.md](${ARCHETYPES_BASEDIR}/security-guardian/security-guardian-constitution.md)
- [templates/](${ARCHETYPES_BASEDIR}/security-guardian/templates/)
