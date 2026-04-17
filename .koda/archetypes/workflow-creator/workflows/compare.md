---
description: Compare two or more LangGraph workflow patterns side-by-side on topology, complexity, and routing efficiency (Workflow Creator)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Patterns or files**: Two or more patterns or file paths to compare (e.g., `"linear vs supervisor"`, `graph/v1.py graph/v2.py`)
- **Comparison dimension**: `complexity` | `scalability` | `routing` | `resilience` | `all`
- **Optional flags**: `--inputs state_file.json` to provide shared test state for live routing comparison, `--export` to write the comparison table to a markdown report

### 2. Load and Compile Both Graphs
- Import each workflow module (or instantiate from built-in pattern templates) and call `.compile()` on each
- Call `get_graph()` on each compiled graph to extract the node set, directed edge list, and conditional branch count
- Confirm both graphs compile independently before proceeding — if either fails, halt with the compile error
- Normalize node names across graphs (e.g., strip version suffixes) for fair structural comparison when comparing revisions of the same workflow

### 3. Analyze Topology and Complexity Metrics

Compute structural metrics for each graph side-by-side:

```python
from langgraph.graph import StateGraph, END

def graph_metrics(compiled_graph) -> dict:
    topology = compiled_graph.get_graph()
    nodes = list(topology.nodes.keys())
    edges = list(topology.edges)
    conditional = [e for e in edges if getattr(e, "conditional", False)]

    # Estimate max path length via BFS from __start__ to END
    def bfs_max_depth(graph, start="__start__", end="__end__"):
        from collections import deque
        q = deque([(start, 0)])
        max_d = 0
        while q:
            node, depth = q.popleft()
            max_d = max(max_d, depth)
            for e in graph.edges:
                if e.source == node and e.target != end:
                    q.append((e.target, depth + 1))
        return max_d

    return {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "conditional_branches": len(conditional),
        "max_path_length": bfs_max_depth(topology),
    }

metrics_a = graph_metrics(graph_a.compile())
metrics_b = graph_metrics(graph_b.compile())

header = f"{'Metric':<30} {'Graph A':>10} {'Graph B':>10}"
print(header)
for key in metrics_a:
    print(f"{key:<30} {metrics_a[key]:>10} {metrics_b[key]:>10}")
```

- Flag any structural incompatibility: if one graph uses subgraphs and the other is flat, note the asymmetry and limit quantitative metrics to node/edge counts
- Compute routing fanout: average number of outgoing conditional edges per node — higher fanout means more complex decision logic

### 4. Benchmark Routing Paths with Shared Inputs
- If `--inputs` is provided, load the shared state file and invoke both compiled graphs with identical input; compare terminal output states
- Measure invocation latency over N=10 runs and report mean ± std for each graph
- Compare path length: count how many nodes are visited per graph for the same input state
- Score each graph per dimension (complexity, routing determinism, error resilience) and compute an overall weighted score

### 5. Generate Recommendation
- State a clear winner per dimension with explicit reasoning — no ambiguous hedging
- Enumerate trade-offs explicitly: e.g., "supervisor adds 3 nodes (+27%) but scales linearly to N workers; linear is simpler but cannot parallelize"
- If graphs are functionally equivalent, recommend the one with lower node count and fewer conditional branches (less attack surface, simpler maintenance)
- Write a markdown comparison table with a `Winner` column if `--export` is provided

## Error Handling

| Condition | Action |
|---|---|
| Missing `$ARGUMENTS` | Prompt: "Please provide: pattern_a pattern_b [dimension] [--inputs state_file] [--export]" |
| Missing constitution file | Halt: constitution required — run `/scaffold-archetype-architect` first |
| `langgraph` not installed | Halt: `pip install langgraph>=0.0.40` |
| Incompatible graph topologies | Warn: graphs have structurally incompatible designs (e.g., one uses compiled subgraphs, other is fully flat) — comparison limited to node/edge counts; live routing benchmark skipped |
| Insufficient test inputs | Warn: `--inputs` not provided — live routing benchmark skipped; only static topology metrics available for comparison |
| Ambiguous routing winner | Note: no clear winner on the requested dimension — surface all metrics and trade-offs explicitly; ask user to specify the primary constraint (latency vs. simplicity vs. scalability) before finalizing recommendation |

## Examples

**Example 1**: `/compare-workflow-creator "linear vs supervisor" scalability`
Instantiates both pattern templates, computes structural metrics, finds supervisor has 4 additional nodes (+33%) but supports N-worker parallelism via `Send`; recommends supervisor when expected worker count exceeds 3.

**Example 2**: `/compare-workflow-creator graph/v1.py graph/v2.py all --inputs test_state.json --export`
Loads both versioned graphs, runs 10 invocations with shared test state (v2 is 18% faster at p50), computes topology scores (v2 has 2 fewer conditional branches), exports full comparison table to `comparison_report.md` with a clear v2 recommendation.
