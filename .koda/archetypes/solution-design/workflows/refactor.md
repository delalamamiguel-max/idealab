---
description: Refactor an existing Solution Intent document to improve constitution compliance, coverage, and accuracy
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory.

### 1. Assess Current State

Extract from $ARGUMENTS:
- SI document to refactor
- Refactoring focus (coverage gaps, LoE accuracy, new data integration, formatting)

// turbo
Read `${ARCHETYPES_BASEDIR}/solution-design/SI_Constitution.md` for standards.

### 2. Identify Improvements

Audit the SI document against constitution:
- **Coverage**: Applications or interfaces missing from summary tables
- **Accuracy**: LoE or Impact Type values that need updating based on new evidence
- **Formatting**: Tables using markdown instead of HTML, column mismatches
- **Diagram**: Missing nodes or arrows in Mermaid context diagram
- **New Data**: Integrate updated application summary or interface summary files
- **Exclusions**: Undocumented exclusions needing Assumptions entries
- **TBD Resolution**: TBD items that can now be resolved with SME input

### 3. Apply Refactoring

For each improvement:
- Add missing applications to summary table and per-app detail sections
- Update Impact Type and LoE values with new evidence
- Convert markdown tables to HTML format
- Update Mermaid diagram with new/changed nodes and arrows
- Merge new application summary or interface summary data
- Document newly resolved TBD items

### 4. Validate

Run all 12 quality gates to confirm refactored document passes.

## Error Handling

**No SI Document**: Request path to the SI document to refactor.
**Conflicting Data**: Flag conflicts between old SI data and new source data for user resolution.

## Examples

```
/refactor-solution-intent "Update SI with new app-summary-v4.1 data and fix markdown tables"
```

```
/refactor-solution-intent "Add 10 new applications from target list reconciliation to existing SI"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/solution-design/SI_Constitution.md`
- **Template**: `${ARCHETYPES_BASEDIR}/solution-design/templates/SI_Template.md`
