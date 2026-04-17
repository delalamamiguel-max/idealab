---
description: Compare two Graph Data Scientist implementations or approaches (Graph Data Scientist)
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

### 3. Parse Comparison Request
Extract from $ARGUMENTS:
- Comparison type: algorithms, embedding methods, community detection approaches, pathfinding strategies, or full pipeline implementations
- Candidate A and Candidate B descriptions
- Evaluation criteria: accuracy, performance, memory usage, interpretability, business fit

### 4. Build Comparison Matrix
For each candidate evaluate:
- **Algorithm fit**: suitability for the stated business question
- **Memory profile**: estimated heap via `gds.<algo>.estimate()` on representative data
- **Execution time**: expected runtime at target data scale
- **Result quality**: precision of centrality/community/embedding output
- **Constitution compliance**: projection documentation, estimate calls, experiment tracking present
- **Baseline availability**: prior run results available for drift detection

### 5. Apply Decision Logic from Constitution
- **Centrality**: PageRank (influence) vs Betweenness (bridges) vs Degree (connectivity)
- **Community**: Louvain (modularity) vs Leiden (quality) vs Label Propagation (speed)
- **Embeddings**: FastRP (speed) vs node2vec (quality) vs GraphSAGE (inductive)
- **Similarity**: Jaccard (set overlap) vs Cosine (continuous) vs Overlap (hierarchical)
- **Pathfinding**: Dijkstra (weighted) vs A* (geographic) vs BFS (unweighted)

### 6. Produce Recommendation
- Select preferred approach with constitution-backed justification
- Summarise memory and performance trade-offs
- Provide suggested parameter starting points for the winner

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `compare-graph-data-scientist "Louvain vs Leiden for community detection on a citation graph"`
2. `compare-graph-data-scientist "FastRP vs node2vec for link prediction downstream task"`
3. `compare-graph-data-scientist "PageRank vs Betweenness Centrality for identifying key suppliers in supply chain graph"`

## References

- [graph-data-scientist-constitution.md](${ARCHETYPES_BASEDIR}/graph-data-scientist/graph-data-scientist-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/graph-data-scientist/templates/env-config.yaml)
