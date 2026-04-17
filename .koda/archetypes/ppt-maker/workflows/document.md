---
description: Generate markdown executive summary and documentation from PowerPoint presentation (PPT-Maker)
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

### 1. Parse Documentation Request

Extract from $ARGUMENTS:
- **Target presentation**: File path to document
- **Output format**: Executive summary, detailed breakdown, or both
- **Audience level**: Technical, executive, general
- **Sections to include**: All slides or specific sections

### 2. Inspect Presentation

Run `python3 ../../scripts/ppt_engine_focused.py inspect [TARGET_FILE]` to extract all content and metadata.

### 3. Analyze Presentation Structure

Identify:
- Presentation topic and purpose
- Key messages and themes
- Content organization and flow
- Slide types and their usage
- Visual/textual balance

### 4. Extract Content by Slide

For each slide:
- Slide number and type
- Title and subtitle
- Body content and key points
- Visual elements (images, diagrams)
- Speaker notes (if available)

### 5. Generate Documentation

Create comprehensive markdown document:

```markdown
# Presentation Summary: [TITLE]

**Source**: [FILENAME]
**Generated**: [TIMESTAMP]
**Total Slides**: [COUNT]
**Template**: AT&T Day-to-Day Quickstart 2025

---

## Executive Summary

[3-5 sentence high-level overview of presentation content, purpose, and key takeaways]

**Primary Audience**: [TARGET_AUDIENCE]
**Key Message**: [MAIN_POINT]
**Call to Action**: [CTA_IF_APPLICABLE]

---

## Table of Contents

1. [Introduction](#slide-1-title)
2. [Section 1](#section-1)
3. [Section 2](#section-2)
   - [Subsection A](#slide-n)
   - [Subsection B](#slide-m)
4. [Conclusion](#conclusion)

---

## Detailed Content

### Slide 1: Title Slide
**Type**: Title  
**Purpose**: Introduction

**Title**: [MAIN_TITLE]  
**Subtitle**: [SUBTITLE]  
**Metadata**: [DATE/VERSION]

**Summary**: This presentation introduces [TOPIC] to [AUDIENCE], focusing on [KEY_ASPECTS].

---

### Slide 2: [SLIDE_TITLE]
**Type**: [SLIDE_TYPE e.g., "Cover with Photo"]  
**Section**: [SECTION_NAME]

**Title**: [TITLE_TEXT]

**Content**:
[BODY_CONTENT or bullet points]
- Point 1
- Point 2
- Point 3

**Visual Elements**:
- [Description of images/graphics]

**Key Message**: [MAIN_TAKEAWAY]

---

### Slide 3: [SLIDE_TITLE]
**Type**: [SLIDE_TYPE e.g., "Simple Divider"]  
**Section**: [SECTION_NAME]

**Purpose**: Section divider introducing [NEXT_SECTION]

**Text**: "[DIVIDER_TEXT]"

---

[... continue for all slides ...]

### Slide [N]: Logo Slide
**Type**: Final Logo  
**Purpose**: Closing

AT&T logo on gradient background - standard closing slide.

---

## Key Insights

### Main Themes
1. **Theme 1**: [DESCRIPTION]
   - Covered in slides [N, M, ...]
   - Key points: [SUMMARY]

2. **Theme 2**: [DESCRIPTION]
   - Covered in slides [N, M, ...]
   - Key points: [SUMMARY]

3. **Theme 3**: [DESCRIPTION]
   - Covered in slides [N, M, ...]
   - Key points: [SUMMARY]

### Critical Messages

1. **[MESSAGE_1]**
   - Context: [EXPLANATION]
   - Evidence: [SUPPORTING_POINTS]
   - Impact: [SIGNIFICANCE]

2. **[MESSAGE_2]**
   - Context: [EXPLANATION]
   - Evidence: [SUPPORTING_POINTS]
   - Impact: [SIGNIFICANCE]

### Data & Metrics

[IF_QUANTITATIVE_DATA_PRESENT]:
- Metric 1: [VALUE] (Slide [N])
- Metric 2: [VALUE] (Slide [N])
- Trend: [DESCRIPTION]

### Visual Strategy

**Slide Type Distribution**:
- Text-heavy slides: [COUNT] ([PERCENTAGE]%)
- Visual slides (photo, dividers): [COUNT] ([PERCENTAGE]%)
- Layout slides (two-column, four-box): [COUNT] ([PERCENTAGE]%)

**Effectiveness**: [ANALYSIS of visual vs. text balance]

---

## Content Flow Analysis

### Presentation Structure

**Introduction** (Slides 1-2):
- [SUMMARY]

**Body** (Slides 3-[N]):
- Section 1 (Slides 3-5): [TOPIC]
- Section 2 (Slides 6-8): [TOPIC]
- Section 3 (Slides 9-11): [TOPIC]

**Conclusion** (Slide [N]):
- [SUMMARY]

**Logical Flow**: [ASSESSMENT - does it build coherently?]

### Narrative Arc

1. **Setup**: [HOW_PRESENTATION_OPENS]
2. **Development**: [HOW_IDEAS_PROGRESS]
3. **Climax**: [PEAK_MESSAGE or CALL_TO_ACTION]
4. **Resolution**: [HOW_IT_CONCLUDES]

---

## Technical Details

### Template Conformance

✓ **Validation Score**: [SCORE]/100
✓ **Errors**: [COUNT]
✓ **Warnings**: [COUNT]
✓ **Brand Compliance**: [PASS/FAIL]

**Issues** (if any):
- [ISSUE_1]
- [ISSUE_2]

### Content Statistics

- **Total word count**: ~[ESTIMATE] words
- **Average words per slide**: ~[AVERAGE]
- **Longest slide**: Slide [N] ([CHARS] characters)
- **Shortest slide**: Slide [N] ([CHARS] characters)
- **Content density**: [LOW/MEDIUM/HIGH]

### Slide Type Usage

| Slide Type | Count | Percentage |
|---|---|---|
| Title | 1 | [X]% |
| Text-heavy | [N] | [X]% |
| Two-column | [N] | [X]% |
| Four-box | [N] | [X]% |
| Dividers | [N] | [X]% |
| Photo slides | [N] | [X]% |
| Logo | 1 | [X]% |

---

## Recommendations

### Strengths
1. [STRENGTH_1]
2. [STRENGTH_2]
3. [STRENGTH_3]

### Areas for Improvement
1. [IMPROVEMENT_1]
   - **Current**: [ISSUE]
   - **Suggestion**: [FIX]

2. [IMPROVEMENT_2]
   - **Current**: [ISSUE]
   - **Suggestion**: [FIX]

### Potential Enhancements
- Consider adding [SUGGESTION]
- Could strengthen [ASPECT] by [ACTION]
- Opportunity to [IMPROVEMENT]

---

## Appendix

### Slide Reference Quick Guide

| Slide # | Type | Title | Key Content |
|---|---|---|---|
| 1 | Title | [TITLE] | Introduction |
| 2 | [TYPE] | [TITLE] | [BRIEF_SUMMARY] |
| 3 | [TYPE] | [TITLE] | [BRIEF_SUMMARY] |
| ... | ... | ... | ... |
| [N] | Logo | - | Closing |

### Search Keywords

[LIST_OF_KEY_TERMS_AND_CONCEPTS_COVERED]

### Presentation Metadata

- **File size**: [SIZE]
- **Last modified**: [DATE]
- **Template version**: AT&T Day-to-Day Quickstart 2025
- **Conformance validated**: [YES/NO]

---

## Usage Notes

**Best for**: [AUDIENCE_TYPE, e.g., "Executive briefings, team updates, client presentations"]

**Presentation time**: Estimated [TIME] minutes (assuming [X] minutes per slide)

**Follow-up materials**: [SUGGESTIONS for supporting docs, handouts, etc.]

**Contact**: [IF_CONTACT_INFO_IN_PRESENTATION]

---

*This documentation was auto-generated by PPT-Maker. For questions or to modify the presentation, use `/refactor-ppt`.*
```

