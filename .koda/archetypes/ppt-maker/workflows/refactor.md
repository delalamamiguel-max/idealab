---
description: Modify existing PowerPoint presentation while maintaining template conformance (PPT-Maker)
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

### 1. Parse Modification Request

Extract from $ARGUMENTS:
- **Target presentation**: File path to modify
- **Changes requested**: Specific slides/content to update
- **Modification type**: Text updates, content additions, slide reordering
- **Image additions**: New visuals to incorporate

### 2. Inspect Existing Presentation

Run `python3 ../../scripts/ppt_engine_focused.py inspect [TARGET_FILE]` to analyze current structure.

Review:
- Current slide count and types
- Existing content and structure
- Validation status
- Areas of concern

### 3. Plan Modifications

**AI Prompt for Content Adaptation**:

```text
Analyze modification request against PPT-Maker constitution:

1. Identify which slides need changes
2. For each modification:
   - Check against ppt_engine_focused.yaml field limits
   - Adapt new content to match template constraints
   - Summarize or split if content too long
   - Preserve existing style and tone

3. For diagram modifications:
   - Update Mermaid .mmd files if changing architecture
   - Regenerate PNGs with correct aspect ratios
   - Update programmatic diagram configs in YAML
   - ⚠️  Do NOT add manual `position` blocks - let engine auto-size
   - ⚠️  NEVER set `validate_aspect_ratio: false` - causes distortion

4. Ensure constitutional compliance:
   - Character limits respected for ALL fields
   - No placeholder text introduced
   - Aspect ratio validation ENABLED for all diagrams
   - Mandatory slides preserved

**FORBIDDEN WORKAROUNDS** (NEVER DO THIS):
- ❌ NEVER set `validate_aspect_ratio: false` to bypass quality checks
- ❌ NEVER add manual `position` blocks to work around overlap
- ❌ NEVER disable any quality check to "make it work"
- ✅ ALWAYS fix root cause (shorten text, omit position, regenerate diagram)
```

### 4. Update YAML Specification

**Constitutional Note**: Per constitution, do NOT create presentation-specific Python scripts. Instead, modify the YAML specification.

Load existing YAML from assets folder:
```bash
# YAML should be persisted in assets folder
cp assets/[presentation_name].yaml assets/[presentation_name]_modified.yaml
```

Edit YAML to apply modifications:
- Update slide content with new text
- Modify diagram specifications if needed
- Ensure all character limits respected
- Add/remove slides as needed

### 5. Regenerate Diagrams (if modified)

**For modified Mermaid diagrams**:
```bash
# Update .mmd file
vim assets/[diagram_name].mmd

# Regenerate PNG with correct aspect ratio
PUPPETEER_EXECUTABLE_PATH=/opt/homebrew/bin/chromium \
  mmdc -i assets/[diagram_name].mmd -o assets/[diagram_name].png \
  -w [WIDTH] -H [HEIGHT] -b transparent
```

### 6. Execute Regeneration with Validation Loop (Max 3 Attempts)

**IMPORTANT**: This workflow implements a 3-attempt retry pattern. Cascade interprets validation results and automatically corrects issues. The Python script only reports validation data - Cascade decides what to do next.

**Step 6.1: Compare YAML to Script Configuration**

Before regenerating, compare modified YAML to script configuration:

```bash
cat ../../scripts/ppt_engine_focused.yaml
```

**🔍 REQUIRED: Verify YAML Compatibility**

**Cascade MUST check**: All slide types and field names match script configuration.

**If mismatches found**: Fix YAML to match script config.

**Step 6.2: Pre-Generation Content Validation**

After YAML compatibility check, validate modified content:
- ✓ Required slides still present (01_title, 12_final_slide)
- ✓ Character limits: Check against FIELD_LENGTH_CONSTRAINTS
- ✓ Diagram blocks present for diagram-intended slides
- ✓ No placeholder text patterns introduced
- ✓ Modified image file paths exist

If content validation fails, fix issues before proceeding.

---

**Step 6.3: Generation, Inspection, and Validation Loop**

Initialize retry tracking:
```bash
ATTEMPT=0
MAX_ATTEMPTS=3
STRUCTURE_VERIFIED=false
VALIDATION_PASSED=false
```

**Retry Loop (Cascade-Driven)**:

While `ATTEMPT < MAX_ATTEMPTS` and `VALIDATION_PASSED == false`:

**Attempt N: Regenerate Presentation**

```bash
ATTEMPT=$((ATTEMPT + 1))
echo "🔄 Attempt $ATTEMPT/$MAX_ATTEMPTS - Regenerating presentation"

# Regenerate from modified YAML
cat assets/[presentation_name]_modified.yaml | \
  python3 ../../scripts/ppt_engine_focused.py create \
  outputs/[output_name].pptx --assets-folder assets
```

**🔍 REQUIRED: Review Generation Output**

