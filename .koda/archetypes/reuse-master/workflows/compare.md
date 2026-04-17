---
description: Compare discovery strategies, catalog versions, or embedding models for the Reuse Master component engine
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Comparison Parameters
- **Extract comparison subjects** from `$ARGUMENTS` — subjects can be: search strategies (`semantic` vs `keyword` vs `hybrid`), embedding models (`all-MiniLM-L6-v2` vs `all-mpnet-base-v2`), catalog versions (v1.2 vs v1.3), or similarity thresholds (0.70 vs 0.75 vs 0.80)
- **Define evaluation query set**: minimum 20 labeled queries with known relevant components — comparisons on fewer queries are statistically unreliable
- **Establish evaluation metrics upfront**: primary metric (NDCG@10), secondary metrics (Precision@5, Recall@5, mean latency ms)

### 2. Establish Baselines for Each Subject
- **Run each candidate strategy independently** against the identical evaluation query set:

```python
from reuse_master.evaluation import Evaluator

evaluator = Evaluator(
    catalog_path="component catalog file",
    query_set="benchmark query file",
    labeled_results="expected results file"
)

results = {
    "semantic": evaluator.run(strategy="semantic", model="all-MiniLM-L6-v2"),
    "keyword":  evaluator.run(strategy="keyword"),
    "hybrid":   evaluator.run(strategy="hybrid", semantic_weight=0.7),
}
for name, r in results.items():
    print(f"{name:12s}  NDCG@10={r.ndcg:.3f}  P@5={r.precision:.3f}  latency={r.latency_ms:.0f}ms")
```

- **Capture per-query breakdowns**, not just aggregate scores — aggregate wins can mask catastrophic failures on minority query types

### 3. Statistical Significance Check
- **Compute pairwise significance** using a paired t-test or Wilcoxon signed-rank test on per-query scores — a 2-point aggregate NDCG difference is only meaningful if p < 0.05
- **Identify query subsets** where each strategy outperforms: some strategies win on infrastructure queries but lose on business-logic queries — this nuance determines whether a single winner is appropriate or a hybrid routing approach is required
- **Document score distributions**, not just means — a strategy with lower mean but lower variance may be preferable for production stability

### 4. Produce Comparison Report
- **Generate ranked comparison table** with statistical confidence intervals
- **Highlight tradeoffs**: latency vs. quality, implementation complexity vs. recall gain, threshold sensitivity differences
- **Make a concrete recommendation** with justification — "Strategy X is preferred because Y" — do not emit a report without a decision

### 5. Apply Winning Configuration
- **Update `env-config.yaml`** `variables.similarity_threshold` and any strategy flags to reflect winning configuration
- **Rebuild embedding index** with winning model if a model comparison was performed
- **Archive comparison report** to `docs/comparison-reports/YYYY-MM-DD-comparison.md`

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: specify what to compare — e.g. `/compare-reuse-master "semantic vs keyword vs hybrid" catalog/components.yaml`. |
| Insufficient data for comparison (fewer than 20 labeled queries) | Stop. Comparisons on small query sets yield unreliable conclusions. Expand labeled set before running. Document minimum sample size in report header. |
| Ambiguous winner (strategies are statistically tied on primary metric) | Do not force a pick. Report the tie explicitly. Use secondary metrics (latency, implementation cost) as tiebreakers. If still tied, recommend A/B production test. |
| Tied similarity scores (two components with identical score for same query) | Break ties by `usage_count` descending, then by `last_updated` descending. Document tie-breaking rule in comparison report for reproducibility. |
| One strategy fails to run (missing model or library) | Mark that strategy as `ERRORED` in the results table. Continue comparison with remaining strategies. Do not silently skip — `ERRORED` must appear in final report. |
| Evaluation query set lacks labeled ground truth | Stop. Running comparison without ground truth produces meaningless metrics. Create labeled results file from subject matter expert review before proceeding. |

## Examples

**Example 1**: `/compare-reuse-master "semantic vs keyword vs hybrid" catalog/components.yaml` — full strategy comparison on default benchmark query set

**Example 2**: `/compare-reuse-master "all-MiniLM-L6-v2 vs all-mpnet-base-v2" catalog/components.yaml threshold=0.75` — embedding model comparison holding threshold constant
