---
description: Debug RelationalAI ontology errors, performance issues, and deployment failures
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

# Debug Ontology Workflow

**Archetype**: Ontology Engineer  
**Purpose**: Troubleshoot RAI ontology issues  
**Complexity**: Medium  
**Expected Duration**: 5-15 minutes

---

## When to Use This Workflow

Use `/debug-ontology` when you encounter:
- Rule conflicts or circular dependencies
- Slow query performance
- Model deployment failures
- Data quality issues (missing entities, broken relationships)
- Unexpected query results
- Memory or timeout errors

---

## What This Workflow Does

✅ **Analyzes error messages** and stack traces  
✅ **Identifies root causes** (rule conflicts, data issues, performance)  
✅ **Suggests fixes** with code examples  
✅ **Validates rules** for circular dependencies  
✅ **Profiles query performance** to find bottlenecks  
✅ **Checks data connectivity** to source tables  
✅ **Generates debug report** with recommendations

---

## Common Issues and Solutions

### Issue 1: Circular Rule Dependencies

**Symptom**: Model deployment fails with "circular dependency" error

**Diagnosis**:
```python
# Rule A depends on Rule B
with model.rule():
    entity.property_a = entity.property_b + 1

# Rule B depends on Rule A (circular!)
with model.rule():
    entity.property_b = entity.property_a * 2
```

**Fix**: Reorder rules or use intermediate properties
```python
# Fix: Use explicit ordering
with model.rule():
    entity.property_b = entity.original_value * 2

with model.rule():
    entity.property_a = entity.property_b + 1
```

---

### Issue 2: Slow Query Performance

**Symptom**: Queries timeout or take >60 seconds

**Diagnosis**: Missing filters, Cartesian joins, unbounded queries

**Fix**: Add filters on high-cardinality attributes first
```python
# Before (slow)
with model.query() as select:
    addr = Address()
    addr.city_name == search_term  # Scans all addresses

# After (fast)
with model.query() as select:
    addr = Address()
    addr.state_id == 'NC'  # Filter first (reduces 98%)
    addr.city_name == search_term  # Then search
```

---

### Issue 3: Deployment Failures

**Symptom**: Model deployment fails with authentication or connection errors

**Diagnosis**: Check RAI credentials, network connectivity, model size

**Fix**:
```python
# Add error handling and validation
try:
    rai_client = rai.Client(profile=config.get('relationalai.profile'))
    rai_client.deploy_model(model)
except rai.AuthenticationError:
    logger.error("RAI authentication failed. Check profile configuration.")
except rai.DeploymentError as e:
    logger.error(f"Deployment failed: {e}. Check model size and syntax.")
```

---

## Example Usage

```
User: /debug-ontology My model deployment is failing with "circular dependency" error

AI: Analyzing your ontology for circular dependencies...

Found circular dependency:
  Rule at line 45: entity.cleansed_city depends on entity.resolved_city
  Rule at line 67: entity.resolved_city depends on entity.cleansed_city

Recommended fix:
1. Reorder rules so cleansed_city is computed first
2. Use cleansed_city as input to resolved_city
3. Remove backward dependency

✅ Circular dependency resolved
```

---

## Error Handling

**No Error Message**: Request specific symptoms or behavior being observed.

**Multiple Issues**: Prioritize by severity - fix hard-stop violations first, then performance.

**Environment Issues**: Verify RAI connectivity and credentials before deep debugging.

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/ontology-engineer/ontology-engineer-constitution.md`
- **Related**: scaffold-ontology-engineer, refactor-ontology-engineer

---

**Archetype**: Ontology Engineer  
**Version**: 1.0.0  
**Last Updated**: 2025-10-09
