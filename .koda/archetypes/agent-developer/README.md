# Agent Developer

**Category:** 10-agentic-development  
**Version:** 1.0.0  
**Status:** Active

## Overview

The Agent Developer archetype provides patterns and scaffolding for building production-grade AI agents using LangGraph and LangChain. It supports ReAct agents, RAG pipelines, tool-calling agents, and multi-agent orchestration.

## Purpose

Build enterprise AI agents with:
- **ReAct Patterns**: Reasoning + Action loops with observation
- **RAG Integration**: Retrieval-augmented generation
- **Tool Calling**: Validated function execution
- **Memory Management**: Conversation and persistent state
- **Guardrails Integration**: Safety controls for L3+ agents

## When to Use

Use this archetype when:
- Building conversational AI agents
- Creating tool-using assistants
- Implementing RAG-based Q&A systems
- Designing multi-agent workflows
- Developing autonomous AI systems

## Available Workflows

| Workflow | Command | Description |
|----------|---------|-------------|
| **Scaffold** | `/scaffold-agent-developer` | Generate new agent with full structure |
| **Refactor** | `/refactor-agent-developer` | Improve existing agent code |
| **Debug** | `/debug-agent-developer` | Fix loops, tool errors, state issues |
| **Test** | `/test-agent-developer` | Generate test suites |
| **Compare** | `/compare-agent-developer` | Compare architectures/frameworks |
| **Document** | `/document-agent-developer` | Generate documentation |

## Quick Start

```bash
# Create a basic ReAct agent
/scaffold-agent-developer my-assistant react L2 tools=search

# Create an L3 transactional agent with guardrails
/scaffold-agent-developer support-bot react L3 tools=database,email SOX=yes

# Create a RAG agent
/scaffold-agent-developer faq-bot rag L2 memory=conversation
```

## Agent Maturity Levels

| Level | Description | Requirements |
|-------|-------------|--------------|
| **L1** | Scripted flows with LLM enhancement | None |
| **L2** | RAG or read-only tools | Memory recommended |
| **L3** | Tools with side effects | Guardrails, checkpointing required |
| **L4** | Autonomous multi-agent | Full observability stack |

## Architecture

```
┌─────────────────────────────────────────┐
│              StateGraph                  │
├─────────────────────────────────────────┤
│  ┌─────────┐    ┌─────────┐    ┌─────┐ │
│  │ Retrieve │───▶│  Agent  │───▶│ END │ │
│  └─────────┘    └────┬────┘    └─────┘ │
│                      │                   │
│                      ▼                   │
│                ┌─────────┐              │
│                │  Tools  │              │
│                └────┬────┘              │
│                     │                    │
│                     └───────────────────┘│
└─────────────────────────────────────────┘
```

## Key Features

- **Type-Safe State**: TypedDict with annotations
- **Bounded Loops**: Iteration limits prevent runaway agents
- **Error Handling**: Graceful degradation on failures
- **Checkpointing**: Resume interrupted workflows
- **Observability**: LangSmith/Phoenix tracing

## Dependencies

- `langchain` - Core LLM abstractions
- `langgraph` - State machine for agents
- `langsmith` - Tracing and evaluation
- `openai` / `anthropic` - LLM providers

## Related Archetypes

- **guardrails-engineer** - Runtime safety (required for L3+)
- **prompt-engineer** - System prompt optimization
- **eval-specialist** - Agent evaluation
- **mcp-developer** - MCP tool servers

## References

- Constitution: `agent-developer-constitution.md`
- Environment Config: `templates/env-config.yaml`
- LangGraph Docs: https://langchain-ai.github.io/langgraph/
