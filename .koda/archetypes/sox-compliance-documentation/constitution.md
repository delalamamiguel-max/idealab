# SOX Compliance - Release Security Attestation Constitution

## Purpose

Validate that code changes are **traceable**, **compliant with change management**, and **meet security quality gates**. This archetype operates in **two modes**:

1. **Development Mode**: Post-coding validation on feature branches
2. **Release Mode**: Pre-release validation on release branches for production deployment

---

## Mode Detection

| Condition | Mode |
|-----------|------|
| Analysis on **feature branch** (e.g., `feature/*`, `SPTOCE-*`, `*-*`) | **Development** |
| Analysis on **release branch** (e.g., `release/*`, `REL-*`) | **Release** |
| User specifies "release" or release version in prompt | **Release** |
| User specifies "development" or "dev" in prompt | **Development** |

**If mode is unclear**: Ask user to specify the release version or confirm development mode.

---

## User Story Input

**ALWAYS prompt the user for the User Story number** before starting validation.

### Prompt Template
```
Please provide the User Story number(s) to validate (e.g., SPTOCE-104040):
```

### Input Format
- Single story: `SPTOCE-104040`
- Multiple stories: `SPTOCE-104040, SPTOCE-104041, SPTOCE-104042`

### Validation
- User story number must match pattern: `{PROJECT}-{NUMBER}` (e.g., `SPTOCE-104040`)
- If no user story provided, prompt user before proceeding
- If invalid format, request correction

### After User Story Input
1. Extract user story number(s) from user input
2. Call `get_multiple_work_items` with:
   ```json
   {
     "organization": "{PROJECT}",
     "project": "{PROJECT_KEY}",
     "itemIds": ["{USER_STORY_NUMBER}"],
     "targetAlm": "itrack"
   }
   ```
3. **Validate work item response has Components and Fix Version**
4. If Components is NOT empty, proceed with component-based validation
5. If Components is empty, flag as hard-stop violation

---

## Component-Based Validation Workflow

**After fetching work item, if Components field is NOT empty:**

### Step 1: Extract Components
Parse the `work_item_tags` or component fields from the work item response to identify all affected repositories/components.

### Step 2: Get Git History for Each Component
For each component identified:
1. Use `get_repo_latest_changes` or `get_user_assigned_repositories` to locate the repository
2. Fetch recent commits related to the user story
3. Extract commit history for compliance validation

### Step 3: Validate SOX Compliance for Each Component
Execute the following validations against the component's codebase:

| Validation | Description | Tool/Method |
|------------|-------------|-------------|
| Logger Compliance | Scan for prohibited logging patterns | grep/code search |
| Credential Exposure | Scan for exposed secrets | grep/code search |
| Test Coverage | Run unit tests and measure coverage | mvnw test / gradlew test |
| SAST Coverage | Verify Veracode scan status | get_veracode_alerts |
| Commit Traceability | Verify commits reference iTrack tickets | git log analysis |

---

## I. Hard-Stop Rules (Non-Negotiable)

### A. Hard-Stop Rules — BOTH MODES
The LLM must **fail validation** if:

- ✘ **AOTS Ticket # is present in iTrack**: The "AOTS Ticket #" field must be **empty**. Any value is a hard stop.
- ✘ **Component not tagged**: User story must have the correct component specified in iTrack.
- ✘ **Fix Version missing**: User story must have a Fix Version assigned.
- ✘ **SQL queries logged**: Logger statements must NOT log raw SQL queries.
- ✘ **API Request logged**: Logger statements must NOT log full API request payloads.
- ✘ **API Response logged**: Logger statements must NOT log full API response payloads.
- ✘ **Credentials exposed**: No API keys, passwords, tokens, certificates in code, config, or logs.
- ✘ **PCI/RPI/SPI logged**: Loggers must NOT record Payment Card, Regulated Personal, or Sensitive Personal Information.

### B. Hard-Stop Rules — RELEASE MODE ONLY
The LLM must **fail validation** in Release Mode if:

- ✘ **Work item status not Accepted**: All User Stories (US) must be in **"Accepted"** status.
- ✘ **Fix Version mismatch**: User story Fix Version must match the target release.
- ✘ **Stories incorrectly added**: Compare release with previous release; any story not belonging to current release is a hard stop.
- ✘ **SAST/Veracode coverage missing**: 100% SAST coverage required.
- ✘ **Out-of-scope commits**: Release branch must only contain commits for current release scope.

