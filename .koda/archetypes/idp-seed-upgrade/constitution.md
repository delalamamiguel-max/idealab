# Constitution: IDP Seed Upgrade

## Purpose
Govern the upgrade of IDP Java Seed parent artifact versions to ensure security compliance, compatibility, and smooth migration across microservices. This archetype manages the detection, planning, and execution of Seed framework upgrades.

### Target Artifact
```xml
<parent>
    <groupId>com.att.idp</groupId>
    <artifactId>sdk-java-parent</artifactId>
    <version>{TARGET_VERSION}</version>
</parent>
```

> **Scope**: This archetype governs upgrades to `com.att.idp:sdk-java-parent` and any intermediate SDK layers (e.g., `com.att.oce:oce-sdk-parent`) that depend on it.

> **IMPORTANT**: This constitution defines **static rules** that apply to ALL Seed upgrades. Version-specific details (code changes, dependency versions, deprecations) are **dynamically loaded** from IDP wiki pages at runtime. See Section IV for required user inputs and Section VI for wiki integration.

---

### I. Required User Input (MANDATORY BEFORE EXECUTION)

**⚠️ HALT CONDITION**: The LLM **MUST prompt the user** for the following wiki URLs **BEFORE** executing any scaffold, refactor, test, or document workflow. Do NOT proceed with any implementation until these inputs are collected.

#### 1.1 Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| **User Story Number** | iTrack/ADO user story or ticket number for traceability | `XXXXXX-XXXXXX` or `XXXXX-XXXXX` |
| **Release Notes Wiki URL** | URL to the target Seed version's release notes page | `https://wiki.web.att.com/pages/viewpage.action?spaceKey=IDSEPA&title=Seed+3.0.1+-+Release+Notes` |
| **Upgrade Instructions Wiki URL** | URL to the target Seed version's upgrade instructions page | `https://wiki.web.att.com/display/IDSEPA/Seed+3.0.1+-+Upgrade+Instructions` |

#### 1.2 Optional Fields

| Field | Description | Example |
|-------|-------------|---------|
| **FAQ Wiki URL** (Optional) | URL to the target Seed version's FAQ page for known issues and fixes | `https://wiki.web.att.com/display/IDSEPA/FAQ+-+3.0.1` |

#### 1.3 User Prompt Template

When a user invokes any workflow in this archetype, the LLM **MUST** display the following prompt and wait for user response:

```
📋 IDP Seed Upgrade - Input Required

Before proceeding with the Seed upgrade, please provide the following information:

0️⃣ User Story Number (REQUIRED):
   Example: XXXXXX-XXXXXX or XXXXX-XXXXX
   Your User Story: _______________

1️⃣ Release Notes Wiki URL (REQUIRED):
   Example: https://wiki.web.att.com/pages/viewpage.action?spaceKey=IDSEPA&title=Seed+3.0.1+-+Release+Notes
   Your URL: _______________

2️⃣ Upgrade Instructions Wiki URL (REQUIRED):
   Example: https://wiki.web.att.com/display/IDSEPA/Seed+3.0.1+-+Upgrade+Instructions
   Your URL: _______________

3️⃣ FAQ Wiki URL (OPTIONAL - press Enter to skip):
   Example: https://wiki.web.att.com/display/IDSEPA/FAQ+-+3.0.1
   Your URL: _______________

⏳ Waiting for your input...
```

#### 1.4 Validation Rules

- **User Story Number**: Must be a valid iTrack (e.g., `XXXXXX-XXXXXX`) or ADO ticket number (e.g., `XXXXX-XXXXX`)
- **Release Notes URL**: Must contain `wiki.web.att.com` and reference a Seed release notes page
- **Upgrade Instructions URL**: Must contain `wiki.web.att.com` and reference upgrade instructions
- **FAQ URL**: Optional, but if provided must contain `wiki.web.att.com`

#### 1.5 Git Conventions (Using User Story Number)

The user story number **MUST** be used in all git operations for traceability:

**Branch Naming Convention**:
```bash
git checkout -b feature/{USER_STORY_NUMBER}

# Examples:
git checkout -b feature/XXXXXX-XXXXXX
git checkout -b feature/XXXXX-XXXXX
```

