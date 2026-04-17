---
description: Refactor bash/PowerShell script to apply security, idempotency, and reliability patterns (Automation Scripter)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype automation-scripter --json ` and parse for SHELL_VERSION, OS_TYPE, AVAILABLE_CLIS, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/automation-scripter/templates/env-config.yaml` for shell type, security policies, retry settings

### 3. Parse Input
Extract from $ARGUMENTS: existing script file path or inline code, refactoring goals (retry logic, logging, security, idempotency), target shell (bash/PowerShell). Request clarification if incomplete.

### 4. Analyze Existing Code
Load and analyze existing script:
- Identify hard-stop rule violations (plaintext credentials, missing strict mode, no signal traps, unstructured logging, missing argument parsing, hard-coded paths)
- Identify missing mandatory patterns (retry logic, structured logging, argument parsing, signal traps, idempotent operations, parameterization, test harness)
- Identify opportunities for preferred patterns (function size ≤75 LOC, shellcheck compliance, naming conventions, help text, modular organization, lock files)
- Calculate technical debt score

Report findings:
```
Analysis Results:
✘ Hard-Stop Violations: [count] found
  - Line 12: Plaintext credential detected
  - Line 3: Missing 'set -euo pipefail'
  - Line 45: External call without retry wrapper
✔ Mandatory Patterns Missing: [count]
  - Structured JSON logging not implemented
  - Signal traps not configured
  - No argument parsing (getopts)
➜ Preferred Patterns: [count] opportunities
  - Function exceeds 75 LOC (line 20-150)
  - No help text provided
  - Shellcheck warnings present
```

### 5. Generate Refactored Script

Create refactored script applying:

**Hard-Stop Fixes**:
- Move credentials to environment variables
- Add `set -euo pipefail` (bash) or `ErrorAction Stop` (PowerShell)
- Wrap external calls in retry function
- Replace echo with structured JSON logging
- Add argument parsing with getopts/param
- Add signal traps for cleanup
- Parameterize all hard-coded paths

**Mandatory Patterns**:
```bash
#!/bin/bash
set -euo pipefail

# Configuration from environment
SOURCE_DIR="${SOURCE_DIR:-/var/data}"
DEST_DIR="${DEST_DIR:-/backup}"
MAX_RETRIES="${MAX_RETRIES:-3}"
DRY_RUN="${DRY_RUN:-false}"

# Structured logging
timestamp() {
  date --utc +"%Y-%m-%dT%H:%M:%SZ"
}

log() {
  local level="$1"
  local message="$2"
  local context="${3:-{}}"
  printf '{"timestamp":"%s","level":"%s","message":"%s","context":%s}\n' \
    "$(timestamp)" "$level" "$message" "$context" >&2
}

# Retry logic with exponential backoff
retry() {
  local n=1
  local delay=2
  until "$@"; do
    ((n++)) || true
    if ((n > MAX_RETRIES)); then
      log "ERROR" "Failed after $MAX_RETRIES attempts" "{\"command\":\"$*\"}"
      return 1
    fi
    log "WARN" "Retry #$n" "{\"command\":\"$*\",\"delay\":$delay}"
    sleep "$delay"
    delay=$((delay * 2))
  done
}

# Cleanup handler
TEMP_FILES=()
cleanup() {
  log "INFO" "Cleanup handler triggered"
  for file in "${TEMP_FILES[@]}"; do
    if [ -f "$file" ]; then
      rm -f "$file"
      log "INFO" "Removed temp file" "{\"file\":\"$file\"}"
    fi
  done
}
trap cleanup EXIT SIGINT SIGTERM

# Argument parsing
usage() {
  cat <<EOF
Usage: $0 [OPTIONS]

Refactored script with retry logic, structured logging, and error handling.

OPTIONS:
  -h, --help          Show this help message
  -s, --source DIR    Source directory (default: $SOURCE_DIR)
  -d, --dest DIR      Destination directory (default: $DEST_DIR)
  -n, --dry-run       Dry run mode
  -r, --retries NUM   Max retries (default: $MAX_RETRIES)

EXAMPLES:
  $0 --source /data --dest /backup
  $0 --dry-run

ENVIRONMENT VARIABLES:
  SOURCE_DIR          Source directory
  DEST_DIR            Destination directory
  MAX_RETRIES         Maximum retry attempts
  DRY_RUN             Set to 'true' for dry run

EOF
}

while [[ $# -gt 0 ]]; do
  case $1 in
    -h|--help)
      usage
      exit 0
      ;;
    -s|--source)
      SOURCE_DIR="$2"
      shift 2
      ;;
    -d|--dest)
      DEST_DIR="$2"
      shift 2
      ;;
    -n|--dry-run)
      DRY_RUN=true
      shift
      ;;
    -r|--retries)
      MAX_RETRIES="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
done

# Main function (≤75 LOC)
main() {
  log "INFO" "Script started" "{\"source\":\"$SOURCE_DIR\",\"dest\":\"$DEST_DIR\",\"dry_run\":$DRY_RUN}"
  
  # Validation
  if [ ! -d "$SOURCE_DIR" ]; then
    log "ERROR" "Source directory not found" "{\"dir\":\"$SOURCE_DIR\"}"
    exit 1
  fi
  
  # Main operation with retry
  if [ "$DRY_RUN" = true ]; then
    log "INFO" "Dry run mode - no changes will be made"
    retry rsync -avz --dry-run --checksum "$SOURCE_DIR/" "$DEST_DIR/"
  else
    retry rsync -avz --checksum "$SOURCE_DIR/" "$DEST_DIR/"
  fi
  
  log "INFO" "Script completed successfully"
  exit 0
}

main
```

