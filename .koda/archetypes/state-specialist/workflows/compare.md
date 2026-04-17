---
description: Compare state schema approaches for efficiency and maintainability (State Specialist)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Schema A and Schema B**: Either two file paths (e.g., `graph/state_v1.py`, `graph/state_v2.py`) or two named approaches (e.g., `"minimal"` vs `"full"`)
- **Comparison dimension**: One of `memory` | `complexity` | `checkpointer-fit` | `migration-cost` | `all`
- **Maturity level context**: L1–L4 — determines whether persistent checkpointer overhead factors into the evaluation
- **Workload profile**: Expected message volume and session lifetime — a schema optimal for L2 short sessions may be wrong for L4 long-running threads

### 2. Enumerate Schema Differences
- List every field present in one schema but absent in the other — these are migration cost drivers
- Identify reducer differences (e.g., `add_messages` vs custom bounded reducer) — different reducers yield different checkpoint sizes for the same conversation
- Note type precision differences (e.g., `dict` vs `dict[str, str]`) — wider types silently accept more data and bloat checkpoints

```python
from typing import Annotated, TypedDict, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

# Schema A: minimal — only what the graph strictly needs
class MinimalState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    error: Optional[str]
    # Total checkpoint overhead: O(messages) only

# Schema B: full — includes rich context and metadata
class FullState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    context: list[str]              # grows with conversation depth
    metadata: dict[str, str]        # unbounded KV store
    user_preferences: dict[str, str]
    session_tags: list[str]
    iteration_count: int
    error: Optional[str]
    # Total checkpoint overhead: O(messages) + O(context) + O(metadata)
```

### 3. Measure Memory and Checkpoint Size
- For each schema, construct a representative state at N=10, N=50, and N=100 messages and serialize with `pickle` or `json` to estimate checkpoint payload size
- Compare the checkpoint write latency by timing `SqliteSaver` round-trips with each schema — heavier schemas have higher write latency per `invoke()` call
- For in-memory (`MemorySaver`), compare peak heap usage using `sys.getsizeof` on the state dict at max depth

```python
import sys
import json
from langchain_core.messages import HumanMessage, AIMessage

def estimate_checkpoint_size(state: dict, label: str) -> None:
    """Estimate serialized size of a state snapshot."""
    serialized = json.dumps(
        {k: str(v) for k, v in state.items()},  # rough approximation
        default=str
    )
    print(f"[{label}] Estimated checkpoint bytes: {len(serialized.encode())}")
    print(f"[{label}] In-memory size (sys.getsizeof): {sys.getsizeof(state)} bytes")

# Populate sample states at N=50 messages
msgs = [HumanMessage(content=f"msg {i}") for i in range(50)]
minimal = {"messages": msgs, "error": None}
full = {"messages": msgs, "context": ["ctx"] * 50, "metadata": {str(i): str(i) for i in range(50)},
        "user_preferences": {}, "session_tags": [], "iteration_count": 50, "error": None}

estimate_checkpoint_size(minimal, "MinimalState")
estimate_checkpoint_size(full, "FullState")
```

### 4. Score Each Schema on Four Axes
- **Memory efficiency**: Smaller serialized size → fewer I/O cycles per checkpoint → lower latency at scale
- **Type safety**: Fully-typed schemas catch bugs at schema validation time; `dict`/`Any` fields push errors to runtime
- **Migration cost**: Schemas with fewer fields and no renames are cheaper to migrate between agent versions
- **Checkpointer fit**: Minimal schemas pair better with `MemorySaver` (L2); rich schemas are worth the overhead only when context is genuinely reused across sessions (L3+)

### 5. Produce Recommendation
- State which schema wins on each axis; declare an overall winner for the given workload profile and maturity level
- If performance is tied across all axes (within 10%), call it a tie only after exhausting differentiation — note where the tie breaks under load scaling
- Provide a concrete migration path if recommending the non-incumbent schema

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide two schema paths/names, comparison dimension, and maturity level. |
| `state-specialist-constitution.md` not found | Stop. Restore constitution to repo root before continuing. |
| Incompatible state schemas (different required fields) | Flag as incompatible; produce side-by-side field diff and list breaking changes before asserting a winner. |
| Insufficient state samples for size estimation | Generate synthetic states at N=10/50/100 messages using `HumanMessage`/`AIMessage` stubs; document sample generation method. |
| Tied performance across all axes | Expand sample size to N=200; if still tied, recommend minimal schema as default (less migration risk). |
| `update_state()` raises validation error during migration test | Schema B has stricter types than A accepted — document as a migration risk in the recommendation. |

## Examples

**Example 1**: `/compare-state-specialist "MinimalState vs FullState" memory L3`
At N=50 messages, `MinimalState` checkpoint is ~4 KB vs `FullState` at ~18 KB. Recommend `MinimalState` for L3 with external context store (Redis/DB) if context recall is needed across sessions.

**Example 2**: `/compare-state-specialist graph/state_v1.py graph/state_v2.py all L2`
`v2` adds 3 fields (migration cost: low — all optional with defaults). `v2` is 12% heavier in memory but provides better type safety. Recommend `v2` for its type safety improvement; no migration needed for L2 (MemorySaver, no persistent state).
