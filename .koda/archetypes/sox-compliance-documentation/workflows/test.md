---
description: Validate code changes against SOX compliance rules in Development or Release mode (SOX Compliance)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Set ARCHETYPES_BASEDIR [⋯]
 
**SUCCESS CRITERIA**:
- Search for directory: "00-core-orchestration"
- Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory
 
**HALT IF**:
- Directory "00-core-orchestration" is not found
- `${ARCHETYPES_BASEDIR}` is not set (workflow will halt if this variable is not present in the environment)
 
// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Environment Setup
// turbo
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype sox-compliance --json` and parse for ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- Read `${ARCHETYPES_BASEDIR}/sox-compliance/sox-compliance-constitution.md` for validation rules
- Load `${ARCHETYPES_BASEDIR}/sox-compliance/templates/env-config.yaml` for mode-specific settings

### 3. Detect Mode and Parse Input
Extract from $ARGUMENTS: ticket IDs, branch name, release version (if specified).

**Mode Detection:**
- If branch is `feature/*`, `SPTOCE-*`, `bugfix/*` → **Development Mode**
- If branch is `release/*`, `REL-*`, or user specifies release version → **Release Mode**
- If user says "development", "dev" → **Development Mode**
- If user says "release", "production", or provides release version → **Release Mode**

**If mode unclear**: Ask user to specify release version or confirm development mode.

### 4. Repository Discovery
- Check if repository is available in workspace
- If NOT available:
  - Extract component name from user story
  - Use `mcp0_get_user_assigned_repositories` to find repository
  - Derive branch name from Fix Version in user story

### 5. Validate iTrack Fields (Both Modes)
For each user story:
- ✔ Verify **Component** is correctly tagged
- ✔ Verify **Fix Version** is present
- ✔ Verify **AOTS Ticket #** field is **EMPTY** — **HARD STOP if populated**
- ✘ Skip Code Review field check (NOT required)

### 6. Validate Logging Compliance (Both Modes)
Scan code changes for logging violations:
- ✘ **SQL queries logged**: Search for SELECT/INSERT/UPDATE/DELETE in logger statements — **HARD STOP**
- ✘ **API Request logged**: Search for request payload logging — **HARD STOP**
- ✘ **API Response logged**: Search for response payload logging — **HARD STOP**
- ✘ **PCI/RPI/SPI logged**: Search for sensitive data patterns — **HARD STOP**

**Acceptable logging**: Correlation IDs, timestamps, status codes, error messages (without payloads)

### 7. Validate Credential Exposure (Both Modes)
- Scan for exposed API keys, passwords, tokens, certificates
- Check configuration files for hardcoded secrets
- **HARD STOP** if any credentials found

---

## Development Mode Steps (Skip if Release Mode)

### 8D. Validate Work Item Status (Development)
- Verify User Story is in **"In Progress"** or **"Dev Complete"** status (expected)
- Flag if status is "New" or "Blocked" (warning, not hard stop)

### 9D. Validate Test Coverage (Development)
**If repository is in local workspace:**
- Run unit tests with coverage: `./mvnw test jacoco:report` or `./gradlew test jacocoTestReport`
- Parse JaCoCo coverage report for actual percentage
- Report actual coverage for new code

**If NOT in local workspace:**
- Report "Coverage unavailable - tests not executed"
- Recommend running tests locally

### 10D. Check Implementation Status (Development) - OPTIONAL
- Search for execution summary file: `docs/{TICKET-ID}/*-execution-summary.md`
- **If execution summary exists:**
  - Parse implementation status from summary
  - **If NOT fully implemented** (phases incomplete, tests not created):
    - Display as ⚠️ **WARNING** (not hard-stop)
    - List incomplete phases/tests
- **If execution summary does NOT exist:**
  - Skip this section entirely (do not include in report)

### 11D. Generate Development Report
Generate **Development Compliance Report** with:

**MUST INCLUDE:**
- ✅ PASS / ⚠️ WARN / 🔴 FAIL status
- iTrack field validation results (Component, Fix Version, AOTS Ticket #, Status)
- Hard-stop validation results
- Logging compliance scan results
- Credential exposure scan results
- **Actual test coverage** (if local workspace — run tests)
- Compliance decision
- Remediation actions

**MUST EXCLUDE:**
- ✘ Raw MCP response JSON data
- ✘ SAST/Veracode status section

**OPTIONAL (show as warning if conditions met):**
- ⚠️ Implementation status summary (only if execution summary exists AND incomplete)

---

## Release Mode Steps (Skip if Development Mode)

### 8R. Ask for Release Version (Release)
If release version not provided in $ARGUMENTS:
- Ask user: "Please specify the release version (e.g., 26.2.4)"
- Wait for response before proceeding

### 9R. Fetch Veracode Coverage (Release)
- Extract component name from user story
- Call `mcp0_get_veracode_alerts` with component name
- Verify 100% SAST coverage — **HARD STOP if not met**
- Verify no high-severity findings — **HARD STOP if found**

### 10R. Validate Work Item Status (Release)
- Verify all User Stories (US) are **"Accepted"** — **HARD STOP if not**
- Verify all Non-US items (bugs, tasks) are **"Test Complete"**

### 11R. Validate Fix Version (Release)
- Verify each user story Fix Version matches target release
- Verify release date falls within Fix Version date range
- **HARD STOP** if Fix Version mismatch

### 12R. Identify Impacted Services (Release)
- Extract **Components** field from all user stories in release
- List all impacted microservices

### 13R. Compare with Previous Release (Release)
- Get previous release version for each component
- Compare commits/stories between releases
- Identify stories that:
  - Should NOT be in current release (wrong Fix Version)
  - Are missing from current release (expected but not present)
- **HARD STOP** if stories incorrectly added to release

### 14R. Validate Release Branch Hygiene (Release)
- Identify out-of-scope or future release commits
- Flag commits not matching release scope
- **HARD STOP** if out-of-scope commits found

### 15R. Generate Go/No-Go Decision (Release)
Based on validation results:
- ✅ **GO**: All checks pass
- 🔴 **NO-GO**: Any hard-stop rule violated

### 16R. Generate Release Report
Generate **Release Compliance Report** with:
- Go/No-Go decision with rationale
- Veracode coverage status
- Work item status validation
- Fix Version validation
- Impacted services list
- Release comparison results
- Logging compliance results
- Secrets scan results
- Failures with remediation required

---

## Error Handling
**AOTS Ticket Present**: Hard stop — must be removed from iTrack.
**SQL/API Logging**: Hard stop — must remove logging statements.
**Secrets Detected**: Immediate escalation and remediation.
**SAST Failures (Release)**: Block release until remediated.
**Status Not Accepted (Release)**: Block until all US accepted.

## Examples
**Example 1**: `/test-sox-compliance SPTOCE-104857` - Detects feature branch → Development Mode validation
**Example 2**: `/test-sox-compliance release 26.2.4 SPTOCE-104857 SPTOCE-104858` - Release Mode with specified version
**Example 3**: `/test-sox-compliance dev SPTOCE-12345` - Explicit Development Mode

## References
- SOX Compliance Constitution: `${ARCHETYPES_BASEDIR}/sox-compliance/sox-compliance-constitution.md`
- Environment Config: `${ARCHETYPES_BASEDIR}/sox-compliance/templates/env-config.yaml`
- Wiki: https://wiki.web.att.com/pages/viewpage.action?pageId=2524256762