**Preferred Patterns**:
- Break large functions into smaller ones (≤75 LOC each)
- Apply shellcheck recommendations
- Use consistent naming (snake_case for bash, PascalCase for PowerShell)
- Add comprehensive help text
- Organize into modular structure (lib/ directory for reusable functions)
- Add lock file to prevent concurrent execution

### 6. Add Recommendations

Include inline comments for:
- **Parallel execution**: Opportunities to run tasks concurrently
- **Caching**: Strategies to avoid redundant operations
- **Monitoring**: Integration with monitoring systems
- **Alerting**: Hooks for failure notifications
- **Performance**: Optimization opportunities

Provide summary:
```
Refactoring Summary:
✅ Fixed 6 hard-stop violations
✅ Applied 7 mandatory patterns
✅ Implemented 5 preferred patterns

Security Improvements:
- Credentials moved to environment variables
- No plaintext secrets in code
- Proper error handling prevents information leakage

Reliability Improvements:
- Retry logic with exponential backoff
- Signal traps ensure cleanup
- Idempotent operations (rsync --checksum)

Maintainability Improvements:
- Structured logging for debugging
- Argument parsing with help text
- Functions ≤75 LOC for testability

Next Steps:
1. Test with Bats test framework
2. Run shellcheck for additional improvements
3. Add to CI/CD pipeline
4. Monitor execution in production
```

### 7. Validate and Report


Generate optional Bats test harness. Report completion with file paths, applied improvements, security enhancements, next steps.

## Error Handling

**Hard-Stop Violations in Original**: Explain each violation clearly (e.g., "Plaintext credential on line 12 violates security policy"), show compliant alternative with environment variable.

**Incomplete Input**: List missing information (script file path or code, refactoring goals, target shell), provide well-formed example.

**Environment Failure**: Report missing shell or CLI tools, suggest installation steps and environment setup.

## Examples

**Example 1: Add Retry Logic**
```
/refactor-automation Add retry logic to backup.sh for rsync operations

Input: Script with direct rsync calls
Output: Refactored with retry function, exponential backoff, structured logging
```

**Example 2: Security Hardening**
```
/refactor-automation Remove hardcoded credentials from deploy.sh

Input: Script with API_KEY="${API_KEY:-<REDACTED>}" 
Output: Refactored with API_KEY="${API_KEY:-}" and validation, environment variable usage
```

**Example 3: Complete Refactor**
```
/refactor-automation Refactor legacy_sync.sh to follow all best practices

Input: Old script with no error handling, echo statements, hard-coded paths
Output: Complete refactor with strict mode, logging, retry, signal traps, argument parsing
```

## References

