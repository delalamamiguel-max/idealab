---
description: Consolidate duplicate agents by merging overlapping capabilities into a single canonical agent (Scope Deduplicator)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Consolidation Input
- **Agents to merge**: Comma-separated list of agent names with confirmed similarity scores above threshold (e.g., `agent_a=support-router,agent_b=helpdesk-dispatcher`)
- **Merge strategy**: `union` (combine all capabilities) or `intersection` (keep only shared capabilities); defaults to `union`
- **Catalog path**: Path to the live agent catalog (default `catalog/agents.yaml`)
- **Dry-run flag**: Set `dry_run=true` to preview the merged output without writing any changes to the live catalog

### 2. Pre-Merge Capability Audit
- Load all agents to be merged and print their full capability lists side-by-side for visual inspection
- Compute pairwise similarity across all agents in the merge set to confirm overlap justifies consolidation
- Identify capabilities that are **unique** to each agent — these represent the consolidation risk surface (dropping them creates a capability gap)
- Flag any downstream consumers or orchestrators that reference the agents by name; they will need path updates after consolidation is complete

```python
def audit_merge_candidates(agents: list[dict]) -> dict:
    """Identify unique vs shared capabilities across merge candidates."""
    all_caps = [set(a["capabilities"]) for a in agents]
    shared = set.intersection(*all_caps)
    unique_per_agent = {
        a["name"]: all_caps[i] - shared
        for i, a in enumerate(agents)
    }
    at_risk = {name: caps for name, caps in unique_per_agent.items() if caps}
    return {"shared": shared, "unique_at_risk": at_risk}
```

### 3. Generate Merged Agent Definition
- Construct the merged agent using the primary agent's name (or a supplied canonical name) and apply the chosen merge strategy
- Assign a new `version` field and increment the catalog schema version
- Write the merged agent definition to a staging file (`catalog/staging/<canonical_name>.yaml`) before touching the live catalog — do not skip this step
- Confirm the merged agent passes constitution hard-stop validation: capability count must be non-empty, name must be unique across the entire catalog

### 4. Update the Live Catalog
- Remove the source agents from `catalog/agents.yaml` and insert the merged agent entry in their place
- Update all cross-references: orchestrator configs, routing tables, and any workflow files that reference the deprecated agent names
- Run a catalog integrity check (`/validate-catalog`) to confirm no orphan references remain
- Commit the catalog change with a structured message: `refactor(catalog): merge {agent_a} + {agent_b} → {canonical_name} [similarity={score:.2f}]`

### 5. Post-Merge Validation
- Run the full similarity scan against the updated catalog to confirm the merged agent does not itself create a new duplicate with any remaining agent
- Verify the merged agent's capabilities cover 100% of the union of the source agents' capabilities (or document explicitly what was intentionally dropped and why)
- Archive the deprecated agent definitions in `catalog/archive/` with a `deprecated_at` timestamp and a `replaced_by` field pointing to the canonical name

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide at least two agent names and the catalog path for consolidation. |
| `scope-deduplicator-constitution.md` not found | Stop. Ensure constitution file is present at repo root before proceeding. |
| Consolidation breaks an existing agent or orchestrator reference | Do not proceed. Identify all downstream consumers (e.g., `python -c "import pathlib; [print(p) for p in pathlib.Path('.').rglob('*') if '<agent_name>' in p.read_text(errors='ignore')]"`) and update or redirect them before retrying consolidation. |
| Capability gap after merge (unique capability would be dropped) | Halt merge. Present the at-risk capabilities to the reviewer. Either add them explicitly to the merged agent or create a minimal satellite agent to preserve them. |
| Rollback needed after a catalog update | Restore `catalog/agents.yaml` from the pre-merge backup in `catalog/archive/`. Re-run the similarity scan to confirm catalog integrity is fully restored. |
| Merged agent similarity exceeds threshold with a third catalog agent | Flag the new duplicate immediately. Do not activate the merged agent until the new overlap is resolved or explicitly approved through the governance workflow. |

## Examples

**Example 1**: `/refactor-scope-deduplicator "agent_a=support-router,agent_b=helpdesk-dispatcher strategy=union catalog=<agent catalog file>"`

**Example 2**: `/refactor-scope-deduplicator "agent_a=ticket-bot,agent_b=issue-tracker dry_run=true"` — preview merge output without writing to live catalog
