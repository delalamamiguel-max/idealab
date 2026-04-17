---
description: Diagnose and fix LangGraph routing issues, infinite loops, orphan nodes, and dead ends (Workflow Creator)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Workflow file**: Path to the LangGraph workflow Python file (e.g., `graph/workflow.py`)
- **Issue description**: Free-text description of the symptom (e.g., "infinite loop at agent node", "orphan node never executes")
- **Optional flags**: `--trace` to enable verbose state transition logging, `--dry-run` to skip file writes

### 2. Load and Instrument the Graph
- Import the workflow module and call `workflow.compile()` to produce a `CompiledGraph`
- Call `compiled.get_graph()` to retrieve: full node list, directed edges, and conditional branch mappings
- Attach a `RecursionError` sentinel by temporarily setting `recursion_limit=5` to surface cycle issues early
- Log all state transitions to stderr using `langsmith` trace or manual checkpoint hooks to reconstruct the execution trace

### 3. Trace Execution and Identify Root Cause

Run diagnostic checks against the compiled graph structure:

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

compiled = graph.compile()
topology = compiled.get_graph()

# Orphan detection: every node except entry must have at least one incoming edge
incoming = {e.target for e in topology.edges}
orphans = [n for n in topology.nodes if n not in incoming and n != "__start__"]
if orphans:
    print(f"[WARN] Orphan nodes detected (unreachable from entry): {orphans}")

# Cycle + bounds check: attempt bounded invocation to flush any infinite cycle
try:
    result = graph.invoke({"messages": [], "iteration_count": 0}, config={"recursion_limit": 10})
except RecursionError as e:
    print(f"[ERROR] Unbounded cycle confirmed: {e}")

# Missing END check: every terminal branch must route to END
terminal_nodes = [n for n in topology.nodes if not any(e.source == n for e in topology.edges)]
print(f"[INFO] Terminal nodes (must route to END): {terminal_nodes}")
```

- Cross-reference each `add_conditional_edges` path map — verify every return value has a defined target node
- Check all terminal paths eventually reach `END`; a missing `END` edge causes a silent hang

### 4. Apply Targeted Fixes
- **Infinite loop**: inject `iteration_count` field into `StateTypedDict`; add guard `if state["iteration_count"] >= max_iterations: return END` inside the routing function
- **Orphan node**: trace where the node should be reached and add `workflow.add_edge(predecessor, orphan_node)` or a conditional branch to it
- **Missing END**: add `workflow.add_edge("terminal_node", END)` and ensure the routing function returns a key mapped to `END`
- **Dead conditional branch**: update the `add_conditional_edges` path map to cover every possible return value of the router function
- **State leak**: verify the offending subgraph uses its own isolated `TypedDict`; remove any shared fields between parent and subgraph state

### 5. Re-Validate the Fixed Graph
- Recompile with `workflow.compile()` — must succeed without any `ValueError`
- Re-run the bounded invocation with `recursion_limit=25`; confirm no `RecursionError`
- Confirm all previously detected orphans are absent from `compiled.get_graph().nodes`
- Verify every execution path terminates at `END` by inspecting the output state's `__end__` key

### 6. Generate Debug Report
- Summarize: root cause category (loop / orphan / dead-end / missing-END / state-leak), affected node(s), fix applied
- Append a `## Debug History` entry to the workflow file with timestamp, issue, and resolution
- Run `graph.get_graph().draw_mermaid()` and embed the corrected topology diagram in the report

## Error Handling

| Condition | Action |
|---|---|
| Missing `$ARGUMENTS` | Prompt: "Please provide: workflow_file_path [issue_description] [--trace] [--dry-run]" |
| Missing constitution file | Halt: constitution required — run `/scaffold-archetype-architect` first |
| `langgraph` not installed | Halt: `pip install langgraph>=0.0.40` |
| Infinite loop detected | Halt (constitution violation): routing function has no termination branch — add `iteration_count >= max_iterations → END` guard to state and router |
| Orphan node unreachable | Warn: node has no incoming edges from entry — add a connecting edge or remove the dead node entirely |
| Missing END node | Halt (hard-stop): every terminal branch must route to `END` — add missing edge or update the routing path map |

## Examples

**Example 1**: `/debug-workflow-creator graph/workflow.py "Infinite loop at agent node"`
Traces the `agent` node's routing function, discovers `route_agent()` never returns `END`, injects `iteration_count` field into `AgentState` with a `>= 25 → END` guard, recompiles, confirms bounded invocation completes.

**Example 2**: `/debug-workflow-creator graph/supervisor.py "classify node never executes" --trace`
Detects `classify` node has no incoming edge — missing key in the supervisor's `add_conditional_edges` path map. Adds `"classify": "classify"` to the mapping, re-validates topology, confirms orphan is resolved.