### C. Validation Rules — DEVELOPMENT MODE ONLY
In Development Mode:

- ✔ Work item status should be **"In Progress"** (acceptable, not hard stop if different).
- ✔ SAST/Veracode coverage is **NOT required**.
- ✔ If test coverage not available, **run unit tests** and identify coverage percentage.
- ✔ Feature branch analysis only (not release branch hygiene).

---

## II. SOX Compliance Controls (10 Control Areas)

### Control 1: End-to-End Traceability (Change Management Compliance)

**Goal:** Every production change must be fully traceable as part of release attestation.

#### Traceability Model (Bidirectional)
We enforce traceability in both directions to ensure full audit coverage:

**Forward Traceability:**
```
Commits → iTrack Ticket → AOTS Change Request (CR / CANA)
```

**Reverse Traceability:**
```
AOTS CR / Release Scope → iTrack Tickets → Commits
```

#### How We Ensure It
- All production-bound commits must reference a valid iTrack ticket (via commit message/tagging convention)
- Every iTrack ticket included in a release must map back to an approved AOTS CR (CANA)
- We strictly monitor release-level commits using code commit integrity checks to ensure the release contains only intended, authorized work

#### Validation Steps
1. Parse commit messages for iTrack ticket references
2. Verify each ticket has valid Fix Version
3. Confirm ticket maps to approved CR/CANA
4. Flag any commits without proper traceability

---

### Control 2: Code Commit Integrity Checks (Release Attestation Control)

**Goal:** Ensure the release branch contains only authorized changes for the specific release, with correct CR and ticket linkage.

#### Step A — Identify New Commits
Extract all new commits planned for deployment by comparing:
- The upcoming release branch vs.
- The latest production release baseline

This isolates only the delta that is intended for production.

#### Step B — Trace Change Requests from Commits
For each new commit:
- Parse the commit message to extract the referenced iTrack ticket

#### Step C — Validate Ticket & CR Eligibility
For each referenced iTrack ticket, validate:
- Fix Version matches the current release
- Status meets the required state (Accepted for US, Test Complete for bugs/tasks)
- The ticket maps to the correct AOTS CR approved for the release scope
- The CR is valid (not invalid/closed/out-of-scope)

#### Step D — Flag and Stop on Inconsistencies
Commits are flagged for review (and must be remediated) if we detect:
- Missing iTrack reference in the commit
- Mismatch between commit tagging and release tagging
- Reference to invalid/closed/out-of-scope CR
- Ticket fix version does not match the release
- Any scenario suggesting the commit does not belong in the release

**This process prevents "silent drift" into release branches and provides a clear audit trail for every deployed change.**

---

### Control 3: SAST Coverage (Security Quality Gate)

**Goal:** Ensure every component included in the release has completed Static Application Security Testing (SAST).

#### Standard
- 100% SAST coverage is required for all components planned for release
- Results must be available and reviewed in Veracode for the specific release scope

#### Enforcement
Any component without a passing SAST report must be:
- Remediated before release, OR
- Excluded from the release scope

#### Validation
```
Tool: get_veracode_alerts
Parameter: veracodeAppName = {component_name}

Acceptance Criteria:
- No critical severity findings
- No high severity findings (or approved exceptions)
- Scan completed within release window
```

---

### Control 4: Release Branch Hygiene (Correct Scope Enforcement)

**Goal:** Release branches must include only the User Stories (US) committed for that release.

#### Standard
- Only work items committed to the current release are allowed in the release branch
- Commits related to future releases must be identified and reverted if present

#### Verification Options
- Manual review via GitHub history inspection, OR
- Run internal automation/scripts for:
  - Branch Cut validation
  - Cherry-pick validation
  - Revert commit validation

**Important:** If any revert/addition happens after pre-deployment, an EM ticket must be created and referenced for auditability.

---

### Control 5: Logger Data Handling (Privacy & Regulatory Compliance)

**Goal:** Prevent leakage of customer identification or regulated data through logs.

