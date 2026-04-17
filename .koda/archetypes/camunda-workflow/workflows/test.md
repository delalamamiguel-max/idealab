---
description: Generate test suite for Camunda 7 BPMN workflows with Spock and camunda-bpm-assert (Camunda Orchestration)
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
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype camunda-orchestration --json ` and parse for CAMUNDA_VERSION, JAVA_VERSION, SPOCK_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- Read `${ARCHETYPES_BASEDIR}/camunda-orchestration/constitution.md` for testing rules
- Load `${ARCHETYPES_BASEDIR}/camunda-orchestration/templates/env-config.yaml` for test configuration

### 3. Parse Input
Extract from $ARGUMENTS: BPMN file path, test scope (unit/integration/end-to-end), specific elements to test (gateways, external tasks, timers, messages, call activities), coverage goals. Request clarification if incomplete.

### 4. Analyze Code

Identify testable components:

**BPMN Structure Tests**:
- Process is executable with correct historyTimeToLive
- All element IDs are snake_case and descriptive
- All exclusive gateways have default sequence flows
- Every task has a decision gateway with fallout/success paths

**External Task Tests**:
- Topic name variables resolve correctly
- Error boundary events trigger on failures
- Call activities bind to deployment version
- Variable mapping (in/out) passes correct data
- ParentProcessInstanceId is set

**Gateway Tests**:
- Decision gateways route correctly for fallout vs success
- Default sequence flows activate when no condition matches
- Groovy condition expressions evaluate correctly
- Event-based gateways respond to message and timer events

**DMN Tests**:
- Decision tables return expected results for input combinations
- Hit policies (FIRST, COLLECT) behave correctly
- DMN resources are registered and accessible

**Fallout Handling Tests**:
- Fallout sub-process invokes correctly
- User task creates with correct assignee
- Conditional sequence flow validates recovery
- Fallout resolution resumes main process

**Timer and Message Tests**:
- Timer expressions fire at correct intervals
- Message correlation matches expected instances
- Event-based gateway handles message before timeout and timeout before message

Report test coverage plan.

### 5. Generate Test Suite

Create test suite using constitution testing rules:

**Spock Specifications** (`*Spec.groovy`):
- Process deployment spec (validates BPMN loads correctly)
- Gateway routing spec (tests all gateway conditions)
- External task spec (tests topic resolution, error handling)
- Fallout handling spec (tests fallout path end-to-end)
- Message correlation spec (tests message events)
- Timer spec (tests timer expressions)

**JUnit Tests** (`*Test.java`):
- `camunda-bpm-assert` based process instance assertions
- `assertThat(processInstance).isWaitingAt("external_task_name")`
- `assertThat(processInstance).hasPassed("gateway_pre_fallout")`
- Variable assertion after task completion

**Test Configuration**:
- H2 in-memory database for test profiles
- Test BPMN/DMN files in `src/test/resources/bpmn/`
- Spring Boot test context with embedded Camunda engine
- Mock external task workers

Include complete test code with imports, setup, and assertions.

### 6. Add Recommendations

Include recommendations for:
- Test individual BPMN elements in isolation before integration tests
- Mock external systems for external task testing
- Test timer expressions with accelerated clock
- Verify message correlations with multiple instances
- CI/CD integration (run `mvn test` on PR)
- Coverage targets for gateway paths and fallout flows

### 7. Validate and Report

// turbo

Report completion with test file paths, test count, coverage summary, execution command (`mvn test`), next steps.

## Error Handling

**Insufficient Code**: Request complete BPMN file and supporting Java/Groovy code.

**No Test Environment**: Provide Maven dependency setup for camunda-bpm-assert, Spock, H2.

**Complex Mocking**: Suggest mocking strategies for external tasks and Camel routes.

## Examples

**Example 1**: `/test-camunda-orchestration Generate tests for call_and_wait_for_event_flow.bpmn` - Output: 15 Spock specs covering gateways, external tasks, message events, timers, fallout paths

**Example 2**: `/test-camunda-orchestration Create gateway routing tests for order_activation.bpmn` - Output: Tests for all gateway conditions including fallout/success paths

**Example 3**: `/test-camunda-orchestration Add fallout handling tests for provisioning_flow.bpmn` - Output: End-to-end fallout tests with user task resolution and recovery validation

## References

Constitution: `${ARCHETYPES_BASEDIR}/camunda-orchestration/constitution.md` | Env Config: `${ARCHETYPES_BASEDIR}/camunda-orchestration/templates/env-config.yaml`
