---
description: Generate new PowerPoint presentation from AT&T template with diagram support (PPT-Maker)
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

### 1. Parse User Requirements

Extract from $ARGUMENTS:
- **Presentation topic/title**: Main subject matter
- **Target audience**: Internal/external, technical level
- **Key messages**: 3-5 main points to communicate
- **Slide count estimate**: Rough number of slides needed
- **Content sections**: Logical flow and organization

Request clarification if requirements are incomplete.

### 2. Verify Environment and Template

**Check environment dependencies** from `${ARCHETYPES_BASEDIR}/ppt-maker/templates/env-config.yaml`:
- Python packages: pyyaml, python-pptx, Pillow
- NPM packages: @mermaid-js/mermaid-cli (if using Mermaid diagrams)
- Chromium path: `/opt/homebrew/bin/chromium` or `/usr/bin/chromium`

Run inspection to verify template and slide metadata:
```bash
python3 ../../scripts/ppt_engine_focused.py inspect CDO-AIFC/reference/templates/09-documentation-requirements/ppt-maker/ppt-maker-template-library.pptx
```

### 3. Content Strategy Planning

**AI Prompt for Content Adaptation**:

```text
Based on user requirements and PPT-Maker constitution, create presentation content strategy:

1. Analyze key messages and map to appropriate slide types from ppt_engine_focused.yaml
2. For each content section, determine:
   - Best slide type from 12 templates (see constitution Section V)
   - COMPLETE content (no placeholders!) within character limits
   - Whether diagrams enhance the message (Mermaid CLI or programmatic)
   - Whether content should be split across multiple slides

3. For diagrams, determine:
   - Complex architecture: Use Mermaid CLI (image-based)
   - Simple flow/timeline: Use programmatic (python-pptx)
   - Correct aspect ratio for target placement

4. Provide FULL, ACTUAL content - not Lorem ipsum, not examples, not placeholders

Constitution Hard-Stop Rules:
- ✘ Character limits must not be exceeded
- ✘ No placeholder text allowed
- ✘ No aspect ratio distortion >10%
- ✘ Required slides: 01_title (first), 12_final_slide (last)
```

### 4. Generate YAML Content Spec

Create YAML specification with COMPLETE content and optional diagrams:

```yaml
title:
  title: "[FULL PRESENTATION TITLE]"
  subtitle: "[COMPLETE SUBTITLE]"
  metadata: "[DATE/VERSION]"

footer:
  title: "[SHORT TITLE FOR FOOTER]"
  month: "[MONTH NAME]"
  day: "[DD]"
  year: "[YYYY]"

slides:
  - type: "[SLIDE_TYPE_ID]"  # See ppt_engine_focused.yaml for types
    content:
      title: "[COMPLETE TITLE - no placeholders]"
      [element_id]: "[FULL CONTENT - actual text, not examples]"
      [element_id]: "[COMPLETE TEXT - respects character limits]"
    diagram:  # Optional - for image or programmatic diagrams
      type: "image"  # or "programmatic"
      path: "diagram.png"  # for image type
      # ⚠️  Do NOT specify 'position' - let engine auto-size/auto-center
      # ⚠️  NEVER set validate_aspect_ratio: false - causes distortion
```

**Critical Rules**:
- ✅ All content must be COMPLETE and REAL
- ❌ NO "Lorem ipsum" or template examples
- ❌ NO placeholder text like "[Insert text here]"
- ✅ Content MUST fit within character limits
- ✅ Professional, polished language

**FORBIDDEN WORKAROUNDS** (NEVER DO THIS):
- ❌ NEVER set `validate_aspect_ratio: false` to bypass quality checks
- ❌ NEVER add manual `position` blocks to work around overlap
- ❌ NEVER disable any quality check to "make it work"
- ✅ ALWAYS fix root cause (shorten text, omit position, regenerate diagram)

### 5. Validate Content Plan

Check YAML specification against constraints:
- ✓ Title slide content provided
- ✓ All required fields populated with REAL content
- ✓ Character counts within limits for each element
- ✓ No placeholder or example text
- ✓ Total slide count reasonable (typically 5-15 slides)

If violations found, revise YAML specification.

### 6. Generate Diagrams (if needed)

