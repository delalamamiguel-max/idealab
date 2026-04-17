---
description: Compare impact analysis approaches, risk assessments, or change strategies (Impact Analyzer)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Identify Comparison Scope

Extract from $ARGUMENTS:
- Items to compare (reports, approaches, strategies)
- Comparison criteria
- Decision context

**Comparison Types:**
- **Report Comparison**: Compare two impact analysis reports
- **Approach Comparison**: Compare change implementation strategies
- **Risk Assessment**: Compare risk levels of different change options

### 2. Gather Comparison Data

**For Report Comparison:**
- Load both impact reports
- Extract key metrics (files affected, risk levels, estimates)

**For Approach Comparison:**
- Document each approach's impact profile
- Assess risk and effort for each

### 3. Generate Comparison Matrix

| Criterion | Option A | Option B | Recommendation |
|-----------|----------|----------|----------------|
| Files Affected | | | |
| High Risk Items | | | |
| Effort Estimate | | | |
| Rollback Complexity | | | |
| Orchestration Impact | | | |

### 4. Provide Recommendation

Based on comparison:
- Recommend lower-risk option
- Note trade-offs
- Suggest mitigation strategies

## Error Handling

**Insufficient Data**: Request additional analysis for fair comparison.

**Incomparable Items**: Note fundamental differences that prevent direct comparison.

## Examples

### Example 1: Report Comparison

```
/compare-impact-analyzer "
Compare impact of renaming TABLE_A vs adding VIEW_A alias.
Reports: impact_rename.md, impact_alias.md
Which approach is lower risk?
"
```

### Example 2: Strategy Comparison

```
/compare-impact-analyzer "
Compare big-bang migration vs phased column addition.
Target: Adding 5 columns to CUSTOMER table.
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/impact-analyzer/impact-analyzer-constitution.md`
- **Risk Assessment**: Constitution Section IV - Risk Assessment Rules
