---
description: Generate documentation for impact analysis methodology and reports (Impact Analyzer)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Identify Documentation Scope

Extract from $ARGUMENTS:
- What to document (methodology, report, configuration)
- Target audience
- Documentation depth

### 2. Generate Documentation

**For Methodology Documentation:**
- Multi-layer scanning approach
- Risk assessment criteria
- Estimation heuristics
- Report structure

**For Report Documentation:**
- Executive summary for stakeholders
- Technical details for developers
- Action items for operations

**For Configuration Documentation:**
- Scan scope settings
- Risk rules explanation
- Customization guide

### 3. Assemble Documentation Package

Deliver:
- `docs/METHODOLOGY.md` - How impact analysis works
- `docs/REPORT_GUIDE.md` - How to read impact reports
- `docs/CONFIGURATION.md` - How to customize analysis

## Error Handling

**Missing Context**: Request specific analysis or configuration to document.

## Examples

### Example 1: Stakeholder Summary

```
/document-impact-analyzer "
Create executive summary of impact analysis methodology.
Audience: Project managers and stakeholders
Focus: Risk levels and decision criteria
"
```

### Example 2: Technical Guide

```
/document-impact-analyzer "
Document how to configure impact analyzer for new project.
Include scan scope, risk rules, and estimation settings.
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/impact-analyzer/impact-analyzer-constitution.md`
- **Documentation Standards**: Delegate to documentation-evangelist for prose quality
