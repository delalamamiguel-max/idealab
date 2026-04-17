---
description: Compare two or more optimization strategies head-to-head using A/B testing (Workflow Optimizer)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Comparison Configuration
- **Workflow variants**: Two or more named variants to compare (e.g., `"caching vs parallel"` or paths to two workflow files)
- **Comparison axis**: `latency` | `cost` | `quality` | `all`
- **Input set**: Standard benchmark input set (minimum 50 samples per variant per `ab_test_min_samples` config)
- Validate that both variants operate on identical input sets — comparing across different inputs produces meaningless results

### 2. Establish Comparable Baselines for Each Variant
- Both variants must be profiled on the **same hardware, same input set, same time window** to be comparable
- Tag each variant run in LangSmith distinctly:

```python
from langsmith import traceable

@traceable(name="variant-A-caching", tags=["compare", "variant-A"])
def run_variant_a(inputs: list[dict]) -> list[dict]:
    # Caching-based workflow implementation
    ...

@traceable(name="variant-B-parallel", tags=["compare", "variant-B"])
def run_variant_b(inputs: list[dict]) -> list[dict]:
    # Parallelism-based workflow implementation
    ...
```

- Record P50/P95 latency, average cost per request, and quality scores for each variant

### 3. Run A/B Benchmark (Minimum 50 Samples Each)
- Interleave variant runs (A, B, A, B …) rather than running all A then all B — this controls for temporal drift
- Minimum sample count per variant: `ab_test_min_samples = 50` from `env-config.yaml`
- If either variant produces < 50 valid (non-error) samples, the comparison is invalid — collect more data
- Compute statistical significance with a two-sample t-test; require p-value ≤ 0.05 before declaring a winner

### 4. Analyze Trade-offs
- Build a structured comparison matrix:

  | Metric | Variant A | Variant B | Delta | Winner |
  |--------|-----------|-----------|-------|--------|
  | P95 Latency | {ms} | {ms} | {%} | {A/B/TIE} |
  | Cost/req | ${a} | ${b} | {%} | {A/B/TIE} |
  | Faithfulness | {score} | {score} | {delta} | {A/B/TIE} |
  | Relevancy | {score} | {score} | {delta} | {A/B/TIE} |

- Document the cost-latency trade-off: if A wins latency but B wins cost, record the business context for which metric to prioritize

### 5. Recommend and Document
- Select the winning variant using the priority order: quality > latency > cost (never sacrifice quality)
- If variants are statistically tied on the comparison axis, default to the lower-complexity implementation
- Write the comparison result to `OPTIMIZATION_LOG.md` with a recommendation and rationale

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide two variant identifiers and comparison axis (latency/cost/quality). |
| Incomparable baselines (different input sets used per variant) | Stop. Re-run both variants on the same standard input set before comparing. |
| Insufficient sample size (< 50 valid samples per variant) | Collect more samples. Do not declare a winner from small samples — results are noise. |
| Tied performance (p-value > 0.05 on primary metric) | Do not force a winner. Document as "statistically inconclusive." Default to lower-complexity variant. |
| Quality regression in proposed winner | Disqualify that variant. The winner must not sacrifice quality below pre-comparison baseline. |
| Constitution file not found | Stop. Ensure `workflow-optimizer-constitution.md` is present before running comparisons. |

## Examples

**Example 1**: `/compare-workflow-optimizer "caching vs parallel" latency`
- Runs 50 samples each; caching wins P95 latency (8.2s vs 11.4s, p=0.003); cost is identical; caching selected

**Example 2**: `/compare-workflow-optimizer "gpt-4o vs gpt-4o-mini" cost`
- gpt-4o-mini is 60% cheaper; quality (faithfulness) drops from 0.92 to 0.78 — falls below 0.80 threshold; gpt-4o-mini disqualified despite cost win