#### Standard
Loggers must NOT record or expose:
- **PCI** (Payment Card Information)
- **RPI** (Regulated Personal Information)
- **SPI** (Sensitive Personal Information)
- Raw SQL queries (SELECT, INSERT, UPDATE, DELETE)
- Full API request payloads
- Full API response payloads

#### Microservice/Component Identification
Before scanning, identify the microservice(s) from the work item:

1. **Extract Component Name** from iTrack `work_item_tags` or Component field
2. **Derive Repository Name** using naming convention:
   - Component tag → Repository name (e.g., `oce-shippingms`, `oce-enrichmentms`)
3. **Derive Branch Name** based on mode:
   - **Development Mode**: `feature/{USER_STORY_ID}` (e.g., `feature/SPTOCE-104040`)
   - **Release Mode**: `release/{FIX_VERSION}` (e.g., `release/26.2.4`)

#### Code Change Metrics (Per Microservice)

Use MCP tools to retrieve code change metrics without cloning repositories:

```
Tool: get_repo_latest_changes
Parameter: repoName = {repository_name} (e.g., "oce-shippingms")
Parameter: timeframe = 7 (days)

Response provides:
- Recent merged PRs with summary
- Files changed per PR
- Lines added/removed per PR
- Change descriptions
```

```
Tool: get_pr_status
Returns: PR details for current user including:
- Files changed
- Lines added (additions)
- Lines removed (deletions)
- PR status and approval state
```

#### Test Coverage Metrics (Per Microservice)

Use MCP tools and direct CI/CD pipeline URLs to retrieve test coverage:

##### CI/CD Pipeline URL Pattern
```
Jenkins Base URL: https://az-community-four.vci.att.com/jenkins/job/com.att.oce/job/ST_OCE3_BSSE/job/{MicroserviceName}/

Example URLs:
- DeviceManagementMs: https://az-community-four.vci.att.com/jenkins/job/com.att.oce/job/ST_OCE3_BSSE/job/DeviceManagementMs/
- OrderManagementMs: https://az-community-four.vci.att.com/jenkins/job/com.att.oce/job/ST_OCE3_BSSE/job/OrderManagementMs/
- ShippingMs: https://az-community-four.vci.att.com/jenkins/job/com.att.oce/job/ST_OCE3_BSSE/job/OrderShippingMs/
```

##### Branch Checking Order (Priority)
When verifying builds, check branches in the following order:

| Priority | Branch Pattern | When to Use |
|----------|----------------|-------------|
| 1️⃣ **First** | `feature/{USER_STORY_ID}` | Development Mode (e.g., `feature/SPTOCE-104040`) |
| 2️⃣ **Second** | `release/{FIX_VERSION}` | Release Mode (e.g., `release/26.2.4`) |
| 3️⃣ **Third** | `master` | Fallback if feature/release branch not found |

##### Pipeline URL Construction
```
For feature branch:
{Jenkins_Base_URL}/job/feature%2F{USER_STORY_ID}/

For release branch:
{Jenkins_Base_URL}/job/release%2F{FIX_VERSION}/

For master branch:
{Jenkins_Base_URL}/job/master/

Example - DeviceManagementMs feature branch:
https://az-community-four.vci.att.com/jenkins/job/com.att.oce/job/ST_OCE3_BSSE/job/DeviceManagementMs/job/feature%2FSPTOCE-104040/
```

##### SonarQube URL Pattern
```
SonarQube Base URL: https://sonar.it.att.com/dashboard?id={MOTS_ID}%3A{GROUP_ID}%3A{ARTIFACT_ID}

Example URLs:
- DeviceManagementMs: https://sonar.it.att.com/dashboard?id=23488%3Acom.att.oce.fmo%3ADeviceManagementMs
- OrderManagementMs: https://sonar.it.att.com/dashboard?id=23488%3Acom.att.oce.fmo%3AOrderManagementMs
- ShippingMs: https://sonar.it.att.com/dashboard?id=23488%3Acom.att.oce.fmo%3AOrderShippingMs

SonarQube provides:
- Unit Test Coverage %
- Component Test Coverage %
- Code Smells
- Bugs
- Vulnerabilities
- Duplications %
- Quality Gate Status (Passed/Failed)
```

