---
description: Refactor Java microservice code to apply IDP Seed upgrade changes (IDP Seed Upgrade)
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
- Load `${ARCHETYPES_BASEDIR}/idp-seed-upgrade/templates/env-config.yaml` for wiki URL templates

### 3. Parse Input
Extract from $ARGUMENTS:
- Target Seed version (e.g., 3.0.1) - **REQUIRED**
- Project path - **REQUIRED**
- Specific refactoring scope (optional: pom, annotations, soap, azure, tests, all)

Request clarification if target version or project path is not specified.

### 4. Fetch Wiki Content (Dynamic)
**CRITICAL**: All code changes MUST be fetched from wiki, not hardcoded.

Construct wiki URLs using templates from env-config.yaml:
```
TARGET_VERSION = {from $ARGUMENTS}
upgrade_instructions_url = wiki.url_templates.upgrade_instructions.replace("{VERSION}", TARGET_VERSION)
faq_url = wiki.url_templates.faq.replace("{VERSION}", TARGET_VERSION)
```

Call `get_wiki_content` MCP tool:
```
1. get_wiki_content(upgrade_instructions_url)
   → Extract ALL code change sections with old/new patterns
   
2. get_wiki_content(faq_url)
   → Extract known issues and fixes
```

### 5. Parse Wiki for Code Changes
Extract version-specific changes from wiki HTML:

**5.1 POM Changes**
- Parent version: Extract from `<version>X.X.X</version>` in upgrade instructions
- Dependency updates: Extract group_id, artifact_id, version for each dependency section
- New dependencies: Identify dependencies marked as "Add" or "new"

**5.2 Code Replacements**
For each numbered section in upgrade instructions (e.g., 3.0.a, 3.0.b):
```yaml
code_change:
  id: "{section_id}"
  condition: "{Optional/If applicable text}"
  old_pattern: "{code in Old column or 'Change' section}"
  new_pattern: "{code in New column or 'To' section}"
  import_changes:
    remove: ["{old imports}"]
    add: ["{new imports}"]
```

**5.3 FAQ Fixes**
Extract workarounds from FAQ page (e.g., RestAssured preemptive auth)

### 6. Apply POM Changes (Dynamic)
Using extracted POM changes from wiki:

**6.1 Update Parent Version**
```xml
<parent>
    <groupId>com.att.idp</groupId>
    <artifactId>sdk-java-parent</artifactId>
    <version>{VERSION_FROM_WIKI}</version>
</parent>
```

**6.2 Update/Add Dependencies**
For each dependency extracted from wiki:
- If exists: Update version to wiki-specified version
- If new: Add dependency with wiki-specified version

### 7. Apply Code Replacements (Dynamic)
For each code_change extracted from wiki:

**7.1 Check Applicability**
- If condition contains "Optional" or "If applicable", scan project first
- Skip if pattern not found in project

**7.2 Search and Replace**
```
grep_search(project_path, old_pattern)
For each file found:
  edit(file, old_pattern → new_pattern)
```

**7.3 Update Imports**
If code_change has import_changes:
- Remove old imports
- Add new imports at top of file

### 8. Apply FAQ Fixes (Dynamic)
For each fix extracted from FAQ:
- Search for applicable pattern in project
- Apply fix if found

### 9. Validate Changes
- Verify all POM changes are syntactically correct
- Ensure no old patterns remain (re-scan for each old_pattern)
- Check import statements are updated
- Validate no hardcoded credentials

### 10. Generate Change Report
Output summary of all changes made:

```markdown
# Refactor Report: Seed {VERSION}

## Wiki Sources
- Upgrade Instructions: {url}
- FAQ: {url}

## Changes Applied

### POM Changes
| File | Change | Status |
|------|--------|--------|
| pom.xml | Parent → {version} | ✅ |
| pom.xml | {dependency} → {version} | ✅ |

### Code Replacements
| Pattern | Files Modified | Status |
|---------|----------------|--------|
| {old} → {new} | {count} files | ✅ |

### Import Updates
| File | Removed | Added |
|------|---------|-------|
| {file} | {old_import} | {new_import} |

## Warnings
{Any patterns that couldn't be applied}

## Next Steps
- Run unit tests
- Run component tests
- Verify SAST coverage
```

## Error Handling
**Wiki Fetch Failed**: 
- Warn user that dynamic content is unavailable
- Check for cached version in `templates/seed-versions/`
- HALT - do not apply hardcoded changes

**POM Parse Error**: Report XML syntax issues, suggest corrections

**Pattern Not Found**: Log as "Not Applicable" - not an error

**Partial Refactor**: List remaining items that need manual attention

## Examples
**Example 1**: `/refactor-idp-seed-upgrade --to 3.0.1 --project /path/to/usermanagementms`
Output: Fetches 3.0.1 wiki, applies all applicable code changes

**Example 2**: `/refactor-idp-seed-upgrade --to 3.0.2 --project /path/to/myservice --scope pom`
Output: Fetches 3.0.2 wiki, applies only POM changes

## References
- Constitution: `${ARCHETYPES_BASEDIR}/idp-seed-upgrade/idp-seed-upgrade-constitution.md`
- Env Config: `${ARCHETYPES_BASEDIR}/idp-seed-upgrade/templates/env-config.yaml`
- Wiki URL Templates defined in env-config.yaml (dynamically constructed per version)
