---
description: Improve and optimize existing Graph Pattern Detective code and configuration (Graph Pattern Detective)
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

### 3. Audit Pattern Catalog
Review `docs/PATTERN_CATALOG.md` for:
- Patterns missing Cypher queries, business meaning, risk score, or recommended action
- Undocumented patterns present in code but absent from the catalog
- Stale patterns no longer relevant to the domain
- Traversal queries using unbounded depth (`*` without limits)

### 4. Enforce Traversal Depth Limits
- Scan all Cypher queries for `*` without explicit bounds
- Replace `*` with `*1..<n>` where `<n>` is the maximum meaningful depth for that pattern
- Add a comment explaining the depth choice for each query

### 5. Improve Risk Scoring Model
- Verify numerical risk scores use documented criteria: severity, frequency, blast radius
- Standardise score range (e.g., 0–100) across all patterns
- Add temporal decay to risk scores for patterns that become less likely over time
- Ensure confidence levels are computed and attached to each detection result

### 6. Strengthen Baseline Definitions
- For each pattern, define statistical baselines: node degree distribution, relationship frequency, temporal window
- Encode baselines in parameterised Cypher queries rather than hardcoded thresholds
- Add scheduled refresh of baseline metrics

### 7. Validate After Refactor
- Re-run all pattern queries and confirm detections match expected test cases
- Verify all traversals include explicit depth bounds
- Confirm pattern catalog is complete and up-to-date

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `refactor-graph-pattern-detective "Add depth limits to all unbounded traversal queries in fraud detection patterns"`
2. `refactor-graph-pattern-detective "Standardise risk scoring model across all pattern types"`
3. `refactor-graph-pattern-detective "Update pattern catalog with missing business meanings and recommended actions"`

## References

- [graph-pattern-detective-constitution.md](${ARCHETYPES_BASEDIR}/graph-pattern-detective/graph-pattern-detective-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/graph-pattern-detective/templates/env-config.yaml)
