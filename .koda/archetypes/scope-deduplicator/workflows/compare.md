---
description: Perform a detailed pairwise capability comparison between two or more agents and produce a consolidation recommendation (Scope Deduplicator)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Comparison Input
- **Agents**: Comma-separated agent names or IDs to compare (minimum 2; maximum governed by `max_agents_scanned` in `env-config.yaml`)
- **Catalog path**: Path to the agent catalog (default `catalog/agents.yaml`)
- **Threshold**: Similarity threshold for flagging a pair as a duplicate candidate (default `0.8`)
- **Output format**: `table` (default), `json`, or `yaml` — controls the format of the comparison report

### 2. Load and Normalize Agent Capabilities
- Retrieve each named agent from the catalog and validate that all have a non-empty `capabilities` list
- Normalize capability strings before comparison: lowercase, replace hyphens with spaces, strip leading/trailing whitespace, deduplicate within each agent's list
- If an agent has zero capabilities after normalization, halt and report it — an empty capabilities list is a catalog data quality violation under the constitution

```python
def load_and_normalize(agent_name: str, catalog: dict) -> list[str]:
    """Load and normalize a single agent's capability list for comparison."""
    agent = catalog.get(agent_name)
    if not agent or not agent.get("capabilities"):
        raise ValueError(f"Agent '{agent_name}' missing or has empty capabilities in catalog")
    return list(dict.fromkeys(            # preserve order while deduplicating
        cap.lower().replace("-", " ").strip()
        for cap in agent["capabilities"]
    ))
```

### 3. Compute Pairwise Similarity Matrix
- For every pair in the agent set, compute both cosine similarity (via sentence-transformer embeddings) and Jaccard coefficient (token-level overlap)
- Store scores in a symmetric N×N matrix where entry (i,j) is the similarity between agent i and agent j
- Flag all pairs where **either** cosine ≥ threshold **or** Jaccard ≥ threshold as high-overlap candidates for further review

```
Similarity Matrix (cosine | jaccard):
                      support-router   helpdesk-dispatcher   data-validator
support-router           1.00 | 1.00        0.87 | 0.73         0.21 | 0.08
helpdesk-dispatcher      0.87 | 0.73        1.00 | 1.00         0.19 | 0.06
data-validator           0.21 | 0.08        0.19 | 0.06         1.00 | 1.00
```

### 4. Identify Overlapping and Unique Capabilities
- For each flagged high-overlap pair, produce a three-column breakdown: capabilities unique to agent A | shared by both | unique to agent B
- Compute the **overlap ratio** = |shared| / |union| and surface this alongside the raw similarity scores
- Highlight capabilities that are semantically equivalent but lexically different (e.g., "ticket routing" vs "route support tickets") — these require embedding-based detection, not just exact-match token overlap

### 5. Generate Consolidation Recommendation
- Pairs with similarity ≥ threshold: recommend `CONSOLIDATE` and link directly to the `/refactor-scope-deduplicator` workflow
- Pairs with 0.6 ≤ similarity < threshold: recommend `REVIEW` — overlap is notable but not conclusive; escalate to governance
- Pairs with similarity < 0.6: recommend `KEEP SEPARATE` — no meaningful overlap detected
- Write the full report (matrix, per-pair breakdown, recommendations) to `reports/compare-<timestamp>.yaml`

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide at least two agent names and the catalog path for comparison. |
| `scope-deduplicator-constitution.md` not found | Stop. Ensure constitution file is present at repo root before proceeding. |
| Insufficient agents to compare (fewer than 2 valid agents resolved from catalog) | Halt. List the agent names that could not be found and ask the user to correct them or add them to the catalog first. |
| Ambiguous similarity winner (multiple agents all score ≥ threshold against a single target) | Do not auto-select a merge target. Report all candidates ranked by score with a `MULTI-OVERLAP` flag and surface the full ranked list to the reviewer. |
| Tied scores (two or more agents return identical similarity scores) | Break the tie using Jaccard coefficient as a secondary metric. If still tied, flag as `REVIEW REQUIRED` — require human adjudication before consolidation proceeds. |
| Agent capability list empty after normalization | Catalog data quality failure. Do not proceed with comparison for that agent. File a catalog quality issue and request the agent owner to populate the capabilities field. |

## Examples

**Example 1**: `/compare-scope-deduplicator "agents=support-router,helpdesk-dispatcher catalog=<agent catalog file> threshold=0.8"`

**Example 2**: `/compare-scope-deduplicator "agents=ticket-bot,issue-tracker,chat-agent threshold=0.75 output=json"` — three-way comparison with JSON output for programmatic downstream consumption
