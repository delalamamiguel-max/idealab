---
description: Restructure LangGraph workflow topology, extract subgraphs, and optimize routing logic (Workflow Creator)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Workflow file**: Path to the target workflow Python file (e.g., `graph/workflow.py`)
- **Refactor goal**: One of `subgraphs` | `supervisor` | `routing` | `parallel` | `cleanup`
- **Optional flags**: `--preview` to show planned changes without writing, `--backup` to snapshot the original file before editing

### 2. Analyze Current Topology
- Load and compile the current graph; call `compiled.get_graph()` to inspect all nodes, edges, and conditional branches
- Identify topology anti-patterns: monolithic node chains, duplicate routing logic, flat graphs with >12 nodes that should be hierarchical
- Count total nodes and edges — if node count exceeds 15 in a flat topology, flag as subgraph extraction candidate
- Map all `add_conditional_edges` callsites; identify duplicate routing functions that can be merged into a shared router factory

### 3. Plan and Preview Refactoring Changes

Produce a before/after structural outline before writing any code:

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

# BEFORE: flat monolithic graph — agent → tools → agent → END
# AFTER: extract research cluster into isolated subgraph

class ResearchState(TypedDict):
    query: str
    results: Annotated[list, operator.add]
    iteration_count: int

research_subgraph = StateGraph(ResearchState)
research_subgraph.add_node("search", search_node)
research_subgraph.add_node("synthesize", synthesize_node)
research_subgraph.add_edge("search", "synthesize")
research_subgraph.add_edge("synthesize", END)
compiled_research = research_subgraph.compile()

# Parent graph invokes subgraph as a compiled node
parent = StateGraph(ParentState)
parent.add_node("research", compiled_research)
parent.add_node("respond", respond_node)
parent.add_edge("research", "respond")
parent.add_edge("respond", END)
parent.set_entry_point("research")
```

- For supervisor pattern: introduce a `supervisor` node with `add_conditional_edges` dispatching to named worker agents; workers return via `add_edge(worker, "supervisor")`
- For parallel execution: use `Send` API to fan out work across workers and merge results in a dedicated aggregation node

### 4. Apply Structural Changes
- Extract identified node clusters into isolated `StateGraph` subgraphs, each with its own `TypedDict` state schema
- Update the parent graph to invoke subgraphs as compiled nodes: `parent.add_node("subgraph_name", subgraph.compile())`
- Consolidate duplicate routing functions — replace repeated `if/elif` chains with a shared router returning consistent string keys
- Add missing cleanup/logging hooks at every `END` boundary (constitution requirement)

### 5. Validate Subgraph State Isolation
- Confirm subgraph `TypedDict` has zero shared fields with parent state — shared fields cause silent state bleed across boundaries
- Compile each subgraph independently before embedding: `subgraph.compile()` must succeed in isolation
- Run a dry-fire invocation of the parent with minimal stub inputs to confirm the subgraph boundary is correctly wired

### 6. Compile and Regression-Test
- Full recompile of the refactored parent graph — zero `ValueError` tolerance
- Re-run any existing test suite and confirm all routing paths produce identical outcomes to the pre-refactor baseline
- Generate updated topology diagram: `graph.get_graph().draw_mermaid()` and append or replace the docstring diagram

## Error Handling

| Condition | Action |
|---|---|
| Missing `$ARGUMENTS` | Prompt: "Please provide: workflow_file_path refactor_goal [--preview] [--backup]" |
| Missing constitution file | Halt: constitution required — run `/scaffold-archetype-architect` first |
| `langgraph` not installed | Halt: `pip install langgraph>=0.0.40` |
| Breaking node rename detected | Warn: renaming a node invalidates all `add_edge` and `add_conditional_edges` references — update every callsite before recompiling |
| Edge logic regression | Halt: post-refactor routing test produced a different execution path than the baseline — revert and re-examine the conditional logic |
| Subgraph isolation failure | Halt: subgraph `TypedDict` shares fields with parent state — define separate state schemas and use explicit input/output transformers at subgraph boundaries |

## Examples

**Example 1**: `/refactor-workflow-creator graph/workflow.py subgraphs`
Identifies a 12-node flat graph, extracts the `search → synthesize` cluster into a standalone `ResearchSubgraph` with isolated state, rewires the parent to call it as a compiled node, recompiles, runs regression tests — all paths match baseline.

**Example 2**: `/refactor-workflow-creator graph/multi_agent.py supervisor --backup`
Snapshots the original file, introduces a `supervisor` node using `add_conditional_edges` to dispatch to `researcher`, `coder`, and `critic` worker agents, sets `recursion_limit=25` in compile config, confirms all workers converge back through supervisor to `END`.
