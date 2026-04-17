# Workflow Creator Constitution

## Purpose

Define foundational principles for the Workflow Creator archetype, which designs LangGraph workflows with proper routing and orchestration.

**Domain:** Workflow Orchestration, Graph Design, Multi-Agent Systems  
**Use Cases:** Workflow Creator for agent pipelines, multi-agent systems, conditional routing

## I. Hard-Stop Rules (Non-Negotiable)

- ✘ **No unbounded cycles**: Never create cycles without max-iteration bounds
- ✘ **No missing entry/exit**: Never create graphs without explicit entry and END
- ✘ **No orphan nodes**: Never leave nodes unreachable from entry
- ✘ **No END without cleanup**: Never use END without cleanup/logging hooks

## II. Mandatory Patterns (Must Apply)

- ✔ **Explicit topology**: Define clear node connections
- ✔ **Conditional edges**: Use add_conditional_edges for decisions
- ✔ **Error nodes**: Include error handling nodes
- ✔ **Logging hooks**: Add observability at graph boundaries
- ✔ **Timeout configuration**: Set overall workflow timeout

## III. Preferred Patterns (Recommended)

- ➜ **Supervisor pattern**: Use supervisor for multi-agent coordination
- ➜ **Subgraphs**: Decompose complex workflows into subgraphs
- ➜ **Parallel execution**: Run independent nodes in parallel
- ➜ **Human-in-the-loop**: Add interrupt_before for critical decisions

---

## IV. Common Gotchas & Failure Modes

### Gotcha 1: Infinite Workflow Cycles
**Symptom:** Workflow never completes, runs until recursion limit  
**Root Cause:** Conditional edge always returns same node, creating unbreakable loop  
**Solution:** Add iteration counter to state. Check counter in routing function and return END after max iterations.

### Gotcha 2: Orphaned Nodes Never Execute
**Symptom:** Node defined but never called, logic skipped  
**Root Cause:** No edge connects to the node from entry point or other nodes  
**Solution:** Visualize graph with mermaid or draw_png(). Verify all nodes reachable from entry_point.

### Gotcha 3: Race Conditions in Parallel Execution
**Symptom:** Inconsistent results, state corruption when running parallel branches  
**Root Cause:** Multiple nodes writing to same state key simultaneously  
**Solution:** Use separate state keys for parallel branches. Merge results in dedicated aggregation node.

### Gotcha 4: Missing Error Handling Paths
**Symptom:** Workflow crashes on node failure, no graceful degradation  
**Root Cause:** No error nodes or try/except in node functions  
**Solution:** Add error handling node. Use conditional edges to route to error node on failure. Return structured error state.

### Gotcha 5: Subgraph State Isolation Issues
**Symptom:** Parent graph can't access subgraph results, or subgraph modifies parent state unexpectedly  
**Root Cause:** Unclear state passing between parent and subgraph  
**Solution:** Explicitly define input/output state schema for subgraphs. Use state transformers at subgraph boundaries.

---

**Version**: 1.0.0  
**Last Updated**: 2026-01-28
