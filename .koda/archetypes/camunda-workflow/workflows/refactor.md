---
description: Refactor Camunda BPMN workflows to apply constitution best practices and fix violations (Camunda Orchestration)
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
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype camunda-orchestration --json ` and parse for CAMUNDA_VERSION, JAVA_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- Read `${ARCHETYPES_BASEDIR}/camunda-orchestration/constitution.md` for hard-stop rules
- Load `${ARCHETYPES_BASEDIR}/camunda-orchestration/templates/env-config.yaml` for engine settings

### 3. Parse Input
Extract from $ARGUMENTS: existing BPMN file path or inline XML, supporting Java/Groovy code, refactoring goals (add decision gateways, fix naming, add boundary events, improve fallout handling), constraints. Request clarification if incomplete.

### 4. Analyze Existing Code

Load and analyze existing BPMN and code:

**BPMN Design Rule Violations**:
- Process IDs not in snake_case
- Element IDs not descriptive or not snake_case
- Missing `camunda:historyTimeToLive`
- Process not marked `isExecutable="true"`
- Exclusive gateways without default sequence flows
- Tasks without decision gateways for fallout/success paths
- Java delegates instead of external tasks
- Missing error boundary events on external tasks and call activities
- Missing event-based gateways for wait patterns
- BPMN/DMN files in wrong directories
- Resources not registered in `processes.xml`

**External Task Violations**:
- Hardcoded topic names instead of variables
- Missing error event handling on boundaries
- `calledElementBinding` not set to `deployment`
- Using `variables="all"` without justification
- Missing `ParentProcessInstanceId`

**DMN Violations**:
- DMN files in wrong directory
- Inappropriate hit policy
- Not registered in `processes.xml`

**Camel Integration Violations**:
- Routes not Spring-managed
- Missing `CamelHealthCheckAutoConfiguration` exclusion
- Routes not in `route/` or `integration/` packages

**Error Handling Violations**:
- No reusable fallout sub-process
- Missing user tasks for manual resolution
- Service task instead of conditional sequence flow for post-fallout validation

**Variable Violations**:
- No `initVars` service task
- Large payloads as process variables
- Inline scripts instead of Spring-managed beans

Report findings with element names, line numbers, and severity.

### 5. Generate Refactored Code

Create refactored BPMN and supporting code applying all fixes:

- Rename process/element IDs to snake_case
- Add `historyTimeToLive` and `isExecutable`
- Add default sequence flows on all exclusive gateways
- Insert decision gateways after every task with fallout/success paths
- Convert Java delegates to external tasks
- Add error boundary events to external tasks and call activities
- Add event-based gateways for wait patterns
- Move files to correct directories
- Register resources in `processes.xml`
- Add `initVars` service task
- Implement reusable fallout sub-process
- Fix variable mapping and topic name variables
- Update Camel routes to Spring-managed beans

Include complete refactored BPMN XML and code files.

### 6. Add Recommendations

Include inline comments for:
- Cockpit monitoring improvements
- Test coverage for refactored elements
- Deployment considerations for version migration
- Performance implications of pattern changes

Provide summary of improvements with before/after comparison.

### 7. Validate and Report

// turbo

Generate optional Mermaid process diagram. Report completion with file paths, applied improvements, constitution compliance status, testing commands, next steps.

## Error Handling

**Hard-Stop Violations in Original**: Explain each violation clearly (e.g., "External task on line 42 missing decision gateway for fallout path"), show compliant alternative.

**Incomplete Input**: List missing information (BPMN file, refactoring goals), provide well-formed example.

**Environment Failure**: Report missing Camunda installation or configuration, suggest setup steps.

## Examples

**Example 1: Add Decision Gateways**
```
/refactor-camunda-orchestration Add fallout/success decision gateways after all tasks in order_activation.bpmn

Input: BPMN with tasks flowing directly to next task
Output: Refactored with exclusive gateway after each task, fallout path to sub-process, success path to next task
```

**Example 2: Convert to External Tasks**
```
/refactor-camunda-orchestration Convert Java delegates to external tasks in provisioning_flow.bpmn

Input: BPMN with embedded JavaDelegate service tasks
Output: Refactored with external tasks, topic variables, error boundary events
```

**Example 3: Fix Naming Conventions**
```
/refactor-camunda-orchestration Fix element IDs and process ID to use snake_case in CallAndWaitFlow.bpmn

Input: BPMN with camelCase IDs
Output: Refactored with snake_case IDs, descriptive element names
```

## References

Constitution: `${ARCHETYPES_BASEDIR}/camunda-orchestration/constitution.md` | Env Config: `${ARCHETYPES_BASEDIR}/camunda-orchestration/templates/env-config.yaml`
