---
description: Generate test harness for RelationalAI ontology with unit tests, integration tests, and performance benchmarks
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

# Test Ontology Workflow

**Archetype**: Ontology Engineer  
**Purpose**: Generate comprehensive test suite for RAI ontology  
**Complexity**: Medium  
**Expected Duration**: 10-15 minutes

## When to Use

Use `/test-ontology` to generate tests for:
- Type definitions and hierarchies
- Data cleansing rules
- Matching and inference rules
- Query patterns
- End-to-end workflows
- Performance benchmarks

## What This Generates

✅ Unit tests for individual rules  
✅ Integration tests for workflows  
✅ Performance benchmarks  
✅ Data quality assertions  
✅ Test fixtures and mock data  
✅ pytest configuration

## Example Output

```python
def test_city_cleansing():
    """Test city name standardization"""
    config = load_test_config()
    model = create_model(config)
    
    with model.query() as select:
        addr = Address()
        addr.original_city == 'new york'
        result = select(addr.cleansed_city)
    
    assert result.results[0] == 'NEW YORK'
```

## Error Handling

**No Ontology Path**: Request path to ontology files to analyze for test generation.

**Missing Test Dependencies**: Add pytest and fixtures to requirements.txt.

**RAI Connection Required**: Note tests requiring live RAI connection vs. mock-based tests.

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/ontology-engineer/ontology-engineer-constitution.md`
- **Related**: scaffold-ontology-engineer, debug-ontology-engineer

---

**Archetype**: Ontology Engineer  
**Version**: 1.0.0