**For Mermaid CLI diagrams**:
```bash
# Create .mmd file in assets/
cat > assets/architecture.mmd << 'EOF'
graph TB
    A[Component A] --> B[Component B]
EOF

# Generate PNG with correct aspect ratio
# For 9.0" x 5.0" target = 1.8:1, use 2400x1333 pixels
PUPPETEER_EXECUTABLE_PATH=/opt/homebrew/bin/chromium \
  mmdc -i assets/architecture.mmd -o assets/architecture.png \
  -w 2400 -H 1333 -b transparent
```

**For programmatic diagrams**: Define directly in YAML (no external generation needed)

### 7. Execute Generation with Validation Loop (Max 3 Attempts)

**IMPORTANT**: This workflow implements a 3-attempt retry pattern. Cascade interprets validation results and automatically corrects issues. The Python script only reports validation data - Cascade decides what to do next.

**Step 7.1: Compare YAML to Script Configuration**

Before generating, compare presentation YAML to `${ARCHETYPES_BASEDIR}/ppt-maker/scripts/ppt_engine_focused.yaml`:

```bash
# Load script configuration to check available slide types and fields
cat ../../scripts/ppt_engine_focused.yaml
```

**🔍 REQUIRED: Verify YAML Compatibility**

**Cascade MUST check**:
1. **Slide Types**: All `type:` values in presentation YAML exist in script config
   - Valid types: `01_title`, `02_cover_photo`, ..., `12_final_slide`
   - Invalid type = generation will fail

2. **Content Fields**: All `content:` fields match template requirements
   - Example: `05_content_single_column` requires `title` and `body`
   - Example: `06_large_text_three_columns` requires `title`, `statement`, `column1_header`, etc.
   - Missing required field = generation will fail

3. **Field Names**: Exact spelling/casing of field names
   - Script config shows exact field names (e.g., `column1_header` not `column_1_header`)

**If mismatches found**:
- Fix presentation YAML to match script configuration
- Regenerate YAML with correct types/fields
- Re-run this comparison

**Step 7.2: Pre-Generation Content Validation**

After YAML compatibility check, validate content:
- ✓ Required slides present (01_title, 12_final_slide)
- ✓ Diagram blocks present for diagram-intended slides
- ✓ Character limits: Check against FIELD_LENGTH_CONSTRAINTS
- ✓ No placeholder text patterns
- ✓ Image file paths exist

If content validation fails, fix issues and regenerate YAML before proceeding.

---

**Step 7.3: Generation, Inspection, and Validation Loop**

Initialize retry tracking:
```bash
ATTEMPT=0
MAX_ATTEMPTS=3
STRUCTURE_VERIFIED=false
VALIDATION_PASSED=false
```

**Retry Loop (Cascade-Driven)**:

While `ATTEMPT < MAX_ATTEMPTS` and `VALIDATION_PASSED == false`:

**Attempt N (Current attempt number): Generate Presentation**

```bash
ATTEMPT=$((ATTEMPT + 1))
echo "🔄 Attempt $ATTEMPT/$MAX_ATTEMPTS"

# Generate presentation from YAML
cat << 'EOF' | python3 ../../scripts/ppt_engine_focused.py create outputs/[FILENAME].pptx --assets-folder assets
[YAML_SPECIFICATION_HERE]
EOF
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
- For each field exceeding limits:
  - Read original text from YAML
  - **Cascade**: Rewrite text to fit within limit while preserving intent
  - Update YAML with reworded text
- If `ATTEMPT < MAX_ATTEMPTS`: Continue loop with updated YAML
- If `ATTEMPT == MAX_ATTEMPTS`: Stop and report failure (manual intervention required)

**If generation succeeds**: Proceed to inspection

---

**Attempt N: Inspect Generated Presentation**

```bash
python3 ../../scripts/ppt_engine_focused.py inspect outputs/[FILENAME].pptx
```

**🔍 REQUIRED: Compare Inspect Output to YAML**

Before proceeding to validation, **Cascade MUST verify structural alignment**:

1. **Slide Count Match**:
   - Inspect shows: "Total Slides: [N]"
   - YAML has: [N] slides in `slides:[]` array
   - Must match exactly (accounting for title slide auto-generated)

2. **Slide Type Match**:
   - For each slide, inspect shows: "Slide [N]: [Layout Name]"
   - Compare to YAML `type:` field
   - Example: YAML `type: "05_content_single_column"` → Inspect should show "Content Single Column"

3. **Content Structure Match**:
   - Inspect shows: "Content shapes: [N]"
   - Verify expected fields were populated
   - Example: If YAML has `title` and `body`, inspect should show 2+ text shapes

4. **Diagram Presence Match**:
   - If YAML has `diagram:` block, inspect should show "Images: [N]" > 0
   - If no diagram in YAML, inspect should show "Images: 0" (unless template has embedded images)

**If misalignment detected** (structure doesn't match intent):
```bash
STRUCTURE_VERIFIED=false
echo "⚠️  Structure mismatch detected"
```

**Example Mismatch 1 - Slide Count**:
```
YAML specifies: 10 slides
Inspect shows: "Total Slides: 8"
→ Mismatch! 2 slides failed to generate (check for errors in generation output)
```

**Example Mismatch 2 - Missing Diagram**:
```
YAML slide 5: `diagram: {type: "image", path: "chart.png"}`
Inspect slide 5: "Images: 0"
→ Mismatch! Diagram not embedded (check file path or generation errors)
```

**Example Match (Good)**:
```
YAML: 10 slides, 3 with diagrams
Inspect: "Total Slides: 10", slides 3,7,9 show "Images: 1"
→ Match! Structure verified ✓
```

**Cascade action**:
- Analyze mismatch (which slides, what's different)
- Root cause: Wrong slide type? Missing diagram path? Incorrect field names?
- **Regenerate YAML** with corrections
- **Continue loop** (increment ATTEMPT, regenerate)
- Do NOT proceed to validation until structure matches

**If alignment verified**:
```bash
STRUCTURE_VERIFIED=true
echo "✓ Structure verified: Inspect output matches YAML intent"
# Proceed to validation
```

**Attempt N: Validate Presentation**

```bash
python3 ../../scripts/ppt_engine_focused.py validate outputs/[FILENAME].pptx --json > outputs/[FILENAME]_validation.json