##### MCP Tool Integration
```
Tool: get_build_results
Parameter: type = "byPipeline"
Parameter: pipelineUrl = {pipeline_url}
Parameter: timeframe = 7 (days)

Response provides:
- Build status (success/failure)
- Test results summary
- Code coverage percentage (if configured in pipeline)
```

```
Tool: get_build_results
Parameter: type = "bySpecificBuild"
Parameter: buildUrl = {build_url}

Response provides:
- Detailed build logs
- Test execution results
- Coverage reports (JaCoCo/Cobertura)
- Quality gate status
```

##### Test Coverage Report Format
```
Microservice: {component_name}
Jenkins Pipeline: {jenkins_url}
SonarQube Dashboard: {sonarqube_url}
Branch Checked: {branch_name} (Priority: {1|2|3})

Coverage Metrics:
- Unit Test Coverage: {percentage}% (Required: ≥80%)
- Component Test Coverage: {percentage}% (Required: ≥70%)
- Quality Gate: PASSED/FAILED

Build Status:
- Last Build: #{build_number}
- Status: SUCCESS/FAILURE
- Test Results: {passed}/{total} tests passed
```

#### Manual Logger Verification

Use MCP semantic search to verify logger statements without cloning:

```
Tool: semantic_code_search
Parameter: query = "log.info logger.info LOG.info logging statements"
Parameter: filter.motsId = "23488"
Parameter: filter.repositories = ["{repository_key}"]
Parameter: score_threshold = 0.7
Parameter: fetch_k = 20

Review returned code chunks for:
- Sensitive data in log statements
- PCI/RPI/SPI exposure
- SQL queries in logs
- API request/response payloads
```

```
Tool: get_repo_latest_changes
Parameter: repoName = {repository_name}
Parameter: timeframe = 14 (days)

Review PR summaries for:
- Logger changes mentioned in PR descriptions
- Files with logging modifications
- NO_LOGGERS or LOGGER label references
```

#### Logger Patterns to Verify
| Pattern | Action |
|---------|--------|
| `log.info(...)` | Verify no sensitive data |
| `log.debug(...)` | Verify no sensitive data |
| `log.error(...)` | Verify no stack traces with sensitive data |
| `logger.info(...)` | Verify no sensitive data |
| `LOG.info(...)` | Verify no sensitive data |

#### Verification Commands
```bash
# Scan for SQL query logging
grep -rn "log\." --include="*.java" src/ | grep -iE "(SELECT|INSERT|UPDATE|DELETE)"

# Scan for API payload logging
grep -rn "log\." --include="*.java" src/ | grep -iE "(request|response|payload|body)"

# Scan for sensitive data patterns
grep -rn "log\." --include="*.java" src/ | grep -iE "(ssn|creditcard|cardnumber|cvv|password|accountNumber)"
```

#### Report Format (Per Microservice)
```
Microservice: {component_name}
Repository: {repository_name}
Branch: {branch_name}

Code Changes:
- Files Changed: {count}
- Lines Added: {count}
- Lines Removed: {count}
- Lines Modified: {count}

Logger Verification:
- Logger statements found: {count}
- Logger statements verified: {count}
- Violations found: {count}

Logger Compliance: PASS/FAIL
```

#### Acceptable Logging
- Correlation IDs
- Timestamps
- Status codes
- Error messages (without sensitive payload)
- Transaction IDs
- Business identifiers (non-PII)

---

### Control 6: Credential Exposure Prevention (Secrets Management)

**Goal:** Ensure no credentials or secrets are exposed in code, config, or logs.

#### Microservice/Component Identification
Before scanning, identify the microservice(s) from the work item:

1. **Extract Component Name** from iTrack `work_item_tags` or Component field
2. **Derive Repository Name** using naming convention:
   - Component tag → Repository name (e.g., `oce-shippingms`, `oce-enrichmentms`)
3. **Derive Branch Name** based on mode:
   - **Development Mode**: `feature/{USER_STORY_ID}` (e.g., `feature/SPTOCE-104040`)
   - **Release Mode**: `release/{FIX_VERSION}` (e.g., `release/26.2.4`)

#### Report Format (Per Microservice)
```
Microservice: {component_name}
Repository: {repository_name}
Branch: {branch_name}
Credential Exposure: PASS/FAIL
```

