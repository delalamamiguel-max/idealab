---
description: Compare different approaches for guardrails implementation and recommend optimal configuration (Guardrails Engineer)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Environment Setup

// turbo
Verify comparison tools available:
- Python with yaml, json support
- Benchmarking utilities

### 2. Load Configuration

- Read `guardrails-engineer-constitution.md` for evaluation criteria
- Load configurations to compare

### 3. Parse Input

Extract from $ARGUMENTS:
- **Comparison type**: frameworks | thresholds | architectures | models
- **Candidates**: List of options to compare
- **Evaluation criteria**: security | performance | cost | coverage | all
- **Use case context**: Agent type, SOX scope, traffic volume

If incomplete, request:
```
Please provide:
1. Comparison Type: frameworks | thresholds | architectures | models
2. Candidates: (e.g., "Galileo vs custom vs NeMo Guardrails")
3. Evaluation Criteria: security | performance | cost | coverage | all
4. Use Case: (e.g., "L3 SOX agent, 1000 requests daily")
```

### 4. Generate Comparison Framework

**4.1. Framework Comparison**
Compare guardrails frameworks:

| Criterion | Weight | Galileo | NeMo Guardrails | Custom DeepEval | LangChain Guards |
|-----------|--------|---------|-----------------|-----------------|------------------|
| **Security Coverage** | 25% | | | | |
| Prompt Injection | | ✅ Built-in | ✅ Built-in | ⚠️ Custom | ⚠️ Custom |
| PII Detection | | ✅ Built-in | ⚠️ Limited | ✅ Presidio | ⚠️ Custom |
| Hallucination | | ✅ Built-in | ⚠️ Limited | ✅ DeepEval | ✅ Built-in |
| **Performance** | 25% | | | | |
| Latency (P95) | | ~200ms | ~100ms | ~300ms | ~150ms |
| Throughput | | High | Very High | Medium | High |
| **Cost** | 20% | | | | |
| License | | Proprietary | Apache 2.0 | Apache 2.0 | MIT |
| Infrastructure | | SaaS | Self-hosted | Self-hosted | Self-hosted |
| LLM Calls | | Optimized | Minimal | Per-check | Per-check |
| **Integration** | 15% | | | | |
| LangChain | | ✅ | ✅ | ✅ | ✅ Native |
| LangGraph | | ✅ | ⚠️ | ✅ | ✅ Native |
| Phoenix | | ✅ | ⚠️ | ✅ | ⚠️ |
| **Customization** | 15% | | | | |
| Custom Rules | | ⚠️ Limited | ✅ Colang | ✅ Full | ✅ Full |
| Threshold Tuning | | ✅ | ⚠️ | ✅ | ✅ |

**4.2. Threshold Comparison**
Compare threshold configurations:

| Guardrail | Conservative | Balanced | Permissive | Recommended |
|-----------|--------------|----------|------------|-------------|
| Prompt Injection | 0.6 | 0.8 | 0.9 | 0.8 |
| Hallucination | 0.95 | 0.9 | 0.8 | 0.9 (SOX) |
| Toxicity | 0.999 | 0.99 | 0.95 | 0.99 |
| PII Leakage | 1.0 | 1.0 | 0.95 | 1.0 |

Trade-off analysis:
- **Conservative**: High security, more false positives, lower UX
- **Balanced**: Good security, acceptable false positives, good UX
- **Permissive**: Lower security, minimal false positives, best UX

**4.3. Architecture Comparison**
Compare guardrails architectures:

| Architecture | Pros | Cons | Best For |
|--------------|------|------|----------|
| **Inline (Sync)** | Simple, deterministic | Adds latency | Low-traffic, critical apps |
| **Sidecar (Async)** | Low latency, scalable | Complex, eventual consistency | High-traffic apps |
| **Tiered** | Cost-effective, fast | More complex | Production systems |
| **Distributed** | Highly scalable | Operational overhead | Enterprise scale |

**4.4. Model Comparison**
Compare classifier models for guardrails:

| Model | Latency | Accuracy | Cost | Best For |
|-------|---------|----------|------|----------|
| gpt-3.5-turbo | ~200ms | 85% | $$ | General use |
| gpt-4 | ~500ms | 95% | $$$$ | High-stakes |
| Claude Haiku | ~150ms | 82% | $ | Cost-sensitive |
| Fine-tuned BERT | ~20ms | 90% | $ | High-volume |
| Regex/Rules | ~1ms | 70% | Free | First-pass filter |

### 5. Run Benchmarks (if applicable)

```python
"""Benchmark guardrails configurations."""

import asyncio
import time
from dataclasses import dataclass

@dataclass
class BenchmarkResult:
    config_name: str
    latency_p50: float
    latency_p95: float
    accuracy: float
    false_positive_rate: float
    cost_per_1k: float

async def benchmark_config(config, test_suite):
    """Benchmark a guardrails configuration."""
    latencies = []
    correct = 0
    false_positives = 0
    
    for test_case in test_suite:
        start = time.perf_counter()
        result = await evaluate_with_config(config, test_case.input)
        latencies.append(time.perf_counter() - start)
        
        if result.blocked == test_case.should_block:
            correct += 1
        elif result.blocked and not test_case.should_block:
            false_positives += 1
    
    return BenchmarkResult(
        config_name=config.name,
        latency_p50=statistics.median(latencies) * 1000,
        latency_p95=statistics.quantiles(latencies, n=20)[18] * 1000,
        accuracy=correct / len(test_suite),
        false_positive_rate=false_positives / len(test_suite),
        cost_per_1k=estimate_cost(config, 1000)
    )
```

### 6. Generate Recommendation

```markdown
## Guardrails Comparison Report

### Use Case
- Agent Type: {agent_type}
- SOX Scope: {sox_scope}
- Traffic Volume: {volume}
- Priority: {security | performance | cost}

### Comparison Summary

| Candidate | Security | Performance | Cost | Overall |
|-----------|----------|-------------|------|---------|
| {option_1} | {score} | {score} | {score} | {weighted} |
| {option_2} | {score} | {score} | {score} | {weighted} |
| {option_3} | {score} | {score} | {score} | {weighted} |

### Recommendation

**Recommended: {winner}**

Rationale:
- {reason_1}
- {reason_2}
- {reason_3}

Trade-offs:
- {tradeoff_1}
- {tradeoff_2}

### Implementation Path

1. {step_1}
2. {step_2}
3. {step_3}

### Migration Notes (if switching)
- {note_1}
- {note_2}
```

### 7. Validate and Report

// turbo
Ensure recommendation meets constitution requirements:
- [ ] Recommended option meets minimum security requirements
- [ ] Latency within acceptable bounds
- [ ] Cost within budget
- [ ] SOX compliance maintained (if applicable)

## Error Handling

| Error | Resolution |
|-------|------------|
| Insufficient data | Request more context |
| No clear winner | Present trade-offs, let user decide |
| All options fail requirements | Suggest hybrid approach |

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide agent name, scope (input/output/both), and guardrail level (L1–L4). |
| `guardrails-engineer-constitution.md` not found | Stop. Ensure file is present at repo root. |
| `deepeval` or `presidio` not installed | Run `pip install deepeval presidio-analyzer presidio-anonymizer`. |
| Guardrail blocks all inputs unexpectedly | Check threshold in `config.template.json` — L1 defaults may be too strict for your domain. |
| PII detection false positives | Review Presidio entity list; exclude irrelevant entity types for your context. |
| Injection pattern test fails | Verify test prompts in `references/` match your threat model; add domain-specific patterns. |

## Examples

**Example 1**: `/compare-guardrails-engineer frameworks "Galileo vs custom" security L3-SOX`
- Output: Framework comparison with security focus

**Example 2**: `/compare-guardrails-engineer thresholds "conservative vs balanced" L2-high-traffic`
- Output: Threshold comparison with UX considerations

**Example 3**: `/compare-guardrails-engineer models "gpt-3.5 vs fine-tuned-bert" cost 10k-req/day`
- Output: Model comparison with cost analysis

## References

Constitution: `guardrails-engineer-constitution.md`
