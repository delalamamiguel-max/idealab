# Archetype Architect

## Overview

The **Archetype Architect** is the meta-archetype responsible for creating, refining, quality-controlling, and documenting all archetypes in the ecosystem. It serves as the foundation for maintaining consistency, quality, and discoverability across the entire archetype inventory.

## When to Use

- **Creating new archetypes** - Design and scaffold complete archetype packages
- **Refactoring existing archetypes** - Improve structure, update manifests, fix issues
- **Quality control** - Validate archetypes against ecosystem standards
- **Documentation** - Generate comprehensive documentation for archetypes
- **Comparing approaches** - Evaluate different archetype design options

## Quick Start

```bash
# Create a new archetype
/scaffold-archetype-architect "Create an archetype for data validation pipelines"

# Validate an existing archetype
/test-archetype-architect data-pipeline-builder

# Refactor an archetype to current standards
/refactor-archetype-architect sql-query-crafter

# Generate documentation for an archetype
/document-archetype-architect documentation-evangelist
```

## Workflows

| Workflow | Purpose |
|----------|---------|
| `/scaffold-archetype-architect` | Create new archetypes with all required components |
| `/refactor-archetype-architect` | Improve existing archetypes to meet current standards |
| `/compare-archetype-architect` | Evaluate archetype design options and approaches |
| `/test-archetype-architect` | Validate archetype structure and quality |
| `/debug-archetype-architect` | Diagnose and fix archetype issues |
| `/document-archetype-architect` | Generate comprehensive archetype documentation |

## Key Principles

1. **No versioning in core assets** - Version tracking belongs in `changelog.md`, not manifests or workflows
2. **Leverage core orchestration** - Delegate general work to `00-core-orchestration` workflows
3. **Maximize routing benefits** - Use specialist archetypes for their expertise
4. **Inventory awareness** - Check ecosystem size before creating new archetypes (threshold: 50)
5. **Handle circular dependencies gracefully** - Meta-operations on self are normal and expected

## Standard Archetype Structure

All archetypes should follow this structure:

```
{archetype-slug}/
├── manifest.yaml              # Required: Discovery metadata
├── {slug}-constitution.md     # Required: Rules and guardrails
├── README.md                  # Required: Human-readable overview
├── changelog.md               # Optional: Version history
├── docs/                      # Optional: Extended documentation
├── .koda/workflows/       # Required: Workflow definitions
├── scripts/                   # Optional: Archetype-specific scripts
└── templates/                 # Optional: Archetype-specific templates
```

## Related Archetypes

- `documentation-evangelist` - For high-quality documentation prose and structure
- `00-core-orchestration` - Core routing and discovery infrastructure

## References

- [Constitution](./archetype-architect-constitution.md) - Rules and guardrails
- [Design](./docs/design.md) - Comprehensive architecture documentation
- [Implementation Plan](./docs/implementation-plan.md) - Current refactoring roadmap
- [Changelog](./changelog.md) - Version history
