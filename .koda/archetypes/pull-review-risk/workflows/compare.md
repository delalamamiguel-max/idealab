---
description: Compare risk profiles between PRs or analysis approaches
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Identify Comparison

Extract from $ARGUMENTS:
- Items to compare (PRs, reports, patterns)
- Comparison criteria

### 2. Gather Data

Load risk reports or analyze PRs for comparison.

### 3. Generate Comparison

Create comparison matrix:
- Risk levels
- Violation counts
- Governance scores

### 4. Recommend

Provide recommendation based on comparison.

## Error Handling

**Insufficient Data**: Request additional PRs or reports.

## Examples

```
/compare-pull-review-risk "Compare risk profile of PR #123 vs PR #124"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/pull-review-risk/pull-review-risk-constitution.md`
