---
description: Validate state management with bounds and checkpoint tests (State Specialist)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **File path**: Module containing the `TypedDict` state definition and `StateGraph` compilation
- **Test scope**: One of `schema` | `bounds` | `checkpointing` | `full` — determines which test suites to generate
- **Maturity level**: L1–L4 — L3+ requires checkpoint round-trip tests; L4 requires compliance audit log assertions
- **Fixture strategy**: Whether to use `MemorySaver` (fast, deterministic) or a real `SqliteSaver` on a temp file for integration tests

### 2. Test State Schema Integrity
- Generate tests that construct a minimal valid state dict and assert all required keys are present and correctly typed
- Assert that `messages` field uses `Annotated[list[BaseMessage], add_messages]` by invoking the graph twice and checking messages accumulate (not overwrite)
- Assert that no field accepts `None` unless it is declared `Optional`

```python
import pytest
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver

def test_message_reducer_appends_not_overwrites():
    """Messages must accumulate via add_messages, not be overwritten."""
    from my_agent.graph import build_graph

    graph = build_graph(checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": "test-001"}}

    graph.invoke({"messages": [HumanMessage(content="hello")]}, config)
    state = graph.get_state(config)
    assert len(state.values["messages"]) >= 1

    graph.invoke({"messages": [HumanMessage(content="follow-up")]}, config)
    state2 = graph.get_state(config)
    # Reducer must append — not reset
    assert len(state2.values["messages"]) > len(state.values["messages"])
```

### 3. Verify Bounds Enforcement
- Invoke the graph `max_messages + 10` times with the same `thread_id` and assert `len(state["messages"]) <= max_messages` after each step
- Assert that `iteration_count` increments monotonically and is bounded by graph logic (does not overflow `int`)
- Test the boundary condition at exactly `max_messages` — state must not exceed limit on the next invocation

```python
def test_message_bound_at_max_messages():
    """State must not grow past max_messages even after many invocations."""
    from my_agent.graph import build_graph
    from my_agent.config import MAX_MESSAGES

    graph = build_graph(checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": "bound-test"}}

    for i in range(MAX_MESSAGES + 10):
        graph.invoke({"messages": [HumanMessage(content=f"msg {i}")]}, config)

    final_state = graph.get_state(config)
    msg_count = len(final_state.values["messages"])
    assert msg_count <= MAX_MESSAGES, (
        f"State exceeded max_messages bound: {msg_count} > {MAX_MESSAGES}"
    )
```

### 4. Test Checkpointing Round-Trip (L3+)
- Compile the graph with a `SqliteSaver` on a `tmp_path` fixture and invoke once; then recompile with the SAME `SqliteSaver` and invoke again with the same `thread_id` — second invocation must see first invocation's state
- Assert `get_state_history()` is non-empty after first invocation
- Simulate crash recovery: create graph, invoke, GC the graph object, recreate graph from same checkpointer, invoke again — state must persist

```python
import tempfile
from pathlib import Path
from langgraph.checkpoint.sqlite import SqliteSaver

def test_checkpoint_persists_across_graph_instances(tmp_path):
    """State must survive graph object recreation (simulates crash recovery)."""
    from my_agent.graph import build_graph

    db_path = str(tmp_path / "test_checkpoints.db")
    thread_config = {"configurable": {"thread_id": "persist-test"}}

    with SqliteSaver.from_conn_string(db_path) as cp:
        g1 = build_graph(checkpointer=cp)
        g1.invoke({"messages": [HumanMessage(content="first")]}, thread_config)

    with SqliteSaver.from_conn_string(db_path) as cp:
        g2 = build_graph(checkpointer=cp)
        state = g2.get_state(thread_config)
        assert len(state.values["messages"]) >= 1, "State lost after checkpoint DB reopen"
```

### 5. Generate Test Report
- Run `pytest -v --tb=short` on the generated test suite and capture output
- Flag any non-deterministic failures (tests that fail on re-run without state changes) — these indicate missing state isolation between tests
- Report: total pass/fail, any missing checkpoint fixtures, boundary conditions exercised

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide file path, test scope, and maturity level. |
| `state-specialist-constitution.md` not found | Stop. Restore constitution to repo root before continuing. |
| Non-deterministic state in tests | Ensure each test uses a unique `thread_id`; never share `MemorySaver` instances across tests. |
| Missing checkpoint fixtures for L3 tests | Scaffold `tmp_path`-based `SqliteSaver` fixture; do not rely on real DB for unit tests. |
| Boundary condition fails at exactly `max_messages` | Check off-by-one in trim logic — slice should be `[-max_messages:]`, not `[-(max_messages-1):]`. |
| `get_state_history()` returns empty list in checkpoint test | Checkpointer not passed to `compile()`; verify fixture passes same `checkpointer` instance to both graph instances. |

## Examples

**Example 1**: `/test-state-specialist graph/state.py bounds L2`
Generate pytest suite: invoke graph 60 times (MAX_MESSAGES=50), assert final message count is exactly 50. Confirm `iteration_count` increments each step. All tests use isolated `MemorySaver` per test function.

**Example 2**: `/test-state-specialist agents/support_agent/ full L3`
Generate full suite: schema integrity, bounds (max=50), checkpoint round-trip with `SqliteSaver` on `tmp_path`, crash recovery simulation. Report: 12 tests, 0 failures, boundary condition at `max_messages+1` verified.
