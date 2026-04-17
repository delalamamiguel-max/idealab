---
description: Validate duplicate detection accuracy with precision/recall metrics against known agent fixture pairs (Scope Deduplicator)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Test Input
- **Catalog path**: Path to the agent catalog under test (default `catalog/agents.yaml`)
- **Fixtures path**: Path to labeled test fixtures with known duplicate/non-duplicate pairs (default `tests/fixtures/agent_pairs.yaml`)
- **Threshold**: Similarity threshold to test against (default `0.8`; pass multiple values for a sweep, e.g., `thresholds=0.7,0.8,0.9`)
- **Metric**: Similarity metric to evaluate — `cosine`, `jaccard`, or `both` (default `both`)

### 2. Load and Validate Test Fixtures
- Load the fixture file and confirm all referenced agent names exist in the catalog; abort with a clear list of missing agents if any cannot be resolved
- Validate fixture schema: each pair must have `agent_a`, `agent_b`, and `expected_label` (`duplicate` | `distinct`)
- Split fixtures into **positive pairs** (expected: duplicate) and **negative pairs** (expected: distinct) and report counts before running scoring

```yaml
# tests/fixtures/agent_pairs.yaml — expected format
pairs:
  - agent_a: support-router
    agent_b: helpdesk-dispatcher
    expected_label: duplicate
    notes: "80%+ capability overlap confirmed in manual review"
  - agent_a: data-validator
    agent_b: support-router
    expected_label: distinct
    notes: "Different domains: data pipeline vs customer support"
```

### 3. Run Similarity Scoring Against All Fixture Pairs
- For each pair, compute both cosine similarity (embedding-based) and Jaccard coefficient (token overlap)
- Apply the threshold to classify each pair as `duplicate` or `distinct`
- Collect true positives (TP), false positives (FP), true negatives (TN), and false negatives (FN) against the fixture labels

```python
def run_test_suite(pairs: list[dict], catalog: dict, threshold: float = 0.8) -> dict:
    """Evaluate duplicate detection accuracy against labeled fixtures."""
    tp, fp, tn, fn = 0, 0, 0, 0
    for pair in pairs:
        score = compute_similarity(catalog[pair["agent_a"]], catalog[pair["agent_b"]])
        predicted = "duplicate" if score >= threshold else "distinct"
        label = pair["expected_label"]
        if predicted == "duplicate" and label == "duplicate":   tp += 1
        elif predicted == "duplicate" and label == "distinct":  fp += 1
        elif predicted == "distinct"  and label == "distinct":  tn += 1
        else:                                                    fn += 1
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall    = tp / (tp + fn) if (tp + fn) else 0.0
    f1        = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    return {"precision": precision, "recall": recall, "f1": f1,
            "tp": tp, "fp": fp, "tn": tn, "fn": fn}
```

### 4. Evaluate Precision, Recall, and Threshold Sensitivity
- Report precision, recall, and F1 for each tested threshold value
- Highlight **threshold boundary pairs**: pairs whose similarity score falls within ±0.05 of the threshold — these are highest-risk classifications requiring human review
- If running a threshold sweep, tabulate F1 vs threshold to identify the optimal operating point
- Constitution requirement: precision must be ≥ 0.85 and recall ≥ 0.80 at the configured threshold before any catalog update is accepted

### 5. Generate and Store Test Report
- Write a structured test report to `tests/reports/test-<timestamp>.yaml` including: threshold used, metric used, precision, recall, F1, full confusion matrix, and any boundary pairs flagged for review
- Exit with non-zero status code if precision < 0.85 or recall < 0.80 — do not silently pass a failing test run
- Attach the report path to the governance audit trail entry for traceability across catalog changes

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide catalog path and fixture file path, or confirm the defaults are acceptable. |
| `scope-deduplicator-constitution.md` not found | Stop. Ensure constitution file is present at repo root before proceeding. |
| Flaky similarity scores (non-deterministic results across identical runs) | Pin random seed (`numpy.random.seed(42)`) and pin the embedding model version in `env-config.yaml`. If scores still vary, the model is non-deterministic — switch to a deterministic alternative or use Jaccard as the primary metric. |
| Missing agent fixtures (fixture references agents not in catalog) | List all missing agent names and abort. Do not silently skip missing pairs — they represent untested coverage gaps that hide real failures. |
| Threshold boundary failure (score within ±0.05 of threshold) | Flag the pair as `REVIEW REQUIRED`. Do not auto-classify boundary pairs — surface them to a human reviewer per the constitution's governance workflow. |
| Precision < 0.85 or recall < 0.80 at configured threshold | Fail the test run with a non-zero exit code. Adjust the threshold or swap the embedding model. Do not approve catalog changes until metrics are within specification. |

## Examples

**Example 1**: `/test-scope-deduplicator "catalog=<agent catalog file> fixtures=<fixture file> threshold=0.8"`

**Example 2**: `/test-scope-deduplicator "catalog=<agent catalog file> thresholds=0.7,0.8,0.9 metric=cosine"` — threshold sweep to find the optimal F1 operating point
