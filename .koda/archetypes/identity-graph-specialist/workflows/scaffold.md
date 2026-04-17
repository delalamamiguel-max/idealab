---
description: Initialize a new Identity Graph Specialist project with required structure and configuration (Identity Graph Specialist)
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
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype identity-graph-specialist --json ` and confirm ENV_VALID. Halt if false.

### 2. Load Configuration
- Read `${ARCHETYPES_BASEDIR}/identity-graph-specialist/identity-graph-specialist-constitution.md` for guardrails and required artifacts
- Load `${ARCHETYPES_BASEDIR}/identity-graph-specialist/templates/env-config.yaml` for tool versions and configuration

### 3. Parse Input
Extract from $ARGUMENTS: source systems, entity types, PII classification, match rules, confidence thresholds, governance requirements.

### 4. Validate Privacy Controls
- ✘ Reject if PII fields lack encryption/masking plan
- ✘ Require access control matrix
- ✘ Demand retention policy for identity records

### 5. Generate Identity Model
Produce:
- Identity graph schema (source records → match → golden record)
- Blocking key definitions
- Similarity measure configuration
- Confidence tier thresholds
- `docs/MATCH_STRATEGY.md`

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `scaffold-identity-graph-specialist "Set up a new knowledge graph project"`
2. `scaffold-identity-graph-specialist "Review existing implementation for best practices"`

## References

- [identity-graph-specialist-constitution.md](${ARCHETYPES_BASEDIR}/identity-graph-specialist/identity-graph-specialist-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/identity-graph-specialist/templates/env-config.yaml)
