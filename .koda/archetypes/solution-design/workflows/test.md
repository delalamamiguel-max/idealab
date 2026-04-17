---
description: Validate a Solution Intent document against constitution rules and quality gates
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory.

### 1. Identify Test Scope

Extract from $ARGUMENTS:
- SI document to validate
- Test focus (full, structure-only, data-integrity, diagram-only, formatting-only)

### 2. Load Constitution

// turbo
Read `${ARCHETYPES_BASEDIR}/solution-design/SI_Constitution.md` for Hard-Stop Rules, Mandatory Patterns, and Quality Gates.

### 3. Run Quality Gate Tests

Execute all 12 quality gates:

**Hard-Stop Tests:**
- QG-1: Verify all 18 required sections present in correct order
- QG-2: Verify all tables use HTML format with correct borders; zero column mismatches
- QG-3: Verify every app in detail sections exists in Applications Summary Table
- QG-4: Verify every interface in per-app tables exists in master Interfaces Summary Table
- QG-5: Verify all MOTS IDs are numeric and from verified sources
- QG-6: Verify all application names match ITAP or verified SI sources

**Mandatory Tests:**
- QG-7: Verify all applications appear as nodes in context diagram
- QG-8: Verify all Enhance/Test interfaces have corresponding diagram arrows (≥90%)
- QG-9: Verify all Impact Type values are from the allowed enum
- QG-10: Verify all LoE values are from the allowed enum
- QG-11: Verify all excluded apps are documented in Assumptions
- QG-12: Verify all TBD items have SME action notes

**Standard Notation Check:**
- Flag any HS-* violations (HS-MOTS, HS-AppName, HS-Interface, HS-Orphan-App, HS-Orphan-Int, HS-ColMismatch, HS-Format, HS-Section)
- Flag any M-* gaps (M-Template, M-ImpactType, M-LoE, M-Diagram, M-TaggedValues, M-ACD, M-Exclusion, M-TBD)

### 4. Generate Test Report

Report with:
- Pass/Fail status for each quality gate
- List of Hard-Stop violations with line numbers
- List of Mandatory gaps with line numbers
- Overall constitution compliance score
- Remediation recommendations for each failure

## Error Handling

**No SI Document**: Request path to the SI document to validate.
**Partial Document**: Test only the sections that exist; report missing sections as QG-1 failure.

## Examples

```
/test-solution-intent "Validate 1371708_Solution_Intent.md against constitution"
```

```
/test-solution-intent "Run formatting-only tests on ESPR_SI.md"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/solution-design/SI_Constitution.md`
