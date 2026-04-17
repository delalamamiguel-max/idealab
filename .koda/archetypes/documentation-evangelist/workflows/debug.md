---
description: Debug documentation issues including broken diagrams, invalid syntax, and formatting errors (Documentation Evangelist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype documentation-evangelist --json ` and parse for DOC_FORMAT, DIAGRAM_TOOL, MARKDOWN_LINTER, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/documentation-evangelist/templates/env-config.yaml` for linting rules, diagram validation settings

### 3. Parse Input
Extract from $ARGUMENTS: documentation file path, reported issue/error, symptoms (rendering fails, diagrams broken, links dead, validation errors). Read documentation file. Request clarification if incomplete.

### 4. Run Diagnostic Checks

Execute comprehensive validation:

**Markdown Linting**:
```bash
markdownlint <file>.md --json
```
Check for: line length violations, heading hierarchy issues, list formatting problems, missing blank lines around code blocks, trailing whitespace.

**Mermaid Diagram Validation**:
```bash
mmdc --input <file>.md --validate
```
Check for: syntax errors in Mermaid blocks, invalid node/edge definitions, unclosed blocks, unsupported diagram types.

**Link Validation**:
- Check all internal links resolve
- Verify external links are parameterized
- Identify broken references
- Check anchor links exist

**Code Block Validation**:
- Verify syntax highlighting language specified
- Check embedded code examples for syntax errors
- Validate code examples match documented language version

**Metadata Validation**:
- Check YAML frontmatter syntax
- Verify required fields present (title, author, date, version)
- Validate date formats

**Structure Validation**:
- Verify required sections present
- Check heading hierarchy (no skipped levels)
- Validate table of contents matches actual sections

### 5. Analyze Issues

Categorize findings:

**Critical Issues** (prevent rendering):
- Invalid Mermaid syntax
- Malformed YAML frontmatter
- Broken internal links
- Unclosed code blocks

**Major Issues** (reduce quality):
- Missing required sections
- Line length violations
- Hard-coded links/paths
- Outdated content markers (TODO, FIXME)

**Minor Issues** (style/consistency):
- Inconsistent heading capitalization
- Missing code block languages
- Trailing whitespace
- Inconsistent list formatting

Identify root causes for each issue.

### 6. Generate Fix Recommendations

For each issue, provide:
- **Issue Description**: What's wrong and where (line number)
- **Impact**: How it affects documentation usability
- **Root Cause**: Why the issue exists
- **Fix**: Specific corrective action with example
- **Prevention**: How to avoid in future

**Example Fix Format**:
```
Issue: Invalid Mermaid syntax at line 45
Impact: Diagram fails to render, breaks documentation flow
Root Cause: Missing semicolon after node definition
Fix: Add semicolon: `A[Start] --> B[Process];`
Prevention: Use mermaid-cli validation before commit
```

### 7. Apply Fixes (if requested)

If user requests automatic fixes, apply corrections:
- Fix Mermaid syntax errors
- Correct line length violations (wrap text)
- Fix heading hierarchy
- Add missing blank lines
- Remove trailing whitespace
- Add missing code block languages
- Parameterize hard-coded links

### 8. Validate and Report


Generate diagnostic report:
- **Issues Found**: Count by severity (critical/major/minor)
- **Issues Fixed**: List of applied corrections
- **Remaining Issues**: Issues requiring manual intervention
- **Validation Results**: Pass/fail for each check
- **Recommendations**: Preventive measures and best practices

## Error Handling

**Validation Tool Missing**: Report missing tool (markdownlint, mermaid-cli), provide installation instructions.

**File Not Found**: Report missing file, suggest correct path, verify file extension.

**Parse Errors**: Report unparseable content, identify problematic section, suggest restructuring.

## Examples

**Broken Mermaid Diagram**: `/debug-documentation path/to/architecture.md "Mermaid diagram not rendering, shows syntax error"`
Output: Identifies syntax error at line 67 (missing arrow), provides corrected Mermaid code, validates fix.

**Markdown Lint Failures**: `/debug-documentation path/to/README.md "CI pipeline failing on markdown lint with 15 errors"`
Output: Lists all 15 lint errors with line numbers, categorizes by severity, provides fixes for each, optionally applies corrections.

**Broken Links**: `/debug-documentation path/to/api_guide.md "Multiple broken internal links, table of contents doesn't match sections"`
Output: Identifies 5 broken links, shows correct anchor format, regenerates TOC, validates all links resolve.

**Invalid Code Examples**: `/debug-documentation path/to/tutorial.md "Embedded Python code examples have syntax errors"`
Output: Runs Python syntax check on code blocks, identifies 3 syntax errors, provides corrected code, adds proper syntax highlighting.

## References

Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/documentation-evangelist/templates/env-config.yaml`
