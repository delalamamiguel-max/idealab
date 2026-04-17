---
description: Debug IDP Seed upgrade issues, conflicts, and failures (IDP Seed Upgrade)
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
- Read `${ARCHETYPES_BASEDIR}/idp-seed-upgrade/idp-seed-upgrade-constitution.md` for known issues
- Load `${ARCHETYPES_BASEDIR}/idp-seed-upgrade/templates/env-config.yaml` for troubleshooting patterns

### 3. Parse Input
Extract from $ARGUMENTS:
- Error type (compilation, runtime, test, dependency)
- Error message or stack trace
- Project path
- Current migration state

Request clarification if incomplete.

### 4. Diagnose Issue Category

**Compilation Errors:**
- Missing imports after annotation replacement
- Incompatible API changes
- Dependency resolution failures

**Runtime Errors:**
- Spring context initialization failures
- Bean creation exceptions
- Configuration property issues

**Test Failures:**
- RestAssured 401 Unauthorized
- MockBean/SpyBean deprecation warnings
- Spring test context issues

**Dependency Conflicts:**
- Version mismatches
- Transitive dependency issues
- Exclusion problems

### 5. Apply Known Fixes

**RestAssured 401 Unauthorized:**
```java
// Add .preemptive() after .auth()
.auth().preemptive().basic(username, password)
```

**MockBean Import Error:**
```java
// Old import
import org.springframework.boot.test.mock.mockito.MockBean;
// New import
import org.springframework.test.context.bean.override.mockito.MockitoBean;
```

**SOAP Interceptor ClassNotFoundException:**
```java
// Old
HttpComponents5MessageSender.RemoveSoapHeadersInterceptor()
// New
HttpComponents5ClientFactory.RemoveSoapHeadersInterceptor()
```

**Spring Context Failure with idp-config:**
```java
// Remove com.att.idp.config from excludeFilters
@ComponentScan(basePackages = "com", excludeFilters = {
    @ComponentScan.Filter(type=FilterType.REGEX, pattern="com.(azure|microsoft).*")
})
```

**Azure App Config Compatibility:**
```xml
<!-- Update to compatible version -->
<dependency>
    <groupId>com.azure.spring</groupId>
    <artifactId>spring-cloud-azure-appconfiguration-config-web</artifactId>
    <version>6.1.0</version>
</dependency>
```

### 6. Dependency Conflict Resolution
// turbo
Run `mvn dependency:tree -Dverbose` to identify conflicts.

Common resolutions:
- Add explicit version in dependencyManagement
- Use exclusions for conflicting transitive dependencies
- Align with Seed BOM versions

### 7. Generate Debug Report
Create troubleshooting report:

```markdown
# Seed Upgrade Debug Report

## Issue Summary
{Description of the issue}

## Root Cause
{Identified root cause}

## Resolution
{Steps taken to resolve}

## Verification
{How to verify the fix}

## Prevention
{How to prevent similar issues}
```

### 8. Escalation Path
If issue cannot be resolved:
1. Check FAQ wiki page
2. Search IDP support channels
3. Create support ticket with debug report

## Error Handling
**Unknown Error**: Collect diagnostic information, suggest escalation
**Multiple Issues**: Prioritize and address sequentially
**Environment Issue**: Distinguish between code and environment problems

## Examples
**Example 1**: `/debug-idp-seed-upgrade --error "401 Unauthorized" --project usermanagementms`
Output: Diagnose and fix RestAssured authentication issue

**Example 2**: `/debug-idp-seed-upgrade --error "ClassNotFoundException: RemoveSoapHeadersInterceptor"`
Output: Fix SOAP interceptor class location change

## References
- Constitution: `${ARCHETYPES_BASEDIR}/idp-seed-upgrade/idp-seed-upgrade-constitution.md`
- Env Config: `${ARCHETYPES_BASEDIR}/idp-seed-upgrade/templates/env-config.yaml`
- [FAQ 3.0.1](https://wiki.web.att.com/display/IDSEPA/FAQ+-+3.0.1)
