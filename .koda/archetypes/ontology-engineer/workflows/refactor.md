---
description: Refactor existing RelationalAI ontology to apply security, performance, and maintainability best practices
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

# Refactor Ontology Workflow

**Archetype**: Ontology Engineer  
**Purpose**: Improve existing RAI ontology code quality and standards compliance  
**Complexity**: Medium  
**Expected Duration**: 10-20 minutes

---

## When to Use This Workflow

Use `/refactor-ontology` when you need to:
- Bring legacy ontology code up to current standards
- Eliminate hard-stop violations (hard-coded values, missing docs)
- Apply modular structure to monolithic ontology files
- Add parameterization for multi-environment deployment
- Improve performance and query optimization
- Add comprehensive documentation and tests

---

## What This Workflow Does

✅ **Analyzes existing ontology** for standards violations  
✅ **Fixes hard-stop violations** (hard-coded sources, unversioned models)  
✅ **Applies mandatory patterns** (documentation, parameterization, tests)  
✅ **Restructures code** into modular organization  
✅ **Adds error handling** and logging  
✅ **Generates tests** for existing rules  
✅ **Creates configuration files** for deployment  
✅ **Documents changes** in refactoring summary

---

## Workflow Steps

### Step 1: Analyze Existing Code

The workflow will:
1. Scan all ontology files for violations
2. Identify hard-coded database/schema names
3. Check for unversioned model names
4. Assess documentation coverage
5. Evaluate code organization
6. Generate analysis report

**Example Output**:
```
Analysis Report:
❌ 4 hard-stop violations found
⚠️  6 mandatory patterns missing
📋 5% documentation coverage
🔧 Monolithic structure (1 file, 3000 lines)

Violations:
1. Hard-coded source: 'PBACON_ATT_DB.BCL.USPS_CITIES' (line 6)
2. Unversioned model: rai.Model('address_matching') (line 4)
3. No error handling in deployment code
4. No test harness
```

---

### Step 2: Fix Hard-Stop Violations

**Before**:
```python
model = rai.Model('address_matching')
RawUSPSCity = model.Type('RawUSPSCity', source='PBACON_ATT_DB.BCL.USPS_CITIES')
```

**After**:
```python
model = rai.Model(config.get_model_full_name())  # Returns: 'address_matching_v1_0_0'
RawUSPSCity = model.Type('RawUSPSCity', source=config.get_data_source('usps_cities'))
```

---

### Step 3: Restructure Code

**Before** (Monolithic):
```
ontology.py  # 3000 lines with types, rules, queries all mixed
```

**After** (Modular):
```
src/ontology/
├── types.py              # Type definitions (300 lines)
├── rules/
│   ├── cleansing.py     # Cleansing rules (200 lines)
│   ├── matching.py      # Matching rules (250 lines)
│   └── inference.py     # Inference rules (150 lines)
└── queries.py           # Query patterns (200 lines)
```

---

### Step 4: Add Documentation

The workflow adds:
- File-level docstrings with purpose and author
- Function docstrings with Args, Returns, Examples
- Rule-level comments explaining business logic
- Architecture documentation
- API reference

---

### Step 5: Generate Configuration

Creates environment-specific config files:
```yaml
# CDO-AIFC/reference/config/dev.yaml
snowflake:
  database: "{{var.database}}"
  schema: "{{var.schema}}"

relationalai:
  model_name: "address_matching"
  version: "1.0.0"

data_sources:
  usps_cities: "USPS_CITIES"
```

---

### Step 6: Generate Tests

Creates test harness:
```python
def test_existing_rule():
    """Test that existing cleansing rule works correctly"""
    config = load_config('CDO-AIFC/reference/config/test.yaml')
    model = create_model(config)
    
    # Test existing business logic
    with model.query() as select:
        # ... test implementation
```

---

### Step 7: Generate Refactoring Summary

Creates detailed summary document:
- List of all changes made
- Before/after comparisons
- Metrics (documentation coverage, test coverage)
- Migration path
- Risk assessment

---

## Constitutional Guardrails Applied

### ✅ All Hard-Stop Rules Enforced
- Parameterized all data sources
- Added version to model name
- Removed any credentials
- Converted notebooks to scripts
- Documented all rules

### ✅ All Mandatory Patterns Applied
- Modular structure
- Comprehensive documentation
- Full parameterization
- Error handling
- Test harness
- Structured logging

---

## Example Usage

```
User: /refactor-ontology Refactor the code in /path/to/ontology.py

AI: Analyzing existing ontology code...

Found 4 hard-stop violations:
1. Hard-coded source: 'PBACON_ATT_DB.BCL.USPS_CITIES'
2. Unversioned model name
3. No error handling
4. Missing documentation

Refactoring...

✅ Fixed all hard-stop violations
✅ Restructured into modular organization
✅ Added comprehensive documentation (5% → 65%)
✅ Generated test harness
✅ Created configuration files
✅ Generated REFACTORING_SUMMARY.md

Refactored code saved to: ontology_refactored/

Next steps:
1. Review changes in REFACTORING_SUMMARY.md
2. Update config files with your environment values
3. Run tests: pytest tests/
4. Deploy to DEV: python CDO-AIFC/reference/scripts/deploy_ontology.py --config CDO-AIFC/reference/config/dev.yaml
```

---

## Post-Refactoring Checklist

- [ ] All hard-stop violations fixed
- [ ] Code restructured into modules
- [ ] Documentation coverage >60%
- [ ] Configuration files created
- [ ] Tests generated and passing
- [ ] Refactoring summary reviewed
- [ ] Ready for deployment

---

## Error Handling

**No Code Provided**: Request path to ontology files for refactoring analysis.

**Major Violations**: Address hard-stop violations before proceeding with other improvements.

**Production Code**: Recommend staging deployment for testing before production rollout.

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/ontology-engineer/ontology-engineer-constitution.md`
- **Related**: scaffold-ontology-engineer, debug-ontology-engineer

---

**Archetype**: Ontology Engineer  
**Version**: 1.0.0  
**Last Updated**: 2025-10-09
