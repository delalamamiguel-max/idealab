---
description: Validate a Graph Data Scientist implementation for correctness and best practices (Graph Data Scientist)
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

### 3. Validate Projections
- `CALL gds.graph.list()` — confirm all expected named projections exist
- Verify each projection has a documentation block: labels, relationship types, properties, orientation
- Confirm `gds.<algo>.estimate()` is called before each algorithm invocation

### 4. Validate Algorithm Compliance
For each algorithm in the pipeline:
- Confirm memory estimate is performed and result checked before execution
- Verify algorithm parameters are documented with business justification
- Confirm results write-back strategy is declared (write/mutate/stream/export)
- Check experiment tracking log is updated after each run

### 5. Validate Embeddings (if applicable)
- Run cosine similarity on representative node pairs to confirm meaningful score range
- Confirm embedding model name and version are logged
- If used in downstream ML: verify evaluation metric meets the defined threshold in constitution

### 6. Validate Baseline Comparison
- Confirm a baseline or prior run result exists for comparison
- Check that anomalous drift (>threshold) produces an alert or log entry

### 7. Constitution Hard-Stop Compliance
- ✘ No algorithm runs without a named projection — verify none exist
- ✘ No embeddings used in downstream ML without validation — verify quality check is present
- ✘ No memory-blind execution — verify `estimate()` calls are present for each algorithm

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `test-graph-data-scientist "Validate PageRank implementation against constitution rules"`
2. `test-graph-data-scientist "Check all GDS pipelines have memory estimation and experiment tracking"`
3. `test-graph-data-scientist "Verify node2vec embeddings pass quality threshold before ML training"`

## References

- [graph-data-scientist-constitution.md](${ARCHETYPES_BASEDIR}/graph-data-scientist/graph-data-scientist-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/graph-data-scientist/templates/env-config.yaml)
