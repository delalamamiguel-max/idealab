---
description: Validate a Identity Graph Specialist implementation for correctness and best practices (Identity Graph Specialist)
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

### 3. Validate PII Protection
- Scan all node/relationship properties for PII fields (name, email, SSN, DOB, address)
- Verify encryption-at-rest is configured for each PII field
- Confirm masking is applied in all query result paths before data leaves the graph layer
- Check access control matrix exists and is enforced on identity node labels

### 4. Validate Matching Pipeline
- Confirm `docs/MATCH_STRATEGY.md` exists and contains: blocking keys, similarity measures, threshold values, confidence tiers
- Run benchmark record pairs through the pipeline and verify precision/recall meet defined targets
- Verify every match result carries a confidence tier label (Exact / High / Medium / Low)
- Confirm no match is marked as resolved without a confidence score

### 5. Validate Golden Record Integrity
- Select 10 representative golden records and verify all required properties are populated
- Check survivorship rules produce deterministic output for conflicting source records
- Confirm audit trail entry exists for each golden record creation and update

### 6. Validate Retention Policy
- Verify retention window is defined in `docs/MATCH_STRATEGY.md`
- Confirm automated deletion/archival job is scheduled and operational
- Spot-check that records beyond retention window are absent from the graph

### 7. Constitution Hard-Stop Compliance
- ✘ No PII without protection — verify encryption and masking on all PII fields
- ✘ No unscored matches — verify confidence tier present on all match results
- ✘ No unprotected access — verify RBAC on identity and golden record labels
- ✘ No indefinite retention — verify retention policy is defined and enforced

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `test-identity-graph-specialist "Validate PII protection and access controls across identity graph"`
2. `test-identity-graph-specialist "Verify matching pipeline precision/recall against benchmark dataset"`
3. `test-identity-graph-specialist "Check all match results carry confidence tier labels and survivorship audit trail"`

## References

- [identity-graph-specialist-constitution.md](${ARCHETYPES_BASEDIR}/identity-graph-specialist/identity-graph-specialist-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/identity-graph-specialist/templates/env-config.yaml)
