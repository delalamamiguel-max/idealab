---
description: Validate a Graph Pattern Detective implementation for correctness and best practices (Graph Pattern Detective)
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

### 3. Validate Pattern Catalog
- Confirm `docs/PATTERN_CATALOG.md` exists and is non-empty
- Verify each entry contains: pattern name, Cypher query, business meaning, risk score, recommended action
- Check no entries reference undocumented baseline definitions

### 4. Validate Traversal Depth Limits
- Scan all pattern Cypher queries for unbounded traversals (`*` without depth bounds)
- Flag any query using `*` without `*<min>..<max>` syntax
- Verify depth choices are documented with a rationale comment

### 5. Validate Risk Scoring and Confidence
- Run each pattern query against test data and confirm risk score is attached to each result
- Verify confidence levels are computed for each detection
- Confirm only detections above the threshold trigger alerts

### 6. Validate Baseline Definitions
- For each pattern, confirm a statistical baseline exists: node degree, relationship frequency, temporal window
- Run baseline measurement queries and verify they return data
- Check baseline refresh schedule is configured

### 7. Validate Alert Configuration
- Confirm each pattern with risk score above threshold has an associated alert channel
- Test alert delivery for at least one pattern using a synthetic detection event
- Verify silent alert suppression requires explicit justification in code

### 8. Constitution Hard-Stop Compliance
- ✘ No pattern flagged without baseline and confidence level — verify all detections include these
- ✘ No unbounded traversals — verify all queries have explicit depth limits
- ✘ No silent alerts above threshold — verify alert channels are configured
- ✘ No dependency analysis without version info — verify version properties on all dependency nodes

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `test-graph-pattern-detective "Validate fraud detection patterns against constitution compliance rules"`
2. `test-graph-pattern-detective "Check all traversal queries have explicit depth limits"`
3. `test-graph-pattern-detective "Verify risk alert configuration fires correctly for high-risk patterns"`

## References

- [graph-pattern-detective-constitution.md](${ARCHETYPES_BASEDIR}/graph-pattern-detective/graph-pattern-detective-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/graph-pattern-detective/templates/env-config.yaml)
