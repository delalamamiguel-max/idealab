---
description: Generate, audit, and update documentation for the Reuse Master component catalog and discovery API
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Documentation Scope
- **Extract scope** from `$ARGUMENTS` — targets: `catalog` (generate component index), `api` (document `ComponentDiscovery` public API), `README` (update usage guide), `full` (all three)
- **Inventory existing docs**: check `docs/`, `README.md`, `catalog/README.md`, and inline docstrings — identify what exists vs. what is missing or stale
- **Set freshness threshold**: documentation older than the last catalog update date is considered outdated and must be flagged

### 2. Generate Component Catalog Index
- **Auto-generate a human-readable catalog index** from `catalog/components.yaml`:

```python
from reuse_master.docs import generate_catalog_index

index = generate_catalog_index(
    catalog_path="component catalog file",
    output_path="catalog index output file",
    include_usage_stats=True,
    group_by="type"  # archetype | tool | prompt | workflow
)
print(f"Generated index: {index.component_count} components, {index.section_count} sections")
```

- **Structure the index** by component type (archetypes, tools, prompts, workflows) with alphabetical sort within each section
- **Include for each component**: name, type, description (first sentence), keywords summary, usage count, version, last-updated date, and link to full spec

### 3. Document the Discovery API
- **Extract all public methods** from `ComponentDiscovery` class — `__init__`, `search`, `recommend`, `embed_catalog`, `get_component`
- **Verify docstrings exist and are complete** for each method — parameter types, return types, and at least one usage example:
  ```python
  def search(self, query: str, top_k: int = 5, threshold: float = 0.75) -> list[dict]:
      """
      Search catalog for components semantically relevant to query.

      Args:
          query:     Natural language description of needed capability.
          top_k:     Maximum results to return (default 5).
          threshold: Minimum cosine similarity to include (default 0.75).

      Returns:
          List of component dicts sorted by score descending.
          Each dict: {name, type, description, score, keywords, version}.

      Example:
          >>> discovery.search("handle user authentication with OAuth", top_k=3)
      """
  ```
- **Generate `docs/API_REFERENCE.md`** from extracted docstrings with navigation links between sections

### 4. Update README and Usage Guide
- **Audit `README.md`** for stale content: installation steps, quick-start example, supported Python versions, and library version requirements
- **Update library versions** from `env-config.yaml` `variables.available_libraries` — README and config must stay in sync
- **Verify all external links** (GitHub, PyPI, model hub URLs) — flag broken links for immediate correction
- **Add a "How to discover components" section** if missing — most developers never read the API reference; a 10-line quick-start drives 80% of adoption

### 5. Validate and Publish Documentation
- **Lint all generated Markdown** with a schema check — broken tables, missing headers, and unclosed code fences degrade readability
- **Run link checker** on all local cross-references in docs (`docs/**/*.md`) — ensure anchor links resolve correctly
- **Update `docs/LAST_UPDATED.md`** with generation timestamp and scope of this documentation run — auditors need this trail

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: specify documentation target — e.g. `/document-reuse-master catalog/components.yaml full` or `/document-reuse-master api`. |
| Missing docstrings in source (`ComponentDiscovery` methods undocumented) | Do not generate empty API reference stubs. Flag each undocumented method by name and stop. Require docstrings to be written first — empty docs are worse than no docs. |
| Outdated README (last modified before latest catalog update) | Flag as stale. Show diff of what changed in catalog since README was last updated. Prompt user to review and approve updated sections before overwriting. |
| Broken links found in docs or README | List all broken URLs with their source file and line number. Do not publish documentation containing broken links. Fix or remove each broken link before finalising. |
| `catalog/components.yaml` empty or missing | Stop. Cannot generate catalog index from empty source. Ensure catalog is populated and schema-validated before documentation run. |
| Generated documentation exceeds 5000 lines | Split output into multiple files by component type. Update navigation links accordingly. Warn user of catalog size and suggest archiving legacy components. |

## Examples

**Example 1**: `/document-reuse-master catalog/components.yaml full` — generates catalog index, API reference, and updates README in one pass

**Example 2**: `/document-reuse-master catalog/components.yaml api` — documents only the `ComponentDiscovery` public API methods and writes `docs/API_REFERENCE.md`
