---
description: Validate component discovery accuracy, recommendation quality, and catalog integrity (Reuse Master)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Test Scope
- **Extract catalog path and test mode** from `$ARGUMENTS` — modes: `unit` | `integration` | `benchmark` | `full`
- **Resolve test fixture paths**: `tests/fixtures/sample_catalog.yaml`, `tests/benchmark_queries.yaml`, `tests/expected_results.yaml` — fail fast if any are missing
- **Determine coverage targets**: recall@5 ≥ 0.80, precision@5 ≥ 0.75, catalog schema 100% valid — document these in run header

### 2. Validate Catalog Integrity
- **Schema validation** — every component entry must have `name`, `type`, `description`, `keywords`, `last_updated`:

```python
from reuse_master.validation import validate_catalog_schema

report = validate_catalog_schema(catalog_path)
if report.errors:
    for err in report.errors:
        print(f"[SCHEMA ERROR] {err.component}: {err.message}")
    raise SystemExit(1)
```

- **Duplicate detection**: scan for components with identical `name` or near-duplicate `description` (cosine similarity > 0.97) — flag for maintainer review
- **Freshness check**: components with `last_updated` older than 180 days are flagged as potentially stale

### 3. Run Unit Tests for Discovery Logic
- **Test similarity calculation**: verify `cosine_similarity()` produces expected scores for known pairs
- **Test threshold filtering**: confirm components below threshold are excluded and near-threshold components are surfaced as near-misses
- **Test `recommend()` ranking**: given a fixed embedded query, verify top-5 ordering is deterministic and matches expected fixture:
  ```python
  def test_recommend_deterministic(discovery, sample_query_embedding):
      results_a = discovery._rank_by_similarity(sample_query_embedding, top_k=5)
      results_b = discovery._rank_by_similarity(sample_query_embedding, top_k=5)
      assert results_a == results_b, "Recommendation order must be deterministic"
  ```

### 4. Run Benchmark Relevance Suite
- **Execute all benchmark queries** from `tests/benchmark_queries.yaml` — score each using NDCG@10, Precision@5, Recall@5
- **Compare against expected results** in `tests/expected_results.yaml` — fail test if any metric drops below its target threshold
- **Report near-misses**: components that ranked 6th–10th when expected in top-5 — these indicate threshold or embedding issues, not systemic failures

### 5. Generate Coverage and Quality Report
- **Produce a structured test report**: total queries run, pass/fail counts by metric, worst-performing queries with scores
- **Identify coverage gaps**: query categories (by domain: data, auth, ETL, infra, UI) where recall is consistently below target
- **Write report to `tests/reports/YYYY-MM-DD-test-report.md`** — required artifact for catalog governance

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide catalog path and test scope mode — e.g. `/test-reuse-master catalog/components.yaml benchmark`. |
| Test flakiness / intermittent failure (passes on retry) | Do not re-run and declare pass. Log the failure, inspect for non-deterministic ordering or async embedding calls, and add a reproducibility assertion before closing. |
| Missing test fixtures (`sample_catalog.yaml`, `benchmark_queries.yaml`) | Stop. Test cannot run without fixtures. Create minimal fixtures from real catalog data before proceeding — do not use empty placeholders. |
| Coverage gap detected (entire query category below 0.60 recall) | Flag as HIGH priority finding. Document in test report. Do not mark test run as "passing" — a coverage gap is a test failure at system level. |
| Catalog schema validation fails | Stop all downstream tests. Schema errors corrupt benchmark results. Fix schema first, then re-run full suite. |
| Embedding index out of date (modified catalog but stale `.faiss_index`) | Force index rebuild before running benchmark tests. Stale embeddings will produce misleading quality metrics. |

## Examples

**Example 1**: `/test-reuse-master catalog/components.yaml benchmark` — runs full relevance benchmark and generates a dated quality report

**Example 2**: `/test-reuse-master catalog/components.yaml unit` — runs determinism, threshold, and schema unit tests only, skipping heavy embedding benchmark
