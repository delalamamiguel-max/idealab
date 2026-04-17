---
description: Build production-grade AI agents with ReAct, RAG, tools, and memory using LangGraph (Agent Developer)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Environment Setup

// turbo
Verify LangGraph/LangChain environment:
- Python 3.10+
- langchain>=0.1.0
- langgraph>=0.0.20
- langsmith (optional but recommended)
Run the cross-platform environment validation utility for `agent-developer` in JSON mode and halt if `ENV_VALID` is false.

### 2. Load Configuration

- Read `agent-developer-constitution.md` for hard-stop rules
- Load `templates/env-config.yaml` for defaults

### 3. Parse Input

Extract from $ARGUMENTS:
- **Agent name**: Name for the agent (kebab-case)
- **Agent type**: basic | react | rag | multi-agent
- **Maturity level**: L1 | L2 | L3 | L4
- **Tools**: List of tools the agent needs
- **Memory**: none | conversation | persistent
- **SOX scope**: Whether SOX compliance is required

If incomplete, request:
```
Please provide:
1. Agent Name: (e.g., "customer-support-agent")
2. Agent Type: basic | react | rag | multi-agent
3. Maturity Level: L1 (scripted) | L2 (augmented) | L3 (transactional) | L4 (autonomous)
4. Tools: (e.g., "search, calculator, database")
5. Memory: none | conversation | persistent
6. SOX Scope: yes | no
```

### 4. Validate Requirements Against Maturity Level

**L1 (Scripted):**
- Simple chain, no tools required
- No guardrails required

**L2 (Augmented):**
- RAG or read-only tools
- Guardrails recommended

**L3 (Transactional):**
- Tools with side effects
- **Guardrails REQUIRED**
- Checkpointing REQUIRED

**L4 (Autonomous):**
- Multi-agent or self-correction
- **Full observability stack REQUIRED**
- **Guardrails REQUIRED**

### 5. Generate Agent Structure

Create the following directory structure:
```
{agent_name}/
├── graph/
│   ├── __init__.py
│   ├── state.py          # State schema
│   ├── nodes.py          # Node implementations
│   ├── edges.py          # Conditional routing
│   └── graph.py          # Compiled graph
├── tools/
│   ├── __init__.py
│   └── definitions.py    # Tool definitions
├── prompts/
│   └── system.md         # System prompt
├── config/
│   └── settings.py       # Configuration
├── tests/
│   ├── __init__.py
│   ├── test_nodes.py
│   └── test_graph.py
└── main.py               # Entry point
```

### 6. Generate Core Files

**6.1. State Schema (`graph/state.py`)**
```python
"""State schema for {agent_name}."""

from typing import Annotated, TypedDict, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """State for {agent_name} agent."""
    
    # Message history with automatic message merging
    messages: Annotated[list[BaseMessage], add_messages]
    
    # Current processing step for observability
    current_step: str
    
    # Tool execution results
    tool_results: dict[str, any]
    
    # Context for RAG (if applicable)
    context: Optional[list[str]]
    
    # Error tracking
    error: Optional[str]
    
    # Iteration counter for loop protection
    iteration_count: int
```

**6.2. Node Implementations (`graph/nodes.py`)**
```python
"""Node implementations for {agent_name}."""

import logging
from typing import Any
from langchain_core.messages import AIMessage, SystemMessage
from langchain_openai import ChatOpenAI

from .state import AgentState
from ..config.settings import settings

logger = logging.getLogger(__name__)

# Initialize model
model = ChatOpenAI(
    model=settings.MODEL_NAME,
    temperature=settings.TEMPERATURE,
)

async def agent_node(state: AgentState) -> dict[str, Any]:
    """Main agent reasoning node."""
    try:
        logger.info(f"Agent node processing, iteration {state.get('iteration_count', 0)}")
        
        # Build messages with system prompt
        messages = [
            SystemMessage(content=settings.SYSTEM_PROMPT),
            *state["messages"]
        ]
        
        # Add context if available (RAG)
        if state.get("context"):
            context_str = "\n".join(state["context"])
            messages.insert(1, SystemMessage(content=f"Context:\n{context_str}"))
        
        # Invoke model
        response = await model.ainvoke(messages)
        
        return {
            "messages": [response],
            "current_step": "agent",
            "iteration_count": state.get("iteration_count", 0) + 1,
            "error": None
        }
        
    except Exception as e:
        logger.error(f"Agent node error: {e}")
        return {
            "error": str(e),
            "current_step": "error"
        }

async def retrieval_node(state: AgentState) -> dict[str, Any]:
    """RAG retrieval node (if applicable)."""
    try:
        from ..tools.retriever import retriever
        
        # Get query from last message
        query = state["messages"][-1].content
        
        # Retrieve relevant documents
        docs = await retriever.ainvoke(query)
        context = [doc.page_content for doc in docs]
        
        logger.info(f"Retrieved {len(context)} documents")
        
        return {
            "context": context,
            "current_step": "retrieval"
        }
        
    except Exception as e:
        logger.error(f"Retrieval error: {e}")
        return {
            "error": str(e),
            "context": []
        }

async def tool_executor_node(state: AgentState) -> dict[str, Any]:
    """Execute tool calls from agent."""
    from langgraph.prebuilt import ToolNode
    from ..tools.definitions import tools
    
    tool_node = ToolNode(tools)
    return await tool_node.ainvoke(state)
```

