# PPT-Maker Constitution

## Purpose

This constitution defines the foundational principles and hard-stop rules for the PPT-Maker archetype, which generates professional AT&T-branded PowerPoint presentations using YAML specifications and programmatic/image-based diagrams.

**Source**: Developed from ppt_engine_focused.py implementation and production testing

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** if these rules are violated:

- ✘ **Character limits**: Do not exceed field character limits defined in `ppt_engine_focused.yaml` (enforced at generation time with auto-truncation)
- ✘ **Template conformance**: Do not create presentation-specific PowerPoint scripts; use the YAML + library approach
- ✘ **Aspect ratio tolerance**: Do not embed images with aspect ratio distortion >10% (90-110% tolerance)
- ✘ **Placeholder text**: Do not include Lorem ipsum, "[Insert text here]", or other placeholder content in YAML specs (validated before generation)
- ✘ **Required slides**: Do not omit mandatory title slide (type `01_title`) or final slide (type `12_final_slide`) (enforced by validation - blocks generation)
- ✘ **Asset pollution**: Do not place YAML specs or generated images outside the designated assets folder
- ✘ **Footer overlap**: Do not allow text to extend into footer area (y > 6.5") - maintain minimum line gap above footer
- ✘ **Title wrapping**: Do not exceed slide-type-specific title limits to prevent multi-line wrapping (grid slides: 30 chars)

## II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify these patterns:

- ✔ **Complete content**: All YAML content must be complete, meaningful, professional text—never placeholders
- ✔ **Footer metadata**: Include footer section with title, month, day, year in YAML spec
- ✔ **Slide type validation**: Use only the 12 supported slide types from template
- ✔ **Text length validation**: Verify all text fields against character limits before generation (script enforces with truncation warnings)
- ✔ **Aspect ratio validation**: For image diagrams, calculate and validate aspect ratio matches target dimensions
- ✔ **Assets folder**: Persist YAML specs and images to configurable assets folder (default: `assets/`)
- ✔ **Diagram specification**: When using diagrams, properly specify type (`image` or `programmatic`), path, position, and validation flags
- ✔ **Collision detection**: After generation, validate no shape overlaps (text over footer, headers over bodies, diagrams over logos)
- ✔ **Smart diagram positioning**: For blank slides, auto-adjust diagram position/size to avoid logo overlap (y + height ≤ 6.5")

## III. Preferred Patterns (Recommended)

The LLM **should adopt** these patterns unless user overrides:

- ➜ **Mermaid CLI integration**: Use Mermaid CLI for complex architecture diagrams with correct aspect ratios
- ➜ **Theme colors**: Leverage AT&T theme colors for programmatic diagrams (primary_blue, dark_blue, light_blue, accent_yellow)
- ➜ **Diagram placement**: Use blank slides (type `11_blank_end_slide`) for full-page diagrams
- ➜ **Image dimensions**: Calculate ideal image dimensions to match slide aspect ratio: width ÷ height = target width ÷ target height
- ➜ **Smart text sizing**: Let programmatic diagrams auto-calculate font sizes (10-12pt) to prevent wrapping
- ➜ **Milestone markers**: Include milestone circles on timeline diagrams for visibility
- ➜ **Version control**: Keep .mmd files and YAML specs in assets folder for reproducibility

## IV. Sizing and Positioning Guidelines

### Slide Dimensions
- **Slide size**: 13.33" width × 7.5" height (16:9 widescreen)
- **Safe content area**: Variable margins (see below)
- **Diagram area (blank/end slides)**: 12.0" × 5.5" (0.5" top margin, 1.5" bottom margin, horizontally centered)
- **Content area (text slides)**: ~9.0" × 6.5" for text content placement

### Positioning Coordinates
- **Origin**: Top-left corner (0, 0)
- **Units**: Inches (use `Inches()` from `pptx.util`)
- **X-axis**: 0.0" (left edge) to 13.33" (right edge)
- **Y-axis**: 0.0" (top edge) to 7.5" (bottom edge)

### ⚠️  Manual Diagram Positioning (NOT RECOMMENDED)

**CRITICAL**: Do NOT manually specify `position` blocks in YAML unless absolutely necessary. The engine's auto-sizing and auto-centering handles diagrams correctly and prevents footer overlap.

**Why manual positioning fails**:
- Causes footer overlap (y + height > 6.5")
- Breaks aspect ratio preservation
- Skips readability checks (scaling < 75%)
- Requires manual calculation prone to errors

**If you must use manual positioning** (rare edge cases only):
```yaml
# MUST ensure: y + height <= 6.5 to avoid footer
# MUST validate aspect ratio matches source image
position: {x: 0.5, y: 0.5, width: 9.0, height: 5.5}  # Max height = 6.0" to be safe
```

**Preferred approach**: Omit `position` entirely - let engine handle it automatically.

### Aspect Ratio Calculation
```python
# For an image with dimensions W×H pixels
image_aspect = W / H

# For target placement at width×height inches
target_aspect = width / height

# Validation check (must be within 90-110%)
ratio_match = image_aspect / target_aspect
valid = 0.90 <= ratio_match <= 1.10

# If invalid, recalculate ideal dimensions:
# Option 1: Fix width, adjust height
height_ideal = width / image_aspect

# Option 2: Fix height, adjust width  
width_ideal = height * image_aspect
```

## V. Slide Type Selection Guide

### Character Limits - Configuration Reference

**All character limits are defined in** `.cdo-aifc/scripts/python/ppt_engine_focused.yaml` under `slide_types → fields → char_limit`.

**Key Principles**:
- **Conservative limits** prevent text wrapping and overflow
- **Large fonts** (dividers, covers) have stricter limits (~30 chars)
- **Body text** has more room (300-500 chars depending on layout)
- **Multi-column layouts** need tighter limits to prevent footer overlap
- **Grid layouts** require very strict limits (22 char headers, 130 char bodies)

**Example from config**:
```yaml
"05_content_single_column":
  name: "Title + Subtitle (1 column w/ headers)"
  fields:
    title:
      char_limit: 50
      description: "Title field - prevent wrapping to 3+ lines"
    body:
      char_limit: 500
      description: "Main content text (body has more room)"
```

**For specific character limits, consult the configuration file** - it is the authoritative source.

---

### When to Use Each Type

**`01_title`** - Title slide (mandatory first slide)
- Full presentation title, subtitle, metadata/date
- **Note**: Conservative limits to prevent wrapping on cover slide

**`02_cover_photo`** - Cover slide with presenter info
- Alternative cover with subtitle, presenter name, and date
- **Note**: Large font on cover - strict title limit to prevent wrapping

**`03_divider`** - Simple divider slide
- Section divider with title only
- **Note**: Large divider text - strict limit to prevent wrapping

**`04_divider_section`** - Numbered divider slide
- Section divider with title, subtitle, and section number
- **Note**: Large divider text - strict limits

**`05_content_single_column`** - Single column with header
- Process explanations, instructions
- **Note**: Conservative title limit to prevent wrapping to 3+ lines

**`06_large_text_three_columns`** - Statement + three columns
- Key message with supporting points
- **Note**: Column bodies limited to prevent footer overlap; must leave line gap above footer

**`07_two_columns`** - Two equal columns with headers
- Comparisons, before/after, pros/cons

**`08_four_columns_enumerated`** - Four numbered columns
- Step-by-step processes, frameworks

**`09_grid_with_icons`** - 2×2 grid with statement
- Key capabilities, features, benefits
- **Note**: Title and header limits strictly enforced to prevent wrapping on grid layout

**`10_content_with_image`** - Text with image placeholder
- Product showcases, screenshots
- **Note**: Left side has less room than full slide

**`11_blank_end_slide`** - Blank with logo (for diagrams)
- Full-page diagrams, architecture views
- No editable text fields—perfect for programmatic/image diagrams

**`12_final_slide`** - Logo end slide (mandatory last slide)
- Closing slide with centered AT&T logo

### Slide Type Compatibility Matrix

| Slide Type | Text Content | Single Image | Multiple Images | Programmatic Diagrams | Notes |
|------------|--------------|--------------|-----------------|----------------------|-------|
| `01_title` | ✅ Title, subtitle, metadata | ❌ | ❌ | ❌ | First slide only |
| `02_cover_photo` | ✅ Title, subtitle, presenter, date | ❌ | ❌ | ❌ | Alternative cover slide |
| `03_divider` | ✅ Title only | ❌ | ❌ | ❌ | Section divider (simple) |
| `04_divider_section` | ✅ Title, subtitle, section number | ❌ | ❌ | ❌ | Section divider (numbered) |
| `05_content_single_column` | ✅ Title, body | ❌ | ❌ | ❌ | Text-only |
| `06_large_text_three_columns` | ✅ Statement + 3 columns | ❌ | ❌ | ❌ | Text-only |
| `07_two_columns` | ✅ Title + 2 columns | ❌ | ❌ | ❌ | Text-only |
| `08_four_columns_enumerated` | ✅ Title + 4 numbered columns | ❌ | ❌ | ❌ | Text-only |
| `09_grid_with_icons` | ✅ Title, statement, 4 grid boxes | ❌ | ❌ | ❌ | **CRITICAL**: Has decorative icons (?, ▲, ✓, 🔔) baked into template - ONLY use if content explicitly mentions these icon meanings |
| `10_content_with_image` | ✅ Title, body | ✅ Right side | ❌ | ✅ | Text + diagram |
| `11_blank_end_slide` | ❌ No text placeholders | ✅ Full slide | ✅ | ✅ | Diagram-only |
| `12_final_slide` | ❌ Logo only | ❌ | ❌ | ❌ | Last slide only |

**Usage Guidance**:
- **For opening slide**: Use `01_title` (mandatory first slide)
- **For alternative cover**: Use `02_cover_photo` (includes presenter and date fields)
- **For section breaks**: Use `03_divider` (simple) or `04_divider_section` (with section number)
- **For full-page diagrams**: Use `11_blank_end_slide` (no text, DIAGRAM ONLY - maximum visual impact)
- **For diagram + text**: Use `10_content_with_image` (text on left, image on right) ONLY when you need BOTH text explanation AND diagram
- **For programmatic diagrams**: Use `11_blank_end_slide` (preferred for standalone diagrams) or `10_content_with_image` (only if text is needed)
- **For text-only slides**: Use `05` through `09` (no diagram support)
- **For closing slide**: Use `12_final_slide` (mandatory last slide)

**Common Mistakes to Avoid**:
- ❌ Using text-only slide types (`05`-`09`) for diagrams
- ❌ Expecting `11_blank_end_slide` to have text placeholders (it's blank = no text)
- ❌ **CRITICAL**: Using `10_content_with_image` for diagram-only content (wastes 50% of slide space)
- ❌ Using `10_content_with_image` when no text explanation is needed - use `11_blank_end_slide` instead
- ❌ Adding diagrams to `01_title` or `12_final_slide`
- ❌ Omitting required first/last slides
- ❌ **CRITICAL**: Using `09_grid_with_icons` for generic 4-box content (icons are baked in and will show even with generic content)
- ❌ Using `09_grid_with_icons` when content doesn't explicitly reference question marks, warnings, checkmarks, or alerts

### Template Selection Guidelines

#### Multi-Column Text Content

**Use `06_large_text_three_columns` when**:
- You have a main statement + 3 columns of text
- Example: "Metrics Framework" with Leading Indicators, Lagging Indicators, Business Value
- Clean layout without decorative elements

**Use `07_two_columns` when**:
- You have 2 columns of text with headers
- Balanced left/right content presentation

**Use `08_four_columns_enumerated` when**:
- You have 4 columns representing a numbered sequence (1, 2, 3, 4)
- Template includes baked-in numbered circles

**Avoid `09_grid_with_icons` unless**:
- You specifically want decorative icons (?, ▲, ✓, 🔔)
- Icons are NOT content-driven—they're fixed template decorations
- Better for conceptual/abstract topics where icons add visual interest
- **Never use for metric tables, data columns, or sequential information**

#### Decision Tree for Text Slides

**STEP 1 - CHECK ICON INTENT** (Most Important!):
```
Does the content EXPLICITLY reference these specific icon meanings?
  - ? (Question/Help)
  - ▲ (Warning/Alert)
  - ✓ (Success/Checkmark)
  - 🔔 (Notification/Alert)

├─ YES, content explicitly uses these concepts
│   └─ Use 09_grid_with_icons (2×2 grid with baked-in decorative icons)
│
└─ NO, generic 4-box content OR different icons needed
    └─ SKIP 09_grid_with_icons → Go to STEP 2
```

**STEP 2 - SELECT BY COLUMN COUNT**:
```
How many columns of text?
├─ 1 column → Use 05_content_single_column
├─ 2 columns → Use 07_two_columns
├─ 3 columns → Use 06_large_text_three_columns
└─ 4 columns → Use 08_four_columns_enumerated
```

**WARNING**: 09_grid_with_icons will display ?, ▲, ✓, 🔔 icons even if your content doesn't reference them. Choose carefully!

#### Decision Tree for Diagram Slides

**STEP 1 - CHECK IF YOU NEED TEXT EXPLANATION**:
```
Does the diagram need accompanying text explanation on the same slide?

├─ NO, diagram is self-explanatory OR has embedded labels
│   └─ Use 11_blank_end_slide (full-slide diagram, maximum visual impact)
│
└─ YES, need text bullets/paragraphs to explain the diagram
    └─ Use 10_content_with_image (text left, diagram right)
```

**CRITICAL RULES**:
- ❌ **NEVER** use `10_content_with_image` for diagram-only content (wastes 50% of slide space)
- ✅ **ALWAYS** use `11_blank_end_slide` for standalone diagrams (flowcharts, process diagrams, architecture diagrams)
- ✅ Use `10_content_with_image` ONLY when you have BOTH meaningful text AND a supporting diagram
- ✅ If the diagram title can go in the slide title field, use `11_blank_end_slide`

**Examples**:
- ✅ "How Standards Are Enforced" flowchart → `11_blank_end_slide` (diagram has embedded labels)
- ✅ "System Architecture" diagram → `11_blank_end_slide` (self-explanatory)
- ✅ "Key Benefits: bullet 1, bullet 2, bullet 3" + supporting chart → `10_content_with_image` (needs text explanation)

## VI. Diagram Generation Standards

### A. Auto-Sizing Behavior (Engine Default)

**CRITICAL**: Do NOT specify `position` blocks in YAML - let the engine auto-size and auto-center diagrams. Manual positioning often causes footer overlap and scaling issues.

**For Blank/End Slides** (`11_blank_end_slide` - diagram-only layouts):
- **Auto-sizing (AUTOMATIC)**: Diagrams are sized to maximize space usage while preserving aspect ratio
- **Maximum safe area**: 12" × 5.5" (optimal for readability with margins)
- **Positioning**: Horizontally centered, 0.5" top margin, 1.5" bottom margin
- **Aspect ratio preserved**: Engine scales to fit max area while maintaining source aspect ratio
- **Wide diagrams**: Fit to max width (12"), height calculated from aspect ratio
- **Tall diagrams**: Fit to max height (5.5"), width calculated from aspect ratio
- **Auto-positioning**: `x = (13.33 - width) / 2`, `y = 0.5"`
- **⚠️  Do NOT manually specify position** - auto-sizing handles this perfectly

### B. Validation Thresholds (Enforced Post-Generation)

**Diagram Fit Analysis** (two separate checks):

1. **Area Coverage Check** (threshold: 50%) - **CRITICAL VALIDATION**:
   - Formula: `(width × height) / (12.0 × 5.5)`
   - **FAILS validation** if diagram uses < 50% of available slide space
   - Indicates inefficient aspect ratio or content layout
   - Validation error type: `diagram_low_coverage`
   - Suggested fix: Adjust diagram aspect ratio to match 2.18:1 (12:5.5)

2. **Scaling Ratio Check** (threshold: 75%) - **CRITICAL VALIDATION**:
   - **Measures**: How much of the 12" × 5.5" slide space the diagram occupies
   - **Formula**: `min(rendered_width_inches / 12.0, rendered_height_inches / 5.5)`
   - **FAILS validation** if diagram uses < 75% of available space
   - **Root cause**: Aspect ratio mismatch - diagram shape doesn't fit slide shape (2.18:1)
   - **Why it matters**: Below 75%, text and details become difficult to read
   - **Validation error type**: `diagram_undersized`
   - **Fix**: Adjust diagram aspect ratio toward 2.18:1, not just increase pixels
   - **Note**: A 2200×1000px image (2.2:1) renders better than 2400×200px (12:1) despite lower width

**⚠️ CRITICAL**: These checks are enforced during **validation**, not just generation warnings. Presentations with undersized or poorly-fitted diagrams will **FAIL** validation and must be regenerated.

**Note**: Auto-sizing always preserves aspect ratio mathematically. Post-generation validation verifies no aspect ratio distortion occurred.

**For Content Slides** (diagrams alongside text):
- **Auto-sizing enabled**: If no `position` block specified, engine preserves source aspect ratio
- **Aspect ratio protection (DEFAULT)**: Engine auto-adjusts dimensions to prevent distortion (>10%)
- **Safe zone**: Keeps diagram within y + height ≤ 6.5" (avoids footer/logo)
- **Fit to width**: Starts with 9.0" width, calculates height from source aspect ratio
- **Fit to height**: Falls back if too tall (max 5.75" height)
- **No distortion**: Display dimensions match source aspect ratio within 10% tolerance

### C. Recommended Source Dimensions

**For optimal space utilization and readability**:

**PRIMARY RECOMMENDATION**: Match slide aspect ratio of 2.18:1 (12:5.5)
- **Any resolution with 2.18:1 ratio** will fill 100% of available space
- Examples at 250 PPI: 3000×1375px (optimal), 2400×1100px (good), 3600×1650px (high-res)
- Examples at 200 PPI: 2400×1100px (optimal), 3000×1375px (high-res)
- **Higher resolution = crisper text** (recommend 1100px+ on shortest dimension for clarity)
- **It's the SHAPE that matters, not the pixel count!**

**Understanding Aspect Ratio Impact**:
- **2.18:1 ratio** (matches slide): 100% scaling ✅ (perfect fit)
- **2:1 ratio** (slightly squarer): ~91% scaling ✅ (good fit)
- **1.5:1 ratio** (much squarer): ~69% scaling ⚠️ (may fail, suboptimal)
- **12:1 ratio** (very wide): ~13% scaling ❌ (fails both checks, text unreadable)

**Common Diagram Issues**:
- **Gantt charts** (horizontal): Often 10:1+ ratio → fails validation ❌
- **Timelines** (horizontal): Often 8:1+ ratio → fails validation ❌
- **Fix**: Change orientation (vertical instead of horizontal) or use different layout

**CRITICAL THRESHOLDS**:
- **Scaling ratio < 75%**: VALIDATION FAILURE (diagram too small, text may be hard to read)
- **Area coverage < 50%**: VALIDATION FAILURE (wasted space, poor utilization)

**Key Insight**: A 2400×1100px diagram (2.18:1) renders larger and more readable than a 2400×200px diagram (12:1), despite having same width. Shape fit matters more than pixel count!

### D. Mermaid CLI Integration

**Image-Based Diagrams** (Mermaid CLI Example):

```bash
# Step 1: Create Mermaid diagram (.mmd file)
cat > assets/architecture.mmd << 'EOF'
graph TB
    A[Component A] --> B[Component B]
    B --> C[Component C]
EOF

# Step 2: Generate PNG with optimal aspect ratio (2.18:1 = 12:5.5 slide shape)
# Recommended: 3000×1375px (250 PPI) or 2400×1100px (200 PPI)
PUPPETEER_EXECUTABLE_PATH=/path/to/chromium \
  mmdc -i assets/architecture.mmd \
       -o assets/architecture.png \
       -w 3000 -H 1375 -b transparent

# Step 3: Reference in YAML (let engine auto-size)
diagram:
  type: "image"
  path: "architecture.png"
  # No position block = auto-sized to preserve source aspect ratio
  
# OR manually specify dimensions:
diagram:
  type: "image"
  path: "architecture.png"
  position: {x: 0.5, y: 0.75, width: 9.0, height: 5.0}
  # validate_aspect_ratio: true (DEFAULT - auto-adjusts to prevent distortion)
  # validate_aspect_ratio: false (EXPLICIT - allows distortion if needed)
```

### Programmatic Diagrams (python-pptx)

**Flow Diagram**:
```yaml
diagram:
  type: "programmatic"
  style: "flow"
  config:
    steps:
      - {text: "Input", x: 1.0, y: 4.5}
      - {text: "Process", x: 3.5, y: 4.5}
      - {text: "Output", x: 6.0, y: 4.5}
    connectors:
      - {x1: 2.0, y1: 4.85, x2: 3.5, y2: 4.85}
      - {x1: 4.5, y1: 4.85, x2: 6.0, y2: 4.85}
```

**Timeline Diagram**:
```yaml
diagram:
  type: "programmatic"
  style: "timeline"
  config:
    timeline_bar: {x: 1.0, y: 3.3, width: 9.0, height: 0.15}
    phases:
      - {name: "Phase 1", x: 1.5, y: 2.0}
      - {name: "Phase 2", x: 4.0, y: 2.0}
      - {name: "Phase 3", x: 6.5, y: 2.0}
      - {name: "Phase 4", x: 9.0, y: 2.0}
```

## VII. Quality Gates and Validation

### Pre-Generation Validation (YAML Specification Checks)

**Constitutional Rules Validation** (`_validate_constitutional_rules()` method):

- ✓ **Required slides present**: Blocks generation if missing `01_title` or `12_final_slide`
- ✓ **Placeholder text detection**: Warns about Lorem ipsum, [insert], placeholder, todo, tbd, xxx patterns
- ✓ **Slide array validation**: Ensures slides array is not empty

**Character Limit Enforcement** (YAML content validation - BEFORE rendering):

**⛔ HARD STOP - GENERATION CANNOT PROCEED**

Content length validation is **MANDATORY and BLOCKING**:
- If ANY field exceeds its character limit, generation MUST NOT proceed
- Content must be rewritten to fit within limits
- User approval required before generation
- NO EXCEPTIONS - limits prevent text wrapping and overlap

**Why This Matters**:
- Character limits derived from battle-tested experience
- Exceeding limits causes text wrapping, overlap, and unreadable slides
- Silent truncation with ellipses is STRICTLY FORBIDDEN
- All limits defined in `.cdo-aifc/scripts/python/ppt_engine_focused.yaml` (single source of truth)

**Validation Requirements**:
- Check all content fields against config limits BEFORE rendering
- If over limit: generation blocked until fixed
- Rewrites must preserve meaning while fitting limits
- User must approve all content changes

**Diagram Intent Validation** (YAML diagram blocks):
- ✓ **Diagram specification present**: Slides intended for diagrams must have `diagram:` block in YAML
- ✓ **Image files exist**: Validate image paths before generation
- ✓ **Aspect ratio distortion**: Check source vs display aspect ratio ≤10% if `validate_aspect_ratio: true`
  - **Source aspect ratio**: Image file dimensions (e.g., 2400×1333 = 1.8:1)
  - **Display aspect ratio**: On-slide dimensions (e.g., 9.0"×5.0" = 1.8:1)
  - **Acceptable**: Display matches source ±10% (no visible stretching/squashing)
  - **Auto-sizing**: If no position specified, engine preserves source aspect ratio (0% distortion)
- ✓ **Programmatic diagram configs**: Ensure required fields present (type, nodes, edges, labels)
- ✓ **Positioning coordinates**: Verify within slide bounds (x, y, width, height)

### Post-Generation Validation (Rendered PPTX Checks - MANDATORY)

**Architecture**: Python script validates and reports data → Cascade interprets results → Cascade applies fixes → Max 3 retry attempts

**Critical Layout Validation**:

- ✘ **HARD STOP: Image/Diagram presence**: All slides with diagram intent MUST have rendered image/diagram
  - Validation: **Check for actual embedded PICTURE shapes in slide.shapes**
  - Validation: **Verify embedded image dimensions > 0** (catch zero-size failures)
  - Validation: **Confirm image count matches diagram intent**
  - Issue Type: `missing_embedded_image`
  - Cascade Action: Check if diagram file exists, verify YAML syntax, regenerate if needed
  - **Script enforces**: Image embedding failures throw exceptions (no silent failures)

- ✘ **HARD STOP: Diagram placement**: Images/diagrams MUST NOT overlap footer zone (y > 6.5")
  - Validation: Check if diagram bottom extends into footer zone
  - Issue Type: `diagram_overlap`
  - Cascade Action: Adjust diagram position/height in YAML (typical fix: height=5.5")

- ✘ **HARD STOP: Text overlap (Content Shapes)**: Content text bounding boxes MUST NOT overlap
  - Validation: Detect overlapping text shapes (EXCLUDING footer/slide number placeholders)
  - **Divider Slide Exception**: Slides with "Divider" or "Cover w/ Subtitle" layouts are EXCLUDED from overlap checks (footer/slide# naturally overlap by design)
  - Issue Type: `text_overlap`
  - Cascade Action: Rewrite overlapping text to be more concise

- ✘ **HARD STOP: Title/Body Overlap**: Title shapes MUST NOT extend into body content region
  - Validation: Check if title bottom > body top by more than 0.1"
  - Common on multi-column slides with long titles
  - Issue Type: `title_body_overlap`
  - Cascade Action: Shorten title text, reduce title font size, or reduce body text

- ✘ **HARD STOP: Text Truncation**: Text MUST NEVER contain ellipses ("..." or "…")
  - Validation: Scan all text shapes for ellipsis characters
  - Indicates silent truncation at render time (PROHIBITED)
  - Issue Type: `text_truncated`
  - Cascade Action: Rewrite affected text to fit proper character limits

- ✘ **HARD STOP: Header/statement brevity**: Headers and statement text MUST appear naturally sized
  - Validation: Check rendered text box fill percentage and line wrapping
  - Issue Type: `text_too_long`
  - Cascade Action: Condense text in YAML

- ✘ **HARD STOP: Programmatic diagram quality**: Shapes, connectors, and labels MUST align correctly
  - Validation: Check connector endpoints align with shape edges (not intersecting bodies)
  - Validation: Check labels fit within shape boundaries
  - Issue Type: `diagram_quality`
  - Cascade Action: Adjust shape sizes, connector coordinates, or label text in YAML

- ✘ **HARD STOP: Diagram sizing (undersized)**: Diagrams on blank/end slides MUST be scaled to ≥75% of available space
  - Validation: Check `min(width / 12.0, height / 5.5) ≥ 0.75`
  - Below 75%, text may become difficult to read
  - Issue Type: `diagram_undersized`
  - Cascade Action: Regenerate diagram with optimal aspect ratio 2.18:1 (3000×1375 or 2400×1100 pixels)

- ✘ **HARD STOP: Diagram space utilization (low coverage)**: Diagrams on blank/end slides MUST use ≥50% of available space
  - Validation: Check `(width × height) / (12.0 × 5.5) ≥ 0.50`
  - Below 50% indicates inefficient aspect ratio or wasted space
  - Issue Type: `diagram_low_coverage`
  - Cascade Action: Regenerate diagram with aspect ratio matching 2.18:1 (12:5.5)

### Validation Error Response Guide

When validation fails, Cascade must interpret error types and apply appropriate fixes. **See workflows for detailed implementation**.

**Error Type: `text_truncated`**
- **Root Cause**: Field content exceeds character limit, causing ellipsis insertion
- **Fix**: Rewrite text to be more concise while preserving meaning
- **Update**: YAML content field

**Error Type: `title_body_overlap`**
- **Root Cause**: Title text too long, extends into body content region
- **Fix Options** (priority order):
  1. Shorten title text
  2. Reduce body text to create more space
- **Update**: YAML title and/or body fields

**Error Type: `text_overlap`**
- **Root Cause**: Content shapes have overlapping bounding boxes
- **Fix**: Rewrite overlapping text to be more concise
- **Update**: YAML content fields

**Error Type: `missing_embedded_image`**
- **Root Cause**: Diagram path in YAML points to non-existent file OR diagram failed to embed
- **Fix**: Check if file exists in assets/, verify YAML diagram block syntax, regenerate diagram if needed
- **Update**: YAML diagram path or regenerate diagram file

**Error Type: `diagram_overlap`**
- **Root Cause**: Diagram extends into footer zone (y+height > 6.5")
- **Fix Options** (priority order):
  1. **REMOVE `position` block entirely** - let engine auto-center (BEST)
  2. Regenerate diagram with different aspect ratio to fit naturally
  3. Move diagram title from diagram image to slide title field
- **FORBIDDEN**: Do NOT adjust manual position as workaround
- **FORBIDDEN**: Do NOT set `validate_aspect_ratio: false`
- **Update**: YAML diagram block or regenerate diagram

**Error Type: `diagram_undersized`**
- **Root Cause**: Diagram uses < 75% of available 12" × 5.5" slide space
- **Issue**: Text becomes harder to read at smaller sizes
- **Primary Cause**: Aspect ratio mismatch (diagram shape doesn't fit slide shape of 2.18:1)
- **Requirement**: Generation must not proceed until resolved
- **Solution Options** (in priority order):
  1. Change diagram orientation (e.g., horizontal → vertical for timelines/Gantts)
  2. Use different diagram type that fits 2.18:1 better (e.g., milestone chart instead of Gantt)
  3. Restructure content to match slide shape
  4. If already good aspect ratio, increase source resolution for clarity
- **Required**: User consultation on best approach before regenerating
- **Target**: Aspect ratio close to 2.18:1 (any resolution: 2400×1100, 3000×1375, 3600×1650)
- **FORBIDDEN**: Accepting "barely readable" diagrams
- **FORBIDDEN**: Auto-regenerating without user consultation

**Error Type: `diagram_low_coverage`**
- **Root Cause**: Diagram aspect ratio doesn't match slide, uses < 50% of space
- **Issue**: Poor space utilization, wasted slide real estate
- **Requirement**: Generation must not proceed until resolved
- **Solution Options**:
  - Change Mermaid layout direction (LR ↔ TB)
  - Modify diagram structure to fit 12×5.5 space better
  - Use different diagram type with better aspect ratio
- **Required**: User consultation on best approach before regenerating
- **Target Aspect Ratio**: 2.18:1 (12:5.5 landscape)
- **Example Fix**: Change 2000×2000 (1:1 square) to 3000×1375 (2.18:1 landscape)
- **FORBIDDEN**: Accepting wasted space as "good enough"
- **FORBIDDEN**: Auto-fixing without user input

**Error Type: `aspect_ratio_distortion`**
- **Root Cause**: Manual position/size specified causes > 10% aspect ratio distortion
- **Fix**: Remove `position` block to enable auto-sizing with aspect ratio preservation
- **Update**: YAML diagram block

**Error Type: `text_too_long`**
- **Root Cause**: Text appears unnaturally long or cramped in rendered shape
- **Fix**: Condense text to more concise phrasing
- **Update**: YAML content field

**Validation Execution Flow** (Cascade-Driven, 3-Attempt Retry):

```
ATTEMPT = 0
MAX_ATTEMPTS = 3
VALIDATION_PASSED = false

While ATTEMPT < MAX_ATTEMPTS and VALIDATION_PASSED == false:
  
  1. ATTEMPT += 1
  
  2. Generate PPTX from YAML:
     $ python3 ppt_engine_focused.py create outputs/[NAME].pptx --assets-folder assets
     
     If content length error:
       - Parse error to identify fields exceeding limits
       - Cascade rewrites text to fit within limits
       - Update YAML with corrected text
       - Continue loop
  
  3. Validate generated PPTX:
     $ python3 ppt_engine_focused.py validate outputs/[NAME].pptx --json > outputs/[NAME]_validation.json
     
     VALIDATION_STATUS = parse JSON ["validation_results"]["overall_status"]
  
  4. If VALIDATION_STATUS == "pass":
       VALIDATION_PASSED = true
       EXIT LOOP → Report success
  
  5. If VALIDATION_STATUS == "fail":
       Parse validation JSON for issue types:
       
       For each issue:
         - text_truncated → Cascade rewrites text to remove ellipses
         - title_body_overlap → Cascade shortens title or body
         - text_overlap → Cascade makes text more concise
         - missing_embedded_image → Check file exists, fix YAML syntax
         - diagram_overlap → Adjust position/height in YAML
       
       Update YAML with corrections
       Continue loop if ATTEMPT < MAX_ATTEMPTS

Exit Conditions:
- Success: VALIDATION_PASSED == true → Proceed to completion
- Failure: ATTEMPT == MAX_ATTEMPTS and VALIDATION_PASSED == false → Exit with error, manual intervention required
```

**Validation Report Format**:

JSON output (`outputs/[NAME]_validation.json`):
```json
{
  "file": "[NAME].pptx",
  "total_slides": 35,
  "validation_results": {
    "overall_status": "pass" | "fail",
    "slides": [
      {
        "slide_number": 5,
        "issues": [
          {
            "type": "title_body_overlap",
            "severity": "critical",
            "message": "Title extends into body content by 0.25\"",
            "title_shape": "Title 1",
            "body_shape": "Content Placeholder 2",
            "overlap_inches": 0.25,
            "suggested_fix": "Reduce title font size or use shorter title text"
          }
        ]
      }
    ]
  }
}
```

**Validation Iteration Limits**:
- Max 3 attempts for entire presentation (not per-slide)
- Each attempt regenerates full presentation with corrections
- Workflow MUST exit with error if validation fails after 3 attempts
- Do NOT report success if validation status is "fail"
- User receives corrective action recommendations for failed slides

### Legacy Post-Generation Checks (Optional Quality Assurance)
- ✓ PPTX file opens without errors
- ✓ No ZIP duplicates or corruption
- ✓ All shapes render correctly
- ✓ Footers updated with correct metadata
- ✓ Theme colors preserved

## VIII. Error Handling Patterns

### Text Length Violations
```
ERROR: Title exceeds 100 character limit (actual: 127)
FIX: Shorten to "Key Insights from Q4 Data Analysis"
```

### Aspect Ratio Violations
```
ERROR: Image aspect ratio mismatch: 75.33% of target (outside 90-110%)
FIX: Recalculate dimensions or regenerate image
  Current: 2400×1800 (1.333:1)
  Target: 9.0"×5.0" (1.8:1)
  Ideal: 9.0"×6.75" or adjust image to 2400×1333
```

### Missing Content
```
ERROR: Placeholder text detected: "[Insert description here]"
FIX: Generate complete content: "Our data pipeline processes 2M records daily..."
```

## IX. Workflow Integration

### Standard Generation Flow
1. **Parse requirements** → Extract topic, audience, key messages
2. **Plan content** → Map messages to slide types
3. **Generate diagrams** → Mermaid CLI for complex, programmatic for simple
4. **Create YAML spec** → Complete content, diagram refs, validation flags
5. **Execute generation** → Run through library with assets folder
6. **Validate output** → Check ZIP integrity, aspect ratios, rendering

### Assets Management
```
assets/
├── presentation_name.yaml          # YAML spec (persisted)
├── architecture_diagram.mmd        # Mermaid source (version control)
├── architecture_diagram.png        # Generated image (183 KB)
└── timeline_example.yaml           # Reusable component specs
```

---

**Version**: 1.0.0  
**Last Updated**: 2025-11-05  
**Source**: `/Users/md464h/projects/ppt/ppt-maker/ppt_engine_focused.py`  
**Template Library**: `.cdo-aifc/templates/09-documentation-requirements/ppt-maker/ppt-maker-template-library.pptx`
