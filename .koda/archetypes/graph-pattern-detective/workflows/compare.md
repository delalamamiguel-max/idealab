---
description: Compare two Graph Pattern Detective implementations or approaches (Graph Pattern Detective)
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
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype graph-pattern-detective --json ` and confirm ENV_VALID. Halt if false.

### 2. Load Configuration
- Read `${ARCHETYPES_BASEDIR}/graph-pattern-detective/graph-pattern-detective-constitution.md` for guardrails and required artifacts
- Load `${ARCHETYPES_BASEDIR}/graph-pattern-detective/templates/env-config.yaml` for tool versions and configuration

### 3. Parse Comparison Request
Extract from $ARGUMENTS:
- Comparison type: detection approaches, risk scoring models, traversal strategies, alert architectures, or full implementations
- Candidate A and Candidate B descriptions
- Evaluation criteria: detection accuracy, performance, false positive rate, operational overhead

### 4. Build Comparison Matrix
For each candidate evaluate:
- **Detection accuracy**: precision and recall against labeled test events
- **Traversal efficiency**: query execution time and memory use at production graph scale
- **False positive rate**: ratio of flagged vs confirmed anomalies against baseline
- **Risk score quality**: correlation of assigned scores with actual incident severity
- **Alert latency**: time from pattern occurrence to alert delivery
- **Constitution compliance**: baseline definitions, depth limits, confidence levels, alert channels all present

### 5. Apply Domain-Specific Criteria
- **Fraud detection**: prioritise recall (catch more fraud) over precision
- **Dependency vulnerability**: prioritise blast radius accuracy
- **Real-time alerting**: prioritise latency and scalability
- **Compliance monitoring**: prioritise audit trail completeness

### 6. Produce Recommendation
- Select preferred approach with constitution-backed justification
- Summarise trade-offs between detection accuracy and operational cost
- Recommend parameter tuning for chosen approach

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `compare-graph-pattern-detective "Cypher subgraph matching vs GDS similarity for fraud ring detection"`
2. `compare-graph-pattern-detective "Real-time streaming pattern detection vs batch scanning for compliance monitoring"`
3. `compare-graph-pattern-detective "Rule-based risk scoring vs ML-based risk scoring for anomaly detection"`

## References

- [graph-pattern-detective-constitution.md](${ARCHETYPES_BASEDIR}/graph-pattern-detective/graph-pattern-detective-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/graph-pattern-detective/templates/env-config.yaml)
