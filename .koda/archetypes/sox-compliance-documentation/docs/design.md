# SOX Compliance Archetype - Design Document

## Overview

The SOX Compliance archetype provides automated validation of code changes against Sarbanes-Oxley (SOX) compliance requirements. It ensures that all production changes are traceable, compliant with change management policies, and meet security quality gates.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SOX Compliance Archetype                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Scaffold   │    │     Test     │    │    Debug     │      │
│  │   Workflow   │    │   Workflow   │    │   Workflow   │      │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘      │
│         │                   │                   │               │
│         └───────────────────┼───────────────────┘               │
│                             │                                   │
│                             ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Constitution v3.0                      │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │  │
│  │  │ Hard-Stop   │  │ 10 Control  │  │ EY/SOX      │       │  │
│  │  │ Rules       │  │ Areas       │  │ Evidence    │       │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                   │
│                             ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    MCP Tool Integration                   │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │  │
│  │  │ Work Item   │  │ Veracode    │  │ Repository  │       │  │
│  │  │ Retrieval   │  │ Alerts      │  │ Discovery   │       │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Dual-Mode Operation

### Development Mode
- Post-coding validation on feature branches
- Focus on code quality and logging compliance
- SAST/Veracode NOT required
- Work item status: "In Progress" expected

### Release Mode
- Pre-release validation on release branches
- Full SOX compliance validation
- SAST/Veracode 100% coverage required
- Work item status: "Accepted" required
- Go/No-Go decision output

## Component-Based Validation Flow

```
┌─────────────────┐
│ User Story Input│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Fetch Work Item │
│ (get_multiple_  │
│  work_items)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│ Components      │ NO  │ Hard-Stop:      │
│ Field Empty?    ├────►│ Component Not   │
└────────┬────────┘     │ Tagged          │
         │ YES          └─────────────────┘
         ▼
┌─────────────────┐
│ For Each        │
│ Component:      │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌───────┐ ┌───────┐
│ Get   │ │ Get   │
│ Git   │ │Veracode│
│History│ │Alerts │
└───┬───┘ └───┬───┘
    │         │
    ▼         ▼
┌───────┐ ┌───────┐
│Logger │ │ SAST  │
│Scan   │ │Check  │
└───┬───┘ └───┬───┘
    │         │
    └────┬────┘
         │
         ▼
┌─────────────────┐
│ Generate Report │
│ (PASS/WARN/FAIL)│
└─────────────────┘
```

## 10 SOX Control Areas

| # | Control Area | Purpose |
|---|--------------|---------|
| 1 | End-to-End Traceability | Bidirectional change management compliance |
| 2 | Code Commit Integrity | Release attestation control |
| 3 | SAST Coverage | Security quality gate (100% Veracode) |
| 4 | Release Branch Hygiene | Correct scope enforcement |
| 5 | Logger Data Handling | Privacy & regulatory compliance |
| 6 | Credential Exposure Prevention | Secrets management |
| 7 | Work Item Status Validation | Release readiness |
| 8 | Security Attestation Decision | Go/No-Go rule |
| 9 | Continuous Security Operations | Weekly release discipline |
| 10 | Timely Audit Readiness | Audit SLA compliance |

## MCP Tool Integration

### Work Item Retrieval
```json
{
  "tool": "get_multiple_work_items",
  "organization": "SPTOCE",
  "project": "SPT-OCE",
  "itemIds": ["SPTOCE-104040"],
  "targetAlm": "itrack"
}
```

### Veracode Alerts
```json
{
  "tool": "get_veracode_alerts",
  "veracodeAppName": "{component_name}"
}
```

### Repository Discovery
```json
{
  "tool": "get_user_assigned_repositories"
}
```

## Evidence Collection Requirements

### Per Interface Evidence Package
1. **Logic Evidence**: Producer + Consumer code/config
2. **Flow Evidence**: Prod ≤72h or Non-Prod + parity proof
3. **Timestamp Coverage**: Local timestamp on every capture
4. **Change Integrity**: Last commit + deployment evidence
5. **Traceability**: iTrack → US → CR → CANA mapping

## Hard-Stop Rules

### Both Modes
- AOTS Ticket # present in iTrack
- Component not tagged
- Fix Version missing
- SQL queries logged
- API Request/Response logged
- Credentials exposed
- PCI/RPI/SPI logged

### Release Mode Only
- Work item status not "Accepted"
- Fix Version mismatch
- Stories incorrectly added
- SAST/Veracode coverage missing
- Out-of-scope commits

## Compliance Decision Matrix

| Mode | Result | Condition |
|------|--------|-----------|
| Development | ✅ PASS | All hard-stops clear, no logging violations |
| Development | ⚠️ WARN | Test coverage <80%, TODO/FIXME present |
| Development | 🔴 FAIL | Any hard-stop violation |
| Release | ✅ GO | All validations pass, SAST 100% |
| Release | 🔴 NO-GO | Any hard-stop violation |

## File Structure

```
sox-compliance/
├── manifest.yaml                    # Archetype metadata
├── sox-compliance-constitution.md   # Rules and guardrails (v3.0)
├── README.md                        # Archetype overview
├── changelog.md                     # Version history
├── docs/
│   └── design.md                    # This document
├── templates/
│   └── env-config.yaml              # Environment configuration
└── .windsurf/workflows/
    ├── scaffold-sox-compliance.md   # Generate checklist/evidence
    ├── test-sox-compliance.md       # Validate compliance
    ├── debug-sox-compliance.md      # Troubleshoot failures
    ├── refactor-sox-compliance.md   # Update compliance rules
    ├── compare-sox-compliance.md    # Compare approaches
    └── document-sox-compliance.md   # Generate documentation
```

## Related Archetypes

- **pull-review-risk**: PR risk analysis and governance
- **git-secret-remediation**: Secret exposure remediation
- **documentation-evangelist**: Documentation generation

## References

- [SOX Release Security Attestation Wiki](https://wiki.web.att.com/pages/viewpage.action?pageId=2524256762)
- [EY/SOX Control Evidence Collection Guidelines](sox-compliance-constitution.md#iii-ey--sox-control-evidence-collection-guidelines)
