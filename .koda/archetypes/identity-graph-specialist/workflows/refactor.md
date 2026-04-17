---
description: Improve and optimize existing Identity Graph Specialist code and configuration (Identity Graph Specialist)
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

### 3. Audit Current Implementation
Review against constitution for:
- PII fields stored without encryption or masking strategy
- Missing or incomplete access control matrix
- Blocking keys that are too broad (causing excessive comparisons) or too narrow (missing matches)
- Hardcoded similarity thresholds lacking documented justification
- Missing or stale retention policy for identity records
- `docs/MATCH_STRATEGY.md` absent or outdated

### 4. Harden PII Protection
- Inventory all node/relationship properties containing PII (name, SSN, email, DOB, address)
- Enforce encryption-at-rest for each PII field
- Add masking to all API response paths that return identity data
- Update access control matrix to reflect minimum required privilege per role

### 5. Improve Matching Pipeline
- Refactor blocking keys to balance recall and precision — document rationale for each key
- Normalise all similarity measures to 0–1 scale before combining into composite score
- Extract hardcoded thresholds to `docs/MATCH_STRATEGY.md` with business justification
- Add confidence tier labels (Exact / High / Medium / Low) to all match results

### 6. Strengthen Survivorship Rules
- Define explicit precedence order for each conflicting field per source system
- Encode survivorship rules in versioned configuration
- Add audit trail entry for every golden record merge/update operation

### 7. Enforce Retention Policy
- Define retention window for source records and match results in `docs/MATCH_STRATEGY.md`
- Implement automated deletion or archival job for records beyond retention window
- Confirm deletion is verifiable via audit log

### 8. Validate After Refactor
- Re-run matching pipeline on benchmark dataset and confirm precision/recall metrics
- Verify PII fields are encrypted and masked in all output paths
- Confirm access control matrix is applied correctly

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `refactor-identity-graph-specialist "Strengthen PII protection across all identity graph node properties"`
2. `refactor-identity-graph-specialist "Refactor blocking keys to improve matching recall without sacrificing precision"`
3. `refactor-identity-graph-specialist "Add confidence tier labels and survivorship audit trail to matching pipeline"`

## References

- [identity-graph-specialist-constitution.md](${ARCHETYPES_BASEDIR}/identity-graph-specialist/identity-graph-specialist-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/identity-graph-specialist/templates/env-config.yaml)
