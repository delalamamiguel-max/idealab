---
description: Debug bash/PowerShell script errors and failures (Automation Scripter)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype automation-scripter --json ` and parse for SHELL_VERSION, OS_TYPE, AVAILABLE_CLIS, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/automation-scripter/templates/env-config.yaml` for shell type, security policies

### 3. Parse Input
Extract from $ARGUMENTS: script file path or inline code, error message (exit code, error output, stack trace), symptoms (script fails, hangs, produces wrong output), context (when it fails, environment, inputs). Request clarification if incomplete.

### 4. Analyze Problem

Identify error category: syntax errors (missing quotes, unclosed brackets, invalid commands), runtime errors (command not found, permission denied, file not found), logic errors (wrong conditions, incorrect loops, variable issues), security issues (exposed credentials, unsafe operations), performance issues (slow execution, resource exhaustion).

Check against constitution for violations. Analyze exit codes, error messages, and script logic.

Report findings with line numbers, error type, root cause, and impact.

### 5. Generate Fix

Create fixed script addressing root cause: fix syntax issues, add error handling, correct logic errors, implement security fixes (move credentials to env vars, add input validation), add performance optimizations (parallel execution, caching).

Include complete fixed script with comments explaining changes and defensive programming patterns.

### 6. Add Recommendations

Include recommendations for prevention (shellcheck/PSScriptAnalyzer, unit tests with Bats/Pester, code review), testing (test with edge cases, test error paths, test on target environment), monitoring (add logging, set up alerts, track execution metrics).

Provide summary with root cause, fix, testing strategy, and prevention measures.

### 7. Validate and Report


Generate optional test cases. Report completion with root cause, fix, testing recommendations.

## Error Handling

**Insufficient Error Information**: Request complete error output, exit code, and execution context.

**Cannot Reproduce**: Request environment details, input parameters, and system state.

**Multiple Possible Causes**: Provide systematic debugging steps with logging.

## Examples

**Example 1: Command Not Found**
```
/debug-automation Script failing with "command not found: rsync"

Root Cause: rsync not installed or not in PATH
Fix: Added dependency check, clear error message, installation instructions
```

**Example 2: Permission Denied**
```
/debug-automation Getting "Permission denied" when writing to /var/log

Root Cause: Script running without sudo, insufficient permissions
Fix: Added permission check, fallback to user-writable location, clear error message
```

**Example 3: Logic Error**
```
/debug-automation Backup script not backing up all files

Root Cause: Incorrect find command excluding hidden files
Fix: Corrected find syntax to include hidden files, added verification
```

## References

