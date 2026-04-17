"""
Example Workflow Graph
Archetype: workflow-creator
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END


class WorkflowState(TypedDict):
    """Workflow state."""
    input: str
    classification: str
    result: str
    error: str | None


def create_routing_workflow() -> StateGraph:
    """Create workflow with conditional routing."""
    
    def classify_node(state: WorkflowState) -> WorkflowState:
        """Classify input."""
        # Mock classification
        if "urgent" in state["input"].lower():
            classification = "urgent"
        elif "question" in state["input"].lower():
            classification = "question"
        else:
            classification = "general"
        
        return {"classification": classification}
    
    def urgent_handler(state: WorkflowState) -> WorkflowState:
        """Handle urgent requests."""
        return {"result": f"URGENT: {state['input']}"}
    
    def question_handler(state: WorkflowState) -> WorkflowState:
        """Handle questions."""
        return {"result": f"ANSWER: {state['input']}"}
    
    def general_handler(state: WorkflowState) -> WorkflowState:
        """Handle general requests."""
        return {"result": f"PROCESSED: {state['input']}"}
    
    def route(state: WorkflowState) -> Literal["urgent", "question", "general"]:
        """Route based on classification."""
        return state["classification"]
    
    # Build graph
    graph = StateGraph(WorkflowState)
    graph.add_node("classify", classify_node)
    graph.add_node("urgent", urgent_handler)
    graph.add_node("question", question_handler)
    graph.add_node("general", general_handler)
    
    graph.set_entry_point("classify")
    graph.add_conditional_edges(
        "classify",
        route,
        {
            "urgent": "urgent",
            "question": "question",
            "general": "general",
        }
    )
    graph.add_edge("urgent", END)
    graph.add_edge("question", END)
    graph.add_edge("general", END)
    
    return graph.compile()
