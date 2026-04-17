---
description: Refactor existing documentation to improve clarity, completeness, and maintainability (Documentation Evangelist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype documentation-evangelist --json ` and parse for DOC_FORMAT, DIAGRAM_TOOL, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/documentation-evangelist/templates/env-config.yaml` for format standards, max line length

### 3. Parse Input
Extract from $ARGUMENTS: documentation file path, refactoring goals (clarity/completeness/structure/diagrams), specific issues to address. Read existing documentation file. Request clarification if incomplete.

### 4. Analyze Existing Documentation

Assess current state:
- **Structure**: Check for required sections (Overview, Data Flow, Schema Definitions, Metrics Glossary)
- **Metadata**: Verify metadata block exists with version, author, date
- **Diagrams**: Validate Mermaid syntax, check diagram completeness
- **Content**: Assess clarity, completeness, accuracy
- **Formatting**: Check line length ≤100 chars, consistent heading levels
- **Links**: Verify all links are parameterized, not hard-coded

Identify issues: missing sections, outdated content, broken diagrams, hard-coded values, inconsistent formatting, unclear explanations.

### 5. Validate Constraints
Check against hard-stop rules:
- ✘ Refuse line length > 100 characters
- ✘ Refuse missing metadata block
- ✘ Refuse invalid Mermaid code
- ✘ Refuse hard-coded links
- ✘ Refuse missing required sections
If violated, plan fixes in refactoring.

### 6. Refactor Documentation

Apply improvements based on analysis:

**Structure Improvements**:
- Add missing required sections
- Reorganize sections for logical flow: Overview → Data Flow → Schema Definitions → Metrics Glossary
- Break long sections into subsections
- Add table of contents if missing

**Content Improvements**:
- Clarify vague descriptions
- Add concrete examples where missing
- Update outdated information
- Fill in TODO/placeholder content
- Add missing context or background

**Diagram Improvements**:
- Fix invalid Mermaid syntax
- Add missing diagrams (architecture, data flow)
- Improve diagram clarity with better labels
- Add annotations and notes to diagrams

**Formatting Improvements**:
- Fix line length violations (wrap at 100 chars)
- Standardize heading levels
- Convert inline lists to proper Markdown lists
- Use tables for structured data
- Add code block syntax highlighting

**Metadata Improvements**:
- Add/update metadata block
- Update version number
- Update last modified date
- Add author if missing

Apply mandatory patterns: metadata header compliance, Mermaid diagram validation, template compliance, parameterized references.

### 7. Add Recommendations

Suggest additional improvements: add FAQ section, include troubleshooting examples, add performance notes, include cost considerations, add security best practices.

### 8. Validate and Report


Generate diff showing changes. Report completion with: changes summary, before/after metrics (sections, diagrams, line count), validation results, remaining issues, next steps.

## Error Handling

**Hard-Stop Violations**: Explain violation, show compliant alternative, apply fix automatically where possible.

**File Not Found**: Report missing file, suggest correct path, provide example of well-formed input.

**Parse Errors**: Report syntax errors in existing doc, suggest fixes, offer to create new version.

## Examples

**Outdated Pipeline Doc**: `/refactor-documentation path/to/pipeline_doc.md "Update outdated Airflow references to TWS, fix broken Mermaid diagrams, add missing troubleshooting section, ensure all links are parameterized"`
Output: Refactored doc with TWS terminology, fixed diagrams, new troubleshooting section, parameterized links.

**Incomplete API Doc**: `/refactor-documentation path/to/api_doc.md "Add missing authentication section, create sequence diagrams for OAuth flow, add error code reference table, improve example clarity"`
Output: Enhanced doc with auth section, OAuth sequence diagram, error code table, clearer examples.

**Messy README**: `/refactor-documentation path/to/README.md "Reorganize sections for better flow, add table of contents, fix line length violations, convert inline lists to proper Markdown, add architecture diagram"`
Output: Well-structured README with TOC, proper formatting, architecture diagram.

## References

Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/documentation-evangelist/templates/env-config.yaml`
