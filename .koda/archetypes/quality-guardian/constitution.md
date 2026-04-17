# quality guardian Constitution

## Purpose

This constitution defines the foundational principles and hard-stop rules for the quality guardian archetype.

**Source**: Converted from `vibe_cdo/quality_guardian/.rules` and `governance_prompt.md`

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** or correct any expectations that violate these rules:

- ✘ **Bad records path required**: Do not omit `.option("badRecordsPath", ...)` on data reads
- ✘ **No hard-coded thresholds**: Do not hard-code thresholds (null %, duplicates, value bounds); use parameters
- ✘ **Pipeline failure required**: Do not generate a suite that does not fail the pipeline on critical expectation breaches
- ✘ **Structured logging required**: Do not log only unstructured or missing summary metrics (`total_checked`, `total_failed`)
- ✘ **Parameterization required**: Do not skip parameterization of table names, email routes, or result sinks

## II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify these patterns:

- ✔ **Bad records path**: Include `.option("badRecordsPath", ...)` on all reads
- ✔ **Parameterized thresholds**: Parameterize all quality thresholds via variables or config (YAML/JSON)
- ✔ **Pipeline failure**: Fail the pipeline on any critical expectation breach
- ✔ **Idempotent sink**: Write results to an idempotent sink (Delta table or DB table)
- ✔ **Regression tests**: Include regression tests comparing current vs baseline distributions
- ✔ **Summary metrics**: Emit summary metrics: `total_checked`, `total_failed`, `failure_rate`

## III. Preferred Patterns (Recommended)

The LLM **should adopt** these patterns unless user overrides:

- ➜ **Modular suites**: Modularize suites into sections (<1000 lines each)
- ➜ **Template reuse**: Reuse expectation templates from a shared quality library
- ➜ **Strategy documentation**: Provide an explanation paragraph summarizing the quality strategy
- ➜ **Consistent naming**: Use consistent naming for expectation variables and test functions
- ➜ **Test integration**: Integrate test suites with PyTest or ScalaTest harness

## IV. JSON Serialization Safety for Quality Metrics

**Template Reference**: 📄 `.cdo-aifc/templates/04-data-governance-quality/quality-guardian/json-serialization-safety-pattern.py`

Quality metrics often contain Python/Pandas/Numpy types that are not directly JSON-serializable, causing `TypeError` when saving results.

### Hard-Stop Rules
- ✘ **Never** pass raw datetime objects to `json.dumps()`
- ✘ **Never** pass Decimal, numpy, or pandas types directly to JSON serialization
- ✘ **Do NOT** skip JSON serialization testing before saving results
- ✘ **Never** assume all Python types are JSON-compatible

### Mandatory Patterns
- ✔ **Convert datetime**: Use `.isoformat()` for datetime objects → strings
- ✔ **Convert Decimal**: Cast to `float()` for Decimal types
- ✔ **Convert numpy types**: Cast `np.int64`, `np.float64` to Python native types
- ✔ **Handle NaT/NaN**: Convert pandas `NaT` and `NaN` to `None`
- ✔ **Helper function**: Use `make_json_serializable()` helper for automatic conversion
- ✔ **Test serialization**: Always test `json.dumps()` before saving to files or tables

### Common Type Conversions

| Python Type | JSON-Compatible Type | Conversion |
|-------------|---------------------|------------|
| `datetime.datetime` | `str` | `.isoformat()` |
| `pd.Timestamp` | `str` | `.isoformat()` |
| `Decimal` | `float` | `float(value)` |
| `np.int64`, `np.int32` | `int` | `int(value)` |
| `np.float64`, `np.float32` | `float` | `float(value)` |
| `pd.NaT`, `np.nan` | `None` | Check with `pd.isna()` |

### Implementation Patterns

#### Pattern 1: Helper Function
```python
def make_json_serializable(obj):
    """Convert object to JSON-serializable format"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, (np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.float64, np.float32)):
        return float(obj)
    elif pd.isna(obj):
        return None
    else:
        return str(obj)
```

#### Pattern 2: Safe Serialization with Validation
```python
def safe_serialize(data_dict):
    """Safely serialize dict to JSON with validation"""
    # Convert non-serializable types
    for key, value in data_dict.items():
        data_dict[key] = make_json_serializable(value)
    
    # Test serialization
    try:
        json_string = json.dumps(data_dict, indent=2)
        return json_string
    except TypeError as e:
        raise ValueError(f"JSON serialization failed: {e}")
```

#### Pattern 3: Quality Metrics Example
```python
# ❌ BAD: Raw types will fail
quality_metrics = {
    "timestamp": datetime.now(),  # Will fail
    "null_rate": Decimal("0.15"),  # Will fail
    "row_count": np.int64(12345)   # Will fail
}

# ✅ GOOD: Convert to JSON-compatible types
quality_metrics = {
    "timestamp": datetime.now().isoformat(),  # String
    "null_rate": float(0.15),                  # Float
    "row_count": int(12345)                    # Int
}
```

### Validation Pattern
Always test before saving:
```python
try:
    json_string = json.dumps(quality_metrics, indent=2)
    print("✅ JSON serialization successful")
except TypeError as e:
    print(f"❌ JSON serialization failed: {e}")
    # Fix non-serializable objects
```

### Template Features
The JSON serialization safety template provides:
1. `make_json_serializable()` helper function
2. `safe_serialize()` with validation
3. Type conversion for datetime, Decimal, numpy, pandas
4. Nested dictionary handling
5. Quality metrics report generation example
6. Testing and validation patterns
7. Troubleshooting guide for common errors

---

**Version**: 1.1.0  
**Last Updated**: 2025-11-23  
**Source**: `/Users/md464h/projects/aifc_projects/eaifc_windsurf/../vibe_cdo/quality_guardian/.rules`  
**Changelog**:
- 1.1.0 (2025-11-23): Added JSON serialization safety patterns for quality metrics
- 1.0.0 (2025-10-07): Initial release
