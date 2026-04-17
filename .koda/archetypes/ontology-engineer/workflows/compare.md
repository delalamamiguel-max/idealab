---
description: Compare RelationalAI ontology design approaches and patterns
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

**SUCCESS CRITERIA**:
- Search for directory: "00-core-orchestration"
- Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory

**HALT IF**:
- Directory "00-core-orchestration" is not found
- `${ARCHETYPES_BASEDIR}` is not set

Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

---

# Compare Ontology Workflow

**Archetype**: Ontology Engineer  
**Purpose**: Evaluate different ontology design approaches  
**Complexity**: Low  
**Expected Duration**: 5-10 minutes

## When to Use

Use `/compare-ontology` to compare:
- Type hierarchy vs. flat structure
- Eager vs. lazy rule evaluation
- Normalized vs. denormalized entity design
- Different matching strategies
- Performance trade-offs

## What This Provides

✅ Side-by-side comparison of approaches  
✅ Pros and cons analysis  
✅ Performance implications  
✅ Maintainability assessment  
✅ Recommendation with rationale

## Example

```
User: /compare-ontology Should I use type hierarchies or flat types for addresses?

AI: Comparing approaches...

Approach 1: Type Hierarchy
Address (abstract) → InlapAddress, CimAddress

Pros:
- Shared properties via inheritance
- Type-specific rules
- Clear semantic meaning

Cons:
- More complex queries
- Potential performance overhead

Approach 2: Flat Types
InlapAddress, CimAddress (independent)

Pros:
- Simpler queries
- Better performance
- Easier to understand

Cons:
- Code duplication
- Harder to maintain shared logic

Recommendation: Use Type Hierarchy
Rationale: Better maintainability outweighs slight performance cost
```

## Error Handling

**Unclear Comparison**: Ask for specific design decision or trade-off to evaluate.

**Missing Context**: Request current ontology structure for informed comparison.

**Performance Critical**: Note when performance must be prioritized over maintainability.

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/ontology-engineer/ontology-engineer-constitution.md`
- **Related**: scaffold-ontology-engineer, refactor-ontology-engineer

---

**Archetype**: Ontology Engineer  
**Version**: 1.0.0