**6.3. Conditional Edges (`graph/edges.py`)**
```python
"""Conditional edge logic for {agent_name}."""

from typing import Literal
from langchain_core.messages import AIMessage

from .state import AgentState
from ..config.settings import settings

def should_continue(state: AgentState) -> Literal["tools", "end", "error"]:
    """Determine next step after agent node."""
    
    # Check for errors
    if state.get("error"):
        return "error"
    
    # Check iteration limit (HARD STOP)
    if state.get("iteration_count", 0) >= settings.MAX_ITERATIONS:
        return "end"
    
    # Check for tool calls
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tools"
    
    return "end"

def should_retrieve(state: AgentState) -> Literal["retrieve", "agent"]:
    """Determine if retrieval is needed (for RAG agents)."""
    
    # Skip retrieval if context already exists
    if state.get("context"):
        return "agent"
    
    return "retrieve"
```

**6.4. Graph Compilation (`graph/graph.py`)**
```python
"""Compiled graph for {agent_name}."""

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from .state import AgentState
from .nodes import agent_node, tool_executor_node, retrieval_node
from .edges import should_continue, should_retrieve
from ..config.settings import settings

def create_graph():
    """Create and compile the agent graph."""
    
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_executor_node)
    
    # Add RAG retrieval if configured
    if settings.ENABLE_RAG:
        workflow.add_node("retrieve", retrieval_node)
        workflow.set_entry_point("retrieve")
        workflow.add_conditional_edges(
            "retrieve",
            should_retrieve,
            {"retrieve": "retrieve", "agent": "agent"}
        )
    else:
        workflow.set_entry_point("agent")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END,
            "error": END
        }
    )
    
    # Tools always return to agent
    workflow.add_edge("tools", "agent")
    
    # Compile with checkpointing for L3+
    checkpointer = None
    if settings.MATURITY_LEVEL >= 3:
        checkpointer = MemorySaver()
    
    return workflow.compile(checkpointer=checkpointer)

# Create singleton graph instance
graph = create_graph()
```

**6.5. Tool Definitions (`tools/definitions.py`)**
```python
"""Tool definitions for {agent_name}."""

from langchain_core.tools import tool
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)

class SearchInput(BaseModel):
    """Input for search tool."""
    query: str = Field(description="Search query")
    max_results: int = Field(default=5, ge=1, le=20)

@tool(args_schema=SearchInput)
async def search(query: str, max_results: int = 5) -> str:
    """Search for information."""
    try:
        # Implement search logic
        logger.info(f"Searching for: {query}")
        # results = await search_api.search(query, limit=max_results)
        return f"Search results for: {query}"
    except Exception as e:
        logger.error(f"Search error: {e}")
        return f"Search failed: {str(e)}"

# Export all tools
tools = [search]
```

**6.6. Configuration (`config/settings.py`)**
```python
"""Configuration for {agent_name}."""

from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    """Agent configuration settings."""
    
    # Agent identity
    AGENT_NAME: str = "{agent_name}"
    MATURITY_LEVEL: int = {level}  # L1=1, L2=2, L3=3, L4=4
    
    # Model configuration
    MODEL_NAME: str = "gpt-4-turbo-preview"
    TEMPERATURE: float = 0.0
    MAX_TOKENS: int = 4096
    
    # Safety limits (HARD STOPS)
    MAX_ITERATIONS: int = 10
    TIMEOUT_SECONDS: int = 300
    
    # Feature flags
    ENABLE_RAG: bool = {enable_rag}
    ENABLE_TOOLS: bool = {enable_tools}
    ENABLE_MEMORY: bool = {enable_memory}
    
    # Observability
    LANGSMITH_PROJECT: str = "{agent_name}"
    ENABLE_TRACING: bool = True
    
    # SOX compliance
    SOX_SCOPE: bool = {sox_scope}
    PHOENIX_ENDPOINT: str = ""
    
    # System prompt
    SYSTEM_PROMPT: str = '''You are {agent_name}, a helpful AI assistant.

Your capabilities:
- {capabilities}

Guidelines:
- Be helpful, harmless, and honest
- If you don't know something, say so
- Use tools when appropriate
- Stay focused on the user's request
'''
    
    class Config:
        env_file = ".env"
        env_prefix = "AGENT_"

settings = Settings()
```