Check script output for:
- ❌ **Content length errors**: "Field exceeds limit" → note fields to shorten
- ⚠️ **Diagram warnings**: Manual positioning, small scaling, footer overlap
- ❌ **Path errors**: "Failed to embed image" → identify missing files
- ✅ **Success markers**: "✓ Embedded image" for each diagram

**Do NOT proceed if generation failed!**

**If generation fails** (e.g., content length errors):
- Parse error message to identify problematic fields
- **Cascade**: Rewrite text to fit within limit while preserving intent
- Update YAML with reworded text
- If `ATTEMPT < MAX_ATTEMPTS`: Continue loop
- If `ATTEMPT == MAX_ATTEMPTS`: Stop and report failure

**If generation succeeds**: Proceed to inspection

---

**Attempt N: Inspect Generated Presentation**

```bash
python3 ../../scripts/ppt_engine_focused.py inspect outputs/[output_name].pptx
```

**🔍 REQUIRED: Compare Inspect Output to YAML**

**Cascade MUST verify structural alignment**:
1. **Slide Count Match**: Inspect "Total Slides" = YAML slide count
2. **Slide Type Match**: Each slide's layout matches YAML `type:`
3. **Content Structure Match**: Expected fields were populated
4. **Diagram Presence Match**: YAML `diagram:` block → Inspect shows images

**Example Mismatch 1 - Slide Count**:
```
YAML specifies: 10 slides
Inspect shows: "Total Slides: 8"
→ Mismatch! 2 slides failed to generate
```

**Example Mismatch 2 - Missing Diagram**:
```
YAML slide 5: `diagram: {type: "image", path: "chart.png"}`
Inspect slide 5: "Images: 0"
→ Mismatch! Diagram not embedded
```

**Example Match (Good)**:
```
YAML: 10 slides, 3 with diagrams
Inspect: "Total Slides: 10", slides 3,7,9 show "Images: 1"
→ Match! Structure verified ✓
```

**If misalignment detected**:
- Set `STRUCTURE_VERIFIED=false`
- Analyze mismatch, regenerate YAML with corrections
- **Continue loop** - do NOT proceed to validation

**If alignment verified**:
- Set `STRUCTURE_VERIFIED=true`
- Proceed to validation

**Attempt N: Validate Presentation**

```bash
python3 ../../scripts/ppt_engine_focused.py validate outputs/[output_name].pptx --json > outputs/[output_name]_validation.json

# Parse validation status
VALIDATION_STATUS=$(python3 -c "import json; print(json.load(open('outputs/[output_name]_validation.json'))['validation_results']['overall_status'])")

echo "📊 Validation Status: $VALIDATION_STATUS"
```

**🔍 REQUIRED: Review Validation Output**

Check validation JSON for:
- ❌ **Overall status**: Must be `"pass"` to proceed
- 📊 **Issue count**: Number of slides in `validation_results.slides[]`
- 🔍 **Issue types**: text_truncated, diagram_overlap, diagram_undersized, etc.
- ⚠️ **Severity**: `critical` issues must be fixed

**Example**: "Overall Status: fail, 3 slides with issues → Validation FAILED"

**Attempt N: Interpret Validation Results**

Based on validation output review above, parse specific fixes needed.

**If `VALIDATION_STATUS == "pass"`**:
```bash
VALIDATION_PASSED=true
echo "✅ Validation PASSED on attempt $ATTEMPT"
# Exit retry loop
```

**If `VALIDATION_STATUS == "fail"`**:
```bash
echo "⚠️  Validation FAILED on attempt $ATTEMPT"
cat outputs/[output_name]_validation.json
```

Apply corrections. **See Constitution Section VII for complete error response guide**.

**For `text_truncated`, `title_body_overlap`, `text_overlap`**:
- Rewrite affected text to fit within proper bounds
- Update YAML content fields

**For `missing_embedded_image`**:
- Check if diagram file exists in assets/
- If missing: Create/regenerate diagram
- If present: Check YAML diagram block syntax
- Update YAML diagram path or regenerate file

**For `diagram_overlap`** (extends into footer):
- **REMOVE `position` block** - let engine auto-center (BEST)
- OR regenerate diagram with different aspect ratio
- OR move diagram title to slide title field
- **See Constitution Section VII for forbidden workarounds**

**For `diagram_undersized`** (scaling < 95%):
- **⛔ STOP GENERATION** - Do not proceed
- **CONSULT USER** with specific context:
  ```
  ⚠️ Diagram "[filename]" is using only X% of slide space.
  Text will be difficult to read at this size.
  
  Can we regenerate with:
  • Different layout (vertical instead of horizontal)?
  • Different diagram type (flowchart vs timeline)?
  • Optimal dimensions (3000×1375 or 2400×1100 pixels)?
  
  Which approach would work best?
  ```
- **COLLABORATE**: Discuss alternatives with user
- **REGENERATE**: Only after user approves approach
- For Mermaid: `mmdc -i diagram.mmd -o diagram.png -w 3000 -H 1375`
- **FORBIDDEN**: Do NOT accept "barely readable" as OK