**Commit Message Format**:
```bash
git commit -m "[{USER_STORY_NUMBER}] : {description}"

# Examples:
git commit -m "[XXXXXX-XXXXXX] : upgrade to Seed 3.0.1, bump SDK to 3.3.0-SNAPSHOT"
git commit -m "[XXXXXX-XXXXXX] : upgrade to oce-sdk-parent 3.3.0-SNAPSHOT (Seed 3.0.1) - fix RestAssured auth"
git commit -m "[XXXXX-XXXXX] : upgrade to Seed 3.0.1 - fix @SpyBean deprecation"
```

> **IMPORTANT**: All migration plan documents and generated scripts **MUST** use the user-provided story number in branch names and commit messages.

#### 1.6 Post-Input Actions

After user provides wiki URLs, the LLM **MUST**:

1. **Call MCP `get_wiki_content` tool** for each provided URL
2. **Parse and validate** the wiki content is accessible and contains expected sections
3. **Display confirmation** of successfully fetched content:
   ```
   ✅ Wiki Content Fetched Successfully:
   - Release Notes: {title from wiki}
   - Upgrade Instructions: {title from wiki}
   - FAQ: {title from wiki or "Not provided"}
   
   Proceeding with migration plan...
   ```
4. **HALT if wiki fetch fails** - do not proceed with hardcoded assumptions

---

### II. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** or correct any code or spec that violates these rules:

✘ **No execution without user-provided wiki URLs** (Section I must be completed first)  
✘ **No execution without calling MCP `get_wiki_content` tool** to fetch wiki content  
✘ No upgrade without verifying current Seed version prerequisite  
✘ No skipping major version upgrades (must follow sequential upgrade path)  
✘ No upgrade without addressing deprecated API usage  
✘ No upgrade without SAST scan completion (100% coverage required)  
✘ No upgrade without regression testing validation  
✘ No hardcoded credentials or secrets in configuration files  
✘ No upgrade without creating a dedicated branch per naming convention  
✘ No changes to master/main branch directly

---

### II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify these patterns:

✔ Verify prerequisite Seed version before upgrade (fetch from wiki release notes)  
✔ Update `pom.xml` parent version to target Seed version  
✔ Apply all **version-specific code changes** as defined in wiki upgrade instructions  
✔ Update Docker base images to align with Seed release (fetch versions from wiki)  
✔ Run full test suite (unit, component, integration) post-upgrade  
✔ Document all changes in migration plan with traceability to iTrack/ADO tickets

> **Dynamic Code Changes**: The specific code modifications (annotation replacements, dependency updates, interceptor changes, etc.) are **fetched dynamically** from the target version's wiki upgrade instructions. Do NOT hardcode version-specific changes in this constitution.

---

### II-A. Multi-Hierarchy Parent Upgrade Rules

When a microservice uses an **intermediate SDK parent** (e.g., `oce-sdk-parent`) that itself depends on `sdk-java-parent`, the following cascade rules apply:

#### Hierarchy Detection

```
Microservice (e.g., usermanagementms)
    └── parent: com.att.oce:oce-sdk-parent:3.2.0-SNAPSHOT
              └── parent: com.att.idp:sdk-java-parent:3.0.0
```

#### Upgrade Cascade Rules

| Scenario | Action Required |
|----------|----------------|
| **Direct Parent** (`sdk-java-parent`) | Update version directly in microservice `pom.xml` |
| **Intermediate SDK Parent** | 1. Upgrade SDK parent's `sdk-java-parent` version<br>2. Increment SDK parent minor version<br>3. Update microservice to use new SDK parent version |

#### Version Increment Strategy for Intermediate SDK

When upgrading `sdk-java-parent` in an intermediate SDK (e.g., `oce-sdk-parent`):

```
Current SDK Version: X.Y.Z-SNAPSHOT
New SDK Version:     X.(Y+1).0-SNAPSHOT

Example:
  oce-sdk-parent 3.2.0-SNAPSHOT → 3.3.0-SNAPSHOT
```

**Rationale**: Minor version increment signals that the underlying Seed framework has changed, which may introduce breaking changes for downstream microservices.

#### Multi-Hierarchy Upgrade Workflow