**6.7. Main Entry Point (`main.py`)**
```python
"""Entry point for {agent_name}."""

import asyncio
import logging
from langchain_core.messages import HumanMessage

from graph.graph import graph
from config.settings import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configure LangSmith tracing
if settings.ENABLE_TRACING:
    import os
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = settings.LANGSMITH_PROJECT

async def run_agent(user_input: str, thread_id: str = "default") -> str:
    """Run the agent with user input."""
    
    config = {"configurable": {"thread_id": thread_id}}
    
    initial_state = {
        "messages": [HumanMessage(content=user_input)],
        "current_step": "start",
        "tool_results": {},
        "context": None,
        "error": None,
        "iteration_count": 0
    }
    
    logger.info(f"Running agent with input: {user_input[:100]}...")
    
    result = await graph.ainvoke(initial_state, config)
    
    if result.get("error"):
        logger.error(f"Agent error: {result['error']}")
        return f"Error: {result['error']}"
    
    return result["messages"][-1].content

async def main():
    """Interactive agent loop."""
    print(f"Starting {settings.AGENT_NAME}...")
    print("Type 'quit' to exit.\n")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "quit":
            break
        
        response = await run_agent(user_input)
        print(f"\nAssistant: {response}\n")

if __name__ == "__main__":
    asyncio.run(main())
```

### 7. Add Guardrails Integration (L3+)

If maturity level is L3 or L4, add guardrails:

```python
# In main.py, wrap the agent with guardrails
from guardrails import with_guardrails

@with_guardrails(load_guardrails_config(config_ref))
async def run_agent_with_guardrails(user_input: str, context: list[str] = None):
    return await run_agent(user_input)
```

### 8. Generate Tests

**8.1. Node Tests (`tests/test_nodes.py`)**
```python
"""Unit tests for agent nodes."""

import pytest
from unittest.mock import AsyncMock, patch

from graph.nodes import agent_node, retrieval_node
from graph.state import AgentState

@pytest.fixture
def initial_state():
    return AgentState(
        messages=[],
        current_step="start",
        tool_results={},
        context=None,
        error=None,
        iteration_count=0
    )

@pytest.mark.asyncio
async def test_agent_node_success(initial_state):
    """Test agent node produces valid response."""
    with patch("graph.nodes.model") as mock_model:
        mock_model.ainvoke = AsyncMock(return_value=AIMessage(content="Hello!"))
        
        result = await agent_node(initial_state)
        
        assert result["error"] is None
        assert len(result["messages"]) == 1
        assert result["iteration_count"] == 1

@pytest.mark.asyncio
async def test_agent_node_error_handling(initial_state):
    """Test agent node handles errors gracefully."""
    with patch("graph.nodes.model") as mock_model:
        mock_model.ainvoke = AsyncMock(side_effect=Exception("API Error"))
        
        result = await agent_node(initial_state)
        
        assert result["error"] is not None
        assert "API Error" in result["error"]
```

### 9. Validate and Report

// turbo
Validate generated agent:
- [ ] State schema properly typed
- [ ] All nodes have error handling
- [ ] Iteration limit configured (HARD STOP)
- [ ] Checkpointing enabled for L3+
- [ ] Guardrails integrated for L3+
- [ ] Tracing configured
- [ ] Tests included
Run the cross-platform guardrails validation utility against `output/` in JSON mode for `agent-developer`.

```
✅ AGENT GENERATED

Agent: {agent_name}
Type: {agent_type}
Level: {maturity_level}
SOX Scope: {sox_scope}

Features:
- Tools: {tool_list}
- Memory: {memory_type}
- RAG: {enabled/disabled}
- Guardrails: {enabled/disabled}

Files Generated:
- graph/state.py
- graph/nodes.py
- graph/edges.py
- graph/graph.py
- tools/definitions.py
- config/settings.py
- main.py
- tests/test_nodes.py

Next Steps:
1. Configure .env with API keys
2. Customize system prompt in config/settings.py
3. Implement tool logic in tools/definitions.py
4. Run tests: pytest tests/ -v
5. Start the agent entry point with the active environment's interpreter.
```

## Error Handling

| Error | Resolution |
|-------|------------|
| Missing maturity level | Default to L2, warn user |
| L3+ without guardrails | Generate guardrails config |
| Invalid agent type | Show supported types |

## Examples

**Example 1**: `/scaffold-agent-developer support-bot react L3 tools=search,database SOX=yes`
- Output: Full ReAct agent with search/database tools, guardrails, and SOX compliance

**Example 2**: `/scaffold-agent-developer faq-agent rag L2 memory=conversation`
- Output: RAG agent with conversation memory

**Example 3**: `/scaffold-agent-developer research-assistant multi-agent L4`
- Output: Multi-agent system with supervisor pattern

## References

Constitution: `agent-developer-constitution.md`
LangGraph Docs: https://langchain-ai.github.io/langgraph/
