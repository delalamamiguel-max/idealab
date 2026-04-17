---
description: Generate documentation for a Graph Data Scientist project (Graph Data Scientist)
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

### 3. Inventory Pipeline Components
Enumerate from the codebase:
- All named graph projections with their label/relationship/property scope
- All GDS algorithms applied with parameters and invocation mode
- All embedding models used with versions
- All results write-back targets (graph properties or export files)

### 4. Document Projections
For each named projection generate a block:
- Projection name and business purpose
- Included node labels and relationship types
- Properties projected and data types
- Orientation (NATURAL/REVERSE/UNDIRECTED)
- Memory footprint from last `estimate()` run

### 5. Document Algorithms
For each algorithm generate a block:
- Algorithm name and GDS procedure
- Business question answered
- Parameters with values and justification
- Output format: stream/mutate/write/export
- Performance metrics from last run (execution time, affected nodes)

### 6. Document Feature Pipeline (if ML downstream)
- List all graph-derived features and the algorithm that produces each
- Document feature engineering transformations applied post-algorithm
- Include evaluation metrics for downstream ML task

### 7. Compile Experiment Log
- Chronological record of algorithm runs: date, algorithm, parameters, result summary
- Baseline comparison table showing drift across runs
- Flag any result changes exceeding defined thresholds

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `document-graph-data-scientist "Generate full pipeline documentation for the fraud detection GDS pipeline"`
2. `document-graph-data-scientist "Create experiment log for all centrality algorithms run in Q1"`
3. `document-graph-data-scientist "Document feature extraction pipeline producing inputs for link prediction model"`

## References

- [graph-data-scientist-constitution.md](${ARCHETYPES_BASEDIR}/graph-data-scientist/graph-data-scientist-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/graph-data-scientist/templates/env-config.yaml)
