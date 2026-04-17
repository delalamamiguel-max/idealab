---
description: Validate IDP Seed upgrade with regression tests and compliance checks (IDP Seed Upgrade)
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
- Read `${ARCHETYPES_BASEDIR}/idp-seed-upgrade/idp-seed-upgrade-constitution.md` for validation rules
- Load `${ARCHETYPES_BASEDIR}/idp-seed-upgrade/templates/env-config.yaml` for test requirements

### 3. Parse Input
Extract from $ARGUMENTS:
- Project path
- Test scope (unit, component, integration, all)
- Skip flags (optional)

Request clarification if incomplete.

### 4. Pre-Upgrade Validation
Verify upgrade prerequisites:
- [ ] Current Seed version matches expected source version
- [ ] No uncommitted changes in repository
- [ ] Feature branch created (not on master/main)
- [ ] All deprecated patterns have been addressed

### 5. Compile Verification
// turbo
Run `mvn clean compile -DskipTests` to verify compilation succeeds with new dependencies.

### 6. Unit Test Execution
// turbo
Run `mvn test` to execute unit tests.

Validate:
- All tests pass
- No deprecation warnings in test output
- Code coverage maintained or improved

### 7. Component Test Execution
Run component/integration tests:
// turbo
Run `mvn verify -P component-tests` (or equivalent profile)

Validate:
- All component tests pass
- RestAssured authentication works correctly
- Spring context loads without errors

### 8. SAST Coverage Check
Verify SAST scan results:
- Coverage must be 100%
- No new critical/high vulnerabilities
- All existing vulnerabilities addressed

### 9. Dependency Analysis
// turbo
Run `mvn dependency:tree` to verify dependency resolution.

Check for:
- No version conflicts
- All managed dependencies resolve correctly
- No duplicate dependencies with different versions

### 10. Generate Test Report
Create test validation report:

```markdown
# Seed Upgrade Test Report

## Summary
- **Project**: {project_name}
- **Source Version**: {source_version}
- **Target Version**: {target_version}
- **Test Date**: {date}

## Test Results
| Test Type | Total | Passed | Failed | Skipped |
|-----------|-------|--------|--------|---------|
| Unit | | | | |
| Component | | | | |
| Integration | | | | |

## SAST Coverage
- Coverage: {percentage}%
- New Vulnerabilities: {count}

## Dependency Analysis
- Conflicts: {count}
- Warnings: {count}

## Recommendation
{PASS/FAIL with details}
```

## Error Handling
**Compilation Failure**: Report errors, suggest dependency fixes
**Test Failure**: Identify failing tests, provide debugging guidance
**SAST Failure**: List vulnerabilities, suggest remediation

## Examples
**Example 1**: `/test-idp-seed-upgrade --project /path/to/usermanagementms --scope all`
Output: Run full test suite and generate comprehensive report

**Example 2**: `/test-idp-seed-upgrade --project /path/to/usermanagementms --scope unit`
Output: Run only unit tests for quick validation

## References
- Constitution: `${ARCHETYPES_BASEDIR}/idp-seed-upgrade/idp-seed-upgrade-constitution.md`
- Env Config: `${ARCHETYPES_BASEDIR}/idp-seed-upgrade/templates/env-config.yaml`