#### Standard
There must be NO exposed:
- API keys
- Passwords
- Tokens (JWT, OAuth, etc.)
- Certificates/private keys
- Secrets in configuration or log output
- Connection strings with credentials

#### Verification Commands (Per Microservice)
```bash
# Navigate to microservice directory
cd {repository_path}
git checkout {branch_name}

# Scan for credential patterns
grep -rn --include="*.java" --include="*.properties" --include="*.yml" --include="*.yaml" \
  -iE "(password|secret|apikey|api_key|token|credential|private_key)" src/ config/

# Scan for hardcoded strings that look like secrets
grep -rn --include="*.java" -E "\"[A-Za-z0-9+/=]{32,}\"" src/

# Check for .env files or secrets files
find . -name "*.env" -o -name "*secret*" -o -name "*credential*"
```

#### Verification
- Automated scanning (including Veracode findings where applicable)
- Manual review during attestation for high-risk areas (configs, pipelines, bootstrap scripts)

---

### Control 7: User Story / Work Item Status Validation (Release Readiness)

**Goal:** Ensure only fully tested and approved work items ship.

#### Required Status

| Work Item Type | Required Status |
|----------------|-----------------|
| User Story (US) | **Accepted** |
| Bug Fix | **Test Complete** |
| Technical Task | **Test Complete** |

#### Verification
- Validate iTrack state for every release-tagged item
- Confirm alignment between tracking data and release tag/scope
- Verify supporting test plan / test results attestation exists

---

### Control 8: Security Attestation Decision (Go / No-Go Rule)

**Goal:** Enforce a consistent release approval standard.

#### Decision Matrix

| Condition | Decision |
|-----------|----------|
| All controls pass | ✅ **GO** |
| Any hard-stop violation | 🔴 **NO-GO** |
| Warnings only (non-blocking) | ⚠️ **GO with conditions** |

**If any of the above gates fail, the release outcome from security attestation is:**
- **No-Go** until remediation is completed
- All failures must be resolved before the release can proceed

#### Required Documentation for Failures
- Specific check that failed
- Remediation action required
- Owner and timeline for resolution
- Escalation path if timeline at risk

---

### Control 9: Continuous Security Operations (Weekly Release Discipline)

**Goal:** Maintain a secure baseline (not just a secure release).

#### Ongoing Operational Best Practices

**Run security scans every release (weekly):**
- SAST / SCA scans are executed each release cycle
- Findings are addressed as early as possible to avoid release blocking

**Maintain security scorecards:**
- Track and resolve PCI vulnerabilities within SLA
- Ensure scorecard posture does not degrade over time

**Maintain GitHub repository hygiene ("sanity"):**
- Clean up unused repos and stale branches
- Reduce exposure surface and operational noise
- Address reported security vulnerabilities promptly (Dependabot/alerts/etc.)

---

### Control 10: Timely Audit Readiness & Closure (Audit SLA Rule)

**Goal:** Ensure all internal/external audit requests and findings are handled on time with complete, audit-ready evidence.

#### Compliance Standard
If any audit request or audit finding is not acknowledged, tracked, supported with required evidence, or closed by the agreed due date, the outcome is:

**Audit No-Go (Non-Compliant)** until evidence is provided and the finding is remediated/closed

#### All audit items must be:
- Logged in the tracking system with an owner and due date
- Acknowledged and triaged within **1 business day**
- Supported with an initial evidence pack or response plan within **3 business days**
- Closed with final evidence and auditor acceptance by the due date (with clarifications addressed within **1–2 business days**)

---

## III. EY / SOX Control Evidence Collection Guidelines

**Scope:** Controls for interfaces where data is packaged, transmitted, and consumed between producer and consumer systems (API / MQ / file).

**Audience:** Producer team, Consumer team, Internal SOX, External EY.

**Objective:** Produce repeatable, audit-ready evidence proving control design and operating effectiveness, with end-to-end traceability.

### Evidence Requirement 1: Live Walkthrough (Required)

Conduct a live end-to-end demonstration with Internal SOX and EY.
- The walkthrough must show the actual interface behavior (not just static screenshots)
- Demonstrate both successful and failure scenarios

### Evidence Requirement 2: Both Sides Coverage (Required)

Collect evidence from **Producer** and **Consumer** for the same interface execution.

#### 2.1 Producer (Source System) — Required Evidence

