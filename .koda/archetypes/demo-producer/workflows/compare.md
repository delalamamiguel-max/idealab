---
description: Compare demo approaches, strategies, and output formats (Demo Producer)
---

**Archetype**: Demo Producer (Demo Production)  
**Constitution**: `${ARCHETYPES_BASEDIR}/demo-producer/demo-producer-constitution.md`

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Parse Input

Extract from $ARGUMENTS:
- **Comparison Type**: approaches | formats | audiences | durations
- **Option A**: First approach/format to compare
- **Option B**: Second approach/format to compare
- **Context**: Product type, audience, goals

### 2. Load Comparison Framework

Based on comparison type, load relevant criteria:

**Approach Comparison:**
- Feature-focused vs Workflow-focused
- Technical vs Business narrative
- Comprehensive vs Highlights-only
- Live demo vs Recorded demo

**Format Comparison:**
- Video (MP4/WebM) vs Screenshots
- GIF vs Video clips
- Interactive HTML vs Static presentation
- PowerPoint vs Web-based

**Audience Comparison:**
- Executive (1-2 min, high-level)
- Business (3-5 min, benefits-focused)
- Technical (5-10 min, detailed)
- Training (10+ min, comprehensive)

**Duration Comparison:**
- Quick teaser (30-60 seconds)
- Standard demo (2-3 minutes)
- Deep dive (5-7 minutes)
- Full walkthrough (10+ minutes)

### 3. Analyze Approaches

**Approach A Analysis:**
```markdown
## Approach A: [NAME]

**Description:** [DESCRIPTION]

**Strengths:**
- [STRENGTH_1]
- [STRENGTH_2]

**Weaknesses:**
- [WEAKNESS_1]
- [WEAKNESS_2]

**Best For:**
- [USE_CASE_1]
- [USE_CASE_2]

**Effort Required:**
- Creation: [LOW/MEDIUM/HIGH]
- Maintenance: [LOW/MEDIUM/HIGH]
- Tools: [LIST]
```

**Approach B Analysis:**
```markdown
## Approach B: [NAME]

**Description:** [DESCRIPTION]

**Strengths:**
- [STRENGTH_1]
- [STRENGTH_2]

**Weaknesses:**
- [WEAKNESS_1]
- [WEAKNESS_2]

**Best For:**
- [USE_CASE_1]
- [USE_CASE_2]

**Effort Required:**
- Creation: [LOW/MEDIUM/HIGH]
- Maintenance: [LOW/MEDIUM/HIGH]
- Tools: [LIST]
```

### 4. Generate Comparison Matrix

```markdown
# Demo Approach Comparison

## Comparison Matrix

| Criterion | Approach A | Approach B | Winner | Rationale |
|-----------|------------|------------|--------|-----------|
| **Engagement** | [SCORE] | [SCORE] | [A/B] | [WHY] |
| **Clarity** | [SCORE] | [SCORE] | [A/B] | [WHY] |
| **Production Effort** | [SCORE] | [SCORE] | [A/B] | [WHY] |
| **Maintenance** | [SCORE] | [SCORE] | [A/B] | [WHY] |
| **Shareability** | [SCORE] | [SCORE] | [A/B] | [WHY] |
| **Accessibility** | [SCORE] | [SCORE] | [A/B] | [WHY] |
| **File Size** | [SCORE] | [SCORE] | [A/B] | [WHY] |
| **Platform Support** | [SCORE] | [SCORE] | [A/B] | [WHY] |

**Overall Winner:** [A/B/TIE]
```

### 5. Provide Detailed Analysis

**Engagement:**
- How well does each approach capture attention?
- Does it maintain interest throughout?
- Is the pacing appropriate?

**Clarity:**
- How clearly does it communicate features?
- Is the narrative easy to follow?
- Are key points emphasized?

**Production Effort:**
- How long to create initially?
- What tools/skills required?
- Can it be automated?

**Maintenance:**
- How easy to update when product changes?
- What breaks when UI changes?
- How much rework needed?

**Shareability:**
- Can it be easily shared via email/Slack?
- Does it work on mobile?
- File size constraints?

**Accessibility:**
- Does it work without sound?
- Are captions available?
- Color contrast adequate?

### 6. Recommend Approach

Based on analysis and context:

```markdown
## Recommendation

**Recommended Approach:** [A/B/HYBRID]

**Rationale:**
[DETAILED_EXPLANATION]

**When to Use Approach A:**
- [SCENARIO_1]
- [SCENARIO_2]

**When to Use Approach B:**
- [SCENARIO_1]
- [SCENARIO_2]

**Hybrid Strategy:**
[IF_APPLICABLE]

**Implementation Steps:**
1. [STEP_1]
2. [STEP_2]
3. [STEP_3]
```

### 7. Report Comparison

```
✅ Demo Comparison Complete

📊 Comparison: [APPROACH_A] vs [APPROACH_B]

🏆 Results:
   Engagement:      [A/B] wins
   Clarity:         [A/B] wins
   Production:      [A/B] wins (lower effort)
   Maintenance:     [A/B] wins (easier updates)
   Shareability:    [A/B] wins
   Accessibility:   [A/B] wins

📋 Overall Winner: [APPROACH]

💡 Recommendation:
   [SUMMARY_RECOMMENDATION]

🔄 Next Steps:
   - Implement: /scaffold-demo --approach [RECOMMENDED]
   - Review full analysis in comparison-report.md
```

## Common Comparisons

### Feature-Focused vs Workflow-Focused

**Feature-Focused:**
- Shows each feature independently
- Good for feature catalogs
- Easy to update individual features
- May feel disconnected

**Workflow-Focused:**
- Shows end-to-end user journey
- Better storytelling
- Shows features in context
- Harder to update (ripple effects)

**Recommendation:** Workflow-focused for sales demos, feature-focused for documentation.

### Video vs Screenshots

**Video:**
- Shows interactions naturally
- Higher engagement
- Larger file sizes
- Harder to update

**Screenshots:**
- Easy to annotate
- Small file sizes
- Easy to update
- Less engaging

**Recommendation:** Video for key workflows, screenshots for feature highlights.

### Executive vs Technical Demo

**Executive (1-2 min):**
- High-level benefits
- ROI focus
- Minimal technical detail
- Strong call to action

**Technical (5-10 min):**
- Detailed features
- Integration points
- Configuration options
- API examples

**Recommendation:** Create both, share appropriate version with audience.

## Error Handling

**Unclear Comparison**: Ask for specific aspects to compare.

**Invalid Options**: Suggest valid comparison types.

**Missing Context**: Request product type and audience information.

## Examples

**Example 1**: `/compare-demo Feature-focused vs workflow-focused approach for AndiSense sales demo`
Output: Detailed comparison recommending workflow-focused for sales context.

**Example 2**: `/compare-demo Video vs GIF format for Slack sharing`
Output: Analysis showing GIF wins for Slack due to auto-play and size limits.

**Example 3**: `/compare-demo 2-minute vs 5-minute demo for executive audience`
Output: Recommends 2-minute with option to "learn more" for those interested.

**Example 4**: `/compare-demo Recorded demo vs live demo for customer calls`
Output: Hybrid recommendation - recorded for consistency, live for Q&A.

## References

- Constitution: (pre-loaded above)
- Related: `/scaffold-demo`, `/document-demo`