### 6. Generate Output

Save documentation to markdown file:
- Filename: `[PRESENTATION_NAME]_summary.md`
- Location: Same directory as presentation or specified output path

### 7. Report Completion

```
✅ Documentation Generated

📄 Output: [OUTPUT_FILE]
📊 Summary Statistics:
   - Slides documented: [COUNT]
   - Key insights: [COUNT]
   - Word count: ~[ESTIMATE]

📋 Document Sections:
   ✓ Executive summary
   ✓ Detailed slide-by-slide breakdown
   ✓ Key insights and themes
   ✓ Content flow analysis
   ✓ Technical details
   ✓ Recommendations
   ✓ Quick reference guide

💡 Next Steps:
   1. Review generated documentation
   2. Share with stakeholders
   3. Use as basis for speaker notes
   4. Reference for future presentations

🔧 Related Commands:
   - Update presentation: /refactor-ppt
   - Validate content: /test-ppt
   - Compare versions: /compare-ppt
```

## Error Handling

**Cannot Extract Content**: File may be corrupted, suggest running /debug-ppt first.

**Empty Slides**: Note slides with no extractable content, suggest manual review.

**Complex Formatting**: Warn if presentation has unusual structure that may not document fully.

## Examples

**Example 1**: `/document-ppt outputs/quarterly_review.pptx`
Output: Full markdown documentation with executive summary and detailed breakdown

**Example 2**: `/document-ppt outputs/project_update.pptx --executive-only`
Output: Concise executive summary focusing on key messages

**Example 3**: `/document-ppt outputs/training.pptx --audience technical`
Output: Technical-focused documentation with implementation details

## References

- `/inspect-ppt` - Technical metadata extraction
- `/test-ppt` - Validation and conformance check
- `/compare-ppt` - Compare documented versions
- `template_metadata.yaml` - Template reference
