---
description: Initialize a new Knowledge Graph Builder project with required structure and configuration (Knowledge Graph Builder)
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

### 3. Parse Input
Extract from $ARGUMENTS: domain description, data sources, expected node/relationship types, target graph database, integration endpoints. Request missing context.

### 4. Validate Constraints
Apply hard-stop checks:
- ✘ Reject if no organizing principle defined
- ✘ Block schema-less graph creation
- ✘ Require connection config via env vars
- ✘ Demand rollback strategy for bulk loads

### 5. Generate Graph Model
Produce `docs/GRAPH_MODEL.md` with:
- Node labels and properties
- Relationship types and properties
- Uniqueness constraints and indexes
- Mermaid entity diagram
- Sample Cypher queries

### 6. Scaffold Loading Pipeline
Generate data loading scripts:
- Schema migration script (constraints, indexes)
- LOAD CSV or bulk import script
- Validation queries to check loaded data
- `templates/env-config.yaml` with connection settings

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `scaffold-knowledge-graph-builder "Set up a new knowledge graph project"`
2. `scaffold-knowledge-graph-builder "Review existing implementation for best practices"`

## References

- [knowledge-graph-builder-constitution.md](${ARCHETYPES_BASEDIR}/knowledge-graph-builder/knowledge-graph-builder-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/knowledge-graph-builder/templates/env-config.yaml)
