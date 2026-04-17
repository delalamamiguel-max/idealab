---
description: Analyse and resolve issues in a Graph Pattern Detective implementation (Graph Pattern Detective)
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

### 3. Identify Issue Category
Classify from $ARGUMENTS:
- **Pattern not detected**: known pattern query returning empty results
- **Traversal OOM/timeout**: unbounded traversal exceeding depth or memory limits
- **Alert not firing**: detected pattern not triggering configured alert channel
- **False positives**: pattern flagged incorrectly against baseline
- **Dependency analysis failure**: blast radius calculation incorrect or missing version info

### 4. Diagnose Root Cause

**Pattern not detected:**
- Verify pattern Cypher query against `docs/PATTERN_CATALOG.md`
- Check that baseline definition exists and sample data matches expected node/relationship structure
- Confirm temporal filters are not excluding current data

**Traversal OOM/timeout:**
- Inspect all traversal queries for missing depth bounds (`*` vs `*1..5`)
- Check `EXPLAIN` / `PROFILE` on the Cypher query to identify full scans
- Add explicit depth limit and re-run

**Alert not firing:**
- Verify risk score of detected pattern exceeds configured threshold
- Check alert channel configuration (webhook URL, message format, credentials)
- Confirm alert suppression rules are not blocking the notification

**False positives:**
- Review baseline statistical definition against current graph metrics
- Check confidence level calculation and threshold — lower confidence should not trigger alerts
- Update baseline if graph structure has legitimately changed

**Dependency analysis failure:**
- Confirm version properties are present on all dependency nodes
- Re-run impact radius query: count downstream entities from root node
- Verify traversal includes all relevant relationship types

### 5. Apply Fix and Verify
- Apply targeted fix for identified root cause
- Re-run pattern detection query and confirm correct result
- Log resolution with step number, root cause, and fix applied

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `debug-graph-pattern-detective "Fraud pattern query returning no results despite known fraud records existing"`
2. `debug-graph-pattern-detective "Traversal timeout on dependency impact analysis for package update"`
3. `debug-graph-pattern-detective "Risk alert not firing when pattern confidence exceeds threshold"`

## References

- [graph-pattern-detective-constitution.md](${ARCHETYPES_BASEDIR}/graph-pattern-detective/graph-pattern-detective-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/graph-pattern-detective/templates/env-config.yaml)
