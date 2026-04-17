---
description: Debug impact analysis failures, scanning issues, and report generation problems (Impact Analyzer)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Identify Issue Category

Extract from $ARGUMENTS:
- Error message or symptom
- Failed analysis details
- Codebase path used
- Target object analyzed

**Issue Categories:**
- **Scanning Failures**: Files not found, permission errors, timeout
- **Ambiguous Targets**: Multiple matches, unclear object specification
- **Report Errors**: Missing sections, incorrect risk scoring
- **Environment Issues**: Missing tools, invalid paths

### 2. Run Diagnostic Checks

**For Scanning Failures:**
- Verify codebase path exists and is accessible
- Check file permissions on target directories
- Verify search tools (grep, find) are available
- Test scanning on small subset

**For Ambiguous Targets:**
- List all matches for target object
- Show context for each match
- Recommend qualification pattern

**For Report Errors:**
- Review constitution compliance
- Check risk categorization logic
- Verify estimation calculations

### 3. Analyze Root Cause

Common root causes:
- Invalid or relative codebase path
- Target object spelled incorrectly
- Files in ignored directories
- Insufficient permissions
- Missing file extensions in scan scope

### 4. Apply Fix

Based on diagnosis:
- Correct path specification
- Qualify ambiguous target (e.g., `TABLE.column`)
- Adjust scan scope in configuration
- Fix permission issues

### 5. Re-run Analysis

Retry the impact analysis with corrected parameters and verify success.

## Error Handling

**Path Not Found**: Provide guidance on absolute path format.

**No Results**: Check if target exists and spelling is correct.

**Timeout**: Suggest narrowing scan scope or excluding large directories.

## Examples

### Example 1: No Results Found

```
/debug-impact-analyzer "
Impact analysis returned 'No Impact Detected' but I know the table is used.
Target: CUSTOMER_DATA
Path: /Users/me/project
"
```

### Example 2: Ambiguous Match

```
/debug-impact-analyzer "
Analysis failed with 'Ambiguous Target' error.
Target: id
Multiple tables have this column.
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/impact-analyzer/impact-analyzer-constitution.md`
- **Search Scope**: Constitution Section V - Search Scope
