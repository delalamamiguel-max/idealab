---
description: Debug pull review analysis failures and false positive/negative issues
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Identify Issue

Extract from $ARGUMENTS:
- Analysis that failed or gave incorrect results
- False positives to investigate
- False negatives to understand

### 2. Diagnose

Check for:
- Scanning tool configuration issues
- Pattern matching errors
- Missing file coverage

### 3. Apply Fix

Correct analysis configuration or improve detection patterns.

### 4. Re-run Analysis

Verify fixed analysis produces correct results.

## Error Handling

**No Analysis Found**: Run scaffold-pull-review-risk first.

## Examples

```
/debug-pull-review-risk "False positive on HS-Secret for test mock data"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/pull-review-risk/pull-review-risk-constitution.md`
