---
description: Improve and optimize existing Graph Data Scientist code and configuration (Graph Data Scientist)
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

### 3. Audit Current Implementation
Review existing GDS pipelines for:
- Undocumented or stale named graph projections
- Algorithm parameters lacking justification comments
- Results write-back strategy inconsistencies
- Missing `gds.<algo>.estimate()` calls before algorithm execution
- Experiment tracking gaps (no parameter/result logging)
- Missing baseline comparison for new algorithm runs

### 4. Refactor Projections
- Consolidate overlapping projections into shared named graphs
- Add documentation block to each projection: labels, relationship types, properties, orientation
- Remove projections that are no longer referenced
- Add `gds.<algo>.estimate()` guard before each algorithm call

### 5. Refactor Algorithm Scripts
- Add header comment per script: `/* Algorithm: <name> | Purpose: <business question> | Chosen over: <alternatives> */`
- Extract hardcoded parameters to configuration variables
- Replace direct `gds.<algo>.write()` with `gds.<algo>.stream()` + validated write where result inspection is needed
- Add result validation step (node count, score range check) after each write-back

### 6. Improve Experiment Tracking
- Add structured log entry per run: algorithm name, parameters, node count, execution time, result summary
- Add baseline comparison block comparing new results against previous run or defined benchmark

### 7. Validate After Refactor
- Re-run all algorithms and confirm results match pre-refactor baseline within acceptable tolerance
- Verify all projections have documentation blocks
- Confirm `estimate()` guard exists before each algorithm call

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `refactor-graph-data-scientist "Consolidate duplicate graph projections across pipeline scripts"`
2. `refactor-graph-data-scientist "Add experiment tracking to PageRank and Louvain community detection pipelines"`
3. `refactor-graph-data-scientist "Extract hardcoded GDS algorithm parameters to configuration variables"`

## References

- [graph-data-scientist-constitution.md](${ARCHETYPES_BASEDIR}/graph-data-scientist/graph-data-scientist-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/graph-data-scientist/templates/env-config.yaml)
