---
description: Analyse and resolve issues in a Identity Graph Specialist implementation (Identity Graph Specialist)
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

### 3. Identify Issue Category
Classify from $ARGUMENTS:
- **Match quality**: too many false positives or missed matches between entity records
- **PII exposure**: unencrypted PII found in graph properties or logs
- **Access control failure**: unauthorised access to identity records or golden records
- **Confidence scoring error**: matches assigned incorrect confidence tier
- **Golden record inconsistency**: conflicting properties across merged records
- **Retention violation**: records retained beyond defined policy window

### 4. Diagnose Root Cause

**Match quality failures:**
- Review blocking key definitions — overly broad keys cause false positives; too narrow causes missed matches
- Inspect similarity measure configuration (Jaccard, Cosine, Levenshtein) and threshold values
- Run sample record pairs through the matching pipeline and inspect intermediate scores

**PII exposure:**
- Scan all node/relationship properties for unencrypted PII fields (name, SSN, DOB, address)
- Verify encryption-at-rest is applied: check database security config
- Audit access logs for queries returning raw PII outside authorised paths

**Access control failure:**
- Verify RBAC roles are applied to identity and golden record node labels
- Check that masking is applied before returning PII fields in API responses
- Confirm service account has minimum required privileges only

**Confidence scoring errors:**
- Inspect confidence tier thresholds in `docs/MATCH_STRATEGY.md`
- Recompute scores for failing record pairs and trace through scoring formula
- Verify all similarity measures are normalised to the same 0–1 range before combining

**Golden record inconsistency:**
- Run survivorship rules against conflicting source records
- Identify which source system wins for each conflicting field
- Re-merge the golden record and validate output

### 5. Apply Fix and Verify
- Apply targeted fix for identified root cause
- Re-run matching pipeline on affected records and confirm expected results
- Log resolution: root cause, fix applied, records verified

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `debug-identity-graph-specialist "High false positive rate in customer entity matching pipeline"`
2. `debug-identity-graph-specialist "PII fields found unencrypted in graph node properties"`
3. `debug-identity-graph-specialist "Golden record has conflicting address fields from two source systems"`

## References

- [identity-graph-specialist-constitution.md](${ARCHETYPES_BASEDIR}/identity-graph-specialist/identity-graph-specialist-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/identity-graph-specialist/templates/env-config.yaml)
