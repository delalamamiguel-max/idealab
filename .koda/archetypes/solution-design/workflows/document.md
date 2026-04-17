---
description: Generate comprehensive documentation for Solution Intent methodology, templates, and governance
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory.

### 1. Identify Scope

Extract from $ARGUMENTS:
- Documentation type (methodology guide, template reference, constitution summary, onboarding guide)
- Target audience (Solution Architects, developers, project managers)

### 2. Load References

// turbo
Read `${ARCHETYPES_BASEDIR}/solution-design/SI_Constitution.md` for governance rules.

// turbo
Read `${ARCHETYPES_BASEDIR}/solution-design/templates/SI_Template.md` for template structure.

### 3. Generate Documentation

Based on requested type:

**Methodology Guide:**
- Impact analysis 3-pass process (Scaffold → Classify → Confidence Review)
- BFS graph traversal methodology
- Seed identification process
- Exclusion rules and TBD handling

**Template Reference:**
- Section-by-section walkthrough of SI Template
- Placeholder value descriptions
- Required vs optional sections
- Table column definitions and allowed enum values

**Constitution Summary:**
- Hard-Stop Rules quick reference card
- Mandatory Patterns checklist
- Quality Gates pass/fail criteria
- Standard notation (HS-* and M-* flags)

**Onboarding Guide:**
- Getting started with SI creation
- Required input data and where to find it
- Step-by-step SI generation walkthrough
- Common pitfalls and how to avoid them

### 4. Deliver

Output documentation in Markdown format with HTML tables following constitution formatting rules.

## Error Handling

**Missing Context**: Request specific documentation type or target audience.

## Examples

```
/document-solution-intent "Create onboarding guide for new Solution Architects"
```

```
/document-solution-intent "Generate constitution quick reference card"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/solution-design/SI_Constitution.md`
- **Template**: `${ARCHETYPES_BASEDIR}/solution-design/templates/SI_Template.md`
- **Example**: `${ARCHETYPES_BASEDIR}/solution-design/_artifacts/Example2/1371708_Solution_Intent.md`
