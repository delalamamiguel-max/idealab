---
description: Validate a Knowledge Graph Builder implementation for correctness and best practices (Knowledge Graph Builder)
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
Extract from $ARGUMENTS: graph database URI, expected node counts, relationship counts, query benchmarks, schema constraints list.

### 4. Schema Validation
- Verify all expected constraints exist
- Check index coverage for common query patterns
- Validate label and relationship type naming conventions

### 5. Data Integrity Tests
- Count nodes per label vs expected
- Verify no orphan nodes exist
- Check relationship cardinality against model
- Validate property completeness (no unexpected nulls)

### 6. Query Performance Tests
- Run benchmark Cypher queries
- Verify query plans use indexes
- Check traversal depth limits

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `test-knowledge-graph-builder "Set up a new knowledge graph project"`
2. `test-knowledge-graph-builder "Review existing implementation for best practices"`

## References

- [knowledge-graph-builder-constitution.md](${ARCHETYPES_BASEDIR}/knowledge-graph-builder/knowledge-graph-builder-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/knowledge-graph-builder/templates/env-config.yaml)
