# SOX Compliance Archetype Changelog

All notable changes to this archetype will be documented in this file.

## [3.0.0] - 2026-02-19

### Added
- **10 SOX Control Areas** with comprehensive validation steps:
  1. End-to-End Traceability (Change Management Compliance)
  2. Code Commit Integrity Checks (Release Attestation Control)
  3. SAST Coverage (Security Quality Gate)
  4. Release Branch Hygiene (Correct Scope Enforcement)
  5. Logger Data Handling (Privacy & Regulatory Compliance)
  6. Credential Exposure Prevention (Secrets Management)
  7. User Story / Work Item Status Validation (Release Readiness)
  8. Security Attestation Decision (Go / No-Go Rule)
  9. Continuous Security Operations (Weekly Release Discipline)
  10. Timely Audit Readiness & Closure (Audit SLA Rule)

- **Component-Based Validation Workflow**: After fetching work item, validates each component via git history
- **EY/SOX Control Evidence Collection Guidelines**: Comprehensive audit-ready evidence requirements
- **Bidirectional Traceability**: Commits ↔ iTrack ↔ CR/CANA mapping
- **Audit SLA Rules**: Evidence package checklist and timeline requirements
- **Enhanced MCP Tool Integration**: Component validation flow with `get_repo_latest_changes`

### Changed
- Restructured constitution to align with SOX audit requirements
- Enhanced workflow execution guide with component-based validation
- Updated MCP tool documentation with detailed examples

## [2.1.0] - 2026-02-17

### Changed
- Development Mode report refinements:
  - Removed raw MCP response JSON from report
  - Removed SAST/Veracode section (not required in Dev mode)
  - Added test execution in local workspace for actual coverage
  - Implementation status now optional (warning only if incomplete)

## [2.0.0] - 2026-02-17

### Added
- Dual-mode support (Development/Release)
- SQL/API logging checks
- MCP tools integration for Veracode

### Changed
- AOTS CR/CANA requirement changed to hard stop if present
- Removed code review requirement

## [1.0.0] - 2025-02-17

### Added
- Initial version based on wiki content (pageId: 2524256762)
- Basic SOX compliance validation rules
- Release attestation framework
