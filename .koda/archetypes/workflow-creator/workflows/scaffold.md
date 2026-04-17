---
description: Design LangGraph workflows with routing, subgraphs, and orchestration (Workflow Creator)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Workflow name**: Name for the workflow
- **Pattern**: linear | branching | loop | multi-agent
- **Nodes**: List of nodes
- **Entry/Exit**: Entry point and end conditions

### 2. Generate Workflow

```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

# Add edges
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {"tools": "tools", "end": END}
)
workflow.add_edge("tools", "agent")

# Set entry
workflow.set_entry_point("agent")

# Compile
graph = workflow.compile()
```

### 3. Add Safeguards
- Iteration limits
- Timeout configuration
- Error handling

### 4. Validate

Run these checks before declaring the workflow production-ready:

```python
from langgraph.graph import StateGraph

# Compile and verify graph structure
compiled = graph.compile()
graph_def = compiled.get_graph()

# Check 1: No orphaned nodes (every node must be reachable from entry)
all_nodes = set(graph_def.nodes.keys())
# Visually inspect or traverse: every node should have at least one incoming edge except entry

# Check 2: No unbounded cycles (every cycle must have an iteration limit)
# Verify your route() function returns END or has a max_iterations guard
```

**Checklist:**
- [ ] All nodes are reachable from the entry point (no orphaned nodes)
- [ ] Every cycle has an iteration limit (`iteration_count >= max_iterations → END`)
- [ ] All terminal paths lead to `END`
- [ ] Timeout configuration is set (required by constitution)
- [ ] Error handling nodes are wired for each branch where failures can occur
- [ ] Subgraph state isolation is verified (subgraph states don't bleed into parent graph)
- [ ] Graph compiles without exceptions: `workflow.compile()` succeeds

## Error Handling

| Condition | Action |
|---|---|
| Missing `$ARGUMENTS` | Prompt: "Please provide: graph_name [node_list] [edge_definitions] [options]" |
| Missing constitution file | Halt: constitution required before scaffolding — run `/scaffold-archetype-architect` first |
| `langgraph` not installed | Halt: `pip install langgraph>=0.0.40` |
| Unbounded cycle detected | Halt (constitution violation): add `recursion_limit` to graph config |
| Entry or END node missing | Halt (hard-stop): every graph requires explicit entry point and END node |
| Orphan node detected | Warn: node unreachable from entry — add connecting edge or remove node |

## Examples
**Example**: `/scaffold-workflow-creator support-flow branching "classify,route,respond"`
