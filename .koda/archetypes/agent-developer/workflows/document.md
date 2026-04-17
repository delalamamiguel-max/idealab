---
description: Generate comprehensive documentation for agents including architecture diagrams, API docs, and runbooks (Agent Developer)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Environment Setup

// turbo
Verify documentation tools available.
Run the cross-platform environment validation utility for `agent-developer` in JSON mode and halt if `ENV_VALID` is false.

### 2. Load Configuration

- Read `agent-developer-constitution.md` for documentation standards

### 3. Parse Input

Extract from $ARGUMENTS:
- **Agent path**: Path to agent code
- **Doc type**: full | api | architecture | runbook
- **Audience**: developer | operator | user

### 4. Analyze Agent

- Parse state schema
- Extract node functions
- Identify tools
- Map graph topology

### 5. Generate Documentation

**README.md:**
- Overview and purpose
- Quick start guide
- Configuration options

**Architecture Docs:**
- Graph topology diagram
- State schema documentation
- Node descriptions

**API Reference:**
- Function signatures
- Input/output types
- Error codes

**Runbook:**
- Deployment guide
- Monitoring setup
- Incident response

### 6. Validate Documentation

// turbo
Check documentation completeness.
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

**Example 1**: `/document-agent-developer ./my-agent full developer`
**Example 2**: `/document-agent-developer ./support-bot runbook operator`

## References

Constitution: `agent-developer-constitution.md`
