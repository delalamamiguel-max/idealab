---
description: Generate comprehensive documentation for the agent catalog including capability matrices, overlap summaries, and governance guides (Scope Deduplicator)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Documentation Input
- **Catalog path**: Path to the agent catalog to document (default `catalog/agents.yaml`)
- **Output directory**: Directory where generated docs will be written (default `docs/catalog/`)
- **Format**: `full` (all sections), `matrix` (capability matrix only), or `governance` (governance guide only); default `full`
- **Include archived agents**: `include_archived=true|false` — whether to include deprecated/archived agent definitions; default `false`

### 2. Validate and Inventory the Catalog
- Load the catalog and validate every agent entry for required fields: `name`, `capabilities` (non-empty list), `version`, and `owner`
- List all agents with **missing capability descriptions** — these are documentation-blockers and must be reported before generation proceeds, per the constitution's mandatory capability inventory pattern
- Check that all `replaced_by` references in archived agents resolve to existing active agents in the catalog
- Report catalog health summary: total agents, agents with incomplete data, agents flagged for >80% overlap with any peer

```python
def inventory_catalog(catalog_path: str) -> dict:
    """Validate catalog completeness and return a health summary."""
    import yaml
    with open(catalog_path) as f:
        catalog = yaml.safe_load(f)
    agents = catalog.get("agents", [])
    incomplete = [
        a["name"] for a in agents
        if not a.get("capabilities") or not a.get("owner")
    ]
    return {
        "total_agents": len(agents),
        "incomplete_entries": incomplete,
        "documentation_blockers": len(incomplete),
    }
```

### 3. Generate the Capability Matrix
- Build an N×agent matrix where rows are capability tokens and columns are agent names; mark each cell `✓` (present) or blank (absent)
- Group capabilities by functional domain (e.g., "customer support", "data pipeline", "routing") using embedding clustering to surface natural groupings in the matrix
- Highlight cells where capability overlap between any two agents is ≥ threshold — these are the cells that governance reviewers will focus on for consolidation decisions

```
Capability Matrix (excerpt):
                         support-router   helpdesk-dispatcher   data-validator
ticket routing                ✓                  ✓
route support tickets         ✓                  ✓
validate data schema                                                  ✓
ingest csv files                                                      ✓
```

### 4. Build the Overlap and Deduplication Summary
- Compute pairwise similarity for all active agent pairs; produce a sorted list of high-overlap pairs (similarity ≥ 0.6) with both cosine and Jaccard scores
- Include a plain-language explanation for each flagged pair: which specific capabilities overlap, and whether a prior consolidation decision was already recorded in the governance audit trail
- Link each flagged pair to the `/compare-scope-deduplicator` and `/refactor-scope-deduplicator` workflows so reviewers have clear next steps without needing to look up the process

### 5. Write the Governance Guide and Finalize Documentation
- Generate `docs/catalog/governance-guide.md` covering: how to add a new agent (must pass similarity scan first), how to deprecate an agent, how to appeal a consolidation recommendation, and how to request a threshold change with approval
- Write the full catalog documentation to `docs/catalog/README.md` including: health summary, capability matrix, overlap report, and all agent definitions with descriptions and owners
- Update the `docs/catalog/LAST_GENERATED` timestamp and confirm the schema version is set to `1.1.0`

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide catalog path and desired output format (`full`, `matrix`, or `governance`). |
| `scope-deduplicator-constitution.md` not found | Stop. Ensure constitution file is present at repo root — the governance guide section references it directly. |
| Missing capability descriptions (agents with empty or null capabilities field) | Halt documentation generation for those specific agents. List all blockers clearly. Do not generate partial documentation silently — a partially documented catalog creates a false sense of completeness. |
| Outdated agent catalog (catalog schema version does not match `env-config.yaml` `schema_version: "1.1.0"`) | Warn prominently and refuse to generate documentation. Run `catalog sync` to reconcile schema versions first — do not generate docs against a stale schema. |
| Broken agent links (`replaced_by` references a non-existent agent) | Flag all broken references in the health summary report. Documentation may continue but the broken-links section must include a remediation note directing the catalog owner to update or remove the stale references. |
| Output directory not writable | Stop. Report the path and the permissions required. Do not silently fall back to a temp directory. |

## Examples

**Example 1**: `/document-scope-deduplicator "catalog=<agent catalog file> output=<catalog output directory> format=full"`

**Example 2**: `/document-scope-deduplicator "catalog=<agent catalog file> format=governance include_archived=true"` — generates only the governance guide, including archived agent history for audit trail completeness
