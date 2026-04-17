---
description: Create component discovery and recommendation system (Reuse Master)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Catalog path**: Path to component catalog
- **Search type**: semantic | keyword | hybrid

### 2. Generate Discovery System

```python
class ComponentDiscovery:
    """Discover reusable components."""
    
    def __init__(self, catalog_path: str):
        self.catalog = load_catalog(catalog_path)
        self.embeddings = create_embeddings(self.catalog)
    
    def search(self, query: str, top_k: int = 5) -> list:
        """Search for relevant components."""
        query_embedding = embed(query)
        return find_similar(query_embedding, self.embeddings, top_k)
    
    def recommend(self, task: str) -> list:
        """Recommend components for a task."""
        return self.search(task)
```

### 3. Generate Catalog Schema

```yaml
components:
  - name: {component_name}
    type: archetype | tool | prompt | workflow
    description: {description}
    keywords: [{keywords}]
    usage_count: {count}
    last_updated: {date}
```

### 4. Validate

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide task description and domain context for similarity search. |
| `reuse-master-constitution.md` not found | Stop. Ensure file is present at repo root. |
| Catalog file not found | Verify `catalog/components.yaml` exists. Run catalog initialisation step if first use. |
| Embedding library not installed | Run `pip install sentence-transformers faiss-cpu numpy`. These are required for semantic search. |
| Similarity search returns 0 results | Catalog may be empty or embeddings not generated. Run `embed_catalog()` before searching. |
| Recommended component is outdated | Check component version and last-updated date. Flag for catalog maintainer review. |

## Examples
**Example**: `/scaffold-reuse-master catalog/components.yaml semantic`
