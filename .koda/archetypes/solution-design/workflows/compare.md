---
description: Compare two Solution Intent documents, approaches, or impact analysis versions
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory.

### 1. Identify Comparison Targets

Extract from $ARGUMENTS:
- Two SI documents, versions, or approaches to compare
- Comparison focus (application coverage, interface coverage, LoE accuracy, diagram completeness)

### 2. Load Constitution

// turbo
Read `${ARCHETYPES_BASEDIR}/solution-design/SI_Constitution.md` for quality gate criteria.

### 3. Analyze Differences

Compare across dimensions:
- **Application Coverage** — apps added, removed, or changed between versions
- **Impact Type Changes** — shifts in Enhance/Test/TBD/No Change classifications
- **LoE Changes** — effort estimate differences (Easy↔Moderate↔Complex↔Difficult)
- **Interface Coverage** — interfaces added, removed, or modified
- **Diagram Coverage** — nodes/arrows present vs missing
- **Constitution Compliance** — quality gate pass/fail delta

### 4. Generate Comparison Report

Create comparison matrix with:
- Side-by-side application lists with delta highlights
- Interface coverage gaps
- LoE drift analysis
- Constitution compliance scores for each version
- Recommendation on which version to adopt or merge

## Error Handling

**Single Document**: Request second document or version for comparison.
**Incompatible Scopes**: Note scope differences and compare overlapping sections only.

## Examples

```
/compare-solution-intent "Compare app-summary-v3.md vs app-summary-v4.md for coverage changes"
```

```
/compare-solution-intent "Compare SI_draft_1.md vs SI_draft_2.md for constitution compliance"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/solution-design/SI_Constitution.md`