Show how data is:
- **Packaged:** mappings, transformations, schema/contract
- **Transferred:** API call, MQ publish, file creation/drop
- **Controlled:** validations, error handling, retries, acknowledgements

**Acceptable Artifacts:**
- Code snippets (mapper/builder, publisher/sender, file writer)
- Config snippets (endpoint/queue/topic/path) — redact secrets
- Logs/traces proving "send" with correlation/message IDs

#### 2.2 Consumer (Downstream System) — Required Evidence

Show how data is:
- **Received:** listener/controller/file watcher
- **Validated/parsed:** input validation logic
- **Consumed:** processing logic, persistence, downstream actions
- **Controlled:** rejections, DLQ/dead-letter routing, error handling

**Must include both:**
- Successful Scenarios
- Failure Scenarios

**Acceptable Artifacts:**
- Code snippets (receiver, validator/parser, handler, persistence)
- Config snippets (subscriptions, routes, bindings) — redact secrets
- Logs/traces proving "receive/consume" with correlation/message IDs

### Evidence Requirement 3: Flow Execution Evidence (Required)

#### 3.1 Default: Production Execution (Preferred)
Capture a real Production execution within the last **72 hours** showing:
1. Producer packages payload
2. Producer transmits payload
3. Consumer receives payload
4. Consumer processes/consumes (and persists/acts)
5. Failure handling

**Must include:**
- Identifiers (correlation ID / message ID / business ID)
- Timestamps from relevant systems
- Enough payload structure to prove mapping/consumption (redact sensitive fields, keep schema/field names where possible)

#### 3.2 Fallback: Non-Prod Execution (Only if Prod is Constrained)
If Production capture is not feasible (privacy/access/risk), capture the same end-to-end flow in Non-Prod, but still tie code evidence to Production-deployed logic.

#### 3.3 Parity Proof (Mandatory When Using Non-Prod Flow Evidence)
Provide proof that:
- Prod = Non-Prod (same version/commit), OR
- Non-Prod is at most one release behind Prod, and interface logic is unchanged

**Acceptable Parity Proof (provide at least one; preferably two):**
- Version/release comparison (Prod vs Non-Prod)
- Git commit SHA/tag comparison
- Deployment/pipeline record (release dashboard, ticket reference)
- Build/artifact equivalence (build ID, image digest, package version)

### Evidence Requirement 4: Timestamp on Every Capture (Required)

Every artifact must show the local timestamp of the machine used to capture it (screenshots, terminal outputs, logs, queries, monitoring, etc.).

**Accepted Methods:**
- System clock visible in screenshot, OR
- `date`/`time` command shown in the same capture (recommended), OR
- Equivalent clear timestamp method

### Evidence Requirement 5: Change Integrity (Required)

#### 5.1 Codebase Change Evidence
Provide:
- Last commit metadata for relevant files (commit hash, author, date)
- Branch/tag aligned to Production deployment

#### 5.2 Production "What is Deployed" Evidence
Where applicable, provide:
- Deployed artifact identity (image digest, package version, build number)
- Deployment record/pipeline evidence mapping to Prod
- OS-level timestamps only if available/allowed; otherwise artifact/deployment metadata is primary

### Evidence Requirement 6: End-to-End Traceability (Required — Never Omit)

Include traceability linking the interface change and deployment to:
```
iTrack → US → CR → CANA
```

**Must show:**
- IDs for each item
- How the release/deployment maps to those IDs
- That the demonstrated logic is covered by the approvals/change records

### Evidence Requirement 7: Minimum Evidence Package Checklist (Per Interface)

| Category | Required Items |
|----------|----------------|
| **Logic Evidence (code/config)** | Producer: mapping/packaging + transmission |
| | Consumer: receive/parse/validate + consume/persist |
| | Relevant config (secrets redacted) |
| **Flow Evidence** | Prod execution ≤72 hours, OR |
| | Non-Prod execution + parity proof |
| **Timestamp Coverage** | Local timestamp visible on every capture |
| **Change Integrity** | Repo last-modified/last-commit evidence |
| | Prod deployment/artifact evidence ("what is deployed") |
| **Traceability** | iTrack → US → CR → CANA mapping tied to the release/deployment |

### Evidence Quality Rules (Recommended)

