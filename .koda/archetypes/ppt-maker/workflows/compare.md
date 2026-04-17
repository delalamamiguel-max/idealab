---
description: Compare two PowerPoint presentations or design approaches (PPT-Maker)
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

### 1. Parse Comparison Request

Extract from $ARGUMENTS:
- **Presentation A**: First file path or approach
- **Presentation B**: Second file path or approach
- **Comparison type**: Side-by-side, diff analysis, or approach evaluation
- **Focus areas**: Content, structure, conformance, or all

### 2. Inspect Both Presentations

Run `python3 ../../scripts/ppt_engine_focused.py inspect [FILE_A]` to extract metadata.

Run `python3 ../../scripts/ppt_engine_focused.py inspect [FILE_B]` to extract metadata.

Run validation on both files to compare conformance levels.

### 3. Perform Comparison Analysis

Analyze differences across dimensions:

**Structural Comparison**:
- Total slide count
- Slide types used
- Slide ordering
- Content distribution

**Content Comparison**:
- Title differences
- Body text changes
- Content density (chars per slide)
- Message focus

**Conformance Comparison**:
- Template adherence score
- Validation errors/warnings
- Brand compliance level
- Layout integrity

**Quality Metrics**:
- Content clarity
- Visual balance
- Message effectiveness
- Audience appropriateness

### 4. Generate Comparison Report

```markdown
# Presentation Comparison Report

**File A**: [PRESENTATION_A]
**File B**: [PRESENTATION_B]
**Compared**: [TIMESTAMP]

## Executive Summary

**Recommendation**: [PREFER_A / PREFER_B / MERGE_BEST_ELEMENTS]

**Rationale**: [BRIEF_EXPLANATION]

## Quick Stats

|  Metric | Presentation A | Presentation B |
|---|---|---|
| **Slides** | [COUNT_A] | [COUNT_B] |
| **Conformance** | [SCORE_A]/100 | [SCORE_B]/100 |
| **Errors** | [ERROR_A] | [ERROR_B] |
| **Warnings** | [WARN_A] | [WARN_B] |
| **Avg Content/Slide** | [CHARS_A] chars | [CHARS_B] chars |

## Structural Comparison

### Slide Count & Organization
- **A**: [COUNT_A] slides ([DISTRIBUTION_A])
- **B**: [COUNT_B] slides ([DISTRIBUTION_B])

**Winner**: [A/B/TIE] - [REASON]

### Slide Types Used

**Presentation A**:
- Title: 1
- Text-heavy: [COUNT]
- Two-column: [COUNT]
- Four-box: [COUNT]
- Other: [COUNT]
- Logo: 1

**Presentation B**:
- Title: 1
- Text-heavy: [COUNT]
- Two-column: [COUNT]
- Four-box: [COUNT]
- Other: [COUNT]
- Logo: 1

**Analysis**: [WHICH_USES_SLIDE_TYPES_MORE_EFFECTIVELY]

## Content Comparison

### Slide-by-Slide Comparison

#### Slide 1: Title
| Element | A | B | Better |
|---|---|---|---|
| Title | [TEXT_A] | [TEXT_B] | [A/B/TIE] |
| Subtitle | [TEXT_A] | [TEXT_B] | [A/B/TIE] |

**Notes**: [ANALYSIS]

#### Slide 2: [SLIDE_TYPE]
| Element | A | B | Difference |
|---|---|---|---|
| Title | [TEXT_A] | [TEXT_B] | [DIFF] |
| Body | [SUMMARY_A] ([CHARS]c) | [SUMMARY_B] ([CHARS]c) | [ANALYSIS] |

**Notes**: [DETAILED_ANALYSIS]

[... continue for all slides ...]

## Conformance Comparison

### Template Adherence

**Presentation A**:
- ✓ Mandatory slides present
- ✓ Layout integrity maintained
- ⚠️ 2 warnings (text overflow)
- **Score**: [SCORE]/100

**Presentation B**:
- ✓ Mandatory slides present
- ✓ Layout integrity maintained
- ✓ No warnings
- **Score**: [SCORE]/100

**Winner**: [A/B/TIE] - [REASON]

### Brand Compliance

| Aspect | A | B | Notes |
|---|---|---|---|
| Font usage | ✓ | ✓ | Both conform |
| Color scheme | ✓ | ✓ | Both conform |
| Layout | ✓ | ⚠️ | B has minor deviation |

## Quality Assessment

### Content Quality
- **Clarity**: [A_RATING] vs [B_RATING] - [WINNER]
- **Completeness**: [A_RATING] vs [B_RATING] - [WINNER]
- **Conciseness**: [A_RATING] vs [B_RATING] - [WINNER]

### Message Effectiveness
- **A**: [STRENGTHS] / [WEAKNESSES]
- **B**: [STRENGTHS] / [WEAKNESSES]

### Audience Fit
- **A**: [AUDIENCE_ANALYSIS]
- **B**: [AUDIENCE_ANALYSIS]

## Detailed Differences

### Content Only in A
1. [UNIQUE_POINT_1]
2. [UNIQUE_POINT_2]

### Content Only in B
1. [UNIQUE_POINT_1]
2. [UNIQUE_POINT_2]

### Shared Content with Variations
1. [TOPIC]: A emphasizes [X], B emphasizes [Y]
2. [TOPIC]: A uses [APPROACH_A], B uses [APPROACH_B]

## Recommendations

### Best Overall: [A / B / HYBRID]

**Rationale**: [DETAILED_EXPLANATION]

### Merge Strategy (If Applicable)

To combine the best elements:

1. **Use A's structure** for [REASON]
2. **Incorporate B's content** on slides [N, M, ...]
3. **Adopt B's approach** for [SPECIFIC_ASPECT]
4. **Keep A's treatment** of [SPECIFIC_TOPIC]

**Implementation**:
\`\`\`python
# Merge script
# Use A as base, incorporate best from B
# [SPECIFIC_CODE_GUIDANCE]
\`\`\`

### Use Case Recommendations

**Use A if**:
- [SCENARIO_1]
- [SCENARIO_2]

**Use B if**:
- [SCENARIO_1]
- [SCENARIO_2]

## Next Steps

[IF CLEAR WINNER]:
✓ Proceed with Presentation [A/B]
✓ Optional: Incorporate specific elements from [B/A]
✓ Run final /test-ppt for validation

[IF MERGE RECOMMENDED]:
1. Create merged version using /refactor-ppt
2. Combine best elements as outlined above
3. Validate merged result with /test-ppt

[IF TIE]:
Both presentations are equally valid
Choice depends on:
- [DECISION_FACTOR_1]
- [DECISION_FACTOR_2]
```

### 5. Present Findings

Display comparison report with:
- Clear recommendation
- Quantitative metrics
- Qualitative analysis
- Actionable next steps

## Error Handling

**File Not Found**: Verify both file paths, suggest correct paths.

**Incompatible Presentations**: Detect if presentations use different templates, note limitations.

**Cannot Compare**: Explain why comparison isn't meaningful (e.g., completely different topics).

## Examples

**Example 1**: `/compare-ppt outputs/version_A.pptx outputs/version_B.pptx`
Output: Full side-by-side comparison with recommendation

**Example 2**: `/compare-ppt outputs/draft.pptx outputs/final.pptx --focus content`
Output: Content-focused comparison showing revisions made

**Example 3**: `/compare-ppt "Use text-heavy slides" "Use visual-heavy approach" --approach`
Output: Conceptual comparison of two design approaches with template recommendations

## References

- `/test-ppt` - Validate presentations
- `/refactor-ppt` - Merge best elements
- `/document-ppt` - Generate summaries for comparison
