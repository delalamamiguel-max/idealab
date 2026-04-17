---
description: Generate structured documentation, Mermaid topology diagrams, and execution guides for LangGraph workflows (Workflow Creator)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Workflow file**: Path to the LangGraph workflow Python file (e.g., `graph/workflow.py`)
- **Output mode**: `full` | `diagram-only` | `nodes-only` | `guide-only`
- **Optional flags**: `--output path/to/output.md` to specify output file, `--overwrite` to replace an existing doc file

### 2. Load and Introspect the Graph
- Import the workflow module and call `workflow.compile()` to obtain a `CompiledGraph`
- Call `compiled.get_graph()` to extract: all node names with their bound Python functions, all directed edges, and all conditional branch mappings with their routing functions
- Identify the entry node (`__start__`) and all terminal nodes (nodes with an outgoing edge to `END`)
- Flag any node function lacking a docstring — these are documentation gaps that must be resolved before the documentation is finalized (constitution requirement)

### 3. Generate Mermaid Topology Diagram

Export the graph structure as a Mermaid flowchart using LangGraph's built-in renderer:

```python
from langgraph.graph import StateGraph, END

compiled = graph.compile()

# LangGraph built-in Mermaid export
mermaid_diagram = compiled.get_graph().draw_mermaid()
print(mermaid_diagram)

# Example output:
# %%{init: {'flowchart': {'curve': 'linear'}}}%%
# graph TD;
#     __start__ --> supervisor;
#     supervisor --> researcher;
#     supervisor --> coder;
#     supervisor --> END;
#     researcher --> supervisor;
#     coder --> supervisor;

# Optional: export PNG for visual review
compiled.get_graph().draw_png("workflow_diagram.png")
```

- If `draw_mermaid()` raises (missing optional graphviz dep), fall back to manually constructing a Mermaid block from `get_graph().edges`
- Embed the diagram under a `## Topology` section in the generated documentation
- Flag any diagram that differs from a previously committed version in the repo as "outdated" — regenerate and replace

### 4. Document Nodes and Edges
For every node in the compiled graph, generate a structured documentation block:
- **Node name** and the Python function it maps to (with module path)
- **Input state fields consumed**: inferred from `TypedDict` annotations and function signature
- **Output state fields produced**: inferred from return type hints or explicit state key assignments
- **Routing logic**: for any node that is a source of `add_conditional_edges`, document each possible return value and its mapped target node
- Flag any conditional routing function that lacks inline comments explaining the decision criteria — this is a constitution violation requiring resolution

### 5. Document State Schema
- Extract the `TypedDict` or `StateTypedDict` class from the module and document every field: name, type, purpose, and default value if specified
- Highlight any field written by more than one node — these are potential race conditions in parallel execution graphs
- Document subgraph state schemas separately under a `### Subgraph: <name>` subsection when subgraphs are present, noting any state transformation applied at the boundary

### 6. Generate Execution Guide
- Write a step-by-step narrative of the happy-path execution: what triggers the workflow, which nodes fire in order, how state evolves at each step, and what the final output looks like
- Document all error paths: which branch routes to an error node and what recovery actions that node performs
- Include a `## Usage` section with a minimal working invocation:
  ```python
  result = graph.invoke({"messages": [], "iteration_count": 0}, config={"recursion_limit": 25})
  print(result["final_answer"])
  ```
- Write output to `--output` target if provided, otherwise print to stdout; never overwrite without `--overwrite` flag

## Error Handling

| Condition | Action |
|---|---|
| Missing `$ARGUMENTS` | Prompt: "Please provide: workflow_file_path [output_mode] [--output path] [--overwrite]" |
| Missing constitution file | Halt: constitution required — run `/scaffold-archetype-architect` first |
| `langgraph` not installed | Halt: `pip install langgraph>=0.0.40` |
| Undocumented conditional logic | Warn: routing function has no docstring or inline comments — add explanation of decision criteria before finalizing the document |
| Missing node descriptions | Warn: N node functions lack docstrings — add docstrings describing inputs, outputs, and side effects for all flagged nodes |
| Outdated graph diagram | Warn: existing diagram in the repository does not match current compiled topology — regenerate with `draw_mermaid()` and replace the stale version |

## Examples

**Example 1**: `/document-workflow-creator graph/workflow.py full --output docs/workflow.md`
Introspects a 6-node branching workflow, generates a Mermaid topology diagram, documents all nodes and the full state schema, writes a step-by-step execution guide to `docs/workflow.md`.

**Example 2**: `/document-workflow-creator graph/supervisor.py diagram-only`
Exports only the Mermaid topology diagram for a supervisor pattern with 3 worker agents (`researcher`, `coder`, `critic`), prints the diagram block to stdout for direct embedding into a project README.
