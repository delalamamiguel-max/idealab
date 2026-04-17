---
description: Compare agent architectures, frameworks, and patterns to recommend optimal approach (Agent Developer)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Environment Setup

// turbo
Verify comparison tools available.
Run the cross-platform environment validation utility for `agent-developer` in JSON mode and halt if `ENV_VALID` is false.

### 2. Load Configuration

- Read `agent-developer-constitution.md` for evaluation criteria

### 3. Parse Input

Extract from $ARGUMENTS:
- **Comparison type**: frameworks | architectures | patterns | models
- **Candidates**: Options to compare
- **Use case**: Target use case context
- **Priorities**: performance | cost | simplicity | scalability

### 4. Generate Comparison Matrix

**Framework Comparison:**
| Framework | Pros | Cons | Best For |
|-----------|------|------|----------|
| LangGraph | Type-safe, checkpointing | Learning curve | Production agents |
| LangChain | Simple, large ecosystem | Less control | Prototypes |
| AutoGen | Multi-agent native | Complexity | Research |

**Architecture Comparison:**
| Pattern | Complexity | Scalability | Use Case |
|---------|------------|-------------|----------|
| Simple Chain | Low | Low | L1 tasks |
| ReAct | Medium | Medium | L2-L3 tasks |
| Plan-Execute | High | High | L3-L4 tasks |
| Multi-Agent | Very High | Very High | L4 tasks |

### 5. Run Benchmarks (if applicable)

Compare latency, cost, and accuracy on sample tasks.

### 6. Generate Recommendation

Provide recommendation with rationale.
Run the cross-platform guardrails validation utility against `output/` in JSON mode for `agent-developer`.

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user for required arguments. |
| `agent-developer-constitution.md` not found | Stop. Ensure repo is at root with constitution file present. |
| Environment validation utility unavailable | Manually verify Python ≥3.10, langgraph, langchain-openai are installed. |
| Tool import fails | Check `available_libraries` in `templates/env-config.yaml` and install missing packages. |
| LLM API key missing | Set `OPENAI_API_KEY` environment variable before running. |

## Examples

**Example 1**: `/compare-agent-developer frameworks "LangGraph vs AutoGen" multi-agent`
**Example 2**: `/compare-agent-developer architectures "ReAct vs Plan-Execute" customer-support`

## References

Constitution: `agent-developer-constitution.md`
