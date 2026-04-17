---
description: Fix state corruption, memory leaks, and checkpoint issues (State Specialist)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **File path or agent name**: Path to the state module (e.g., `graph/state.py`) or agent directory
- **Issue description**: Observed failure to reproduce (e.g., `"messages list grows without bound"`, `"KeyError on resume"`)
- **Maturity level**: L1–L4 — determines which checkpointing assertions apply
- **Environment**: dev vs. production — determines whether `MemorySaver` or a persistent DB is the expected checkpointer

### 2. Inspect the State Schema
- Read the `TypedDict` definition and flag any untyped `dict` or bare `Any` fields — these silently absorb corrupt data without raising errors
- Confirm message fields use `Annotated[list[BaseMessage], add_messages]`; a plain `list` **overwrites** on each update rather than appending
- Check for mutable defaults (`field: list = []`) — Python shares the same list object across all TypedDict instances

```python
from typing import Annotated, TypedDict, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

# WRONG — overwrites on each update (no reducer), silently loses history
class BrokenState(TypedDict):
    messages: list          # plain list, no reducer
    context: dict           # untyped; silently accepts any garbage

# CORRECT — reducer merges safely, all fields explicitly typed
class HealthyState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]  # appends, never overwrites
    context: Optional[list[str]]                          # nullable, not bare dict
    iteration_count: int
    error: Optional[str]
```

### 3. Diagnose the Specific Failure Class
- **State schema mismatch**: A schema migration added/removed fields but old checkpoints predate the change — manifests as `KeyError` or Pydantic `ValidationError` on graph resume; fix with `graph.update_state()` migration before redeployment
- **Unbounded state growth**: Run `len(state["messages"])` after each node invocation; if it exceeds `max_messages`, the trim node is either missing or miswired in the graph edge order
- **Checkpoint desync**: Compare the `thread_id` passed at invocation time with what the original run used — mismatched IDs silently start a brand-new empty state

```python
# Diagnostic helper — log field sizes at every node boundary
def debug_state_size(state: HealthyState) -> HealthyState:
    for key, val in state.items():
        n = len(val) if isinstance(val, (list, str, dict)) else "scalar"
        print(f"  [debug] {key}: {n}")
    return state

# Diagnostic helper — confirm checkpoint history before attempting resume
from langgraph.checkpoint.sqlite import SqliteSaver
from pathlib import Path

db_path = str(Path(AGENT_DATA) / agent_name / "checkpoints.db")
with SqliteSaver.from_conn_string(db_path) as cp:
    history = list(graph.get_state_history(
        {"configurable": {"thread_id": thread_id}}
    ))
    print(f"✓ Checkpoint entries found: {len(history)}")
    if not history:
        print("✗ No checkpoints found — check thread_id consistency")
```

### 4. Apply the Fix
- **Unbounded growth**: Add a `trim_state` cleanup node that slices `messages[-max_messages:]` and insert it on the edge just before the graph's terminal `END` node
- **Schema mismatch**: Iterate all known `thread_id` values and call `graph.update_state(config, {"new_field": default_value})` on each before redeployment
- **Checkpoint desync**: Derive `thread_id` deterministically (e.g., hash of `user_id + session_id`) — never generate `uuid4()` inline at invocation time

```python
# Fix: bounded message history enforcement
MAX_MESSAGES = 50

def trim_state(state: HealthyState) -> dict:
    """Enforce message bound — returns partial update dict for LangGraph merge."""
    msgs = state["messages"]
    if len(msgs) > MAX_MESSAGES:
        return {"messages": msgs[-MAX_MESSAGES:], "iteration_count": state["iteration_count"]}
    return {}

# Wire into graph:
# workflow.add_node("trim", trim_state)
# workflow.add_edge("last_real_node", "trim")
# workflow.add_edge("trim", END)
```

### 5. Add Regression Test and Validate
- Invoke the graph `max_messages + 5` times with the same `thread_id` and assert `len(final_state["messages"]) <= max_messages`
- For checkpoint fixes: invoke twice sequentially with the same `thread_id` and assert the second invocation's state includes the first invocation's output
- Run the full test suite to confirm trim logic and migration scripts introduce no regressions

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide file path, observed issue description, and maturity level. |
| `state-specialist-constitution.md` not found | Stop. Restore constitution to repo root before continuing. |
| State schema mismatch after migration | Call `graph.update_state(config, {new_field: default})` for every known thread before redeployment. |
| Unbounded state growth past `max_messages` | Add `trim_state` cleanup node enforcing `messages[-max_messages:]`; insert before graph `END` edge. |
| Checkpoint desync (`thread_id` mismatch at call sites) | Audit all `invoke()` call sites; enforce deterministic ID derivation — ban inline `uuid4()` at invocation time. |
| `get_state_history()` returns empty list | Checkpointer not attached at compile time, or `thread_id` drifted. Verify `workflow.compile(checkpointer=...)`. |

## Examples

**Example 1**: `/debug-state-specialist graph/state.py "messages list grows unbounded after 25 turns" L2`
Inspect message field — replace bare `list` with `Annotated[list[BaseMessage], add_messages]`. Add a `trim_state` node wired before `END`. Verify `len(state["messages"]) <= 50` in regression test.

**Example 2**: `/debug-state-specialist support_agent/ "KeyError: user_intent on thread resume" L3`
Schema migration added `user_intent` field but SQLite checkpoints predate it. Fix: iterate all thread IDs, call `graph.update_state(config, {"user_intent": None})` for each, then redeploy.
