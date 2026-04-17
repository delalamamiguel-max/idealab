---
description: Diagnose and fix overlap detection failures in the Scope Deduplicator pipeline
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Diagnostic Input
- **Issue description**: Describe the observed failure mode (e.g., "missed obvious duplicate", "all scores stuck at 0.0", "false positive flagging unrelated agents")
- **Affected agents**: Names or IDs of the agent pair involved in the failing comparison
- **Catalog path**: Path to the agent catalog used during the failed run (default `catalog/agents.yaml`)
- **Last known threshold**: Record the similarity threshold value that was active when the issue surfaced

### 2. Reproduce and Isolate the Failure
- Re-run the similarity check in isolation against the reported agent pair to confirm the failure is reproducible
- Capture raw similarity scores, embedding vectors, and tokenized capability strings for side-by-side inspection
- Confirm whether the failure is **deterministic** (always fails) or **intermittent** (random seed, model loading race condition)
- Print the raw capability lists for both agents before encoding to rule out empty or truncated inputs

```python
def debug_similarity(agent_a_caps: list[str], agent_b_caps: list[str]) -> dict:
    """Reproduce a similarity failure for a specific agent pair."""
    from sentence_transformers import SentenceTransformer
    import numpy as np

    model = SentenceTransformer("all-MiniLM-L6-v2")
    # Sanity-check: model must return a non-zero embedding
    sanity = model.encode(["test"])
    assert sanity.any(), "Model returned all-zero embedding — check installation"

    vecs = model.encode([" ".join(agent_a_caps), " ".join(agent_b_caps)])
    cosine = float(np.dot(vecs[0], vecs[1]) / (np.linalg.norm(vecs[0]) * np.linalg.norm(vecs[1])))

    set_a, set_b = set(agent_a_caps), set(agent_b_caps)
    jaccard = len(set_a & set_b) / len(set_a | set_b) if set_a | set_b else 0.0

    print(f"Cosine:  {cosine:.4f}")
    print(f"Jaccard: {jaccard:.4f}")
    return {"cosine": cosine, "jaccard": jaccard}
```

### 3. Diagnose Root Cause
- **All-zero scores**: Verify the embedding model is correctly loaded; a quick `model.encode(["test"])` should return a non-zero 384-dim vector
- **Catalog mismatch**: Diff the catalog schema version used at debug time against the version from the failing run — field renames or added nesting break vector construction
- **No reproducible overlap despite obvious semantic match**: Check whether capability strings are too short (<3 meaningful tokens), excessively generic ("help", "general"), or inconsistently normalized (e.g., `"chat-support"` in one agent vs `"chat support"` in another)
- **False positives**: Confirm tokenization is not over-broad — generic labels like "assist" or "help" inflate Jaccard similarity even when agents serve distinct functional domains

### 4. Apply Targeted Fix
- If capability normalization is the issue: add a pre-processing step that lowercases, strips punctuation, and expands abbreviations before encoding
- If the embedding model version is wrong: pin the correct version in `env-config.yaml` under `available_libraries` and clear the local model cache (default: `~/.cache/huggingface/` on macOS/Linux, `%USERPROFILE%\.cache\huggingface\` on Windows)
- If catalog mismatch: trigger a catalog resync to reconcile field names, then re-index all agents from scratch
- Re-run `debug_similarity` against the original failing pair to confirm the fix resolves the reported score

### 5. Regression Test and Log the Fix
- Run the full test suite (`/test-scope-deduplicator catalog/agents.yaml`) after any change to confirm no new failures were introduced
- Append a structured entry to the governance audit trail documenting: agent pair, failure type, root cause, fix applied, embedding model version, threshold in use, and re-test result
- If the fix required a threshold change, record the justification and get sign-off per the constitution's governance workflow

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide issue description, affected agent names, and catalog path. |
| `scope-deduplicator-constitution.md` not found | Stop. Ensure constitution file is present at repo root before proceeding. |
| Similarity scores all zero | Verify embedding model is loaded (`model.encode(["test"])` returns non-zero tensor). Check that all capability strings are non-empty and contain >3 meaningful tokens. |
| Catalog mismatch between debug and production environments | Diff catalog schema versions. Resync and re-index before retesting — do not trust scores from a mixed-version run. |
| No reproducible overlap despite clear semantic similarity | Normalize capability strings (lowercase, hyphen-to-space, deduplicate synonyms) then rerun. If still failing, switch comparison metric from Jaccard to cosine. |
| Embedding model unavailable or version mismatch | Pin model version in `env-config.yaml`. Clear model cache and reinstall with `sentence-transformers>=2.2.0`. |

## Examples

**Example 1**: `/debug-scope-deduplicator "agent=ticket-bot catalog=<agent catalog file> issue=scores_all_zero"`

**Example 2**: `/debug-scope-deduplicator "agent_a=support-router agent_b=helpdesk-dispatcher issue=missed_duplicate threshold=0.8"`
