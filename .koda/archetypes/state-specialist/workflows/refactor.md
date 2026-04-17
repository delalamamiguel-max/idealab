---
description: Improve state schema typing, bounds, and memory management (State Specialist)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **File path**: Path to the existing state module (e.g., `graph/state.py`) and/or the StateGraph compile site
- **Refactor goal**: One of `typing` | `bounds` | `checkpointer-upgrade` | `full` — scopes what to change
- **Target maturity level**: L1–L4 — determines whether a checkpointer migration is required alongside schema changes
- **Downstream consumers**: List any nodes or tests that depend on specific field names — these are the blast radius of a TypedDict rename

### 2. Audit the Existing Schema
- Enumerate every field in the current `TypedDict`; classify each as: fully-typed, weakly-typed (`Any`/`dict`), or untyped
- Identify fields that have grown beyond their original intent (e.g., a `context: str` that is now JSON-encoded structured data)
- List any fields that have been removed in code but still exist in live checkpoints — these are a schema mismatch waiting to blow up on resume

```python
from typing import Annotated, TypedDict, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

# BEFORE refactor — common antipatterns
class LegacyState(TypedDict):
    messages: list                  # no reducer → overwrites
    context: dict                   # untyped → silent corruption
    metadata: str                   # should be structured data
    user_id: str                    # PII stored in plain state

# AFTER refactor — clean, typed, bounded
class RefactoredState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]  # reducer + typed
    context: Optional[list[str]]                          # structured, nullable
    metadata: Optional[dict[str, str]]                    # typed KV pairs
    iteration_count: int                                  # bounded by graph logic
    error: Optional[str]                                  # explicit error channel
    # user_id removed — passed in config, not state (avoids PII in checkpoints)
```

### 3. Implement Type and Bounds Improvements
- Replace bare `list` message fields with `Annotated[list[BaseMessage], add_messages]`
- Replace `dict` fields with typed `dict[K, V]` or a nested `TypedDict`
- Add a `trim_messages` node if `max_messages` enforcement was previously absent
- Remove any fields that should live in `config["configurable"]` rather than state (e.g., user identifiers, environment flags)

```python
# Bounded message reducer with custom trim logic
from typing import Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

MAX_MESSAGES = 50

def bounded_add_messages(left: list, right: list) -> list:
    """add_messages semantics with a hard cap — oldest messages pruned first."""
    merged = add_messages(left, right)
    if len(merged) > MAX_MESSAGES:
        return merged[-MAX_MESSAGES:]
    return merged

class BoundedState(TypedDict):
    messages: Annotated[list[BaseMessage], bounded_add_messages]
    current_step: str
    iteration_count: int
    error: Optional[str]
```

### 4. Handle Breaking TypedDict Field Changes and Migrations
- A **breaking change** is any field rename, type narrowing, or removal that affects live checkpoint data in SQLite/PostgreSQL
- For each breaking change: write a migration script that loads existing checkpoints, transforms the state dict, and persists the result via `graph.update_state()`
- For non-breaking additions (new optional fields with defaults): no migration needed — missing keys will be `None` on next resume

```python
# Migration: rename legacy field 'context' -> 'context_items'
def migrate_thread(graph, thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    current = graph.get_state(config)
    if "context" in current.values and "context_items" not in current.values:
        graph.update_state(config, {
            "context_items": current.values["context"],
            "context": None   # keep field if schema still has it, else omit
        })
```

### 5. Upgrade Checkpointer if Maturity Level Changed
- L2 → L3 upgrade: swap `MemorySaver` for `SqliteSaver`; state will NOT carry over automatically — migrations must seed the new DB
- L3 → L4 upgrade: move to `PostgresSaver`, enable encryption at rest, add immutable audit log
- Recompile the graph with the new checkpointer and run smoke test with the same `thread_id`

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide file path, refactor goal, and target maturity level. |
| `state-specialist-constitution.md` not found | Stop. Restore constitution to repo root before continuing. |
| Breaking TypedDict field change with live checkpoint data | Write and run a migration script using `graph.update_state()` before redeployment; never drop columns without migrating. |
| Reducer incompatibility after custom reducer swap | Validate new reducer produces identical output for existing test fixtures before merging. |
| Migration needed but no thread inventory available | Query the checkpoint DB directly for all distinct `thread_id` values before running migration. |
| `update_state()` raises validation error | Target checkpoint state is incompatible with the updated schema — check for stricter Pydantic types introduced in refactor. |

## Examples

**Example 1**: `/refactor-state-specialist graph/state.py typing L2`
Audit all fields: replace `list` with `Annotated[list[BaseMessage], add_messages]`, replace `dict` context with `Optional[list[str]]`. No checkpointer migration needed (L2 = MemorySaver, in-memory only).

**Example 2**: `/refactor-state-specialist agents/support/ bounds+checkpointer-upgrade L3`
Add `bounded_add_messages` reducer capped at 50 messages. Swap `MemorySaver` → `SqliteSaver`. Write migration to seed SQLite with existing test thread fixtures. Validate old `thread_id` resumes correctly post-migration.
