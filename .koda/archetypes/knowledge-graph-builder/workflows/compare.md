---
description: Compare two Knowledge Graph Builder implementations or approaches (Knowledge Graph Builder)
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
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype knowledge-graph-builder --json ` and confirm ENV_VALID. Halt if false.

### 2. Load Configuration
- Read `${ARCHETYPES_BASEDIR}/knowledge-graph-builder/knowledge-graph-builder-constitution.md` for guardrails and required artifacts
- Load `${ARCHETYPES_BASEDIR}/knowledge-graph-builder/templates/env-config.yaml` for tool versions and configuration

### 3. Parse Comparison Request
Extract from $ARGUMENTS:
- Comparison type: graph data models, loading strategies, schema design approaches, graph databases, or full implementations
- Candidate A and Candidate B descriptions
- Evaluation criteria: query performance, model expressiveness, maintainability, load speed

### 4. Build Comparison Matrix
For each candidate evaluate:
- **Model completeness**: all node labels, relationship types, and properties documented in `docs/GRAPH_MODEL.md`
- **Schema integrity**: uniqueness constraints and indexes defined for all natural keys and query patterns
- **Loading strategy**: idempotency (MERGE vs CREATE), transaction chunking, rollback strategy
- **Query performance**: index coverage, traversal depth limits, EXPLAIN plan quality
- **Maintainability**: organising principle clarity, naming conventions, migration path for schema changes
- **Constitution compliance**: no schema-less graphs, no hardcoded credentials, no unvalidated bulk imports

### 5. Apply Domain-Specific Criteria
- **Enterprise knowledge graph**: prioritise model expressiveness and cross-domain linking
- **Operational graph**: prioritise query performance and index coverage
- **Data ingestion pipeline**: prioritise loading speed and idempotency
- **Compliance use case**: prioritise audit trail and retention management

### 6. Produce Recommendation
- Select preferred approach with constitution-backed justification
- Summarise schema design trade-offs and migration considerations
- Recommend indexing strategy and loading pattern for chosen approach

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `compare-knowledge-graph-builder "Property graph model vs RDF graph model for enterprise knowledge graph"`
2. `compare-knowledge-graph-builder "LOAD CSV vs apoc.load.json for heterogeneous data ingestion"`
3. `compare-knowledge-graph-builder "Single-label vs multi-label node design for product taxonomy graph"`

## References

- [knowledge-graph-builder-constitution.md](${ARCHETYPES_BASEDIR}/knowledge-graph-builder/knowledge-graph-builder-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/knowledge-graph-builder/templates/env-config.yaml)
