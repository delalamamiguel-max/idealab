---
description: Analyse and resolve issues in a Graph Data Scientist implementation (Graph Data Scientist)
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
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype graph-data-scientist --json ` and confirm ENV_VALID. Halt if false.

### 2. Load Configuration
- Read `${ARCHETYPES_BASEDIR}/graph-data-scientist/graph-data-scientist-constitution.md` for guardrails and required artifacts
- Load `${ARCHETYPES_BASEDIR}/graph-data-scientist/templates/env-config.yaml` for tool versions and configuration

### 3. Identify Issue Category
Classify the failure from $ARGUMENTS:
- **Projection failure**: graph not found, wrong labels/relationships, missing property
- **Memory/OOM**: heap overflow during algorithm execution, missing memory estimate
- **Algorithm failure**: invalid parameters, convergence failure, unexpected results
- **Embedding quality**: poor downstream ML performance, invalid similarity scores
- **Results write-back**: write-back failed, missing node/relationship properties

### 4. Diagnose Root Cause

**Projection failures:**
- List projections: `CALL gds.graph.list() YIELD graphName, nodeCount, relationshipCount`
- Verify included labels and relationship types match the actual database schema
- Confirm projected properties exist: `CALL db.propertyKeys()`

**Memory/OOM failures:**
- Re-run `gds.<algo>.estimate()` and compare to `dbms.memory.heap.max_size`
- Drop stale projections: `CALL gds.graph.drop('<name>')`
- Consider splitting large graphs into sub-projections

**Algorithm failures:**
- Validate parameter bounds against GDS documentation
- Check graph connectivity requirements (e.g., weakly connected components first)
- Run in `stream` mode before committing to `write` or `mutate`

**Embedding quality failures:**
- Compute cosine similarity on sample node pairs to verify value range
- Check embedding dimensions and training iteration count
- Validate downstream evaluation metrics against pre-defined threshold

### 5. Apply Fix and Verify
- Apply targeted fix for the identified root cause
- Re-run algorithm with validation queries
- Log resolution: step number, root cause, parameters adjusted, result confirmation

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `debug-graph-data-scientist "Set up a new knowledge graph project"`
2. `debug-graph-data-scientist "Review existing implementation for best practices"`

## References

- [graph-data-scientist-constitution.md](${ARCHETYPES_BASEDIR}/graph-data-scientist/graph-data-scientist-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/graph-data-scientist/templates/env-config.yaml)
