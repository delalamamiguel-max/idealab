---
description: Generate test harness for bash/PowerShell scripts (Automation Scripter)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype automation-scripter --json ` and parse for SHELL_VERSION, BATS_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/automation-scripter/templates/env-config.yaml` for test configuration

### 3. Parse Input
Extract from $ARGUMENTS: script file path, testing framework (Bats for bash, Pester for PowerShell), coverage goals, test scenarios. Request clarification if incomplete.

### 4. Analyze Code

Identify testable components: functions and commands, input parameters and arguments, file operations, external command calls, error handling paths, exit codes.

Determine test scenarios: positive cases (valid inputs, successful execution), negative cases (invalid inputs, missing files, command failures), edge cases (empty inputs, special characters, large files), integration cases (external dependencies, file system operations).

Report test coverage plan.

### 5. Generate Test Suite

Create comprehensive Bats/Pester test suite with setup/teardown, test fixtures (mock files, test data), unit tests (function tests, command tests), integration tests (end-to-end scenarios), error handling tests (failure cases, exit codes).

Include complete test code with mocking, assertions, and cleanup.

### 6. Add Recommendations

Include recommendations for test execution (run in CI/CD, test on multiple OS/shells), coverage improvements (add more edge cases, test error paths), mocking strategies (mock external commands, use test doubles).

Provide summary with test count and coverage.

### 7. Validate and Report


Generate test execution instructions. Report completion.

## Error Handling

**Insufficient Code Information**: Request complete script or file path.

**No Test Framework**: Suggest Bats for bash, Pester for PowerShell.

**Missing Dependencies**: Provide installation instructions.

## Examples

**Example 1**: `/test-automation Generate Bats tests for backup.sh` - Output: 10 tests covering success, failures, edge cases

**Example 2**: `/test-automation Create Pester tests for deploy.ps1` - Output: 12 tests with mocking and assertions

**Example 3**: `/test-automation Add integration tests for sync_script.sh` - Output: End-to-end tests with file operations

## References

