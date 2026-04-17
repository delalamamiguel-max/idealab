# Guardrails Engineer

**Category:** 10-agentic-development  
**Version:** 1.0.0  
**Status:** Active

## Overview

The Guardrails Engineer archetype provides runtime safety controls for AI agents, including input validation and output filtering. It implements the guardrails layer architecture recommended in the Agent Archetypes Plan.

## Purpose

Design and implement runtime guardrails for:
- **Input Validation**: Prompt injection detection, PII masking, topic boundary enforcement
- **Output Filtering**: Hallucination blocking, toxicity filtering, PII leakage prevention
- **Compliance Gates**: Non-advice compliance, bias detection, SOX audit logging

## When to Use

Use this archetype when:
- Building L3+ agents (transactional/autonomous) that require security guardrails
- Deploying SOX-scoped agents that need audit trails
- Adding safety layers to existing agents
- Implementing defense-in-depth for AI systems

## Available Workflows

| Workflow | Command | Description |
|----------|---------|-------------|
| **Scaffold** | `/scaffold-guardrails-engineer` | Generate guardrails configuration and implementation |
| **Refactor** | `/refactor-guardrails-engineer` | Improve security, performance, or coverage |
| **Debug** | `/debug-guardrails-engineer` | Fix false positives, false negatives, or performance issues |
| **Test** | `/test-guardrails-engineer` | Run adversarial and compliance test suites |
| **Compare** | `/compare-guardrails-engineer` | Compare frameworks, thresholds, or architectures |
| **Document** | `/document-guardrails-engineer` | Generate configuration guides and runbooks |

## Quick Start

```bash
# Generate guardrails for an L3 SOX-scoped agent
/scaffold-guardrails-engineer my-agent L3 SOX=yes

# Test the implementation
/test-guardrails-engineer guardrails/config.yaml all L3 SOX=yes

# Generate documentation
/document-guardrails-engineer guardrails/config.yaml full developer
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Agent Request                         │
└─────────────────────────────┬───────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────┐
│            INPUT GUARDRAILS                              │
│  - Prompt injection detection                            │
│  - PII detection and masking                            │
│  - Topic/scope boundary check                           │
└─────────────────────────────┬───────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────┐
│              AGENT EXECUTION                             │
└─────────────────────────────┬───────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────┐
│            OUTPUT GUARDRAILS                             │
│  - Hallucination check                                   │
│  - PII leakage check                                    │
│  - Toxicity/bias check                                  │
│  - Schema validation                                    │
└─────────────────────────────┬───────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────┐
│                    Agent Response                        │
└─────────────────────────────────────────────────────────┘
```

## Key Features

- **Tiered Evaluation**: Fast regex checks before expensive LLM classification
- **Fail-Closed Design**: Blocks by default when evaluation fails
- **SOX Compliance**: Full audit logging with Arize Phoenix integration
- **Configurable Thresholds**: Tune security/UX tradeoffs per use case
- **Comprehensive Testing**: Adversarial test suite included

## Dependencies

- `deepeval` - Evaluation metrics (Faithfulness, Toxicity, etc.)
- `presidio-analyzer` - PII detection
- `presidio-anonymizer` - PII masking
- `arize-phoenix` - Observability and SOX compliance

## Related Archetypes

- **agent-developer** - Core agent patterns (uses guardrails)
- **agent-validator** - Offline validation (complements guardrails)
- **eval-specialist** - Evaluation framework (metrics source)
- **production-monitor** - Production observability

## References

- Constitution: `guardrails-engineer-constitution.md`
- Environment Config: `templates/env-config.yaml`
- Agent Archetypes Plan: `agent-development/AGENT_ARCHETYPES_PLAN.md`
