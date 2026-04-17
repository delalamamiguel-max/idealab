---
description: Design state schemas for LangGraph agents with typing, checkpointing, and memory (State Specialist)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Agent name**: Name of the agent
- **State fields**: Required state fields
- **Memory type**: none | conversation | persistent
- **Maturity level**: L1-L4

### 2. Generate State Schema

```python
from typing import Annotated, TypedDict, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class {AgentName}State(TypedDict):
    """State schema for {agent_name}."""
    
    # Message history with automatic merging
    messages: Annotated[list[BaseMessage], add_messages]
    
    # Processing state
    current_step: str
    iteration_count: int
    
    # Custom fields
    {custom_fields}
    
    # Error tracking
    error: Optional[str]
```

### 3. Add Checkpointing (L3+)

Choose checkpointer based on `memory_type` from Step 1:

**In-session only (memory_type = "conversation" or "none"):**
```python
from langgraph.checkpoint.memory import MemorySaver
checkpointer = MemorySaver()
graph = workflow.compile(checkpointer=checkpointer)
```

**Cross-session / persistent (memory_type = "persistent"):**
```python
from langgraph.checkpoint.sqlite import SqliteSaver

# SQLite — good for single-process persistent state
with SqliteSaver.from_conn_string("checkpoints.db") as checkpointer:
    graph = workflow.compile(checkpointer=checkpointer)

# PostgreSQL — good for multi-process / production
# from langgraph.checkpoint.postgres import PostgresSaver
# checkpointer = PostgresSaver.from_conn_string(os.environ["DATABASE_URL"])
# graph = workflow.compile(checkpointer=checkpointer)
```

> ⚠️ **Hard stop**: Never use `MemorySaver` when `memory_type = "persistent"` — state will be lost on every restart.

### 4. Add Rollback Support

Rollback to a previous checkpoint using LangGraph's state history API:

```python
config = {"configurable": {"thread_id": "{thread_id}"}}

# List all saved checkpoints for this thread
history = list(graph.get_state_history(config))
# history[0] is most recent, history[-1] is oldest

# Roll back to a specific checkpoint (e.g., 2 steps ago)
target_state = history[2]
graph.update_state(config, target_state.values)

# Resume execution from the rolled-back state
result = graph.invoke(None, config)
```

**Checklist for rollback:**
- [ ] Checkpointer is NOT `MemorySaver` (rollback requires persistent storage)
- [ ] `thread_id` is consistent across the session
- [ ] `get_state_history()` returns non-empty list before attempting rollback

### 5. Validate

```bash
# Test that state persists across graph invocations (same thread_id)
python3 -c "
from langgraph.checkpoint.sqlite import SqliteSaver
# Initialize graph with persistent checkpointer
# Invoke twice with same thread_id — second invocation should see first invocation's state
print('Run state persistence test manually with your graph')
"
```

**Checklist:**
- [ ] State TypedDict uses `Annotated[list[BaseMessage], add_messages]` for message fields
- [ ] `MemorySaver` used only when `memory_type != persistent`
- [ ] `SqliteSaver` or `PostgresSaver` used when `memory_type = persistent`
- [ ] Rollback works: `get_state_history()` returns history; `update_state()` + re-invoke succeeds
- [ ] No untyped `dict` fields in state schema

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide agent name, state fields, memory type, and maturity level. |
| `state-specialist-constitution.md` not found | Stop. Ensure file is present at repo root. |
| `langgraph` not installed | Run `pip install langgraph`. |
| `MemorySaver` used but state lost on restart | `memory_type` requires persistent storage. Switch to `SqliteSaver` or `PostgresSaver`. |
| `get_state_history()` returns empty list | Checkpointer was not attached at compile time, or `thread_id` is inconsistent. Verify `graph.compile(checkpointer=...)`. |
| `update_state()` raises validation error | Target checkpoint state is incompatible with current schema. Check for schema migrations between versions. |

## Examples
**Example**: `/scaffold-state-specialist support-agent "context: list[str], user_id: str" conversation L3`
