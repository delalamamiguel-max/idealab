---
description: Refactor pull review configurations and detection patterns for improved accuracy
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Assess Current Configuration

Review:
- Detection patterns
- Governance matrix weights
- Severity thresholds

### 2. Identify Improvements

Based on feedback:
- Add new risk patterns
- Tune false positive rates
- Update governance criteria

### 3. Apply Refactoring

Update configuration and patterns.

### 4. Validate

Test against known PRs to verify accuracy improvement.

## Error Handling

**Breaking Changes**: Document impact on existing workflows.

## Examples

```
/refactor-pull-review-risk "Add detection for new CVE pattern"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/pull-review-risk/pull-review-risk-constitution.md`
