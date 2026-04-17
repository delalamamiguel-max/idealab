# Reuse Master

**Category:** 10-agentic-development | **Version:** 1.0.0

Discover and recommend reusable agent components, patterns, and archetypes from the organizational catalog.

## Purpose

- Prevent reinvention of existing components across teams
- Enable natural-language semantic search over the component catalog
- Recommend relevant reusable components based on similarity scoring
- Track adoption metrics to prioritize maintenance effort
- Keep the catalog current and discoverable

## When to Use

- You need to find an existing agent, tool, or pattern before building from scratch
- You want to register a new reusable component in the catalog
- You need adoption/usage analytics on shared components

## Quick Start

```
/scaffold-reuse-master "Create component catalog for data-pipeline agents"
/compare-reuse-master "Compare embedding vs keyword search for catalog discovery"
```

## Key Features

- **Semantic Search** — sentence-transformers + FAISS for natural-language queries
- **Similarity Scoring** — configurable threshold (default 0.75) for recommendations
- **Usage Tracking** — adoption counts per component for prioritization
- **Catalog Maintenance** — automated staleness detection

## Dependencies

- `sentence-transformers>=2.2.0`
- `faiss-cpu>=1.7.0`
- `numpy>=1.24.0`

## Workflows

| Workflow | Command | Description |
|----------|---------|-------------|
| Scaffold | `/scaffold-reuse-master` | Create discovery system |
| Refactor | `/refactor-reuse-master` | Improve discovery |
| Debug | `/debug-reuse-master` | Fix discovery issues |
| Test | `/test-reuse-master` | Validate discovery |
| Compare | `/compare-reuse-master` | Compare approaches |
| Document | `/document-reuse-master` | Generate docs |

## References

- [reuse-master-constitution.md](reuse-master-constitution.md)
