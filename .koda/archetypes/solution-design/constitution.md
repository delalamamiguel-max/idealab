# Constitution: Solution Intent (SI)

## Purpose
Ensure comprehensive, accurate, and governed production of Solution Intent documents that enable technical teams to build design documents from a validated high-level solution design — covering application impact analysis, interface mapping, context diagrams, and end-to-end solution narratives with full traceability to ITAP, past SIs, and dependency graph evidence.

---

### I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** or correct any SI output that violates these rules:

✘ No fabricated MOTS IDs — every MOTS ID must come from ITAP or a verified source artifact  
✘ No fabricated application names — every name must match the ITAP registry or a verified past SI  
✘ No fabricated interface connections — every Source→Target relationship must be evidenced by BFS graph data, past SI documentation, or domain KB confirmation  
✘ No orphan applications — every application in per-app detail sections must appear in the Applications Summary Table  
✘ No orphan interfaces — every interface in per-app Interfaces sub-tables must appear in the master Interfaces Summary Table  
✘ No table column mismatches — `<td>` count in every data row must equal the `<th>` count in the header  
✘ No markdown pipe-delimited tables — only HTML `<table>` format with full grid borders is permitted  
✘ No missing required sections — all 18 mandatory sections must be present in the prescribed order

---

### II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify these patterns:

