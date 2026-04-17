---
description: Compare two documentation approaches and patterns (Documentation Evangelist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype documentation-evangelist --json ` and parse for DOC_FORMAT, DIAGRAM_TOOL, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/documentation-evangelist/templates/env-config.yaml` for format standards, best practices

### 3. Parse Input
Extract from $ARGUMENTS: two documentation approaches/files to compare, comparison criteria (structure/clarity/completeness/maintainability), specific concerns or goals. Request clarification if incomplete.

### 4. Analyze Both Approaches

For each approach, assess:

**Structure**:
- Section organization and hierarchy
- Table of contents presence and quality
- Heading levels and consistency
- Required sections coverage

**Content Quality**:
- Clarity and readability
- Completeness of information
- Accuracy and currency
- Example quality and relevance
- Technical depth appropriateness for audience

**Visual Elements**:
- Diagram presence and quality
- Diagram types (architecture, data flow, sequence, ERD)
- Diagram clarity and annotations
- Table usage for structured data
- Code block formatting and syntax highlighting

**Metadata & Standards**:
- Metadata block completeness
- Version information
- Last updated date
- Author attribution
- Change log presence

**Maintainability**:
- Parameterized links vs hard-coded
- Modular structure vs monolithic
- Line length compliance
- Consistent formatting
- Update frequency indicators

**Usability**:
- Navigation ease
- Search-friendliness
- Cross-reference quality
- Troubleshooting accessibility
- Quick-start availability

### 5. Compare Approaches

Generate side-by-side comparison:

**Comparison Matrix**:
```markdown
| Criterion | Approach A | Approach B | Winner | Rationale |
|-----------|------------|------------|--------|-----------|
| Structure | Hierarchical, 7 sections | Flat, 12 sections | A | Better organization |
| Diagrams | 3 Mermaid diagrams | Text descriptions only | A | Visual clarity |
| Completeness | Missing troubleshooting | All sections present | B | Better coverage |
| Maintainability | Hard-coded links | Parameterized links | B | Easier updates |
| Line Length | 15 violations | Compliant | B | Standards adherence |
```

**Detailed Analysis**:

For each criterion, provide:
- **Observation**: What each approach does
- **Pros**: Advantages of each approach
- **Cons**: Disadvantages of each approach
- **Impact**: Effect on documentation quality/usability
- **Recommendation**: Which approach is better and why

**Example Analysis**:
```
Criterion: Diagram Usage

Approach A: Uses 3 Mermaid diagrams (architecture, data flow, sequence)
Pros: Visual clarity, easier to understand complex flows, professional appearance
Cons: Requires Mermaid tooling, may not render in all viewers
Impact: Significantly improves comprehension for visual learners

Approach B: Uses text descriptions with ASCII art
Pros: Works everywhere, no special tools needed, easy to edit
Cons: Less clear, harder to understand complex relationships, looks dated
Impact: May confuse readers, requires more cognitive effort

Recommendation: Approach A (Mermaid diagrams)
Rationale: Modern documentation standards favor visual diagrams. Mermaid is widely supported and significantly improves comprehension. The tooling requirement is minimal compared to the usability benefit.
```

### 6. Provide Recommendations

**Overall Winner**: Declare which approach is superior overall with justification.

**Hybrid Approach**: Suggest combining best elements of both:
- Use Approach A's diagram strategy
- Adopt Approach B's section organization
- Merge troubleshooting sections from both
- Apply Approach B's parameterization pattern

**Implementation Guidance**:
- Specific steps to adopt recommended approach
- Migration path if switching approaches
- Tools and templates needed
- Estimated effort and timeline

**Best Practices**:
- Industry standards for this documentation type
- Common pitfalls to avoid
- Maintenance considerations
- Scalability factors

### 7. Generate Comparison Report

Create comprehensive comparison document:

**Executive Summary**: One-paragraph overview of comparison results and recommendation.

**Detailed Comparison**: Full analysis with comparison matrix and criterion-by-criterion breakdown.

**Recommendations**: Actionable steps to improve documentation based on comparison.

**Appendix**: Screenshots/examples from both approaches, reference materials, tool recommendations.

## Error Handling

**Missing Files**: Report missing documentation files, suggest correct paths.

**Incomparable Approaches**: Explain why approaches can't be compared (different audiences, different purposes), suggest alternative comparison.

**Unclear Criteria**: Request clarification on comparison goals, provide example criteria.

## Examples

**Markdown vs Confluence**: `/compare-documentation "Compare Markdown-based docs in Git vs Confluence wiki for API documentation. Criteria: maintainability, version control, collaboration, search."`
Output: Detailed comparison showing Markdown wins on version control and maintainability, Confluence wins on collaboration and search, with hybrid recommendation.

**Monolithic vs Modular**: `/compare-documentation path/to/single_readme.md path/to/docs_directory/ "Compare single large README vs multiple focused docs. Criteria: navigation, maintainability, findability."`
Output: Analysis showing modular approach wins on navigation and maintainability, monolithic wins on simplicity, with recommendation for modular with strong index.

**Diagram Approaches**: `/compare-documentation "Compare Mermaid diagrams vs PlantUML vs hand-drawn diagrams for architecture documentation. Criteria: clarity, maintainability, tooling, rendering."`
Output: Comparison showing Mermaid wins on maintainability and rendering, PlantUML wins on advanced features, hand-drawn wins on flexibility, with Mermaid recommendation for most cases.

**Documentation Formats**: `/compare-documentation "Compare README.md vs Sphinx docs vs MkDocs for Python library documentation. Criteria: ease of use, features, search, hosting."`
Output: Analysis showing MkDocs wins on balance of features and ease, Sphinx wins on advanced features, README wins on simplicity, with MkDocs recommendation.

## References

Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/documentation-evangelist/templates/env-config.yaml`
