# SOX Compliance Archetype

## Overview
This archetype validates that code changes are **traceable**, **compliant with change management**, and **meet security quality gates**. It operates in **two modes**:

1. **Development Mode**: Post-coding validation on feature branches
2. **Release Mode**: Pre-release validation for production deployment

## When to Use

### Development Mode
- **After coding**: Validate code changes on feature branches
- **Code review phase**: Check logging compliance and credentials
- **Before PR**: Verify iTrack fields and test coverage

### Release Mode
- **Pre-release validation**: Full compliance check before production
- **Release attestation**: Generate evidence for audit
- **Security gate checks**: SAST/Veracode coverage verification

## Mode Detection

| Condition | Mode |
|-----------|------|
| Feature branch (`feature/*`, `SPTOCE-*`) | Development |
| Release branch (`release/*`, `REL-*`) | Release |
| User specifies release version | Release |
| User says "dev" or "development" | Development |

## Key Validation Areas

### Both Modes (Hard Stops)
- ✘ **AOTS Ticket # must be EMPTY** — hard stop if populated
- ✘ **Component must be tagged** in user story
- ✘ **Fix Version must be present**
- ✘ **No SQL queries logged** (SELECT/INSERT/UPDATE/DELETE)
- ✘ **No API Request/Response logged**
- ✘ **No PCI/RPI/SPI in logs**
- ✘ **No credentials exposed** (API keys, passwords, tokens)
- ✔ Code Review in iTrack is **NOT required**

### Development Mode Only
- Work item status should be **"In Progress"**
- SAST/Veracode coverage **NOT required**
- Run unit tests if coverage unavailable
- Recommend ≥80% test coverage

### Release Mode Only
- All User Stories must be **"Accepted"** — hard stop
- SAST/Veracode 100% coverage — hard stop
- Fix Version must match release — hard stop
- Compare with previous release — flag incorrect stories
- Identify impacted services from Components field

## Workflows

| Workflow | Description |
|----------|-------------|
| `/test-sox-compliance` | Validate code in Development or Release mode |
| `/scaffold-sox-compliance` | Generate compliance checklist template |
| `/debug-sox-compliance` | Diagnose compliance failures |
| `/refactor-sox-compliance` | Fix compliance gaps |
| `/document-sox-compliance` | Generate audit documentation |
| `/compare-sox-compliance` | Compare compliance between releases |

## Quick Start

```bash
# Development Mode (feature branch)
/test-sox-compliance SPTOCE-104857

# Explicit Development Mode
/test-sox-compliance dev SPTOCE-104857

# Release Mode with version
/test-sox-compliance release 26.2.4 SPTOCE-104857 SPTOCE-104858

# Release Mode (will ask for version)
/test-sox-compliance release SPTOCE-104857
```

## Decision Rules

### Development Mode
| Result | Condition |
|--------|-----------|
| ✅ PASS | All hard-stops clear, work item "In Progress" |
| ⚠️ WARN | Test coverage below 80%, TODO/FIXME present |
| 🔴 FAIL | Any hard-stop violation |

### Release Mode
| Result | Condition |
|--------|-----------|
| ✅ GO | All checks pass, all US "Accepted", SAST 100% |
| 🔴 NO-GO | Any hard-stop violation |

## MCP Tool Integration

- `mcp0_get_veracode_alerts` — Fetch SAST coverage (Release mode)
- `mcp0_get_multiple_work_items` — Validate iTrack fields
- `mcp0_get_user_assigned_repositories` — Repository discovery

## Source
Derived from [OCE SOX - Release Security Attestation & Engineering Best Practices](https://wiki.web.att.com/pages/viewpage.action?pageId=2524256762).