- Use the same identifier (correlation/message/business ID) across producer + consumer evidence
- Redact minimally; preserve structure and field names
- Prefer primary sources: repo views, pipeline/deploy records, production logs/monitoring
- Ensure captures are readable and show system/environment context

### Live Walkthrough Script (Recommended)

1. Identify interface scope (Producer, Consumer, transport)
2. Show Producer code/config (packaging + send) and Consumer code/config (receive + consume)
3. Show Successful and Failure flow execution evidence (Prod ≤72 hours; else Non-Prod + parity)
4. Show "last modified" + "what is deployed" evidence
5. Show iTrack → US → CR → CANA traceability
6. Address control behaviors (retries, error handling, DLQ, monitoring, reconciliation if applicable)

---

## IV. MCP Tool Integration

### A. Work Item Retrieval
```
Tool: get_multiple_work_items

Parameters:
- organization: The iTrack/Jira organization (e.g., "SPTOCE")
- project: The project key (e.g., "SPT-OCE")
- itemIds: Array of user story IDs entered by user (e.g., ["SPTOCE-104040"])
- targetAlm: The ALM system type ("itrack", "attjira", "ado", "github")

Example - iTrack User Story:
{
  "organization": "SPTOCE",
  "project": "SPT-OCE",
  "itemIds": ["SPTOCE-104040"],
  "targetAlm": "itrack"
}

Response Fields to Validate:
- work_item_id: Unique identifier
- work_item_key: Full ticket key (e.g., "SPTOCE-104040")
- work_item_status: Current status ("In Progress", "Accepted", etc.)
- work_item_tags: Array of labels (check for NO_LOGGERS, SAST_100, component tags)
- acceptance_criteria: AC details for validation
- work_item_assignee_id: Developer assigned

Post-Retrieval Validation:
1. Check if Components field is populated
2. Check if Fix Version is present
3. If Components NOT empty → proceed with component-based validation
4. If Components empty → flag as hard-stop violation
```

### B. Veracode Alerts (Release Mode)
```
Tool: get_veracode_alerts
Parameter: veracodeAppName = {component_name from iTrack}

Usage:
1. Extract component name from user story
2. Call get_veracode_alerts with component name
3. Verify no critical/high severity alerts
4. Report coverage status
```

### C. Repository Discovery
```
Tool: get_user_assigned_repositories

Usage:
1. If repo not in workspace, call to get repository list
2. Match component name to repository
3. Clone or navigate to appropriate branch
```

### D. Repository History (For Component Validation)
```
Tool: get_repo_latest_changes

Usage:
1. For each component identified in work item
2. Fetch recent changes/commits
3. Validate commits reference the user story
4. Scan code changes for compliance violations
```

---

## V. Workflow Execution Guide

### A. Development Mode Workflow

1. **Prompt for User Story**: Ask user for story number(s)
2. **Fetch Work Item**: Call `get_multiple_work_items`
3. **Validate Work Item Response**:
   - Check Components field is NOT empty
   - Check Fix Version is present
   - Check AOTS Ticket # is EMPTY
4. **If Components NOT empty**:
   - For each component, get git history
   - Scan for logger compliance violations
   - Scan for credential exposure
   - Run unit tests for coverage
5. **Generate Development Compliance Report**

### B. Release Mode Workflow

1. **Prompt for User Story**: Ask user for story number(s)
2. **Detect Release Version**: Ask if not provided
3. **Fetch Work Item**: Call `get_multiple_work_items`
4. **Validate Work Item Response**:
   - Status = "Accepted"
   - Fix Version matches release
   - Components tagged
   - AOTS Ticket # empty
5. **If Components NOT empty**:
   - For each component:
     - Fetch Veracode alerts
     - Get git history
     - Validate commit traceability
     - Scan for compliance violations
6. **Compare with Previous Release**: Flag incorrectly added stories
7. **Generate Release Compliance Report with Go/No-Go decision**

### C. Report Rules

**Development Mode Report MUST NOT include:**
- ✘ Raw MCP response data (JSON blocks from work item retrieval)
- ✘ SAST/Veracode status section (not required in Development mode)

