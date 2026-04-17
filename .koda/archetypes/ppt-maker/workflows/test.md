---
description: Validate PowerPoint presentation against template conformance (PPT-Maker)
auto_execution_mode: 1
---

**Archetype**: PPT-Maker (Documentation Requirements)

**The root directory is ../../../../../ from THIS file**

**Constitution**: `${ARCHETYPES_BASEDIR}/ppt-maker/ppt-maker-constitution.md`  
**Environment**: `${ARCHETYPES_BASEDIR}/ppt-maker/templates/env-config.yaml`

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Parse Validation Request

Extract from $ARGUMENTS:
- **Target presentation**: File path to validate
- **Validation level**: Quick check vs. comprehensive audit
- **Focus areas**: Specific aspects to validate (optional)

### 2. Run Validation Suite

Run `python3 ../../scripts/ppt_engine_focused.py validate [TARGET_FILE] --json` to execute full validation.

### 3. Parse Validation Results

Categorize findings:
- **Errors** (Critical violations):
  - Missing mandatory slides (title or logo)
  - Modified slide layouts
  - Non-template elements added
  - Broken template structure
  
- **Warnings** (Recommended fixes):
  - Text exceeding character limits
  - Content overflow in placeholders
  - Non-optimal slide type usage
  
- **Info** (Informational):
  - Slide count
  - Content distribution
  - Style consistency

### 4. Generate Validation Report

Create comprehensive markdown report:

```markdown
# Presentation Validation Report

**File**: [PRESENTATION_NAME]
**Validated**: [TIMESTAMP]
**Template**: AT&T Day-to-Day Quickstart 2025

## Summary

- ✓ **Conformance Score**: [SCORE]/100
- **Errors**: [COUNT] 🔴
- **Warnings**: [COUNT] ⚠️
- **Info**: [COUNT] ℹ️

## Mandatory Slides Check

✓ **Slide 1 (Title)**: Present
✓ **Slide 12 (Logo)**: Present and positioned last

## Content Constraints Check

### Slide-by-Slide Analysis

#### Slide 2: [SLIDE_TYPE]
- **Title**: [LENGTH] chars ([STATUS])
- **Body**: [LENGTH] chars ([STATUS])
- **Issues**: [NONE or LIST_ISSUES]

#### Slide 3: [SLIDE_TYPE]
⚠️ **Warning**: Body content exceeds limit
- Current: 450 chars
- Maximum: 400 chars
- **Suggestion**: Summarize or split content

[... continue for all slides ...]

## Layout Integrity Check

✓ All slide layouts match template
✓ No unauthorized modifications detected
✓ Color scheme preserved

## Brand Compliance

✓ AT&T Aleck Sans fonts used
✓ AT&T Blue color scheme maintained
✓ Template structure intact

## Detailed Findings

### Errors 🔴
[None found or list detailed errors]

### Warnings ⚠️
1. **Slide 3 / body**: Text exceeds recommended length (450/400 chars)
   - **Suggestion**: Reduce content or split across two slides
   
2. **Slide 5 / subtitle**: Content may be too verbose
   - **Suggestion**: Consider condensing key message

### Informational ℹ️
- Total slides: [COUNT]
- Average content density: [METRIC]
- Slide type distribution:
  - Text-heavy: [COUNT]
  - Two-column: [COUNT]
  - Four-box: [COUNT]
  - Other: [COUNT]

## Recommendations

1. **High Priority**: [FIX_ERRORS]
2. **Medium Priority**: [ADDRESS_WARNINGS]
3. **Optional**: [OPTIMIZATION_SUGGESTIONS]

## Conformance Pass/Fail

**Overall Status**: [PASS ✓ / FAIL ✗]

- Errors present: [YES/NO]
- Critical violations: [YES/NO]
- Ready for distribution: [YES/NO]

## Next Steps

[IF PASSED]:
✅ Presentation is template-conformant and ready for use
- No further action required
- Safe to distribute

[IF FAILED]:
🔧 Address identified issues before distribution:
1. Use /refactor-ppt to fix content length issues
2. Use /debug-ppt for detailed troubleshooting
3. Re-validate after changes
```

### 5. Execute Validation

Run validation and generate report.

### 6. Display Results

Show formatted validation report with:
- Color-coded severity levels
- Clear pass/fail status
- Actionable recommendations
- Links to relevant workflows for fixes

## Error Handling

**File Not Found**: Verify file path, check file exists, suggest correct format.

**Corrupted File**: Detect PPTX structure issues, suggest file repair or recreation.

**Template Mismatch**: Identify if presentation uses different template, note compatibility issues.

## Examples

**Example 1**: `/test-ppt outputs/quarterly_review.pptx`
Output: Full validation report with conformance score and detailed findings

**Example 2**: `/test-ppt outputs/kickoff_deck.pptx --focus content-length`
Output: Focused report on text length compliance

**Example 3**: `/test-ppt outputs/presentation.pptx --quick`
Output: Quick validation checking only mandatory requirements

## References

- `/debug-ppt` - Troubleshoot specific issues
- `/refactor-ppt` - Fix identified problems
- `/document-ppt` - Generate presentation summary
