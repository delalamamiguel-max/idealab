---
description: Generate comprehensive documentation for IDP Seed upgrade migration (IDP Seed Upgrade)
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
- Read `${ARCHETYPES_BASEDIR}/idp-seed-upgrade/idp-seed-upgrade-constitution.md` for documentation requirements
- Load `${ARCHETYPES_BASEDIR}/idp-seed-upgrade/templates/env-config.yaml` for version details

### 3. Parse Input
Extract from $ARGUMENTS:
- Source Seed version
- Target Seed version
- Project(s) to document
- Documentation type (plan, summary, report, all)

Request clarification if incomplete.

### 4. Gather Migration Data
Collect information for documentation:
- Current POM configuration
- Code changes applied
- Test results
- SAST coverage
- Dependency changes

### 5. Generate Migration Plan Document
Create `docs/SEED-{version}-Migration-Plan.md`:

```markdown
# SEED {source} to {target} Migration Plan

## Document Information
| Field | Value |
|-------|-------|
| Project | {project_name} |
| Source Version | {source} |
| Target Version | {target} |
| Author | {author} |
| Date | {date} |
| Status | {Draft/Final} |

## Executive Summary
{Overview of migration scope and objectives}

## Prerequisites
- Microservice must be on Seed {source}
- Feature branch created
- All tests passing on current version

## Scope of Changes

### 1. POM Changes
{Detailed POM modifications}

### 2. Code Changes
{Code modifications required}

### 3. Configuration Changes
{Application configuration updates}

### 4. Test Changes
{Test code modifications}

## Migration Steps
{Step-by-step migration procedure}

## Validation Checklist
{Comprehensive validation checklist}

## Rollback Plan
{Rollback procedure if issues arise}

## References
{Links to official documentation}
```

### 6. Generate Migration Summary
Create `docs/SEED-{version}-Migration-Summary.md`:

```markdown
# SEED {source} to {target} Migration Summary

## Overview
{Brief summary of completed migration}

## Changes Applied

### POM Updates
| File | Change | Status |
|------|--------|--------|
| pom.xml | Parent version → {target} | ✅ |

### Code Changes
| Pattern | Files Modified | Status |
|---------|----------------|--------|
| @MockBean → @MockitoBean | {count} | ✅ |

## Test Results
{Test execution summary}

## SAST Coverage
{SAST scan results}

## Traceability
| Item | Reference |
|------|-----------|
| iTrack Ticket | {ticket_id} |
| AOTS CR | {cr_number} |
| Branch | {branch_name} |

## Sign-off
{Approval section}
```

### 7. Generate Upgrade Report
Create detailed technical report for audit purposes:
- All files modified with diff summary
- Dependency tree comparison
- Test coverage comparison
- Security scan comparison

### 8. Update README Changelog
Add migration entry to project README.md changelog section.

## Error Handling
**Missing Data**: Report gaps in migration data, suggest data collection
**Incomplete Migration**: Note incomplete items in documentation
**Template Error**: Provide manual documentation guidance

## Examples
**Example 1**: `/document-idp-seed-upgrade --from 3.0.0 --to 3.0.1 --project usermanagementms --type all`
Output: Generate complete documentation package

**Example 2**: `/document-idp-seed-upgrade --from 3.0.0 --to 3.0.1 --type summary`
Output: Generate migration summary only

## References
- Constitution: `${ARCHETYPES_BASEDIR}/idp-seed-upgrade/idp-seed-upgrade-constitution.md`
- Env Config: `${ARCHETYPES_BASEDIR}/idp-seed-upgrade/templates/env-config.yaml`