**Development Mode Report MUST include:**
- ✔ iTrack field validation results
- ✔ Code change metrics (lines added/removed/modified per microservice)
- ✔ Manual logger verification results (log.info, logger.info, etc.)
- ✔ Logging compliance scan results
- ✔ Credential exposure scan results
- ✔ Unit test coverage percentage
- ✔ Component test coverage percentage
- ✔ Test coverage from actual test execution

**Release Mode Report MUST include:**
- ✔ All Development Mode items
- ✔ Code change metrics per microservice (lines added/removed/modified)
- ✔ Manual logger verification count and status
- ✔ Unit test coverage percentage (must be ≥ 80%)
- ✔ Component test coverage percentage (must be ≥ 70%)
- ✔ SAST/Veracode coverage status
- ✔ Commit traceability validation
- ✔ Release branch hygiene check
- ✔ Go/No-Go decision with justification

---

## VI. Compliance Decision Rules

### A. Development Mode Decision

| Result | Condition |
|--------|-----------|
| ✅ **PASS** | All common hard-stops clear, work item "In Progress", no logging violations |
| ⚠️ **WARN** | Test coverage below 80%, TODO/FIXME items present |
| 🔴 **FAIL** | Any hard-stop violation (AOTS present, logging violations, credentials exposed) |

### B. Release Mode Decision

| Result | Condition |
|--------|-----------|
| ✅ **GO** | All validations pass, all US "Accepted", SAST 100%, no out-of-scope commits |
| 🔴 **NO-GO** | Any hard-stop violation — release cannot proceed |

---

## VII. Metrics & Thresholds

### A. Common Metrics (Both Modes)

| Metric | Threshold |
|--------|-----------|
| AOTS Ticket # populated | 0 (hard stop if any) |
| Components not tagged | 0 |
| Fix Version missing | 0 |
| SQL queries logged | 0 |
| API Request/Response logged | 0 |
| Exposed secrets | 0 |
| PCI/RPI/SPI logged | 0 |

### B. Development Mode Metrics

| Metric | Threshold |
|--------|-----------|
| Unit test coverage (new code) | ≥ 80% (recommended) |
| Component test coverage | ≥ 70% (recommended) |
| TODO/FIXME comments | Flag for review |
| Lines added without tests | Flag for review |

### C. Release Mode Metrics

| Metric | Threshold |
|--------|-----------|
| User Stories not in Accepted | 0 |
| Fix Version mismatches | 0 |
| Stories incorrectly added to release | 0 |
| Components without SAST coverage | 0 |
| High severity Veracode findings | 0 |
| Out-of-scope commits | 0 |
| Unit test coverage | ≥ 80% (required) |
| Component test coverage | ≥ 70% (required) |
| Logger statements not verified | 0 |

---

## VIII. Escalation Triggers

### A. Both Modes
- Detection of exposed secrets (API keys, passwords, tokens)
- SQL queries, API request/response found in logs
- PCI/RPI/SPI exposure in logs
- AOTS Ticket # field is populated

### B. Release Mode Only
- SAST coverage below 100%
- Work items in incorrect status (not Accepted)
- Stories incorrectly added to release
- Out-of-scope commits present in release branch
- Audit evidence not provided within SLA

---

## IX. Versioning & Governance

- **Review cadence**: Quarterly or upon regulatory/audit requirement change
- **Change control**: PR + security architect approval + compliance witness
- **Source of truth**: This constitution co-located in archetype; updates propagate to workflows & runbooks

---

## Changelog

- **v3.0.0** (2026-02-19): Major rewrite with comprehensive SOX compliance framework:
  - Added 10 SOX Control Areas with detailed validation steps
  - Added Component-Based Validation Workflow
  - Added EY/SOX Control Evidence Collection Guidelines
  - Enhanced MCP tool integration with component validation flow
  - Added bidirectional traceability requirements
  - Added audit SLA rules and evidence package checklist
- **v2.1.0** (2026-02-17): Development Mode report refinements
- **v2.0.0** (2026-02-17): Added dual-mode support (Development/Release)
- **v1.0.0** (2025-02-17): Initial version

---

Version: 3.0.0
Last Updated: 2026-02-19
Source: Derived from OCE SOX - Release Security Attestation & Engineering Best Practices (Team Standard) wiki page (pageId: 2524256762) and EY/SOX Control Evidence Collection Guidelines.
