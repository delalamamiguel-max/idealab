---
description: Validate impact analysis for accuracy, completeness, and constitution compliance (Impact Analyzer)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Identify Test Scope

Extract from $ARGUMENTS:
- Analysis report to validate
- Test scope (completeness, accuracy, compliance)
- Known concerns

### 2. Run Completeness Test

Verify all required sections present:
- Executive Summary with risk level
- Affected Artifacts by type
- Risk categorization (High/Medium/Low)
- Recommended actions for High Risk items
- Cost estimate table

### 3. Run Accuracy Test

Validate analysis findings:
- Spot-check reported dependencies exist
- Verify risk categorization correctness
- Check for false negatives (missed dependencies)
- Validate downstream impact chain

### 4. Run Compliance Test

Check constitution adherence:
- Multi-layer scanning completed
- Direct vs downstream impact distinguished
- Markdown format used
- Breaking changes flagged

### 5. Generate Test Report

Produce validation results:
- Completeness score
- Accuracy assessment
- Compliance checklist
- Recommendations for improvement

## Error Handling

**Missing Report**: Cannot test what doesn't exist. Run analysis first.

**Partial Results**: Note gaps and provide guidance on re-running analysis.

## Examples

### Example 1: Full Validation

```
/test-impact-analyzer "
Validate the impact report for CIM_HIST column addition.
Report: impact_report_20250128.md
Check completeness and accuracy.
"
```

### Example 2: Compliance Check

```
/test-impact-analyzer "
Verify report meets constitution requirements.
Focus on risk categorization and recommended actions.
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/impact-analyzer/impact-analyzer-constitution.md`
- **Reporting Standards**: Constitution Section VI - Reporting Standards
