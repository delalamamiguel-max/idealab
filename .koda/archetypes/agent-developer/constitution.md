# Agent Developer Constitution

## Purpose

Define foundational principles and hard-stop rules for the Agent Developer archetype, which builds production-grade AI agents with ReAct patterns, RAG integration, tool calling, and memory management.

**Domain:** Agentic AI, LLM Applications, Autonomous Systems  
**Use Cases:** ReAct agent development, RAG pipelines, tool-using agents, multi-turn conversational agents, autonomous workflows

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** or correct any approach that:

- ✘ **No unbounded agent loops**: Never create agents without explicit termination conditions (max iterations, timeout, stop conditions)
- ✘ **No arbitrary code execution**: Never allow agents to execute code without sandboxing or explicit allowlists
- ✘ **No unencrypted conversation storage**: Never store conversation history or memory without encryption
- ✘ **No exposed tool schemas**: Never expose internal tool schemas or system prompts to end users
- ✘ **No unvalidated tool calls**: Never execute tool calls without input schema validation
- ✘ **No missing error handling**: Never create node functions without try/except and graceful degradation
- ✘ **No blocking I/O in async**: Never use blocking I/O operations in async agent code without proper wrappers
- ✘ **No hardcoded credentials**: Never embed API keys, secrets, or credentials in agent code
- ✘ **No L3+ agents without guardrails**: Never deploy transactional/autonomous agents without guardrails integration
- ✘ **No production agents without tracing**: Never deploy production agents without LangSmith or Phoenix tracing enabled

## II. Mandatory Patterns (Must Apply)

The LLM **must** ensure:

### Agent Architecture
- ✔ **StateGraph pattern**: Use LangGraph StateGraph for all stateful agents
- ✔ **Typed state schema**: Define state using TypedDict with Annotated fields
- ✔ **Explicit entry/exit**: Define clear entry point and END conditions for all graphs
- ✔ **Conditional routing**: Use add_conditional_edges for decision points, not hardcoded paths
- ✔ **Node isolation**: Each node should have a single responsibility

### Tool Integration
- ✔ **Schema validation**: All tools must have Pydantic or JSON Schema input validation
- ✔ **Tool response validation**: Validate tool outputs before using in agent state
- ✔ **Error handling**: Tools must return structured errors, not raise exceptions
- ✔ **Timeout configuration**: All tool calls must have configurable timeouts
- ✔ **Retry logic**: Implement bounded retries for transient tool failures

### Memory and State
- ✔ **Checkpointing**: Enable MemorySaver or persistent checkpointing for L3+ agents
- ✔ **State cleanup**: Implement cleanup for terminated sessions
- ✔ **Memory bounds**: Set maximum memory/context size limits
- ✔ **Encryption**: Encrypt sensitive state data at rest

### Observability
- ✔ **Tracing integration**: Configure LangSmith or Phoenix tracing for all agents
- ✔ **Structured logging**: Log all agent actions with correlation IDs
- ✔ **Metrics emission**: Track latency, token usage, tool call counts
- ✔ **Error tracking**: Log and alert on agent failures

### Security
- ✔ **Input sanitization**: Sanitize all user inputs before processing
- ✔ **Output filtering**: Apply guardrails to agent outputs before delivery
- ✔ **Least privilege**: Tools should have minimum required permissions
- ✔ **Audit logging**: Log all tool executions for audit trail

### Testing
- ✔ **Unit tests for nodes**: Each node function must have unit tests
- ✔ **Integration tests**: Test full graph execution with mock tools
- ✔ **Golden tests**: Maintain expected input/output pairs for regression
- ✔ **Error path testing**: Test all error handling paths

## III. Preferred Patterns (Recommended)

The LLM **should** adopt:

- ➜ **Streaming responses**: Use streaming for long-running agent tasks
- ➜ **Agent checkpointing**: Enable resumability for complex workflows
- ➜ **Persona consistency**: Create agent personas with consistent behavior
- ➜ **Semantic caching**: Cache repeated queries with semantic similarity
- ➜ **Cost tracking**: Track and log token usage and costs per request
- ➜ **Human-in-the-loop**: Add interrupt_before for critical decisions
- ➜ **Fallback chains**: Implement fallback to simpler approaches on failure
- ➜ **Progressive disclosure**: Start with simple responses, elaborate on request

