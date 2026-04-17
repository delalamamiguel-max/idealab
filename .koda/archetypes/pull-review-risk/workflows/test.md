---
description: Validate pull review analysis for accuracy and constitution compliance
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Identify Test Scope

Extract from $ARGUMENTS:
- Analysis report to validate
- Test focus (accuracy, compliance, coverage)

### 2. Run Validation Tests

Check:
- All hard-stop rules enforced
- Mandatory patterns verified
- Report completeness
- Governance matrix accuracy

### 3. Generate Test Report

Report validation results with pass/fail status.

## Error Handling

**No Report**: Run scaffold-pull-review-risk first.

## Examples

```
/test-pull-review-risk "Validate PR #123 risk report"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/pull-review-risk/pull-review-risk-constitution.md`
