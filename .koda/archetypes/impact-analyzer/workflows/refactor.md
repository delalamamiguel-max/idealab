---
description: Refactor impact analysis configurations for improved accuracy and coverage (Impact Analyzer)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Assess Current Configuration

Extract from $ARGUMENTS:
- Configuration to refactor
- Current issues or gaps
- Target improvements

Review existing configuration for:
- Scan scope completeness
- Risk scoring accuracy
- Ignored paths appropriateness
- Estimation heuristics alignment

### 2. Identify Improvements

**Scan Scope:**
- Add missing file extensions
- Include new code layers
- Adjust ignore patterns

**Risk Scoring:**
- Update risk rules for new patterns
- Calibrate severity levels
- Add domain-specific rules

**Estimation:**
- Adjust baseline effort values
- Update buffer percentages
- Add new complexity categories

### 3. Apply Refactoring

Update configuration files:
- `templates/env-config.yaml` - scan settings
- `constitution.md` - risk rules and heuristics
- `estimation-config.json` - effort models

### 4. Validate Changes

Test refactored configuration:
- Run sample analysis
- Verify scan coverage
- Check risk scoring accuracy
- Validate estimation output

## Error Handling

**Breaking Changes**: Document impact on existing workflows.

**Backward Compatibility**: Preserve existing behavior where possible.

## Examples

### Example 1: Expand Coverage

```
/refactor-impact-analyzer "
Add support for .scala files in code layer scanning.
Current configuration only scans .py files.
"
```

### Example 2: Risk Rules Update

```
/refactor-impact-analyzer "
Add risk rule for MERGE operations - should be Medium Risk.
Currently not categorized.
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/impact-analyzer/impact-analyzer-constitution.md`
- **Configuration**: `${ARCHETYPES_BASEDIR}/impact-analyzer/templates/env-config.yaml`