# Parse validation status
VALIDATION_STATUS=$(python3 -c "import json; print(json.load(open('outputs/[FILENAME]_validation.json'))['validation_results']['overall_status'])")

echo "📊 Validation Status: $VALIDATION_STATUS"
```

**🔍 REQUIRED: Review Validation Output**

Before proceeding, **Cascade MUST analyze the validation JSON** for:

1. **Overall Status**: 
   - Check: `validation_results.overall_status`
   - Must be: `"pass"` to proceed
   - If `"fail"`: Do NOT claim success

2. **Slide Issues Count**:
   - Check: Number of slides in `validation_results.slides[]`
   - Each entry represents a slide with problems
   - Zero entries = no issues found

3. **Issue Types** (if any):
   - `text_truncated`: Text has ellipses, field too long
   - `title_body_overlap`: Title extends into body area
   - `text_overlap`: Content shapes overlap
   - `diagram_overlap`: Diagram extends into footer (y+height > 6.5")
   - `missing_embedded_image`: Expected diagram not found
   - `aspect_ratio_distortion`: Image stretched/compressed

4. **Issue Severity**:
   - `critical`: Must fix before claiming success
   - `warning`: Should review but may proceed

**Example validation review**:
```
Overall Status: fail
Slides with Issues: 3
  - Slide 7: text_truncated (critical)
  - Slide 12: diagram_overlap (critical) 
  - Slide 17: title_body_overlap (critical)

