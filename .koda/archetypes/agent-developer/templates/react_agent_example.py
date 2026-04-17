"""
Example ReAct Agent Implementation
Archetype: agent-developer
"""

import asyncio
import logging
from typing import Annotated, TypedDict, Optional
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, ToolMessage, AIMessage
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)


class AgentState(TypedDict):
    """Agent state schema."""
    messages: Annotated[list[BaseMessage], add_messages]
    next_action: str
    error: Optional[str]


def create_react_agent(tools: list, model_name: str = "gpt-4") -> StateGraph:
    """
    Create a ReAct agent with tools.

    Args:
        tools: List of LangChain tools
        model_name: Model to use

    Returns:
        Compiled StateGraph
    """
    model = ChatOpenAI(model=model_name).bind_tools(tools)
    tool_map = {t.name: t for t in tools}

    async def agent_node(state: AgentState) -> AgentState:
        """Agent reasoning node."""
        try:
            response = await model.ainvoke(state["messages"])
            return {
                "messages": [response],
                "next_action": "tools" if response.tool_calls else "end",
                "error": None,
            }
        except Exception as e:
            logger.error("agent_node failed: %s", e)
            return {
                "messages": [],
                "next_action": "end",
                "error": str(e),
            }

    async def tool_node(state: AgentState) -> AgentState:
        """Tool execution node."""
        try:
            last_message = state["messages"][-1]
            tool_messages = []
            for tool_call in last_message.tool_calls:
                tool = tool_map.get(tool_call["name"])
                if tool is None:
                    result = f"Unknown tool: {tool_call['name']}"
                else:
                    result = await asyncio.to_thread(tool.invoke, tool_call["args"])
                tool_messages.append(
                    ToolMessage(
                        content=str(result),
                        tool_call_id=tool_call["id"],
                    )
                )
            return {"messages": tool_messages, "next_action": "agent", "error": None}
        except Exception as e:
            logger.error("tool_node failed: %s", e)
            return {"messages": [], "next_action": "end", "error": str(e)}

    def route(state: AgentState) -> str:
        """Route to next node."""
        return state["next_action"]

    graph = StateGraph(AgentState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)
    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", route, {"tools": "tools", "end": END})
    graph.add_edge("tools", "agent")

    return graph.compile()