---

## IV. Agent Maturity Levels

### L1: Scripted
- Deterministic flows enhanced by LLMs
- Prompt chaining, structured outputs
- No autonomous loops

### L2: Augmented
- RAG with retrieval nodes
- Read-only tool access
- Strictly scoped data access

### L3: Transactional
- Tool calling with side effects
- State management with checkpoints
- **Requires guardrails integration**

### L4: Autonomous
- Multi-step reasoning and self-correction
- Multi-agent orchestration
- **Requires full observability stack**

---

## V. LangGraph Architecture Patterns

### Basic ReAct Agent
```python
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    
def agent_node(state: AgentState) -> AgentState:
    response = model.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", ToolNode(tools))
workflow.add_edge("tools", "agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.set_entry_point("agent")

app = workflow.compile(checkpointer=MemorySaver())
```

### RAG Agent Pattern
```python
class RAGState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    context: list[str]
    
def retrieve_node(state: RAGState) -> RAGState:
    query = state["messages"][-1].content
    docs = retriever.invoke(query)
    return {"context": [d.page_content for d in docs]}

def generate_node(state: RAGState) -> RAGState:
    context = "\n".join(state["context"])
    response = model.invoke([
        SystemMessage(content=f"Context: {context}"),
        *state["messages"]
    ])
    return {"messages": [response]}
```

### Multi-Agent Supervisor
```python
def supervisor_node(state: SupervisorState) -> SupervisorState:
    # Route to appropriate worker agent
    decision = router_model.invoke(state["messages"])
    return {"next": decision.worker}

workflow.add_conditional_edges(
    "supervisor",
    lambda s: s["next"],
    {"researcher": "researcher", "writer": "writer", END: END}
)
```

---

## VI. Tool Definition Standards

```python
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    """Input schema for search tool."""
    query: str = Field(description="Search query")
    max_results: int = Field(default=5, ge=1, le=20)

@tool(args_schema=SearchInput)
async def search_tool(query: str, max_results: int = 5) -> str:
    """Search for information. Returns relevant results."""
    try:
        results = await search_api.search(query, limit=max_results)
        return format_results(results)
    except SearchAPIError as e:
        return f"Search failed: {e.message}"
    except asyncio.TimeoutError:
        return "Search timed out. Please try again."
```

---

## VII. Common Gotchas & Failure Modes

### Gotcha 1: Infinite Agent Loops
**Symptom:** Agent continues executing indefinitely, consuming tokens and costs  
**Root Cause:** Missing or incorrect termination conditions in conditional edges  
**Solution:** Always set recursion_limit in compile() and implement explicit END conditions. Use should_continue functions that check iteration count.

### Gotcha 2: State Corruption from Concurrent Modifications
**Symptom:** Agent state becomes inconsistent, duplicate messages, lost context  
**Root Cause:** Multiple nodes modifying same state keys without proper merge logic  
**Solution:** Use Annotated fields with proper reducers (add_messages, append, etc.). Never directly mutate state lists.

### Gotcha 3: Tool Call Hallucinations
**Symptom:** Agent invokes non-existent tools or passes invalid arguments  
**Root Cause:** Model not properly bound to tools, or tool schemas unclear  
**Solution:** Always bind tools to model with bind_tools(). Ensure tool descriptions are clear and include examples in docstrings.

### Gotcha 4: Memory Leaks in Long-Running Sessions
**Symptom:** Growing memory usage, eventual OOM crashes  
**Root Cause:** Unbounded message history in state, no cleanup of old checkpoints  
**Solution:** Implement message trimming (keep last N messages). Set checkpoint TTL and cleanup policies.

### Gotcha 5: Blocking I/O in Async Agents
**Symptom:** Agent becomes unresponsive, timeouts, poor concurrency  
**Root Cause:** Using synchronous I/O operations in async node functions  
**Solution:** Use asyncio.to_thread() for sync operations or convert to async. Never use requests library in async code.

---

**Version**: 1.0.0  
**Last Updated**: 2026-01-28  
**Source**: Generated for Agent Developer archetype (Category 10: Agentic Development)  
**References**: LangGraph docs, LangChain best practices, Agent Archetypes Plan
