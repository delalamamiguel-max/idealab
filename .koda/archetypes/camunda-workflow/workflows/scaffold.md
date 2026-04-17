---
description: Generate Camunda 7 BPMN workflow with external tasks, decision gateways, and fallout handling (Camunda Orchestration)
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
-- Read `${ARCHETYPES_BASEDIR}/camunda-orchestration/constitution.md` for hard-stop rules
-- Load `${ARCHETYPES_BASEDIR}/camunda-orchestration/templates/env-config.yaml` for engine settings, deployment targets, and integration config

### 3. Parse Input
Extract from $ARGUMENTS: workflow purpose (order activation, provisioning, etc.), tasks and their types (external task, call activity, user task), integration points (Camel routes, REST calls, Kafka topics), decision logic (DMN tables, gateway conditions), fallout handling requirements. Request clarification if incomplete.

### 4. Validate Constraints
Check against constitution hard-stop rules:
- ✘ Refuse processes without `camunda:historyTimeToLive`
- ✘ Refuse processes not marked `isExecutable="true"`
- ✘ Refuse exclusive gateways without default sequence flows
- ✘ Refuse tasks without a decision gateway for fallout/success paths
- ✘ Refuse external tasks without error boundary events
- ✘ Refuse non-snake_case process IDs or element IDs
- ✘ Refuse large payloads stored as process variables
If violated, explain clearly and suggest compliant alternative.

### 5. Generate BPMN Workflow

Create Camunda 7 BPMN 2.0 process with structure:

**Process Definition**: Process ID in snake_case, `isExecutable="true"`, `camunda:historyTimeToLive="60"`, start event and end event(s).

**Task Patterns**: External tasks with `camunda:type="external"` and topic variables (`${calledTopicName}`), call activities with `calledElementBinding="deployment"` and explicit variable mapping, `ParentProcessInstanceId` input parameter for traceability, error boundary events on every external task and call activity.

**Decision Gateways**: After every task, include an exclusive gateway to determine fallout or success. Every task MUST have both a fallout path and a success path. Default sequence flow on all exclusive gateways. Groovy expressions for complex conditions (`language="groovy"`).

**Event Patterns**: Event-based gateways for message + timer wait patterns, abort sub-processes triggered by conditional events, message correlation for callback patterns.

**Fallout Handling**: Reusable fallout sub-process (call activity), user tasks for manual resolution with `${falloutTaskId}`, conditional sequence flow for post-fallout validation.

**Variable Initialization**: Dedicated `initVars` service task at process start, `${expression}` for simple references, Spring-managed beans for complex logic.

**File Placement**: BPMN in `src/main/resources/bpmn/`, DMN in `src/main/resources/dmn/`, register in `META-INF/processes.xml`.

### 6. Generate Supporting Code

Create supporting Java/Groovy code:

**Camel Routes**: Spring-managed route beans in `route/` or `integration/` packages, Kafka consumers, REST/event integration, exclude `CamelHealthCheckAutoConfiguration` if needed.

**DMN Decision Tables**: Place in `src/main/resources/dmn/`, use `FIRST` hit policy for routing, `COLLECT` for aggregation, register in `processes.xml`.

**Spring Boot Configuration**: `camunda-bpm-spring-boot-starter-webapp-ee` for Cockpit, `camunda-bpm-spring-boot-starter-rest` for REST API, `camunda.bpm.*` properties in `application.properties`.

**Test Specifications**: Spock specs (`*Spec.groovy`) and JUnit tests (`*Test.java`), `camunda-bpm-assert` for process assertions, H2 in-memory database for test profiles, test BPMN/DMN in `src/test/resources/bpmn/`.

### 7. Add Recommendations

Include comments for: event-based gateway usage for callback patterns, multi-instance processing for parallel line items, message correlation strategies, timer expression configuration, Cockpit monitoring setup.

### 8. Validate and Report

// turbo

Report completion with file paths, BPMN process structure, applied guardrails, testing commands (`mvn test`), next steps for deployment.

## Error Handling

**Hard-Stop Violations**: Explain violation (e.g., "Missing decision gateway after external task"), suggest compliant alternative with fallout/success paths.

**Incomplete Input**: List missing information (task definitions, integration points, decision logic), provide well-formed BPMN example.

**Environment Failure**: Report missing Camunda or Java configuration, suggest setup steps.

## Examples

**Order Activation**: `/scaffold-camunda-orchestration Create BPMN workflow for order activation with external task calls to provisioning systems, callback events for completion, and fallout handling`
Output: BPMN process with external tasks, event-based gateways, fallout sub-process, DMN routing table.

**Call and Wait**: `/scaffold-camunda-orchestration Create call-and-wait-for-event pattern: invoke external system, wait for message or timeout, handle fallout`
Output: BPMN with external task, event-based gateway (message + timer), fallout paths.

**Multi-Line Processing**: `/scaffold-camunda-orchestration Create multi-instance workflow for processing order lines in parallel with individual fallout handling`
Output: BPMN with multi-instance call activity, per-line fallout handling, aggregation gateway.

## References

Constitution: `${ARCHETYPES_BASEDIR}/camunda-orchestration/constitution.md` | Env Config: `${ARCHETYPES_BASEDIR}/camunda-orchestration/templates/env-config.yaml`
