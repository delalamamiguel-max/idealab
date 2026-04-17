---
description: Debug Camunda 7 process engine issues, stuck instances, and workflow failures (Camunda Orchestration)
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
-- Load `${ARCHETYPES_BASEDIR}/camunda-orchestration/templates/env-config.yaml` for engine configuration

### 3. Parse Input
Extract from $ARGUMENTS: BPMN file path, process instance ID, error message or symptoms (process stuck at gateway, external task timeout, message not correlating, timer not firing, incident in Cockpit), context (execution date, variable state, Cockpit screenshot). Request clarification if incomplete.

### 4. Analyze Problem

Identify error category:

**Process Stuck**: Gateway missing default sequence flow, missing decision gateway after task, condition expression evaluating unexpectedly, event-based gateway not receiving expected message or timer.

**External Task Failures**: Topic name mismatch (`${calledTopicName}` not resolving), missing error boundary event, external worker not picking up task, BPMN error not caught.

**Message Correlation**: Message name mismatch, correlation key not matching, message arriving before process reaches receive task, duplicate message delivery.

**Timer Issues**: Invalid timer expression, timer not firing in test (H2 job executor), async continuation misconfigured.

**Variable Issues**: Variable not initialized (missing `initVars`), large payload stored as variable, Groovy expression syntax error, UEL method call failing.

**Call Activity Issues**: `calledElementBinding` mismatch, sub-process version drift, variable mapping errors (`camunda:in`/`camunda:out`), missing `ParentProcessInstanceId`.

**DMN Issues**: Decision table returning unexpected result, hit policy mismatch, DMN resource not registered in `processes.xml`.

**Camel Integration**: Route not starting, Kafka consumer offset issues, `CamelHealthCheckAutoConfiguration` conflict, bean not found.

Check against constitution for violations that may be causing the issue.

### 5. Generate Fix

Create fix addressing root cause:

- Fix BPMN XML (add default flows, decision gateways, boundary events)
- Fix expressions (Groovy syntax, UEL references, variable initialization)
- Fix configuration (processes.xml registration, application.properties)
- Fix Camel routes (bean registration, health check exclusion)
- Fix test setup (H2 config, test resource paths)

Include complete fixed BPMN snippet or code with proper error handling.

### 6. Add Recommendations

Include recommendations for prevention:
- Validate BPMN against constitution rules before deployment
- Test individual elements (gateways, tasks) in isolation
- Verify timer expressions and message correlations in unit tests
- Use Cockpit to monitor process instance state
- Check Elasticsearch for historical execution data

### 7. Validate and Report

// turbo

Report completion with root cause, fix applied, testing recommendations, prevention strategies.

## Error Handling

**Insufficient Error Information**: Request Cockpit screenshot, process instance ID, Camunda logs, and variable state dump.

**Cannot Reproduce**: Request Camunda version, Spring Boot config, database type, and full BPMN file.

**Multiple Possible Causes**: Provide systematic debugging starting with BPMN validation, then variable state, then engine configuration.

## Examples

**Example 1: Process Stuck at Gateway**
```
/debug-camunda-orchestration Process stuck at gateway_pre_fallout after external task completes

Root Cause: Exclusive gateway missing default sequence flow, condition evaluates to null
Fix: Added default flow, fixed Groovy condition expression
```

**Example 2: Message Not Correlating**
```
/debug-camunda-orchestration Message event not triggering after external system callback

Root Cause: Message name in BPMN doesn't match published message, correlation key mismatch
Fix: Aligned message names, fixed correlation key variable reference
```

**Example 3: External Task Not Picked Up**
```
/debug-camunda-orchestration External task sitting in queue, worker not processing

Root Cause: Topic name variable ${calledTopicName} not initialized in initVars
Fix: Added topic name initialization in initVars service task
```

## References

Constitution: `${ARCHETYPES_BASEDIR}/camunda-orchestration/constitution.md` | Env Config: `${ARCHETYPES_BASEDIR}/camunda-orchestration/templates/env-config.yaml`
