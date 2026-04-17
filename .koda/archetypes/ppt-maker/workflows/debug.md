---
description: Diagnose and fix PowerPoint presentation issues and template violations (PPT-Maker)
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

### 1. Parse Debug Request

Extract from $ARGUMENTS:
- **Target presentation**: File path to debug
- **Reported issue**: Specific problem or error message
- **Symptoms**: What's not working as expected

### 2. Run Full Diagnostic

Run `python3 ../../scripts/ppt_engine_focused.py validate [TARGET_FILE]` for comprehensive analysis.

Run `python3 ../../scripts/ppt_engine_focused.py inspect [TARGET_FILE]` to extract detailed metadata.

### 3. Identify Root Causes

Analyze validation and inspection results:

**Common Issues**:
- Missing mandatory slides
- Text content exceeding limits
- Modified slide layouts
- Broken template structure
- Font or color changes
- Non-template elements added

**For Each Issue**:
- Severity: Error / Warning / Info
- Location: Specific slide and element
- Impact: How it affects presentation
- Root cause: Why the issue occurred

### 4. Generate Diagnostic Report

```markdown
# Presentation Diagnostic Report

**File**: [PRESENTATION_NAME]
**Diagnosed**: [TIMESTAMP]

## Issue Summary

🔴 **Critical Issues**: [COUNT]
⚠️ **Warnings**: [COUNT]
ℹ️ **Informational**: [COUNT]

## Detailed Diagnostics

### Issue 1: [ISSUE_TITLE] 🔴
**Location**: Slide [N], Element [ID]
**Severity**: Critical Error

**Problem**: [DETAILED_DESCRIPTION]

**Root Cause**: [EXPLANATION]
- [SPECIFIC_REASON_1]
- [SPECIFIC_REASON_2]

**Impact**:
- Breaks template conformance
- May cause rendering issues
- Violates brand guidelines

**Fix**: 
\`\`\`python
# Automated fix available
modifier.modify_slide([N], {
    "[ELEMENT_ID]": "[CORRECTED_CONTENT]"
})
\`\`\`

**Manual Fix**:
1. [STEP_1]
2. [STEP_2]
3. [STEP_3]

---

[... repeat for each issue ...]

## Automated Fixes Available

The following issues can be fixed automatically:

1. **Slide 3 - Text Overflow**
   - Can truncate to fit limits
   - Or split across two slides
   
2. **Slide 5 - Missing Subtitle**
   - Can add empty placeholder
   
Run: `/refactor-ppt [FILE] --auto-fix`

## Manual Intervention Required

These issues need human review:

1. **Slide 2 - Content Quality**
   - Content may need rewriting for clarity
   - Consider restructuring message
   
2. **Slide 7 - Visual Element**
   - Image may need replacement
   - Check image resolution

## Recommendations

### Immediate Actions (Critical)
1. [FIX_1]
2. [FIX_2]

### Short-term (Important)
1. [IMPROVEMENT_1]
2. [IMPROVEMENT_2]

### Long-term (Optional)
1. [OPTIMIZATION_1]
2. [OPTIMIZATION_2]
```

### 5. Offer Auto-Fix Options

If auto-fix is possible:
```python
#!/usr/bin/env python3
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent))
from ppt_engine import PPTEngine

# Auto-fix script
template_path = "brand_CDO-AIFC/reference/templates/ATT_Day_to_Day_Quickstart_Template_2025.pptx"
input_file = "[INPUT_FILE]"
output_file = "[INPUT_FILE].fixed.pptx"

engine = PPTEngine(template_path)
modifier = engine.modify_presentation(input_file, output_file)

# Apply automated fixes
[AUTO_FIX_CODE]

output_path = modifier.save()
print(f"✅ Auto-fixed: {output_path}")
```

### 6. Execute Debug Actions

**If auto-fix requested**:
Run the auto-fix script.

**If manual fix**:
Provide step-by-step instructions and wait for user confirmation.

### 7. Verify Fixes

Run `python3 ../../scripts/ppt_engine_focused.py validate [FIXED_FILE]` to confirm issues resolved.

### 8. Report Results

```
✅ Diagnostic Complete

🔍 Issues Found: [TOTAL_COUNT]
   - Critical: [ERROR_COUNT]
   - Warnings: [WARNING_COUNT]
   - Info: [INFO_COUNT]

🔧 Fixes Applied: [FIXED_COUNT]
   - Auto-fixed: [AUTO_COUNT]
   - Manual fixes needed: [MANUAL_COUNT]

✅ Post-Fix Validation:
   - Errors remaining: [COUNT]
   - New warnings: [COUNT]
   - Conformance: [SCORE]/100

📋 Next Steps:
   [IF FULLY FIXED]:
   ✓ All issues resolved
   ✓ Presentation ready for use
   
   [IF PARTIALLY FIXED]:
   ⚠️ Manual intervention still needed:
   1. [REMAINING_ISSUE_1]
   2. [REMAINING_ISSUE_2]
   
   Use /refactor-ppt to address remaining issues

💡 Prevention Tips:
   - Use /scaffold-ppt to ensure template conformance from start
   - Run /test-ppt regularly during development
   - Keep content within recommended character limits
   - Don't modify slide layouts or colors
```

## Error Handling

**Cannot Diagnose**: File corrupted beyond repair, suggest recreating from template.

**Multiple Root Causes**: Explain interconnected issues, suggest fixing in priority order.

**Auto-Fix Failed**: Explain why automatic fix isn't possible, provide detailed manual instructions.

## Examples

**Example 1**: `/debug-ppt outputs/presentation.pptx "Slide 3 won't display properly"`
Output: Diagnosis showing text overflow issue with auto-fix option

**Example 2**: `/debug-ppt outputs/quarterly.pptx --auto-fix`
Output: Automated fixes applied for all resolvable issues

**Example 3**: `/debug-ppt outputs/deck.pptx "Missing title slide error"`
Output: Diagnosis showing slide deletion issue with recreation instructions

## References

- `/test-ppt` - Run validation
- `/refactor-ppt` - Apply fixes
- `/scaffold-ppt` - Recreate from scratch if needed
- `template_metadata.yaml` - Template specifications
