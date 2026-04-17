# XFlow Orchestrator — Feature Backlog

**Created**: 2026-02-25
**Source**: Production config analysis of 15,284 configs — items deferred from proposed-changes-from-production-analysis.md

---

## Backlog Items

### BL-1: `correlationId` Auto-Generation
- **Source**: Section 2.1 (removed by user)
- **Finding**: Present in 99.2% of configs (15,155 / 15,284). Follows pattern `{appId}_{srcId}`.
- **Proposed**: Add as mandatory field, auto-generate from `{appId}_{srcId}`.
- **Priority**: Medium
- **Status**: Deferred

### BL-2: `trimSpacesInd` at Target Level
- **Source**: Section 4.3
- **Finding**: 1,221 configs (8%) place `trimSpacesInd` directly on the target (not inside `globalTransformation`).
- **Proposed**: Document both placements in constitution.
- **Reason deferred**: Not required as Global Transformation is used.
- **Priority**: Low
- **Status**: Deferred

### BL-3: `processOneFileInd`
- **Source**: Section 4.4
- **Finding**: 67 configs use this to control single-file processing mode.
- **Proposed**: Add to target field reference.
- **Priority**: Low
- **Status**: Deferred

### BL-4: `postIngestion` — Post-Processing & Publish
- **Source**: Section 4.6
- **Finding**: 25 configs use advanced post-processing with publish capabilities including HTTP targets and variable substitution.
- **Proposed**: Add to field reference as advanced optional config.
- **Priority**: Low
- **Status**: Deferred

### BL-5: `mappingTable` — Lookup/Mapping Table Joins
- **Source**: Section 4.7
- **Finding**: 8 configs use lookup/mapping table joins during ingestion.
- **Proposed**: Add to field reference as optional advanced feature.
- **Priority**: Low
- **Status**: Deferred

### BL-6: Target Schema Properties (`pii`, `pk`, `srcColumnName`, `encrypted`)
- **Source**: Section 4.8
- **Finding**: Production schemas use `pk`, `pii`, `encrypted`, `srcColumnName` for classification and column mapping.
- **Proposed**: Add all four schema column properties to field reference.
- **Priority**: Medium
- **Status**: Deferred

### BL-7: `JSON` and `text` as Target Formats
- **Source**: Section 5.3
- **Finding**: 6 configs use `JSON`/`json` target format, 2 use `text`.
- **Proposed**: Add to allowed `targetFileFormat` values.
- **Priority**: Low
- **Status**: Deferred

### BL-8: Source Schema `jsonMapping` Field
- **Source**: Section 5.4
- **Finding**: Some source schemas include `jsonMapping` for JSON flattening.
- **Proposed**: Add to schema field reference for JSON source support.
- **Priority**: Low
- **Status**: Deferred

### BL-9: `writeOneFileInd` Scaffold Prompt
- **Source**: Section 6.2
- **Finding**: 3,149 configs (20.6%) use this for file coalescing.
- **Proposed**: Ask during scaffold for file/httpFile sources.
- **Priority**: Medium
- **Status**: Deferred

### BL-10: CSV Delimiter Presets
- **Source**: Section 6.4
- **Finding**: 25+ unique delimiter patterns in production (pipe, unit separator, comma, etc.).
- **Proposed**: Add common delimiter presets to scaffold wizard.
- **Priority**: Low
- **Status**: Deferred

### BL-11: Root-Level Fields (`supportMailingList`, `reconciliationInd`, `lastScalingAt`)
- **Source**: Section 7.1–7.3
- **Finding**: Rare fields — 11, 4, and 76 configs respectively. `lastScalingAt` is likely system-managed.
- **Proposed**: Add to field reference as optional/system-managed fields.
- **Priority**: Low
- **Status**: Deferred

### BL-12: JDBC `auditFileConfig`
- **Source**: Section 3.6 (removed by user)
- **Finding**: 60 configs use JDBC audit trail with `targetLocation`, `targetNameFormat`, `auditFileContentConfiguration`.
- **Proposed**: Add to JDBC field reference as optional advanced config.
- **Priority**: Low
- **Status**: Deferred