**For `diagram_low_coverage`** (area < 50%):
- **⛔ STOP GENERATION** - Do not proceed
- **CONSULT USER** with specific context:
  ```
  ⚠️ Diagram "[filename]" is using only X% of available space.
  Aspect ratio doesn't fit the slide well.
  
  Can we adjust:
  • Change Mermaid layout direction (LR ↔ TB)?
  • Modify structure to fit 12×5.5 better?
  • Use different diagram type?
  
  What would be the best approach?
  ```
- **COLLABORATE**: Explore layout alternatives
- **REGENERATE**: Only after user approves changes
- Target: 2.18:1 aspect ratio (3000×1375 or 2400×1100 pixels)
- **FORBIDDEN**: Do NOT accept wasted space as "good enough"

**After applying corrections**:
- Continue loop if `ATTEMPT < MAX_ATTEMPTS`
- Stop and report failure if `ATTEMPT == MAX_ATTEMPTS`

---

**Step 6.4: Retry Loop Exit Conditions**

**Success Exit** (`VALIDATION_PASSED == true`):
```bash
echo "✅ Presentation modified and validated successfully on attempt $ATTEMPT"
# Proceed to completion reporting
```

**Failure Exit** (`ATTEMPT == MAX_ATTEMPTS` and `VALIDATION_PASSED == false`):
```bash
echo "❌ ❌ ❌ VALIDATION FAILED ❌ ❌ ❌"
echo "❌ Validation failed after $MAX_ATTEMPTS attempts"
echo "❌ Overall Status: FAIL"
echo ""
echo "📋 Remaining issues require manual intervention:"
cat outputs/[output_name]_validation.json
echo ""
echo "🛑 WORKFLOW HAS FAILED - DO NOT PROCEED TO COMPLETION"
echo "💡 Review validation report and manually edit YAML to fix remaining issues"
echo ""
echo "❌ PRESENTATION IS NOT READY FOR USE"
# DO NOT proceed to success - workflow has FAILED
exit 1
```

**CRITICAL**: If validation failed, you MUST:
- ❌ STOP immediately - do NOT proceed to Step 8
- ❌ DO NOT claim "presentation modified successfully"
- ❌ DO NOT mark workflow as complete
- ✅ Report the failure status to user
- ✅ List the validation errors that remain
- ✅ Explain what needs manual intervention

### 8. Report Results

**🛑 STOP - VALIDATION STATUS CHECK REQUIRED 🛑**

Before proceeding with this step, you MUST verify:

```bash
# Check validation status from previous step
if [ "$VALIDATION_PASSED" != "true" ]; then
  echo "❌ ERROR: Attempting to report success but validation failed!"
  echo "❌ VALIDATION_PASSED=$VALIDATION_PASSED"
  echo "❌ Cannot proceed to completion report - workflow FAILED"
  exit 1
fi
```

**CRITICAL GUARDRAILS**:
- ❌ If validation status is "fail" - DO NOT PROCEED with this step
- ❌ If validation had errors - DO NOT claim "modified successfully"
- ❌ If any slides have issues - DO NOT mark as complete
- ✅ ONLY proceed if `overall_status == "pass"` in validation JSON
- ✅ ONLY proceed if `VALIDATION_PASSED == true` from retry loop

**If validation failed**: You should have exited at Step 6.3 with error code 1.
If you reached this step with failed validation, that is a CRITICAL ERROR.

**Proceed with completion report ONLY if all checks passed above.**

```
✅ Presentation Modified and Validated Successfully

📝 Changes Applied:
   - Slide [N]: [DESCRIPTION_OF_CHANGE]
   - Slide [M]: [DESCRIPTION_OF_CHANGE]
   - [OTHER_CHANGES]

✅ Validation Results:
   - Errors: [COUNT]
   - Warnings: [COUNT]
   - Conformance maintained: [YES/NO]

📊 Before/After:
   - Original: [INPUT_FILE]
   - Modified: [OUTPUT_FILE]
   - Slides changed: [COUNT]

💡 Next Steps:
   1. Review modified presentation
   2. Further refine if needed
   3. Run /test-ppt for full validation
```

## Error Handling

**File Not Found**: Verify input file path, check file exists, provide correct path format.

**Content Overflow**: Show which modifications exceed limits, provide adapted content, suggest splitting content.

**Validation Failures**: List violations introduced by changes, suggest corrections, offer rollback option.

## Examples

**Example 1**: `/refactor-ppt Update slide 3 title to 'Q4 Results' and add new metrics to body`

**Example 2**: `/refactor-ppt Change executive summary on slide 2 to focus on cost savings instead of revenue`

**Example 3**: `/refactor-ppt Add new slide after slide 5 showing project timeline`

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/ppt-maker/ppt-maker-constitution.md`
- **Slide Metadata**: `${ARCHETYPES_BASEDIR}/ppt-maker/scripts/ppt_engine_focused.yaml`
- **Related Workflows**:
  - `/scaffold-ppt` - Create new presentation
  - `/test-ppt` - Validate changes
  - `/compare-ppt` - Compare before/after versions
  - `/document-ppt` - Generate summary