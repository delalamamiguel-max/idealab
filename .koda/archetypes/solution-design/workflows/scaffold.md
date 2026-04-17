---
description: Generate a complete Solution Intent document from epic requirements, application summary, and interface summary data
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory.

### 1. Gather Input Data

Extract from $ARGUMENTS:
- Epic/business requirements document (capabilities, scope, out-of-scope)
- Application summary data (MOTS IDs, app names, impact types, LoE)
- Interface summary data (source, target, type, description)
- Past SI references (SI numbers, titles)
- Output location for the generated SI document

### 2. Load Constitution and Template

// turbo
Read `${ARCHETYPES_BASEDIR}/solution-design/SI_Constitution.md` for Hard-Stop Rules, Mandatory Patterns, and Quality Gates.

// turbo
Read `${ARCHETYPES_BASEDIR}/solution-design/templates/SI_Template.md` for the document structure and placeholder format.

### 3. Impact Analysis — Pass 1 (Scaffold)

Identify seed applications from epic/business requirements:
- Extract named applications and MOTS IDs from input data
- Cross-reference with ITAP registry if available
- Run BFS (depth=2) from seeds using `dependency_graph_cleaned.json` if available
- Cross-reference past SIs for applications not reachable by BFS
- Deliver: all candidate applications for each capability

### 4. Impact Analysis — Pass 2 (Classify)

For each discovered application:
- Determine Impact Type: `New`, `Enhance`, `Configure`, `Test`, `TestSupport`, `No Change`, `TBD`
- Determine LoE: `Easy`, `Moderate`, `Complex`, `Difficult`, `Test`, `TestSupport (TSO)`, `Non-Development`, `TBD`
- Assign Parent Package: `{EPIC_ID} Development`, `{EPIC_ID} Non-Development`, `{EPIC_ID} No Impact`, `{EPIC_ID} TBD`
- Apply exclusion rules (hop=2 AND No Change → exclude; migration-only → exclude)

### 5. Impact Analysis — Pass 3 (Confidence Review)

Classify confidence for each application:
- **High**: BFS hop=0-1 + SI evidence
- **Medium**: BFS hop=2 or SI-only evidence
- **Low**: TBD / pending SME confirmation
- Flag TBD or low-confidence items for SME review

### 6. Generate SI Document

Using the SI Template, generate the full document with all 18 required sections:

1. **Header** — SI header table, generated date, validation expiry (+6 months)
2. **Title** — `# {EPIC_ID} {PROJECT_NAME} Solution Intent`
3. **Revision History** — initial version row
4. **Problem Statement** — derived from epic requirements
5. **Contributing Factors** — context and background
6. **Assumptions, Constraints and Dependencies** — grouped A/C/D table
7. **Applications Summary Table** — all apps with Parent Package, Impact Type, MOTS ID, Application, IT App Owner, LoE
8. **Sequencing Summary Table** — ordered execution sequence
9. **Product Team Summary Table** — team assignments
10. **Interfaces Summary Table** — all interfaces with Source, Target, Name, Type, Description, Impact Type
11. **Requirements Summary Table** — NFRs
12. **End to End Solution** — narrative with per-scenario subsections
13. **Context Diagram** — Mermaid flowchart with all app nodes, interface arrows, legend, and standard color palette
14. **Development** — per-app detail blocks (Tagged Values + Interfaces)
15. **Non Development** — per-app detail blocks
16. **No Impact** — per-app detail blocks (if applicable)
17. **TBD** — applications pending SME confirmation
18. **Issues Log** — tracking table

**All tables MUST use HTML format** with `border="1"`, `border-collapse: collapse`, and `border: 1px solid black; padding: 8px` on all cells.

### 7. Validate Against Quality Gates

Run all 12 quality gates from the constitution:
- QG-1: All 18 sections present
- QG-2: All tables HTML format, zero column mismatches
- QG-3: Zero orphan applications
- QG-4: Zero orphan interfaces
- QG-5: Zero fabricated MOTS IDs
- QG-6: Zero fabricated app names
- QG-7: 100% diagram node coverage
- QG-8: ≥90% diagram arrow coverage
- QG-9: All Impact Types from allowed enum
- QG-10: All LoE values from allowed enum
- QG-11: All exclusions documented
- QG-12: All TBD items have SME note

### 8. Deliver

Save the generated SI document to the user-specified output location.

## Error Handling

**Missing Input Data**: Request epic requirements, application summary, or interface summary files.
**No ITAP Registry**: Proceed with SI-sourced MOTS IDs only; note in Assumptions.
**No Dependency Graph**: Proceed with past SI evidence only; note in Constraints.

## Examples

```
/scaffold-solution-intent "Generate SI for Installment Plan Exception Handling using app-summary-v4.md and interface-summary-v4.md"
```

```
/scaffold-solution-intent "Create Solution Intent from epic requirements in epic_1371708.md with past SIs in past_solution_intents/"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/solution-design/SI_Constitution.md`
- **Template**: `${ARCHETYPES_BASEDIR}/solution-design/templates/SI_Template.md`
- **Example**: `${ARCHETYPES_BASEDIR}/solution-design/_artifacts/Example2/1371708_Solution_Intent.md`
