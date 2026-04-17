---
description: Improve and optimize existing Knowledge Graph Builder code and configuration (Knowledge Graph Builder)
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

### 3. Audit Current Implementation
Review against constitution for:
- Missing organising principle in `docs/GRAPH_MODEL.md`
- Node labels or relationship types not defined in the model
- Missing uniqueness constraints or indexes for common query patterns
- Bulk import scripts lacking rollback strategy or idempotency
- Database connection strings hardcoded instead of loaded from env vars
- Missing validation queries after data loads

### 4. Refactor Graph Model
- Update `docs/GRAPH_MODEL.md` to reflect current node labels, relationship types, properties
- Add or refine organising principle if absent (hierarchy, domain, temporal, categorical)
- Generate Mermaid entity diagram from current model
- Ensure every node label has documented required and optional properties

### 5. Harden Schema Constraints
- For each node label, verify a uniqueness constraint exists on its natural key
- Add indexes for all properties used in WHERE clauses or MATCH predicates
- Run `CALL db.constraints()` and `CALL db.indexes()` and compare against model
- Generate schema migration script for any missing constraints/indexes

### 6. Improve Loading Pipeline
- Replace hardcoded connection strings with `os.environ` or `.env` file loading
- Add idempotent MERGE-based loading (not CREATE) to prevent duplicates
- Add transaction chunking for large LOAD CSV operations (USING PERIODIC COMMIT or apoc.periodic.iterate)
- Add rollback/cleanup step invoked if any transaction fails mid-import
- Add post-load validation queries: node counts, property completeness, orphan check

### 7. Validate After Refactor
- Re-run loading pipeline on benchmark dataset and confirm node/relationship counts
- Verify all constraints and indexes are present
- Confirm no hardcoded credentials remain in code

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `refactor-knowledge-graph-builder "Add uniqueness constraints and indexes missing from production graph"`
2. `refactor-knowledge-graph-builder "Replace hardcoded Neo4j credentials with environment variable loading"`
3. `refactor-knowledge-graph-builder "Add idempotent MERGE-based loading and rollback strategy to import pipeline"`

## References

- [knowledge-graph-builder-constitution.md](${ARCHETYPES_BASEDIR}/knowledge-graph-builder/knowledge-graph-builder-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/knowledge-graph-builder/templates/env-config.yaml)
