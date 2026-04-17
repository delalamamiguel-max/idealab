---
description: Identify and prevent duplicate agent capabilities (Scope Deduplicator)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **New agent**: Agent to check for duplicates
- **Catalog path**: Path to agent catalog
- **Threshold**: Similarity threshold (default 0.8)

### 2. Run Similarity Analysis

```python
def check_similarity(new_agent, catalog):
    """Check if agent duplicates existing capabilities."""
    similarities = []
    for existing in catalog:
        score = compute_similarity(
            new_agent.capabilities,
            existing.capabilities
        )
        if score > threshold:
            similarities.append((existing.name, score))
    return similarities
```

### 3. Generate Report

```markdown
## Duplicate Analysis

### New Agent: {agent_name}

### Similar Existing Agents
| Agent | Similarity | Overlapping Capabilities |
|-------|------------|-------------------------|
| {existing1} | {score1} | {capabilities} |

### Recommendation
{consolidate | proceed | review}
```

### 4. Validate

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide agent list or catalog path for deduplication analysis. |
| `scope-deduplicator-constitution.md` not found | Stop. Ensure file is present at repo root. |
| Catalog file not found | Verify catalog path exists. Initialise with `capability_inventory` step if first use. |
| Similarity scoring returns all 0.0 | Check embedding model is loaded and capabilities are descriptive enough to differentiate. |
| Consolidation recommendation rejected | Document rejection reason in governance log. Escalate if >3 rejections on same agent pair. |
| Similarity threshold unclear | Default to 0.80. Document chosen threshold in deduplication report. |

## Examples
**Example**: `/scaffold-scope-deduplicator new-support-bot catalog/agents.yaml threshold=0.8`
