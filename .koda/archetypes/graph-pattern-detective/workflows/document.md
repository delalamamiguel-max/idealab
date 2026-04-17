---
description: Generate documentation for a Graph Pattern Detective project (Graph Pattern Detective)
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

### 3. Inventory Detection Assets
Enumerate from the codebase and `docs/PATTERN_CATALOG.md`:
- All defined patterns with their Cypher queries
- All alert channel configurations
- All baseline definition queries
- All risk scoring functions

### 4. Document Pattern Catalog
For each pattern ensure the catalog entry contains:
- Pattern name and unique identifier
- Cypher query with explicit depth bounds documented
- Business meaning (what real-world event does this pattern represent?)
- Risk score (0–100) with scoring criteria
- Confidence level calculation method
- Recommended action when pattern fires
- Temporal context requirements (time window, creation/modification timestamps)

### 5. Document Baseline Definitions
For each pattern baseline:
- Statistical baseline description: normal degree distribution, relationship frequency, temporal window
- Cypher query that measures the baseline
- Refresh cadence and last-refreshed timestamp
- Deviation thresholds that constitute an anomaly

### 6. Document Alert Architecture
- List all alert channels (webhook, email, ticketing system)
- Document message format and required fields per channel
- Document escalation levels: info / warning / critical thresholds
- Note any suppression rules with explicit justification

### 7. Document Dependency Impact Model
- Graph schema showing dependency node types and version properties
- Impact radius calculation query
- Blast radius reporting format

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `document-graph-pattern-detective "Generate complete pattern catalog documentation for fraud detection system"`
2. `document-graph-pattern-detective "Document alert architecture and escalation levels for compliance monitoring"`
3. `document-graph-pattern-detective "Create dependency impact model documentation for vulnerability tracking system"`

## References

- [graph-pattern-detective-constitution.md](${ARCHETYPES_BASEDIR}/graph-pattern-detective/graph-pattern-detective-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/graph-pattern-detective/templates/env-config.yaml)
