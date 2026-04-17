---
description: Debug Solution Intent document errors including orphan apps, missing interfaces, diagram gaps, and table formatting issues
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory.

### 1. Identify Issue

Extract from $ARGUMENTS:
- SI document with the issue
- Symptom description (rendering errors, missing data, orphan apps, broken tables)

### 2. Load Constitution

// turbo
Read `${ARCHETYPES_BASEDIR}/solution-design/SI_Constitution.md` for Hard-Stop Rules and Quality Gates.

### 3. Diagnose

Run quality gate checks against the SI document:
- **HS-MOTS**: Scan for fabricated or non-numeric MOTS IDs
- **HS-AppName**: Cross-reference app names against source data
- **HS-Orphan-App**: Check every per-app detail heading exists in Applications Summary Table
- **HS-Orphan-Int**: Check every per-app interface row exists in master Interfaces Summary Table
- **HS-ColMismatch**: Validate `<th>` count matches `<td>` count in every table
- **HS-Format**: Scan for markdown pipe-delimited tables
- **HS-Section**: Verify all 18 required sections present in order
- **M-Diagram**: Check all apps appear as Mermaid nodes, all interfaces as arrows

### 4. Apply Fix

For each identified issue:
- Fix table column mismatches by adding/removing cells
- Convert any remaining markdown tables to HTML format
- Add missing applications to summary table or remove orphan detail sections
- Add missing interfaces to master table or remove orphan sub-table rows
- Fix diagram node/arrow coverage gaps

### 5. Re-validate

Re-run all 12 quality gates to confirm fixes resolved the issues.

## Error Handling

**No SI Document**: Request path to the SI document to debug.
**Multiple Issues**: Prioritize Hard-Stop violations first, then Mandatory gaps.

## Examples

```
/debug-solution-intent "Tables not rendering correctly in Solution_Intent.md"
```

```
/debug-solution-intent "Orphan application BSSe-ACF appears in detail section but not in summary table"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/solution-design/SI_Constitution.md`