```
┌─────────────────────────────────────────────────────────────┐
│ PHASE 1: UPGRADE INTERMEDIATE SDK PARENT                    │
│         (e.g., oce-sdk-parent)                              │
├─────────────────────────────────────────────────────────────┤
│ 1. Update sdk-java-parent version in SDK's pom.xml         │
│    <parent>                                                 │
│        <groupId>com.att.idp</groupId>                       │
│        <artifactId>sdk-java-parent</artifactId>             │
│        <version>3.0.1</version>  ← NEW VERSION              │
│    </parent>                                                │
│                                                             │
│ 2. Increment SDK parent version                             │
│    <version>3.3.0-SNAPSHOT</version>  ← MINOR INCREMENT     │
│                                                             │
│ 3. Update idp-config and other explicit dependencies        │
│                                                             │
│ 4. Build and publish SDK parent artifact                    │
├─────────────────────────────────────────────────────────────┤
│ PHASE 2: UPGRADE DOWNSTREAM MICROSERVICES                   │
│         (e.g., usermanagementms, orderms, orderrepoms)      │
├─────────────────────────────────────────────────────────────┤
│ 1. Update parent version to new SDK version                 │
│    <parent>                                                 │
│        <groupId>com.att.oce</groupId>                       │
│        <artifactId>oce-sdk-parent</artifactId>              │
│        <version>3.3.0-SNAPSHOT</version>  ← NEW VERSION     │
│    </parent>                                                │
│                                                             │
│ 2. Apply code changes from wiki upgrade instructions        │
│                                                             │
│ 3. Run tests and validate                                   │
└─────────────────────────────────────────────────────────────┘
```

#### Microservices with Direct sdk-java-parent Dependency

If a microservice directly uses `com.att.idp:sdk-java-parent` (no intermediate SDK):

```xml
<!-- Direct dependency - upgrade version directly -->
<parent>
    <groupId>com.att.idp</groupId>
    <artifactId>sdk-java-parent</artifactId>
    <version>3.0.1</version>  ← UPDATE TO TARGET VERSION
</parent>
```

Also update any explicitly declared `idp-config` dependency:
```xml
<dependency>
    <groupId>com.att.idp</groupId>
    <artifactId>idp-config</artifactId>
    <version>3.0.104</version>  ← FROM WIKI RELEASE NOTES
</dependency>
```

---

### III. Preferred Patterns (Recommended)

The LLM **should adopt** these patterns unless user overrides:

➜ Create feature branch following naming convention before starting upgrade  
➜ Review Seed release notes for breaking changes and deprecations  
➜ Maintain backward compatibility where possible  
➜ Update platform library versions as specified in release notes  
➜ Validate Spring Boot managed dependency alignment  
➜ Document upgrade rationale with links to official release notes  
➜ Notify stakeholders of breaking changes before deployment  
➜ Maintain migration checklist for audit compliance

---

### IV. Dynamic Wiki Integration

This archetype dynamically fetches version-specific information from IDP wiki pages. The following wiki URL patterns are used:

#### Wiki URL Templates
```yaml
release_notes: "https://wiki.web.att.com/pages/viewpage.action?spaceKey=IDSEPA&title=Seed+{VERSION}+-+Release+Notes"
upgrade_instructions: "https://wiki.web.att.com/display/IDSEPA/Seed+{VERSION}+-+Upgrade+Instructions"
faq: "https://wiki.web.att.com/display/IDSEPA/FAQ+-+{VERSION}"
security_vulnerabilities: "https://wiki.web.att.com/display/IDSEPA/Security+Vulnerabilities+in+Seed+{VERSION}"
managed_dependencies: "https://wiki.web.att.com/display/IDSEPA/IDP+Java+Seed+managed+dependency+versions"
```

#### Information Extracted from Wiki

| Wiki Page | Information Extracted |
|-----------|----------------------|
| **Release Notes** | Prerequisites, Spring Boot version, dependency versions, Docker image versions, platform library versions |
| **Upgrade Instructions** | Step-by-step code changes, POM modifications, annotation replacements, interceptor updates, configuration changes |
| **FAQ** | Known issues, workarounds, common error fixes |
| **Security Vulnerabilities** | CVEs addressed, security improvements |

---

### V. Version-Specific Code Changes (Dynamic)

The following categories of code changes are **dynamically determined** by parsing the wiki upgrade instructions for the target version:

#### 5.1 POM Changes
- Parent version update
- Explicit dependency version updates (e.g., `idp-config`)
- New dependency additions (e.g., `spring-cloud-starter`)
- Azure Spring dependency updates

#### 5.2 Annotation Replacements
- Deprecated annotation → replacement annotation
- Import statement updates

