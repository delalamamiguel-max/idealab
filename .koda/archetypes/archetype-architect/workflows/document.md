---
description: Generate comprehensive documentation for an archetype (Archetype Architect)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Identify Archetype to Document

Extract from $ARGUMENTS:
- Archetype slug
- Category
- Documentation scope (full or specific sections)

### 1.5 Gather Archetype Metadata

Read archetype metadata:
```bash
python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/discover-archetype.py \
  --validate {archetype-slug} --json
```

Also read:
- `${ARCHETYPES_BASEDIR}/{archetype-slug}/manifest.yaml` - For keywords, description, workflows
- `${ARCHETYPES_BASEDIR}/{archetype-slug}/{archetype-slug}-constitution.md` - For rules and patterns
- `${ARCHETYPES_BASEDIR}/{archetype-slug}/changelog.md` - For version history (if exists)

### 1.6 Delegate to Solution Document (CRITICAL)

**Purpose:** Leverage specialist archetypes for high-quality documentation.

Execute `/solution-document` with multi-archetype context:

```
/solution-document "
Generate comprehensive documentation for {archetype-slug} archetype.

PRIMARY SPECIALIST: documentation-evangelist
- Handle: Document structure, prose quality, visual presentation
- Expertise: Technical writing, information architecture, accessibility

DOMAIN EXPERT: {archetype-slug}
- Handle: Domain-accurate content, code examples, configuration specifics
- Expertise: The actual technology being documented

OUTPUT REQUIREMENTS:
1. README.md at archetype root (required)
2. docs/design.md if architecture is complex (optional)
3. Workflow-specific examples

CONTENT FROM METADATA:
- Display Name: {display_name}
- Description: {description}
- Keywords: {keywords}
- Constitution Rules: {extracted_rules}
- Workflows: {workflow_list}
"
```

**Benefits of Delegation:**
- ✅ Prose quality from documentation-evangelist
- ✅ Domain accuracy from target archetype
- ✅ Consistent structure across all archetype documentation
- ✅ Best practices automatically applied

### 2. Generate Archetype Overview

```markdown
# {Archetype Display Name}

**Category:** {Category Name}  
**Slug:** `{archetype-slug}`  
**Status:** {Active/Beta/Deprecated}

## Purpose

{One-paragraph description of what this archetype does}

## When to Use

Use this archetype when you need to:
- {Use case 1}
- {Use case 2}
- {Use case 3}

## Technologies

- {Technology 1}
- {Technology 2}
- {Technology 3}
```

### 3. Document Workflows

```markdown
## Available Workflows

### Scaffold
Generate new {artifact} from scratch.

**Usage:**
```bash
/scaffold-{archetype-slug} "Your requirements"
```

**Example:**
```bash
/scaffold-{archetype-slug} "{concrete example}"
```

### Debug
Troubleshoot {artifact} errors and failures.

**Usage:**
```bash
/debug-{archetype-slug} "Error description"
```

### Refactor
Improve existing {artifact} with best practices.

**Usage:**
```bash
/refactor-{archetype-slug} "Code to improve"
```

### Test
Generate test harness for {artifact}.

**Usage:**
```bash
/test-{archetype-slug} "Code to test"
```

### Compare
Evaluate multiple approaches.

**Usage:**
```bash
/compare-{archetype-slug} "Option A vs Option B"
```

### Document
Generate documentation for {artifact}.

**Usage:**
```bash
/document-{archetype-slug} "Code to document"
```
```

### 4. Document Constitution Rules

```markdown
## Governance Rules

### Hard-Stop Rules (Non-Negotiable)

{Extract from constitution}
- ✘ {Rule 1}
- ✘ {Rule 2}
- ✘ {Rule 3}

### Mandatory Patterns (Required)

{Extract from constitution}
- ✔ {Pattern 1}
- ✔ {Pattern 2}
- ✔ {Pattern 3}

### Preferred Patterns (Recommended)

{Extract from constitution}
- ➜ {Pattern 1}
- ➜ {Pattern 2}
```

### 5. Document Configuration

```markdown
## Configuration

### Environment Variables

Required:
- `{ENV_VAR_1}`: {Description}
- `{ENV_VAR_2}`: {Description}

Optional:
- `{ENV_VAR_3}`: {Description}

### Performance Targets

- Expected runtime: {X} seconds
- Maximum runtime: {Y} seconds
- Maximum cost: ${Z}

### Variables

Common variables used in generated code:
- `{{var.variable_1}}`: {Description}
- `{{var.variable_2}}`: {Description}
```

### 6. Add Examples

