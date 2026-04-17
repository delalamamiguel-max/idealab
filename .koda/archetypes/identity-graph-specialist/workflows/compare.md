---
description: Compare two Identity Graph Specialist implementations or approaches (Identity Graph Specialist)
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

### 3. Parse Comparison Request
Extract from $ARGUMENTS:
- Comparison type: matching algorithms, similarity measures, blocking strategies, MDM platforms, or full implementations
- Candidate A and Candidate B descriptions
- Evaluation criteria: match accuracy, PII compliance, scalability, operational cost

### 4. Build Comparison Matrix
For each candidate evaluate:
- **Match precision/recall**: F1 score on benchmark labeled dataset
- **PII compliance**: encryption, masking, and access control coverage
- **Blocking efficiency**: number of candidate pairs generated vs true match pairs
- **Confidence tier quality**: correlation between assigned tier and actual match correctness
- **Golden record consistency**: deterministic survivorship under conflicting inputs
- **Scalability**: performance at 10×, 100× current record volume
- **Retention compliance**: automated enforcement of defined retention policy

### 5. Apply Domain-Specific Criteria
- **Customer MDM**: prioritise golden record quality and cross-system consistency
- **Healthcare identity**: prioritise PII protection and regulatory compliance
- **Fraud prevention**: prioritise recall (catch more duplicates) over precision
- **Data governance**: prioritise audit trail completeness and retention enforcement

### 6. Produce Recommendation
- Select preferred approach with constitution-backed justification
- Summarise compliance, accuracy, and scalability trade-offs
- Recommend configuration starting points for blocking keys and confidence thresholds

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `compare-identity-graph-specialist "Deterministic matching vs probabilistic matching for customer MDM"`
2. `compare-identity-graph-specialist "Levenshtein distance vs Jaro-Winkler similarity for name matching"`
3. `compare-identity-graph-specialist "Token blocking vs sorted neighbourhood blocking for large-scale entity resolution"`

## References

- [identity-graph-specialist-constitution.md](${ARCHETYPES_BASEDIR}/identity-graph-specialist/identity-graph-specialist-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/identity-graph-specialist/templates/env-config.yaml)