✔ Use HTML tables with `border="1"`, `border-collapse: collapse`, and `border: 1px solid black; padding: 8px` on all cells  
✔ Follow the SI Template (`solution-design/templates/SI_Template.md`) for document structure and placeholder format  
✔ Include `SI Generated` date (MM/DD/YY) and ATTENTION validation-expiry date (SI Generated + 6 months)  
✔ Include Revision History table with columns: Author/ATTUID, Revision Date, Version, Revision Description  
✔ Populate Applications Summary Table with columns: Parent Package, Impact Type, MOTS ID, Application, IT App Owner, LoE  
✔ Use only allowed Impact Type values: `New`, `Enhance`, `Configure`, `Test`, `TestSupport`, `No Change`, `TBD`  
✔ Use only allowed LoE values: `Easy`, `Moderate`, `Complex`, `Difficult`, `Test`, `TestSupport (TSO)`, `Non-Development`, `TBD`  
✔ Group applications by Parent Package: Development → Non-Development → No Impact → TBD  
✔ Populate Interfaces Summary Table with columns: Source, Target, Name, Type, Description, Impact Type  
✔ Use only allowed Interface Type values: `API`, `Event`, `Batch`, `mS`, `DirectLink`  
✔ Include a Mermaid `flowchart TB` context diagram with Impact Legend, Line Legend, all application nodes, and styled connections  
✔ Apply standard diagram color palette: impactNew (#00b300), impactEnhance (#00bcd4), impactConfigure (#ff9800), impactTest (#ffc107), impactRetire (#f44336), impactNoChange (#9e9e9e)  
✔ Use correct arrow styles in diagrams: `-->` for Enhance, `-.->` for Test, `-.-` for Configure  
✔ Include per-application detail blocks with Tagged Values table (Application Name, App Lifestyle, App Lifestyle Status, Impact Type, LoE) and Interfaces sub-table for each app that is a source or target  
✔ Populate Assumptions, Constraints and Dependencies table grouped as A1…An, C1…Cn, D1…Dn with group header rows  
✔ Document all exclusions (e.g., hop=2 AND No Change, migration-only scope) in the Assumptions section  
✔ Flag all TBD items with a note explaining what SME input is needed

---

### III. Preferred Patterns (Recommended)

The LLM **should adopt** these patterns unless user overrides:

➜ Sort applications within each Parent Package group by LoE descending (Complex → Difficult → Moderate → Easy → Test → TBD)  
➜ Include diagram node format: `AppID["Name<br/><small>MOTS_ID · Impact · LoE</small>"]:::impactStyle`  
➜ Organize diagram nodes into subgraph layers by functional domain (e.g., Billing, Orchestration, Order Management)  
➜ Include arrow labels with interface name and type: `|"Name<br/>(Type)"|`  
➜ Include interface Description that specifies (a) what data/action flows and (b) which capabilities (Cxx) are involved  
➜ Reference past SI numbers and titles in the Dependencies section  
➜ Include a Sequencing Summary Table with columns: Seq #, Application, Activity/Action, Description (use "ZZZ" for apps not sequenced)  
➜ Include a Product Team Summary Table with columns: Product Team, Notes, MOTS ID, Application, Application LoE  
➜ Include a Requirements Summary Table with columns: NFR, Name, Notes, Apps  
➜ Provide End-to-End Solution narrative with per-scenario subsections, Reporting and Audit, and Future Scope Considerations  
➜ Cross-reference ITAP application registry for MOTS ID and name validation  
➜ Use dependency graph BFS evidence and past SI app tables as dual-source verification

---

### IV. Impact Analysis Process

**Multi-Pass Methodology:**

1. **Pass 1 — Scaffold (Application Discovery)**
   - Identify seed applications from epic/business requirements
   - Run BFS (depth=2) from seeds using `dependency_graph_cleaned.json`
   - Cross-reference past SIs for applications not reachable by BFS
   - Deliver: all candidate applications for each capability

2. **Pass 2 — Refactor (Impact Classification)**
   - For each discovered application, determine Impact Type and LoE
   - Classify using SI evidence, domain KB, and BFS hop distance
   - Apply exclusion rules (hop=2 AND No Change → exclude; migration-only → exclude)
   - Deliver: Impact Type + LoE for every application

3. **Pass 3 — Confidence Review**
   - Classify confidence: **High** (BFS hop=0-1 + SI evidence), **Medium** (BFS hop=2 or SI-only), **Low** (TBD / pending SME)
   - Flag TBD or low-confidence items for SME review
   - Deliver: final validated application and interface lists

---

### V. Review & Reporting Instructions

**Scope:**
- Validate all applications against ITAP registry (MOTS IDs + names)
- Verify all interfaces have Source and Target in the Applications Summary Table
- Confirm diagram coverage: all apps as nodes, all Enhance/Test interfaces as arrows
- Check table formatting: HTML tables, column count consistency, correct border styles
- Validate enum values for Impact Type, LoE, and Interface Type

**Output Requirements:**
- Generate complete SI document following the SI Template structure with all 18 required sections
- All tables rendered in HTML format with full grid borders
- Context diagram in Mermaid with complete application coverage and styled connections
- Per-application detail sections with Tagged Values and Interfaces sub-tables
- Exclusions documented in Assumptions; TBD items annotated with SME action needed

**Standard Notation:**
- **Hard-Stop Flags:** HS-MOTS (fabricated MOTS ID), HS-AppName (fabricated app name), HS-Interface (fabricated connection), HS-Orphan-App (app not in summary), HS-Orphan-Int (interface not in master table), HS-ColMismatch (table column mismatch), HS-Format (markdown table used), HS-Section (missing required section)
- **Mandatory Gaps:** M-Template (template not followed), M-ImpactType (invalid impact type), M-LoE (invalid LoE), M-Diagram (missing diagram element), M-TaggedValues (missing tagged values table), M-ACD (missing assumption/constraint/dependency), M-Exclusion (undocumented exclusion), M-TBD (TBD without SME note)

**Source Data Requirements:**

| Data Source | Purpose | Required? |
|-------------|---------|-----------|
| Epic/business requirements document | Capability scope definition | **Required** |
| Past Solution Intents (`past_solution_intents/`) | Reference for app names, LoE, interfaces | **Required** |
| `dependency_graph_cleaned.json` | BFS graph traversal for app discovery | **Required** |
| ITAP application registry (`applications_itap.json`) | Validate MOTS IDs and application names | **Preferred** |
| Domain Knowledge Base (e.g., platform summaries) | Microservice-level interface confirmation | **Preferred** |
| `impacted_relationships.json` | Graph edge evidence for interface validation | **Preferred** |

---

### VI. Quality Gates

| Gate | Check | Pass Criteria |
|------|-------|---------------|
| QG-1 | All 18 required sections present in correct order | 100% sections present |
| QG-2 | All tables use HTML format with correct borders | Zero markdown tables; zero column mismatches |
| QG-3 | Every app in detail sections exists in summary table | Zero orphan applications |
| QG-4 | Every interface in per-app tables exists in master table | Zero orphan interfaces |
| QG-5 | All MOTS IDs are numeric and from verified sources | Zero fabricated IDs |
| QG-6 | All application names match ITAP or verified SI sources | Zero fabricated names |
| QG-7 | All applications appear as nodes in the context diagram | 100% coverage |
| QG-8 | All Enhance/Test interfaces have diagram arrows | ≥90% coverage |
| QG-9 | All Impact Type values are from the allowed enum | Zero invalid values |
| QG-10 | All LoE values are from the allowed enum | Zero invalid values |
| QG-11 | All excluded apps documented in Assumptions | 100% documented |
| QG-12 | All TBD items have SME action note | 100% documented |

---

Version: 1.0.0  
Last Updated: 2026-03-13