Conclusion: Validation FAILED - apply fixes and retry
```

**Attempt N: Interpret Validation Results**

Based on validation output review above, parse specific fixes needed.

**If `VALIDATION_STATUS == "pass"`**:
```bash
VALIDATION_PASSED=true
echo "✅ Validation PASSED on attempt $ATTEMPT"
# Exit retry loop - proceed to completion
```

**If `VALIDATION_STATUS == "fail"`**:
```bash
echo "⚠️  Validation FAILED on attempt $ATTEMPT"
cat outputs/[FILENAME]_validation.json
```

Analyze validation issues and apply corrections. **See Constitution Section VII for complete error response guide**.

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
- If `ATTEMPT < MAX_ATTEMPTS`: Continue loop with updated YAML
- If `ATTEMPT == MAX_ATTEMPTS`: Stop and report failure

---

**Step 7.4: Retry Loop Exit Conditions**

**Success Exit** (`VALIDATION_PASSED == true`):
```bash
echo "✅ Presentation created and validated successfully on attempt $ATTEMPT"
# Proceed to Step 8 (completion reporting)
```

**Failure Exit** (`ATTEMPT == MAX_ATTEMPTS` and `VALIDATION_PASSED == false`):
```bash
echo "❌ ❌ ❌ VALIDATION FAILED ❌ ❌ ❌"
echo "❌ Validation failed after $MAX_ATTEMPTS attempts"
echo "❌ Overall Status: FAIL"
echo ""
echo "📋 Remaining issues require manual intervention:"
cat outputs/[FILENAME]_validation.json
echo ""
echo "🛑 WORKFLOW HAS FAILED - DO NOT PROCEED TO COMPLETION"
echo "💡 Review validation report and manually edit YAML to fix remaining issues"
echo ""
echo "❌ PRESENTATION IS NOT READY FOR USE"
# DO NOT proceed to success - workflow has FAILED
exit 1
```

**CRITICAL**: If validation failed, you MUST:
- ❌ STOP immediately - do NOT proceed to Step 9
- ❌ DO NOT claim "presentation successfully generated"
- ❌ DO NOT mark workflow as complete
- ✅ Report the failure status to user
- ✅ List the validation errors that remain
- ✅ Explain what needs manual intervention

---

**Step 7.5: Post-Validation Review**

If validation passed, confirm all quality checks satisfied. No additional action needed - presentation is ready.

---

### 9. Report Completion

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
- ❌ If validation had errors - DO NOT claim "successfully generated"
- ❌ If any slides have issues - DO NOT mark as complete
- ✅ ONLY proceed if `overall_status == "pass"` in validation JSON
- ✅ ONLY proceed if `VALIDATION_PASSED == true` from retry loop

**If validation failed**: You should have exited at Step 7.3 with error code 1.
If you reached this step with failed validation, that is a CRITICAL ERROR.

**Proceed with completion report ONLY if all checks passed above.**

```text
✅ PowerPoint Presentation Successfully Generated and Validated

📦 Presentation Details:
   Title: [TITLE]
   Slides: [COUNT] total
   Output: outputs/[FILENAME].pptx
   Template: AT&T Day-to-Day Quickstart 2025

📊 Slide Breakdown:
   ✓ Slide 1: Title slide
   ✓ Slides 2-[N]: Content slides
      - [COUNT] by type
   ✓ Slide [N+1]: Logo slide

🎨 AT&T Brand Compliance:
   ✓ Template layouts preserved
   ✓ AT&T Aleck Sans fonts maintained
   ✓ Color scheme maintained
   ✓ Mandatory slides present

✅ Validation Results:
   - Status: PASSED
   - Attempts: [N] of 3
   - Critical Issues: 0
   - Warnings: [COUNT] (if any)
   - Report: outputs/[FILENAME]_validation.json

📋 Content Quality:
   ✓ No template placeholder text
   ✓ All content complete and professional
   ✓ Character limits respected
   ✓ No text truncation with ellipses
   ✓ No title/body overlap
   ✓ Diagrams properly positioned and sized

💡 Next Steps:
   1. Review: open outputs/[FILENAME].pptx
   2. Modify: /refactor-ppt if changes needed
   3. Validate: /test-ppt for full check
   4. Document: /document-ppt for summary
```

## Error Handling

**Content Too Long**: Show which elements exceed limits, provide adapted content in corrected YAML.

**Incomplete Content**: Identify missing or placeholder content, generate complete replacement.

**Template Issues**: Verify template file exists, check metadata accessibility.

**Validation Failures**: Show specific violations, provide corrected YAML.

## Examples

**Example 1**: `/scaffold-ppt Create quarterly business review with Q4 metrics and planning`

Generates YAML with complete content for 8-10 slides including metrics (four-box), narrative (text-heavy), and planning (two-column).

**Example 2**: `/scaffold-ppt Generate project kickoff for EAIFC workflows introduction`

Creates YAML with overview, features, architecture, and benefits slides with full professional content.

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/ppt-maker/ppt-maker-constitution.md`
- **Environment Config**: `${ARCHETYPES_BASEDIR}/ppt-maker/templates/env-config.yaml`
- **Slide Metadata**: `${ARCHETYPES_BASEDIR}/ppt-maker/scripts/ppt_engine_focused.yaml`
- **Python Library**: `${ARCHETYPES_BASEDIR}/ppt-maker/scripts/ppt_engine_focused.py`
- **Template**: `CDO-AIFC/reference/templates/09-documentation-requirements/ppt-maker/ppt-maker-template-library.pptx`
- **Related Workflows**:
  - `/refactor-ppt` - Modify existing presentation
  - `/debug-ppt` - Fix presentation issues
  - `/test-ppt` - Validate presentation conformance
  - `/compare-ppt` - Compare presentation approaches
  - `/document-ppt` - Generate markdown summary