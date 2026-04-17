---
description: Initialize a new Graph Pattern Detective project with required structure and configuration (Graph Pattern Detective)
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
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype graph-pattern-detective --json ` and confirm ENV_VALID. Halt if false.

### 2. Load Configuration
- Read `${ARCHETYPES_BASEDIR}/graph-pattern-detective/graph-pattern-detective-constitution.md` for guardrails and required artifacts
- Load `${ARCHETYPES_BASEDIR}/graph-pattern-detective/templates/env-config.yaml` for tool versions and configuration

### 3. Parse Input
Extract from $ARGUMENTS: domain, known patterns to detect, data sources, risk thresholds, alert channels, traversal depth limits.

### 4. Validate Constraints
- ✘ Reject unbounded traversals
- ✘ Require baseline definitions
- ✘ Demand alert channel configuration
- ✘ Check depth limits on all Cypher patterns

### 5. Generate Pattern Detection Framework
Produce:
- `docs/PATTERN_CATALOG.md` with initial patterns
- Cypher queries for each pattern
- Alert configuration
- Risk scoring model
- Baseline measurement queries

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `scaffold-graph-pattern-detective "Set up a new knowledge graph project"`
2. `scaffold-graph-pattern-detective "Review existing implementation for best practices"`

## References

- [graph-pattern-detective-constitution.md](${ARCHETYPES_BASEDIR}/graph-pattern-detective/graph-pattern-detective-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/graph-pattern-detective/templates/env-config.yaml)
