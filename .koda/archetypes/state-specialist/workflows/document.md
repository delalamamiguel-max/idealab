---
description: Generate state schema documentation with field descriptions (State Specialist)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **File path**: Module(s) containing `TypedDict` state definitions and the `StateGraph` compile site
- **Doc scope**: One of `fields` | `reducers` | `checkpointer` | `migration` | `full` — determines depth of generated docs
- **Output format**: `markdown` | `docstring` | `both` — inline docstrings vs standalone `.md` reference page
- **Schema version**: Current `schema_version` string (from `env-config.yaml`) — required for migration guide headers

### 2. Generate Field Reference Table
- For each field in the `TypedDict`, extract: name, Python type annotation, reducer function (if `Annotated`), nullability, and any `# comment` from source
- Flag any field that lacks a type annotation — these are documentation gaps AND constitution violations
- Flag any field missing inline field comments — these must be documented at the call-out level

```python
from typing import Annotated, TypedDict, Optional, get_type_hints
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class SupportAgentState(TypedDict):
    """State schema for the support agent (schema_version: 1.0.0)."""

    messages: Annotated[list[BaseMessage], add_messages]
    """Conversation history. Reducer: add_messages (appends, deduplicated by message ID).
    Bounded to max_messages=50 by the trim_state cleanup node."""

    current_step: str
    """Current execution node name. Updated by each node on entry."""

    context: Optional[list[str]]
    """Retrieved context chunks from knowledge base. None when no retrieval performed."""

    iteration_count: int
    """Number of graph iterations completed in this session. Used for loop detection."""

    error: Optional[str]
    """Error message from the most recent failed node. None when last operation succeeded."""
```

### 3. Document Reducers and Merge Semantics
- For each `Annotated` field, document the reducer function: what it does on merge, whether it is idempotent, and edge cases (duplicate message IDs, conflict on concurrent updates)
- Distinguish between LangGraph built-in reducers (`add_messages`) and custom reducers — custom ones must include a docstring explaining the merge contract
- Note which fields use the default `replace` reducer (no annotation) — these are overwritten on every node return, with no merge

```python
# Reducer documentation pattern — include in generated docs
"""
## Field: messages
- **Type**: `Annotated[list[BaseMessage], add_messages]`
- **Reducer**: `add_messages` (LangGraph built-in)
- **Merge behavior**: Appends new messages; deduplicates by message ID (idempotent on re-delivery)
- **Edge case**: Tool messages without a matching tool call ID will raise during merge — validate upstream
- **Bound**: Trimmed to `MAX_MESSAGES=50` by the `trim_state` cleanup node on every graph cycle
- **Checkpointed**: Yes — persisted on every state update for L3+ agents

## Field: current_step
- **Type**: `str`
- **Reducer**: `replace` (default — overwrites on every update)
- **Merge behavior**: Last-write-wins; no merge semantics
- **Checkpointed**: Yes — used for crash recovery to determine resume point
"""
```

### 4. Document Checkpointer Configuration
- Record which checkpointer is used (`MemorySaver` / `SqliteSaver` / `PostgresSaver`), the DB path or connection string pattern, and the `thread_id` derivation strategy
- Document the `checkpoint_write_timeout_ms` and `state_cleanup_interval_seconds` from `env-config.yaml`
- For L3+: document the retention policy, cleanup trigger, and how stale threads are identified

### 5. Generate Migration Guide
- For any schema version bump (e.g., `1.0.0` → `1.1.0`): list every field change (added/removed/renamed/retyped)
- Classify each change as breaking vs non-breaking; provide migration snippet for each breaking change
- Stamp the guide with `schema_version` from `env-config.yaml` and the current date

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide file path, doc scope, output format, and schema version. |
| `state-specialist-constitution.md` not found | Stop. Restore constitution to repo root before continuing. |
| Missing field annotations in TypedDict | Flag each unannotated field in the report as a constitution violation; generate placeholder docs with `[TYPE MISSING]` marker. |
| Outdated checkpointer docs (docs reference MemorySaver but code uses SqliteSaver) | Re-read the compile site; regenerate checkpointer section from source of truth — never document from memory. |
| Schema version undocumented (not in env-config.yaml or TypedDict docstring) | Halt migration guide generation; prompt user to declare `schema_version` in `env-config.yaml` before proceeding. |
| Custom reducer has no docstring | Generate a stub reducer doc with merge contract TBD; flag as a documentation debt item in the report. |

## Examples

**Example 1**: `/document-state-specialist graph/state.py full markdown`
Generate a complete `STATE_REFERENCE.md` with: field table (5 fields, 2 flagged as missing annotations), reducer docs for `messages` (add_messages) and `context` (replace), checkpointer section (SqliteSaver, 30-day retention), migration guide stub for v1.0.0 → v1.1.0.

**Example 2**: `/document-state-specialist agents/support_agent/ checkpointer+migration docstring`
Read compile site to extract `SqliteSaver` config. Generate inline docstrings for the `TypedDict` class documenting checkpointer, `thread_id` strategy, and breaking change from `context: dict` → `context: list[str]` introduced in v1.1.0.
