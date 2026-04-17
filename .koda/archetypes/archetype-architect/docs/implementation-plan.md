# Archetype Architect Refactor - Implementation Plan

## Overview

This document outlines the implementation plan for refactoring the `archetype-architect` to optimize its role as the meta-archetype for creating, refining, and quality-controlling other archetypes within the ecosystem.

---

## Guiding Principles

### 1. No Versioning in Core Assets
- **NEVER** include version information in manifests, constitutions, or workflows
- Version tracking belongs in `changelog.md` or `version-notes.md` within each archetype
- Reduces LLM token consumption and hallucination risk from stale context

### 2. Leverage Core Orchestration
- All archetype operations should delegate to `00-core-orchestration` workflows
- Use `/<workflow-name>` routing for general activities
- Archetype-specific workflows add value on top of core routing

### 3. Maximize Routing Benefits
- Archetypes delegate general work to specialists via discovery
- Example: Documentation workflow uses `documentation-evangelist` for prose quality, but ensures domain-specific content is accurate

### 4. Handle Circular Dependencies Gracefully
- When modifying the archetype that supports the modification (meta-operations)
- Use best available workflow, execute, then evaluate results
- No special "catch-22" handling needed - frontier models handle this naturally

### 5. Inventory Threshold Before Creation
- If ecosystem has <50 archetypes, prompt user to expand inventory first
- Prevents duplication of function across archetypes
- User can override with explicit confirmation

---

## Implementation Phases

### Phase 1: Cleanup and Manifest Schema Update

| Task | Priority | Effort | Description |
|------|----------|--------|-------------|
| 1.1 Delete TEMP workflow | HIGH | 10 min | Remove `TEMP_TO_BE_REFACTORED___integrate-archetype-architect.md` |
| 1.2 Update manifest schema | HIGH | 30 min | Add `constitution` field, `dependencies` field; remove any version fields |
| 1.3 Fix archetype-architect manifest | HIGH | 15 min | Update keywords, add constitution reference, add dependencies |
| 1.4 Create changelog.md template | MEDIUM | 20 min | Version tracking file template for archetypes |

**Deliverables:**
- [ ] TEMP workflow deleted
- [ ] New manifest schema documented
- [ ] archetype-architect manifest updated
- [ ] changelog.md template created

---

### Phase 2: Discovery Script Enhancement

| Task | Priority | Effort | Description |
|------|----------|--------|-------------|
| 2.1 Add constitution inspection | HIGH | 45 min | Extend discover-archetype.py to read constitution metadata |
| 2.2 Add dependency resolution | MEDIUM | 30 min | Support for resolving archetype dependencies |
| 2.3 Add inventory count | MEDIUM | 15 min | Return total archetype count for threshold checks |

**Deliverables:**
- [ ] discover-archetype.py enhanced with constitution support
- [ ] Dependency resolution added
- [ ] Inventory count feature added

---

### Phase 3: Archetype Structure Standards

| Task | Priority | Effort | Description |
|------|----------|--------|-------------|
| 3.1 Define standard structure | HIGH | 30 min | Document required files and directories |
| 3.2 Create README.md template | HIGH | 20 min | Standard README for archetypes |
| 3.3 Update constitution rules | HIGH | 45 min | Add structure validation rules |

**Standard Archetype Structure:**
```
{archetype-slug}/
├── manifest.yaml              # Required: Discovery metadata
├── {archetype-slug}-constitution.md  # Required: Rules and guardrails
├── README.md                  # Required: Human-readable overview
├── changelog.md               # Optional: Version history
├── docs/                      # Optional: Extended documentation
│   ├── design.md
│   ├── implementation-plan.md
│   └── roadmap.md
├── .koda/
│   └── workflows/             # Required: At least scaffold workflow
│       ├── scaffold-{slug}.md
│       ├── refactor-{slug}.md
│       ├── compare-{slug}.md
│       ├── test-{slug}.md
│       ├── debug-{slug}.md
│       └── document-{slug}.md
├── scripts/                   # Optional: Archetype-specific scripts
└── templates/                 # Optional: Archetype-specific templates
```

**Deliverables:**
- [ ] Standard structure documented
- [ ] README.md template created
- [ ] Constitution updated with structure rules

---

### Phase 4: Workflow Refactoring

| Task | Priority | Effort | Description |
|------|----------|--------|-------------|
| 4.1 Refactor scaffold-archetype-architect | HIGH | 2 hrs | Leverage core/solution workflows, add inventory check |
| 4.2 Refactor document-archetype-architect | HIGH | 1.5 hrs | Use solution-document, delegate to documentation-evangelist |
| 4.3 Refactor refactor-archetype-architect | MEDIUM | 1.5 hrs | Leverage core refactor workflow |
| 4.4 Refactor compare-archetype-architect | MEDIUM | 1 hr | Leverage core compare workflow |
| 4.5 Refactor test-archetype-architect | MEDIUM | 1 hr | Add quality assertion tests |
| 4.6 Refactor debug-archetype-architect | MEDIUM | 1 hr | Leverage core debug workflow |
| 4.7 Fix outdated path references | LOW | 30 min | Update all `scripts/python/` to `00-core-orchestration/scripts/` |

