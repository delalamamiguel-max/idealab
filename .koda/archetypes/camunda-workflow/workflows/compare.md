---
description: Compare Camunda workflow approaches, BPMN patterns, and orchestration strategies (Camunda Orchestration)
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
// turbo
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype camunda-orchestration --json ` and parse for CAMUNDA_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- Read `${ARCHETYPES_BASEDIR}/camunda-orchestration/constitution.md` for hard-stop rules
- Load `${ARCHETYPES_BASEDIR}/camunda-orchestration/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: orchestration problem or pattern choice, comparison criteria (scalability, complexity, maintainability, testability), workflow characteristics, constraints. Request clarification if incomplete.

### 4. Generate Alternatives

Create 2-3 BPMN/orchestration approaches. Common comparisons include:

**External Tasks vs Java Delegates**: Decoupled scalable execution vs embedded in-process execution. Constitution favors external tasks.

**Call Activities vs Embedded Sub-Processes**: Reusable versioned sub-processes vs inline sub-process definitions.

**Event-Based Gateway vs Receive Task**: Multiple event wait patterns vs single message wait.

**DMN Business Rule Task vs Gateway Conditions**: Externalized decision logic vs inline Groovy expressions.

**Multi-Instance vs Sequential Loop**: Parallel processing vs ordered execution.

**Message Correlation vs Signal Events**: Targeted instance communication vs broadcast patterns.

Each with BPMN snippets, pros/cons, and constitution compliance analysis.

### 5. Generate Comparison Matrix

Compare on: constitution compliance, scalability, testability, maintainability, Cockpit visibility, error handling capability, deployment complexity, performance. Provide scores and analysis.

### 6. Add Recommendations

Recommend approach with justification aligned to constitution rules. Include migration strategy if switching patterns, testing considerations, monitoring setup in Cockpit.

### 7. Validate and Report

// turbo

## Error Handling

**Insufficient Context**: Request workflow complexity, throughput requirements, team familiarity with patterns.

**Pattern Unfamiliarity**: Provide BPMN examples and Camunda documentation references.

**Constitution Conflict**: If a requested pattern violates constitution rules, explain the violation and recommend the compliant alternative.

## Examples

**Example 1**: `/compare-camunda-orchestration External tasks vs Java delegates for order processing` - Output: Pattern comparison with BPMN snippets and scalability analysis

**Example 2**: `/compare-camunda-orchestration Call activity vs embedded sub-process for fallout handling` - Output: Reusability and versioning comparison

**Example 3**: `/compare-camunda-orchestration Event-based gateway vs polling for callback patterns` - Output: Wait pattern comparison with timer/message analysis

## References

Constitution: `${ARCHETYPES_BASEDIR}/camunda-orchestration/constitution.md`
