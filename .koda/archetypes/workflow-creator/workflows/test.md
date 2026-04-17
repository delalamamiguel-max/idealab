---
description: Validate all LangGraph workflow execution paths, routing coverage, and iteration bounds (Workflow Creator)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Workflow file**: Path to the LangGraph workflow Python file (e.g., `graph/workflow.py`)
- **Test mode**: `all-paths` | `happy-path` | `error-paths` | `bounds`
- **Optional flags**: `--report` to write a structured JSON test report, `--mock` to auto-generate I/O tool stubs

### 2. Map All Execution Paths
- Load and compile the graph; call `compiled.get_graph()` to enumerate all nodes and directed edges
- Perform a BFS/DFS traversal of the topology from `__start__` to generate the complete set of reachable execution paths to `END`
- For every `add_conditional_edges` call, enumerate all possible return values of the associated routing function
- Flag any path that never reaches `END` — these are dead-end branches requiring explicit handling before testing proceeds

### 3. Build Test Fixtures and Mock Tools

Construct minimal valid state objects and mock tool outputs for deterministic test runs:

```python
from unittest.mock import MagicMock, patch
from langgraph.graph import StateGraph, END
from typing import TypedDict

class AgentState(TypedDict):
    messages: list
    iteration_count: int
    tool_result: str

# Minimal fixture for the happy path
happy_state = AgentState(messages=[], iteration_count=0, tool_result="")

# Mock external tool to prevent live network calls
mock_tool = MagicMock(return_value={"output": "mocked_result"})

# Inject mock and invoke the graph
with patch("graph.workflow.search_tool", mock_tool):
    result = graph.invoke(happy_state, config={"recursion_limit": 25})
    assert result.get("tool_result") == "mocked_result", "Unexpected tool output"
    assert result.get("final_answer") or "__end__" in result, "Graph did not reach END"
```

- For routing functions that read external or random state, create parametrized fixtures covering each possible return value
- Stub every tool call that performs network or filesystem I/O — non-deterministic tests are not acceptable per constitution

### 4. Execute Path Coverage
- Invoke the compiled graph with each fixture state, varying routing conditions to exercise every branch
- Assert expected terminal state after each invocation: check `__end__`, final message content, or explicit error flags
- Verify the iteration cap fires correctly: initialize `iteration_count = max_iterations - 1` and confirm the graph routes to `END` on next step
- Test the error path: inject a node that raises `RuntimeError` and confirm the error-handler node is reached, not a silent hang or `RecursionError`

### 5. Verify Iteration Bounds and Cycle Safety
- Set `recursion_limit = max_iterations + 1` during invocation; confirm clean output without `RecursionError`
- Set `recursion_limit = max_iterations - 1`; confirm the early-exit guard in the routing function fires first
- Run every test invocation at least once without any `RecursionError` — a `RecursionError` in a test run is an immediate hard-stop (constitution violation)
- Confirm bounded invocations complete under the `graph_compilation_timeout_ms` threshold defined in `env-config.yaml`

### 6. Generate Coverage Report
- Summarize: total execution paths discovered, paths tested, conditional branches covered, uncovered branches
- Flag any path without a test case as an explicit coverage gap in the report
- Output structured JSON if `--report` flag is provided: `{ "total_paths": N, "covered": M, "gaps": ["path_a", "path_b"] }`
- Fail the test run if coverage drops below 80% of discovered paths

## Error Handling

| Condition | Action |
|---|---|
| Missing `$ARGUMENTS` | Prompt: "Please provide: workflow_file_path [test_mode] [--report] [--mock]" |
| Missing constitution file | Halt: constitution required — run `/scaffold-archetype-architect` first |
| `langgraph` not installed | Halt: `pip install langgraph>=0.0.40` |
| Non-deterministic routing detected | Warn: routing function reads external or random state — create parametrized fixtures covering each possible return value explicitly |
| Missing mock tool fixtures | Halt: tool performs live network or filesystem call during test invocation — mock all I/O-bound tools with `unittest.mock.patch` before running |
| Cycle detection failure | Halt: `RecursionError` raised during bounded invocation — routing function lacks a termination branch; add `iteration_count >= max_iterations → END` guard |

## Examples

**Example 1**: `/test-workflow-creator graph/workflow.py all-paths --report`
Maps 4 execution paths through a branching workflow, builds mock fixtures for 2 external tools, runs all 4 invocations, confirms `END` is reached in each, writes `test_report.json` with 100% path coverage.

**Example 2**: `/test-workflow-creator graph/supervisor.py bounds --mock`
Auto-generates stubs for 3 tool calls, initializes state with `iteration_count = max_iterations - 1` to trigger the bounds guard, confirms the workflow terminates cleanly on the next step, flags a missing error-path invocation as a coverage gap.
