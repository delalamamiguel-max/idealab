---
description: Diagnose and fix component discovery failures and recommendation errors (Reuse Master)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse and Classify the Issue
- **Extract failure description** from `$ARGUMENTS` — identify whether the failure is in search, recommendation, catalog loading, or embedding
- **Classify issue type**: discovery failure (0 results), wrong recommendations (low precision), catalog corruption, or embedding/index errors
- **Locate relevant logs and state**: check `catalog/components.yaml`, any cached index files (e.g. `catalog/.faiss_index`), and last run output

### 2. Reproduce the Failure
- **Replay the failing query** with the exact parameters reported, capturing raw similarity scores before threshold filtering:

```python
discovery = ComponentDiscovery(catalog_path)
raw_results = discovery.search_raw(query="payment processing", threshold=0.0)
for r in raw_results[:10]:
    print(f"{r['name']:40s}  score={r['score']:.4f}")
```

- **Compare against expected results** — if catalog contains known relevant components, verify they appear in `raw_results` at all
- **Document the gap**: record how many components were searched, what scores the "expected" components received, and at what threshold they would surface

### 3. Diagnose Root Cause
- **Stale embeddings**: verify embedding index was rebuilt after the last catalog update — check file modification timestamps
- **Wrong model**: confirm `sentence-transformers` model in use matches the one used to build the index; a mismatch silently produces garbage scores
- **Catalog schema drift**: validate that `catalog/components.yaml` conforms to current schema — new fields or renamed keys break embedding extraction
- **Threshold too aggressive**: if relevant components appear in raw results at score 0.65–0.74 but threshold is 0.75, adjust or surface as near-miss

### 4. Apply Fix
- **Re-embed catalog** if stale or model mismatch:
  ```python
  from reuse_master import embed_catalog
  embed_catalog(catalog_path, force_rebuild=True)
  ```
- **Update threshold** in `env-config.yaml` under `variables.similarity_threshold` if near-miss pattern is confirmed
- **Patch schema** if catalog fields were renamed — update extraction logic to match new schema keys
- **Clear FAISS cache** and rebuild index after any catalog structural change

### 5. Validate the Fix
- **Re-run the original failing query** — confirm expected components now appear in top-5 results
- **Run regression sweep** across 10 representative queries to ensure no previously working searches degraded
- **Update `REMEDIATION_PLAN.md`** with root cause, fix applied, and date — constitution requires all diagnosis decisions to be documented

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide a concrete failure description — e.g. "searched for payment-service, got 0 results" or "wrong component recommended for ETL task". |
| Ambiguous error trace (multiple plausible causes) | Run each diagnostic step independently and record scores at each stage. Present a ranked list of suspected causes before applying any fix. Do not guess. |
| Missing catalog state (no `catalog/.faiss_index` or empty catalog) | Treat as first-run scenario. Re-initialise catalog: run `embed_catalog()` from scratch. Do not infer previous state. |
| No reproducible failure (query now works on retry) | Investigate intermittent embedding cache eviction or race condition in async index refresh. Add explicit cache-lock before concurrent write/read operations. |
| `reuse-master-constitution.md` not found | Stop. Ensure file is present at repo root before any diagnosis — constitution governs all decisions. |
| Embedding library (`sentence-transformers`, `faiss-cpu`) not installed | Stop. Run `pip install sentence-transformers>=2.2.0 faiss-cpu>=1.7.0 numpy>=1.24.0`. Do not proceed without confirmed install. |

## Examples

**Example 1**: `/debug-reuse-master "search for 'authentication-handler' returns 0 results despite component existing in catalog"`

**Example 2**: `/debug-reuse-master "ComponentDiscovery recommends deprecated v0.3 components instead of current v1.x entries — catalog has both, wrong one surfaces"`