```markdown
## Examples

### Example 1: {Use Case}

**Request:**
```bash
/scaffold-{archetype-slug} "{example request}"
```

**Generated Output:**
```{language}
{sample output}
```

### Example 2: {Use Case}

**Request:**
```bash
/debug-{archetype-slug} "{example error}"
```

**Diagnosis:**
{diagnostic output}

**Fix:**
{fix recommendation}
```

### 7. Add Discovery Keywords

```markdown
## Discovery

This archetype is automatically detected when you use keywords like:

**Primary Keywords:**
- "{keyword1}"
- "{keyword2}"
- "{keyword3}"

**Example Queries:**
- `/scaffold {keyword1} for {use case}`
- `/debug {keyword2} error in {context}`
```

### 8. Add Related Archetypes

```markdown
## Related Archetypes

- **{Related Archetype 1}**: {When to use instead}
- **{Related Archetype 2}**: {How they complement each other}
- **{Related Archetype 3}**: {Comparison}
```

### 9. Add Troubleshooting

```markdown
## Troubleshooting

### Issue: {Common Problem}

**Symptoms:** {Description}

**Cause:** {Root cause}

**Solution:**
```bash
{fix command or steps}
```

### Issue: {Common Problem 2}

...
```

### 10. Generate Complete Documentation

Combine all sections into comprehensive markdown document.

## Documentation Patterns

### Pattern 1: Quick Start Guide

For new archetypes, include:
1. 30-second overview
2. Installation/setup (if needed)
3. Simplest possible example
4. Link to full documentation

### Pattern 2: Use Case Matrix

When archetype covers multiple scenarios:

| Use Case | Workflow | Example |
|----------|----------|---------|
| {Use case 1} | scaffold | `{example}` |
| {Use case 2} | refactor | `{example}` |
| {Use case 3} | debug | `{example}` |

### Pattern 3: Decision Tree

When users might be unsure which archetype to use:

```
Need to work with {domain}?
├─ {Specific tool}? → Use {archetype-1}
├─ {Another tool}? → Use {archetype-2}
└─ General {domain}? → Use {archetype-3}
```

## Examples

### Example 1: Full Documentation
```
/document-archetype-architect "
Archetype: kubernetes-operator-builder
Scope: full
"

Output:
→ Generating comprehensive documentation...

Created: kubernetes-operator-builder-guide.md

Sections included:
✓ Overview
✓ When to Use
✓ Technologies
✓ 6 Workflow Guides
✓ Constitution Rules
✓ Configuration
✓ 5 Examples
✓ Discovery Keywords
✓ Related Archetypes
✓ Troubleshooting

File: .windsurf/workflows/05-infrastructure-devops/kubernetes-operator-builder/README.md
```

### Example 2: Quick Reference
```
/document-archetype-architect "
Archetype: sql-query-crafter
Scope: quick-reference
"

Output:
→ Generating quick reference card...

# SQL Query Crafter - Quick Reference

## Usage
```bash
/scaffold-sql "Create query for {use case}"
```

## Key Rules
- ✘ No SELECT * on large tables
- ✔ Use CTEs for complex logic
- ✔ Parameterize with {{var}}

## Example
```bash
/scaffold-sql "Customer spend analysis with date range"
```

File: sql-query-crafter-quickref.md
```

### Example 3: Troubleshooting Guide
```
/document-archetype-architect "
Archetype: api-doc-generator
Scope: troubleshooting
"

Output:
→ Generating troubleshooting guide...

# API Documentation Generator - Troubleshooting

## Discovery Not Working
- Add keywords: "OpenAPI", "swagger", "API docs"
- Test: python discover-archetype.py --input "your query"

## Generated Docs Incomplete
- Check: OpenAPI spec is valid
- Verify: All endpoints have descriptions
- Run: validate-openapi.sh

## Wrong Format
- Set format in env-config: format: "openapi-3.0"
- Supported: openapi-3.0, swagger-2.0, postman

File: api-doc-generator-troubleshooting.md
```

## Error Handling

**Archetype Not Found**:
```
❌ Cannot document: Archetype "{archetype-slug}" not found

Available archetypes:
{list_archetypes_in_category}
```

**Incomplete Archetype**:
```
⚠️ Archetype is incomplete

Missing components:
- {missing_file_1}
- {missing_file_2}

Documentation will be partial.
Proceed? [Y/n]
```

## References

- **System Quick Start**: ../QUICK_START.md
- **Example Docs**: Browse .windsurf/workflows/ for README files
- **Template**: Use existing archetype docs as templates
