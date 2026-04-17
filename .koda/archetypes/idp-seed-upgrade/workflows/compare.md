---
description: Compare IDP Seed versions, breaking changes, and migration requirements (IDP Seed Upgrade)
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
- Read `${ARCHETYPES_BASEDIR}/idp-seed-upgrade/idp-seed-upgrade-constitution.md` for version matrix
- Load `${ARCHETYPES_BASEDIR}/idp-seed-upgrade/templates/env-config.yaml` for version details

### 3. Parse Input
Extract from $ARGUMENTS:
- Source Seed version
- Target Seed version
- Comparison focus (dependencies, breaking-changes, security, all)

Request clarification if incomplete.

### 4. Fetch Version Information
Retrieve release documentation for both versions:
- Release Notes
- Upgrade Instructions
- Security Vulnerabilities addressed

### 5. Compare Dependencies
Generate dependency comparison matrix:

| Dependency | Source Version | Target Version | Change Type |
|------------|----------------|----------------|-------------|
| Spring Boot | 3.3.13 | 3.5.6 | Major |
| Spring Kafka | 3.2.10 | 3.3.10 | Minor |
| Jackson | 2.17.3 | 2.19.2 | Minor |
| ... | ... | ... | ... |

### 6. Identify Breaking Changes
List all breaking changes between versions:

**API Changes:**
- Deprecated: `@MockBean`, `@SpyBean`
- Moved: `RemoveSoapHeadersInterceptor` class location
- Removed: `com.att.idp.config` exclusion requirement

**Behavioral Changes:**
- RestAssured authentication behavior
- Spring Boot property handling
- Azure Spring configuration

### 7. Security Analysis
Compare security posture:

| CVE | Severity | Fixed In | Component |
|-----|----------|----------|-----------|
| CVE-XXXX-XXXX | Critical | 3.0.1 | Tomcat |
| ... | ... | ... | ... |

### 8. Migration Effort Estimation
Estimate effort based on:
- Number of breaking changes applicable to project
- Test coverage requirements
- Documentation updates needed

| Task | Estimated Time |
|------|----------------|
| POM Updates | 5 min |
| Annotation Replacements | 15-30 min |
| SOAP Interceptor Changes | 10 min |
| Test Fixes | 30-60 min |
| **Total** | **60-105 min** |

### 9. Generate Comparison Report
Create comprehensive comparison document:

```markdown
# Seed Version Comparison: {source} vs {target}

## Executive Summary
{Brief overview of key differences}

## Dependency Changes
{Detailed dependency matrix}

## Breaking Changes
{List of breaking changes with migration guidance}

## Security Improvements
{CVEs addressed}

## Migration Effort
{Effort estimation}

## Recommendation
{Upgrade recommendation with rationale}
```

## Error Handling
**Unknown Version**: Report unsupported version, list available versions
**Missing Documentation**: Provide wiki links for manual lookup
**Incomplete Comparison**: Note gaps in comparison data

## Examples
**Example 1**: `/compare-idp-seed-upgrade --from 3.0.0 --to 3.0.1`
Output: Full comparison of Seed 3.0.0 vs 3.0.1

**Example 2**: `/compare-idp-seed-upgrade --from 3.0.0 --to 3.0.1 --focus security`
Output: Security-focused comparison showing CVEs addressed

## References
- Constitution: `${ARCHETYPES_BASEDIR}/idp-seed-upgrade/idp-seed-upgrade-constitution.md`
- Env Config: `${ARCHETYPES_BASEDIR}/idp-seed-upgrade/templates/env-config.yaml`
