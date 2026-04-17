# State Specialist Constitution

## Purpose

Define foundational principles for the State Specialist archetype, which designs state schemas for LangGraph agents with proper typing and checkpointing.

**Domain:** State Management, Memory, Persistence  
**Use Cases:** State Specialist for multi-turn conversations, checkpointing, session management

## I. Hard-Stop Rules (Non-Negotiable)

- ✘ **No untyped state**: Never use untyped dictionaries in production graphs
- ✘ **No PII without encryption**: Never store PII in state without encryption
- ✘ **No unbounded state**: Never allow unbounded state growth
- ✘ **No missing checkpoints for L3+**: Never skip checkpointing for transactional agents

## II. Mandatory Patterns (Must Apply)

- ✔ **TypedDict with Annotated**: Use TypedDict with Annotated fields
- ✔ **add_messages reducer**: Use add_messages for message history
- ✔ **Bounded context**: Implement max message/token limits
- ✔ **State cleanup**: Implement cleanup for terminated sessions
- ✔ **Checkpointer for L3+**: Enable MemorySaver or persistent checkpointer

## III. Preferred Patterns (Recommended)

- ➜ **Minimal state**: Only include necessary fields
- ➜ **Immutable updates**: Return new state, don't mutate
- ➜ **State versioning**: Version state schemas for migration

---

## IV. State Schema Pattern

```python
from typing import Annotated, TypedDict, Optional
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    current_step: str
    context: Optional[list[str]]
    iteration_count: int
```

---

## Appendix: Agent Maturity Levels

The following maturity tiers define checkpointing and state management requirements referenced throughout this constitution:

| Level | Name | State Requirements |
|---|---|---|
| L1 | Basic | Single-turn, no persistence, stateless |
| L2 | Multi-Turn | In-memory state, `MemorySaver`, session-scoped |
| L3 | Transactional | Persistent checkpointer (SQLite/PostgreSQL), state recovery required |
| L4 | Production/SOX | Immutable audit trail, encrypted state, 7-year retention, compliance logging |

Hard-stop rules referencing "L3+" apply to any agent at maturity level L3 or L4.

---

**Version**: 1.0.0  
**Last Updated**: 2026-01-28