**Key Workflow Patterns:**

```markdown
## Example: Delegating to Core Orchestration

### Step N: Generate Documentation
// turbo
Execute `/solution-document` with context:
- Primary archetype: {target-archetype}
- Documentation specialist: documentation-evangelist
- Domain context: {archetype-specific-details}

This ensures prose quality from documentation-evangelist while
maintaining domain accuracy from the target archetype.
```

**Deliverables:**
- [ ] All 6 workflows refactored
- [ ] Core/solution delegation patterns implemented
- [ ] Inventory threshold (50) check in scaffold
- [ ] Path references corrected

---

### Phase 5: Batch Manifest Updates

| Task | Priority | Effort | Description |
|------|----------|--------|-------------|
| 5.1 Create migration script | HIGH | 45 min | Script to update all 70 manifests |
| 5.2 Execute batch update | HIGH | 30 min | Run migration, validate results |
| 5.3 Validate manifests | HIGH | 30 min | Ensure all manifests pass schema validation |

**Manifest Schema Changes:**
```yaml
# Before
archetype:
  name: example-archetype
  description: ...
  keywords: [...]
  workflows: {...}
version: '1.0'  # REMOVE THIS

# After
archetype:
  name: example-archetype
  description: ...
  keywords: [...]
  constitution:
    path: example-archetype-constitution.md
  dependencies:
    - 00-core-orchestration  # Always required
    # Only add hard dependencies, use discovery for general needs
  workflows: {...}
# NO version field - use changelog.md instead
```

**Deliverables:**
- [ ] Migration script created and tested
- [ ] All 70 manifests updated
- [ ] Schema validation passing

---

### Phase 6: Documentation and README Updates

| Task | Priority | Effort | Description |
|------|----------|--------|-------------|
| 6.1 Create archetype-architect README | HIGH | 30 min | Human-readable overview |
| 6.2 Update 00-core-orchestration README | MEDIUM | 20 min | Reference new manifest schema |
| 6.3 Create batch README script | LOW | 45 min | Generate README stubs for archetypes missing them |

**Deliverables:**
- [ ] archetype-architect README.md created
- [ ] 00-core-orchestration README updated
- [ ] README generation script available

---

### Phase 7: Final Validation

| Task | Priority | Effort | Description |
|------|----------|--------|-------------|
| 7.1 Run discover-archetype.py tests | HIGH | 15 min | Validate discovery with new schema |
| 7.2 Test workflow routing | HIGH | 30 min | Validate all core orchestration routes |
| 7.3 Test archetype-architect workflows | HIGH | 45 min | Full cycle: scaffold, refactor, test |
| 7.4 Fix notebook typo (Phase 5 pending) | LOW | 10 min | Name mismatch fix |

**Deliverables:**
- [ ] Discovery script validated
- [ ] Routing validated
- [ ] Workflows validated
- [ ] All pending issues resolved

---

## Timeline Summary

| Phase | Estimated Effort | Dependencies |
|-------|------------------|--------------|
| Phase 1: Cleanup & Schema | 1.5 hours | None |
| Phase 2: Discovery Enhancement | 1.5 hours | Phase 1 |
| Phase 3: Structure Standards | 1.5 hours | Phase 1 |
| Phase 4: Workflow Refactoring | 8.5 hours | Phases 1-3 |
| Phase 5: Batch Manifest Updates | 2 hours | Phases 1-3 |
| Phase 6: Documentation | 1.5 hours | Phases 1-5 |
| Phase 7: Validation | 1.5 hours | All phases |

**Total Estimated Effort: ~18 hours**

---

## Success Criteria

1. **Programmatic Quality Inspection**: `discover-archetype.py` can inspect any archetype's constitution
2. **Zero Version Fields**: No version information in manifests, constitutions, or workflows
3. **Consistent Structure**: All archetypes follow the standard directory structure
4. **Core Orchestration Leverage**: archetype-architect workflows delegate to core/solution workflows
5. **Routing Maximization**: Workflows leverage specialist archetypes for general tasks
6. **Inventory Awareness**: Scaffold prompts user if <50 archetypes exist before creating new ones
7. **README Coverage**: All archetypes have README.md at root
8. **Dependency Clarity**: Hard dependencies declared in manifest; soft dependencies via discovery

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Breaking existing workflows | Incremental rollout, test each phase |
| Missing constitution references | Migration script validates before updating |
| Circular dependency confusion | Document clear meta-operation patterns |
| Discovery script regression | Maintain backward compatibility |

---

## Next Steps

1. Review and approve this implementation plan
2. Begin Phase 1: Cleanup and Schema Update
3. Proceed sequentially through phases
4. Checkpoint after each phase for validation
