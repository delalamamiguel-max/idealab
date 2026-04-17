---
description: Scaffold IDP Seed upgrade migration plan and checklist for Java microservices (IDP Seed Upgrade)
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
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype idp-seed-upgrade --json ` and parse for ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- Read `${ARCHETYPES_BASEDIR}/idp-seed-upgrade/idp-seed-upgrade-constitution.md` for hard-stop rules
- Load `${ARCHETYPES_BASEDIR}/idp-seed-upgrade/templates/env-config.yaml` for wiki URL templates and parsing patterns

### 3. Parse Input
Extract from $ARGUMENTS:
- Target Seed version (e.g., 3.0.1) - **REQUIRED**
- Project/microservice name - **REQUIRED**
- Repository path (optional, defaults to current workspace)

Request clarification if target version or project is not specified.

### 4. Construct Wiki URLs (Dynamic)
Using URL templates from `env-config.yaml`, construct version-specific wiki URLs:

```
TARGET_VERSION = {extracted from $ARGUMENTS}

release_notes_url = wiki.url_templates.release_notes.replace("{VERSION}", TARGET_VERSION)
upgrade_instructions_url = wiki.url_templates.upgrade_instructions.replace("{VERSION}", TARGET_VERSION)
faq_url = wiki.url_templates.faq.replace("{VERSION}", TARGET_VERSION)
```

### 5. Fetch Wiki Content (Dynamic)
**CRITICAL**: All version-specific information MUST be fetched from wiki, not hardcoded.

Call `get_wiki_content` MCP tool for each URL:

```
1. get_wiki_content(release_notes_url)
   → Extract: prerequisites, Spring Boot version, Docker images, platform library versions
   
2. get_wiki_content(upgrade_instructions_url)
   → Extract: ALL code change sections (POM changes, annotation replacements, 
              interceptor changes, configuration changes, dependency updates)
   
3. get_wiki_content(faq_url)
   → Extract: Known issues, workarounds, common fixes (e.g., RestAssured auth)
```

### 6. Parse Wiki HTML for Code Changes
Parse the upgrade instructions HTML to extract version-specific code changes:

**6.1 POM Changes**
- Extract target parent version from `<version>X.X.X</version>` patterns
- Extract dependency updates (group_id, artifact_id, version)
- Extract new dependencies to add

**6.2 Code Replacements**
For each section in upgrade instructions (3.0.a, 3.0.b, etc.):
- Identify OLD pattern/code
- Identify NEW pattern/code
- Note applicability conditions (e.g., "if using SOAP endpoints")

**6.3 Store Extracted Changes**
Create a structured object with all extracted changes:
```yaml
extracted_changes:
  pom:
    parent_version: "{from wiki}"
    dependencies: [{group_id, artifact_id, version, action: add|update}]
  code_replacements:
    - id: "{section_id}"
      condition: "{when applicable}"
      old_pattern: "{from wiki}"
      new_pattern: "{from wiki}"
      file_patterns: ["{applicable files}"]
  known_issues:
    - issue: "{from FAQ}"
      fix: "{from FAQ}"
```

### 7. Analyze Current Project State
For each target project:
1. Read `pom.xml` to identify current parent version
2. Identify explicitly declared IDP dependencies
3. **Scan for patterns that match extracted_changes.code_replacements**
   - For each code_replacement, search project for old_pattern
   - Record which changes are applicable to this project
4. Check for dependencies that need updates per extracted_changes.pom.dependencies

### 8. Generate Migration Plan (Dynamic)
Create migration plan document using ONLY information extracted from wiki:

**Structure:**
```markdown
# SEED {current} to {target} Migration Plan

## Document Information
- Generated: {timestamp}
- Wiki Sources: {list of wiki URLs fetched}

## Executive Summary
{Based on wiki release notes}

## Prerequisites
{Extracted from wiki release notes prerequisites section}

## Scope of Changes

### POM Changes
{From extracted_changes.pom - list all POM modifications}

### Code Changes
{From extracted_changes.code_replacements - only those applicable to project}

### Configuration Changes
{From extracted_changes - configuration-related items}

### Test Changes
{From extracted_changes and FAQ - test-related fixes}

## Migration Steps
{Step-by-step based on wiki upgrade instructions order}

## Validation Checklist
{Dynamic checklist based on applicable changes}

## Rollback Plan

## References
{Wiki URLs used}
```

### 9. Generate Dynamic Upgrade Checklist
Create checklist with ONLY applicable items based on project analysis:

```markdown
## Pre-Migration
- [ ] Verify current Seed version is {prerequisite from wiki}
- [ ] Create feature branch

## POM Changes
{For each applicable POM change from extracted_changes}
- [ ] {change description}

## Code Changes
{For each applicable code replacement found in project}
- [ ] {change description with file locations}

## Validation
- [ ] Run unit tests
- [ ] Run component tests
- [ ] Run integration tests
- [ ] Verify SAST coverage (100%)

## Documentation
- [ ] Update README changelog
- [ ] Document changes with traceability
```

### 10. Output Artifacts
Generate the following files:
1. `docs/SEED-{version}-Migration-Plan.md` - Detailed migration plan
2. `docs/SEED-{version}-Migration-Summary.md` - Quick reference summary
3. `docs/SEED-{version}-Wiki-Cache.yaml` - Cached wiki content for reference

## Error Handling
**Wiki Fetch Failed**: 
- Warn user that dynamic content is unavailable
- Check for cached version in `templates/seed-versions/`
- Request manual input for version-specific changes

**Unknown Version**: 
- Report that wiki pages for this version were not found
- Suggest checking wiki manually for correct version string

**No Applicable Changes**: 
- Report that project already appears compliant
- Recommend verification testing anyway

## Examples
**Example 1**: `/scaffold-idp-seed-upgrade --to 3.0.1 --project usermanagementms`
Output: Fetches 3.0.1 wiki pages, extracts all code changes, generates migration plan with only applicable changes

**Example 2**: `/scaffold-idp-seed-upgrade --to 3.0.2 --project oce-sdk-parent`
Output: Fetches 3.0.2 wiki pages (when available), generates migration plan for that version

## References
- Constitution: `${ARCHETYPES_BASEDIR}/idp-seed-upgrade/idp-seed-upgrade-constitution.md`
- Env Config: `${ARCHETYPES_BASEDIR}/idp-seed-upgrade/templates/env-config.yaml`
- Wiki URL Templates defined in env-config.yaml (dynamically constructed per version)
