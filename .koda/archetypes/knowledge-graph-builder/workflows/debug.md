---
description: Analyse and resolve issues in a Knowledge Graph Builder implementation (Knowledge Graph Builder)
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

### 3. Identify Issue Category
Classify from $ARGUMENTS:
- **Schema violation**: nodes/relationships created without defined labels or types
- **Constraint/index failure**: uniqueness constraint violated, missing index causing slow queries
- **Bulk import failure**: LOAD CSV or import script failing mid-run, orphan data left behind
- **Data quality**: unexpected nulls, missing required properties, wrong data types
- **Query performance**: slow Cypher queries not using indexes, full graph scans
- **Connection/config**: database unreachable, credentials not loaded from env vars

### 4. Diagnose Root Cause

**Schema violations:**
- Run `CALL db.labels()` and `CALL db.relationshipTypes()` — compare against `docs/GRAPH_MODEL.md`
- Identify nodes/relationships created outside the defined schema
- Check if organising principle is defined: hierarchy, domain, temporal, or categorical

**Constraint/index failures:**
- `CALL db.constraints()` — verify all uniqueness constraints from model are present
- `CALL db.indexes()` — verify indexes exist for common query patterns
- `EXPLAIN` slow queries to confirm index usage; add missing index if needed

**Bulk import failures:**
- Check for partial imports: count nodes by label against expected counts
- Verify rollback strategy was invoked if import failed mid-run
- Re-run import script with `--dry-run` or on a test subgraph first

**Data quality issues:**
- Run property completeness queries: `MATCH (n:Label) WHERE n.requiredProp IS NULL RETURN count(n)`
- Verify data type coercions in LOAD CSV (toInteger, toFloat, date())
- Check for orphan nodes: `MATCH (n) WHERE NOT (n)--() RETURN count(n)`

**Query performance:**
- Use `PROFILE` to inspect actual plan and row counts
- Add composite index if query filters on multiple properties
- Check traversal depth and add relationship type filters

### 5. Apply Fix and Verify
- Apply targeted fix for identified root cause
- Re-run validation queries: constraint checks, property completeness, node counts
- Log resolution: root cause, fix applied, validation results

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `debug-knowledge-graph-builder "Bulk import leaving orphan nodes after failure midway through LOAD CSV"`
2. `debug-knowledge-graph-builder "Cypher query running full graph scan despite index existing on property"`
3. `debug-knowledge-graph-builder "Uniqueness constraint violation on node creation in ingestion pipeline"`

## References

- [knowledge-graph-builder-constitution.md](${ARCHETYPES_BASEDIR}/knowledge-graph-builder/knowledge-graph-builder-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/knowledge-graph-builder/templates/env-config.yaml)
