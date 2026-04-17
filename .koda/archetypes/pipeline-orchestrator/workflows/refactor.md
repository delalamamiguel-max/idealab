---
description: Refactor Airflow/TWS DAG to apply reliability, monitoring, and best practices (Pipeline Orchestrator)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype pipeline-orchestrator --json ` and parse for AIRFLOW_VERSION, PYTHON_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/pipeline-orchestrator/templates/env-config.yaml` for default_args, retry settings, SLA thresholds

### 3. Parse Input
Extract from $ARGUMENTS: existing DAG file path or inline code, refactoring goals (SLA monitoring, callbacks, retries, modularity), constraints. Request clarification if incomplete.

### 4. Analyze Existing Code
Load and analyze existing DAG:
- Identify hard-stop rule violations (hardcoded credentials/connection IDs, missing retries/backoff, missing callbacks, unstructured logging, tasks without dependencies/default_args, non-idempotent operations)
- Identify missing mandatory patterns (retries ≥3 with exponential backoff, on_failure/on_success callbacks, environment variables for secrets, DAG run tagging, parameterized schedule/dates, SLA declarations)
- Identify opportunities for preferred patterns (TaskFlow API, DAG factory, functions ≤75 LOC, snake_case naming, Mermaid diagrams, docstrings)

Report findings with task names and line numbers.

### 5. Generate Refactored DAG

Create refactored Airflow DAG applying hard-stop fixes (move credentials to Variables/Connections, add retries with exponential backoff, add failure/success callbacks, implement structured logging, define task dependencies, ensure idempotency), mandatory patterns (comprehensive default_args, DAG run metadata tagging, parameterization, SLA monitoring), and preferred patterns (TaskFlow API, modular task functions, comprehensive docstrings, DAG factory pattern).

Include complete code example with imports, default_args, callback functions, task definitions, and dependency chains.

### 6. Add Recommendations

Include inline comments for monitoring (SLA sensors, task duration alerts), scalability (dynamic task generation, parallel execution), maintainability (shared task libraries, configuration management), and observability (custom metrics, logging integration).

Provide summary of improvements with reliability enhancements and operational benefits.

### 7. Validate and Report


Generate optional Mermaid DAG diagram. Report completion with file paths, applied improvements, monitoring enhancements, next steps.

## Error Handling

**Hard-Stop Violations in Original**: Explain each violation clearly (e.g., "Hardcoded connection ID on line 15"), show compliant alternative using Airflow Variables.

**Incomplete Input**: List missing information (DAG file path or code, refactoring goals, constraints), provide well-formed example.

**Environment Failure**: Report missing Airflow installation or configuration, suggest setup steps and connection configuration.

## Examples

**Example 1: Add SLA Monitoring**
```
/refactor-pipeline Add SLA monitoring to data_pipeline_dag.py with 2-hour threshold

Input: DAG without SLA configuration
Output: Refactored with SLA declarations, SLA miss callbacks, alerting integration
```

**Example 2: Improve Error Handling**
```
/refactor-pipeline Add retry logic and failure callbacks to etl_dag.py

Input: DAG with no retries, no error handling
Output: Refactored with exponential backoff retries, comprehensive callbacks, structured logging
```

**Example 3: Modularize DAG**
```
/refactor-pipeline Convert monolithic_dag.py to use TaskFlow API and modular functions

Input: Large DAG with inline task logic
Output: Refactored with TaskFlow decorators, functions ≤75 LOC, DAG factory pattern
```

## References

