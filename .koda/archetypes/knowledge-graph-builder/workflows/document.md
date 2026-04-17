---
description: Generate documentation for a Knowledge Graph Builder project (Knowledge Graph Builder)
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

### 3. Inventory Graph Assets
Enumerate from the live database and codebase:
- `CALL db.labels()` — all node labels with property lists
- `CALL db.relationshipTypes()` — all relationship types
- `CALL db.constraints()` — all uniqueness and existence constraints
- `CALL db.indexes()` — all indexes and their properties
- All loading scripts and their source systems

### 4. Generate Graph Model Document
Update or create `docs/GRAPH_MODEL.md` with:
- Organising principle: hierarchy, domain, temporal, or categorical
- Node labels table: label, properties (required/optional), natural key, description
- Relationship types table: type, source label, target label, properties, cardinality
- Uniqueness constraints and indexes per label
- Mermaid entity relationship diagram
- Sample Cypher queries for common access patterns

### 5. Document Loading Pipeline
For each loading script:
- Source system and data format
- Target node labels and relationship types
- MERGE key(s) used for idempotency
- Transaction chunk size
- Rollback/cleanup procedure on failure
- Post-load validation query and expected results

### 6. Document Configuration and Operations
- Environment variable list with descriptions (no values): `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`
- Schema migration procedure: how to add new constraints, indexes, or labels
- Backup and restore procedure
- Monitoring queries: node counts by label, relationship counts by type

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `document-knowledge-graph-builder "Generate complete graph model documentation from production Neo4j database"`
2. `document-knowledge-graph-builder "Document all loading scripts with source systems and rollback procedures"`
3. `document-knowledge-graph-builder "Create operations guide including schema migration and monitoring queries"`

## References

- [knowledge-graph-builder-constitution.md](${ARCHETYPES_BASEDIR}/knowledge-graph-builder/knowledge-graph-builder-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/knowledge-graph-builder/templates/env-config.yaml)
