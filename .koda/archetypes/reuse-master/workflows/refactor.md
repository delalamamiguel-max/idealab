---
description: Improve component discovery accuracy and catalog quality through targeted refactoring (Reuse Master)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Refactoring Goal
- **Extract scope** from `$ARGUMENTS` — catalog path, target improvement area (embedding quality, keyword taxonomy, schema normalisation, API contract)
- **Define success metric upfront**: e.g. "top-5 recall improves from 62% to ≥80% on 20 benchmark queries" — without this, refactoring has no exit condition
- **Snapshot current baseline**: run benchmark suite before any changes to establish before/after comparison

### 2. Audit Current Discovery Quality
- **Run precision/recall sweep** across representative query set:

```python
from reuse_master.benchmarks import run_benchmark_suite

baseline = run_benchmark_suite(
    catalog_path="component catalog file",
    query_set="benchmark query file",
    metrics=["precision@5", "recall@5", "ndcg@10"]
)
print(baseline.summary())
```

- **Identify weak areas**: queries with recall < 0.6 are high-priority; inspect why expected components didn't rank
- **Categorise failures**: embedding model inadequacy vs. catalog keyword poverty vs. schema inconsistency vs. threshold calibration

### 3. Implement Targeted Improvements
- **Keyword enrichment**: for taxonomy gaps, add synonym arrays to catalog entries:
  ```yaml
  - name: auth-handler
    keywords: [authentication, auth, login, identity, SSO, OAuth, JWT]
  ```
- **Embedding model upgrade**: if current model underperforms on domain vocabulary, swap to `all-mpnet-base-v2` from `all-MiniLM-L6-v2` and rebuild index
- **Schema normalisation**: standardise `description` field length (100–500 chars) — short stubs degrade embedding quality
- **Threshold recalibration**: use precision-recall curve to select threshold that maximises F1 on benchmark set

### 4. Validate Regression-Free Improvement
- **Re-run full benchmark suite** after each change — do not batch multiple changes before measuring
- **Diff quality metrics** and confirm improvement target is met without degrading previously passing queries
- **Review any public API surface changes** in `ComponentDiscovery` class — consumer contracts in `search()` and `recommend()` must not break silently

### 5. Update Catalog and Rebuild Index
- **Commit catalog changes** with descriptive message referencing improvement rationale
- **Force-rebuild embedding index**: `embed_catalog(force_rebuild=True)` — stale index will produce misleading benchmark results
- **Update `variables.similarity_threshold`** in `env-config.yaml` if recalibration changed the recommended threshold value

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: specify catalog path and the specific accuracy problem to address — e.g. "low recall for infrastructure components" or "false positives for ETL queries". |
| Breaking API change detected in `ComponentDiscovery` public interface | Stop. Require explicit approval before proceeding. Document change in `CHANGELOG.md` under a MAJOR version bump and notify downstream consumers. |
| Regression introduced after refactoring merge | Immediately roll back the change that caused the regression. Do not patch forward. Investigate failure in isolation before re-attempting. |
| Circular dependency discovered between catalog components | Map the dependency cycle explicitly before any restructuring. Split circular components or introduce an interface layer. Never silently remove a dependency. |
| Benchmark suite missing or query set empty | Stop. Refactoring without a measurable quality bar is prohibited by constitution. Create benchmark queries from real historical discovery requests first. |
| Embedding rebuild fails (OOM or model not found) | Reduce `embedding_batch_size` in `env-config.yaml` under `performance`. Verify model name matches an installed `sentence-transformers` model. |

## Examples

**Example 1**: `/refactor-reuse-master catalog/components.yaml "precision@5 below 70% for data-pipeline queries — improve keyword coverage and re-embed"`

**Example 2**: `/refactor-reuse-master catalog/components.yaml "normalize description field lengths across all 340 entries before next quarterly catalog review"`