#### 5.3 API/Class Changes
- Moved classes (e.g., interceptors)
- Renamed methods
- Removed APIs

#### 5.4 Configuration Changes
- `@ComponentScan` filter modifications
- Application property changes
- Bootstrap configuration updates

#### 5.5 Test Code Changes
- Authentication pattern updates (e.g., RestAssured)
- Mock annotation replacements
- Test framework updates

> **Implementation Note**: Workflows must call `get_wiki_content` to fetch the target version's upgrade instructions and parse the HTML to extract specific code changes before applying them.

---

### VI. Workflow Integration Requirements

All workflows in this archetype **MUST**:

1. **Prompt user for wiki URLs first** (per Section I - MANDATORY)
2. **Call MCP LevelUp `get_wiki_content` tool** for each user-provided URL
3. **Parse wiki HTML** to extract:
   - Prerequisites and source version requirements
   - Code change patterns (old → new)
   - Dependency versions
   - Docker image versions
4. **Apply changes based on parsed wiki content**, not hardcoded values
5. **Cache wiki content** for the session to avoid repeated fetches

#### MCP Tool Usage

The `get_wiki_content` tool from the **LevelUp MCP server** is used to fetch wiki page content:

```
Tool: mcp0_get_wiki_content
Parameter: pageUrl (string) - The full wiki page URL

Example calls:
1. get_wiki_content(pageUrl: "https://wiki.web.att.com/pages/viewpage.action?spaceKey=IDSEPA&title=Seed+3.0.1+-+Release+Notes")
2. get_wiki_content(pageUrl: "https://wiki.web.att.com/display/IDSEPA/Seed+3.0.1+-+Upgrade+Instructions")
3. get_wiki_content(pageUrl: "https://wiki.web.att.com/display/IDSEPA/FAQ+-+3.0.1")
```

#### Mandatory Workflow Execution Order

```
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: PROMPT USER FOR WIKI URLs (Section I)              │
│         - Display prompt template                           │
│         - Wait for user input                               │
│         - Validate URLs contain wiki.web.att.com            │
├─────────────────────────────────────────────────────────────┤
│ STEP 2: FETCH WIKI CONTENT (MCP Tool)                       │
│         - Call get_wiki_content for Release Notes URL       │
│         - Call get_wiki_content for Upgrade Instructions URL│
│         - Call get_wiki_content for FAQ URL (if provided)   │
│         - HALT if any required fetch fails                  │
├─────────────────────────────────────────────────────────────┤
│ STEP 3: PARSE AND EXTRACT                                   │
│         - Extract prerequisites from Release Notes          │
│         - Extract code changes from Upgrade Instructions    │
│         - Extract known issues from FAQ                     │
├─────────────────────────────────────────────────────────────┤
│ STEP 4: EXECUTE MIGRATION PLAN                              │
│         - Apply changes based on extracted wiki content     │
│         - Generate documentation with wiki references       │
└─────────────────────────────────────────────────────────────┘
```

> **CRITICAL**: Steps 1 and 2 are **BLOCKING** - do NOT proceed to Step 3 or 4 until wiki content is successfully fetched.

---

### VII. Fallback Behavior

If wiki content cannot be fetched or parsed:

1. **Warn user** that dynamic content is unavailable
2. **Check local cache** in `templates/seed-versions/` directory
3. **Request manual input** for version-specific changes
4. **Never assume** code changes without wiki verification

---

### Version
3.2.0

### Last Updated
2026-02-19

### Change Log
| Version | Date | Changes |
|---------|------|---------|
| 3.2.0 | 2026-02-19 | Added User Story Number to Required Fields; Added Section 1.5 Git Conventions for branch naming and commit message format using user story number |
| 3.1.0 | 2026-02-19 | Added Target Artifact section with groupId specification; Added Section II-A: Multi-Hierarchy Parent Upgrade Rules for intermediate SDK versioning |
| 3.0.0 | 2026-02-19 | Added Section I: Required User Input (mandatory wiki URL prompts before execution); Added MCP `get_wiki_content` tool usage requirements; Added hard-stop rules for wiki URL input |
| 2.0.0 | 2026-02-18 | Refactored to dynamic wiki integration; Removed hardcoded version-specific patterns |
| 1.0.0 | 2026-02-18 | Initial version with static Seed 3.0.1 patterns |
