# Automation Scripter Constitution

## Purpose

This constitution defines the foundational principles and hard-stop rules for the Automation Scripter archetype. All workflows, scripts, and generated code must adhere to these principles.

**Source**: Converted from `vibe_cdo/automation_scripter/.rules` and `governance_prompt.md`

---

## I. Hard-Stop Rules (Non-Negotiable)

These rules **MUST** be enforced. The AI agent must refuse or correct any code that violates these rules.

### 1.1 Security

**Principle**: Never expose credentials or secrets in code.

**Rules**:
- ✘ **NEVER** use plaintext credentials, API tokens, or secrets in scripts
- ✘ **NEVER** log sensitive data (secrets, PII) in plain text
- ✔ **ALWAYS** use environment variables or secure vault CLI for credentials
- ✔ **ALWAYS** enforce TLS 1.2+ for HTTP calls (curl, Invoke-RestMethod)

**Refusal Message**:
```
❌ Request violates Hard-Stop rule 1.1: Plaintext credentials detected.
Credentials must be sourced from environment variables or vault CLI.

Compliant alternative:
# Instead of:
API_KEY="hardcoded_secret_123"

# Use:
API_KEY="${API_KEY:-}"
if [ -z "$API_KEY" ]; then
  log "ERROR" "API_KEY environment variable not set"
  exit 1
fi
```

---

### 1.2 Error Handling

**Principle**: Scripts must fail fast and handle errors explicitly.

**Rules**:
- ✘ **NEVER** omit `set -euo pipefail` in Bash scripts
- ✘ **NEVER** omit `ErrorAction Stop` in PowerShell scripts
- ✘ **NEVER** skip signal traps for cleanup (SIGINT/SIGTERM)
- ✔ **ALWAYS** implement cleanup handlers for temporary resources

**Refusal Message**:
```
❌ Request violates Hard-Stop rule 1.2: Missing strict error handling.
Bash scripts must include 'set -euo pipefail' at the top.

Compliant alternative:
#!/bin/bash
set -euo pipefail

# Cleanup handler
cleanup() {
  log "INFO" "Cleaning up temporary files"
  rm -f "$TEMP_FILE"
}
trap cleanup EXIT SIGINT SIGTERM
```

---

### 1.3 Retry Logic

**Principle**: External calls must be resilient to transient failures.

**Rules**:
- ✘ **NEVER** call external CLI tools (rsync, curl, aws, etc.) without retry wrapper
- ✔ **ALWAYS** wrap external calls in retry logic (maxRetries ≥ 3, exponential backoff)

**Refusal Message**:
```
❌ Request violates Hard-Stop rule 1.3: External call without retry logic.
All external CLI calls must be wrapped in retry function.

Compliant alternative:
# Instead of:
aws s3 sync /local/ s3://bucket/

# Use:
retry aws s3 sync /local/ s3://bucket/
```

---

### 1.4 Logging

**Principle**: Logs must be structured and machine-readable.

**Rules**:
- ✘ **NEVER** log only plain text or unstructured messages
- ✔ **ALWAYS** emit structured JSON logs with fields: timestamp, level, message, context

**Refusal Message**:
```
❌ Request violates Hard-Stop rule 1.4: Unstructured logging detected.
All log output must be structured JSON format.

Compliant alternative:
# Instead of:
echo "Processing file: $filename"

# Use:
log "INFO" "Processing file" "{\"filename\":\"$filename\"}"
```

---

### 1.5 Argument Parsing

**Principle**: Scripts must have robust command-line interfaces.

**Rules**:
- ✘ **NEVER** skip command-line argument parsing (getopts or param block)
- ✔ **ALWAYS** provide help text (-h or --help) with clear examples

**Refusal Message**:
```
❌ Request violates Hard-Stop rule 1.5: Missing argument parsing.
Scripts must use getopts (Bash) or param block (PowerShell).

Compliant alternative:
while getopts "hf:o:" opt; do
  case $opt in
    h) usage; exit 0 ;;
    f) INPUT_FILE="$OPTARG" ;;
    o) OUTPUT_DIR="$OPTARG" ;;
    *) usage; exit 1 ;;
  esac
done
```

---

### 1.6 Configuration

**Principle**: Scripts must be configurable without code changes.

**Rules**:
- ✘ **NEVER** hard-code file paths, URLs, or thresholds
- ✔ **ALWAYS** parameterize configurable values via environment variables or config file

**Refusal Message**:
```
❌ Request violates Hard-Stop rule 1.6: Hard-coded configuration detected.
All paths, URLs, and thresholds must be parameterized.

Compliant alternative:
# Instead of:
BACKUP_DIR="/var/backups"

# Use:
BACKUP_DIR="${BACKUP_DIR:-/var/backups}"
```

---

## II. Mandatory Patterns (Must Apply)

These patterns **MUST** be applied to all generated scripts.

### 2.1 Retry Function

**Pattern**: Exponential backoff retry wrapper

**Implementation**:
```bash
# Bash retry function
MAX_RETRIES=3
retry() {
  local n=1
  local delay=2
  until "$@"; do
    ((n++)) || true
    if ((n > MAX_RETRIES)); then
      log "ERROR" "Failed after $MAX_RETRIES attempts: $*"
      return 1
    fi
    log "WARN" "Retry #$n for: $*"
    sleep "$delay"
    delay=$((delay * 2))
  done
}
```

**PowerShell**:
```powershell
function Invoke-WithRetry {
  param($ScriptBlock, [int]$MaxRetries = 3)
  $count = 0
  do {
    & $ScriptBlock
    if ($?) { break }
    else {
      $count++
      Start-Sleep -Seconds ([math]::Pow(2, $count))
    }
  } while ($count -lt $MaxRetries)
  if ($count -ge $MaxRetries) {
    Write-Log ERROR "Command failed after $MaxRetries"
    exit 1
  }
}
```

---

### 2.2 Structured Logging

**Pattern**: JSON-formatted log output

**Implementation**:
```bash
# Bash logging function
timestamp() {
  date --utc +"%Y-%m-%dT%H:%M:%SZ"
}

log() {
  local level="$1"
  local message="$2"
  local context="${3:-{}}"
  printf '{"timestamp":"%s","level":"%s","message":"%s","context":%s}\n' \
    "$(timestamp)" "$level" "$message" "$context"
}
```

**PowerShell**:
```powershell
function Write-Log {
  param($Level, $Message, $Context = @{})
  $ts = (Get-Date).ToString('o')
  $logEntry = @{
    timestamp = $ts
    level = $Level
    message = $Message
    context = $Context
  }
  Write-Output ($logEntry | ConvertTo-Json -Compress)
}
```

---

### 2.3 Signal Trapping

**Pattern**: Cleanup on exit and interruption

**Implementation**:
```bash
# Bash signal trap
TEMP_FILE=""

cleanup() {
  log "INFO" "Cleanup handler triggered"
  if [ -n "$TEMP_FILE" ] && [ -f "$TEMP_FILE" ]; then
    rm -f "$TEMP_FILE"
    log "INFO" "Removed temporary file: $TEMP_FILE"
  fi
}

trap cleanup EXIT SIGINT SIGTERM
```

---

### 2.4 Idempotency Checks

**Pattern**: Verify operation hasn't already been completed

**Implementation**:
```bash
# Check if operation already completed
if [ -f "$MARKER_FILE" ]; then
  log "INFO" "Operation already completed (marker file exists)"
  exit 0
fi

# Perform operation
perform_operation

# Create marker file
touch "$MARKER_FILE"
log "INFO" "Operation completed successfully"
```

---

### 2.5 Test Harness

**Pattern**: Bats (Bash) or Pester (PowerShell) tests

**Implementation**:
```bash
# test_script.bats
#!/usr/bin/env bats

@test "script exits with 0 on success" {
  run ./script.sh --dry-run
  [ "$status" -eq 0 ]
}

@test "script fails without required arguments" {
  run ./script.sh
  [ "$status" -ne 0 ]
}

@test "script handles missing credentials gracefully" {
  unset API_KEY
  run ./script.sh
  [ "$status" -eq 1 ]
  [[ "$output" =~ "API_KEY" ]]
}
```

---

## III. Preferred Patterns (Recommended)

These patterns **SHOULD** be adopted unless user provides explicit override.

### 3.1 → Function Size

**Guideline**: Keep functions to single responsibility and ≤ 75 lines of code

**Rationale**: Smaller functions are easier to test, debug, and maintain

**Example**:
```bash
# Good: Single responsibility, <75 LOC
validate_input() {
  if [ -z "$INPUT_FILE" ]; then
    log "ERROR" "INPUT_FILE not specified"
    return 1
  fi
  if [ ! -f "$INPUT_FILE" ]; then
    log "ERROR" "INPUT_FILE does not exist: $INPUT_FILE"
    return 1
  fi
  return 0
}

# Bad: Multiple responsibilities, >75 LOC
process_everything() {
  # Validation, processing, upload, cleanup all in one function
  # ... 150 lines of code ...
}
```

---

### 3.2 → Naming Conventions

**Guideline**: Consistent naming across scripts

**Bash**: `snake_case` for functions and variables
**PowerShell**: `PascalCase` for functions, `camelCase` for variables

**Example**:
```bash
# Bash
backup_database() {
  local db_name="$1"
  local backup_dir="$2"
  # ...
}
```

```powershell
# PowerShell
function Backup-Database {
  param($DbName, $BackupDir)
  # ...
}
```

---

### 3.3 → Shellcheck Compliance

**Guideline**: Follow shellcheck linting best practices

**Key Rules**:
- Quote variables to prevent word splitting
- Use fixed shebang (#!/bin/bash, not #!/bin/sh)
- Avoid useless use of cat
- Check command existence before use

**Example**:
```bash
# Good: Quoted variables
if [ -f "$CONFIG_FILE" ]; then
  source "$CONFIG_FILE"
fi

# Bad: Unquoted variables
if [ -f $CONFIG_FILE ]; then
  source $CONFIG_FILE
fi
```

---

### 3.4 Help Text

**Guideline**: Provide clear usage examples

**Implementation**:
```bash
usage() {
  cat <<EOF
Usage: $0 [OPTIONS]

Backup database to S3 with encryption and verification.

OPTIONS:
  -h, --help          Show this help message
  -d, --database NAME Database name to backup
  -b, --bucket NAME   S3 bucket for backup storage
  -e, --encrypt       Encrypt backup before upload
  -v, --verify        Verify backup integrity after upload

EXAMPLES:
  # Backup production database
  $0 --database prod_db --bucket backups --encrypt --verify

  # Dry run
  DRY_RUN=true $0 --database prod_db --bucket backups

ENVIRONMENT VARIABLES:
  AWS_ACCESS_KEY_ID     AWS access key (required)
  AWS_SECRET_ACCESS_KEY AWS secret key (required)
  DRY_RUN               Set to 'true' for dry run mode

EOF
}
```

---

### 3.5 Modular Organization

**Guideline**: Organize reusable code into library modules

**Structure**:
```
scripts/
├── lib/
│   ├── logging.sh      # Logging functions
│   ├── retry.sh        # Retry logic
│   ├── validation.sh   # Input validation
│   └── aws_helpers.sh  # AWS-specific helpers
├── backup_database.sh  # Main script
└── tests/
    └── backup_database.bats
```

**Usage**:
```bash
#!/bin/bash
set -euo pipefail

# Source library modules
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/logging.sh"
source "$SCRIPT_DIR/lib/retry.sh"
source "$SCRIPT_DIR/lib/validation.sh"

# Main script logic
main() {
  validate_environment
  perform_backup
}

main "$@"
```

---

### 3.6 Lock Files

**Guideline**: Use lock files to prevent concurrent execution

**Implementation**:
```bash
LOCK_FILE="/var/run/backup_script.lock"

acquire_lock() {
  if [ -f "$LOCK_FILE" ]; then
    local pid
    pid=$(cat "$LOCK_FILE")
    if ps -p "$pid" > /dev/null 2>&1; then
      log "ERROR" "Script already running (PID: $pid)"
      exit 1
    else
      log "WARN" "Stale lock file found, removing"
      rm -f "$LOCK_FILE"
    fi
  fi
  echo $$ > "$LOCK_FILE"
  log "INFO" "Lock acquired"
}

release_lock() {
  rm -f "$LOCK_FILE"
  log "INFO" "Lock released"
}

trap release_lock EXIT
acquire_lock
```

---

## IV. Quality Standards

### 4.1 Testing Requirements

**Coverage**: ≥80% test coverage for all functions

**Test Types**:
- Unit tests for individual functions
- Integration tests for external CLI calls
- Error scenario tests (missing credentials, network failures)
- Idempotency tests (run twice, same result)

---

### 4.2 Performance Targets

**Execution Time**: Scripts should complete within reasonable time for their purpose
- File transfer: Based on file size and network speed
- Database backup: Based on database size
- Infrastructure setup: <10 minutes for typical deployments

**Resource Usage**:
- Memory: <500MB for typical scripts
- CPU: Minimize busy-waiting, use sleep for retries
- Disk: Clean up temporary files promptly

---

### 4.3 Security Requirements

**Credentials**:
- Never log credentials or secrets
- Use secure credential storage (vault, env vars)
- Rotate credentials regularly

**File Permissions**:
- Scripts: 755 (rwxr-xr-x)
- Config files: 600 (rw-------)
- Log files: 640 (rw-r-----)

**Network**:
- Enforce TLS 1.2+ for all HTTPS connections
- Validate SSL certificates
- Use secure protocols (SFTP, not FTP)

---

## V. Enforcement Mechanisms

### 5.1 Automated Validation

**Guardrail Checks** (via check-guardrails.sh):
- Scan for hardcoded credentials (regex patterns)
- Verify presence of `set -euo pipefail` or `ErrorAction Stop`
- Check for retry wrappers around external calls
- Validate structured logging format
- Verify signal trap presence

**Linting**:
- Run shellcheck on all Bash scripts
- Run PSScriptAnalyzer on all PowerShell scripts
- Fail CI/CD pipeline on linting errors

---

### 5.2 Manual Review

**Code Review Checklist**:
- [ ] No hardcoded credentials or secrets
- [ ] Strict error handling enabled
- [ ] External calls wrapped in retry logic
- [ ] Structured JSON logging
- [ ] Signal traps and cleanup handlers
- [ ] Argument parsing with help text
- [ ] Idempotency checks
- [ ] Test harness with ≥80% coverage

---

### 5.3 Runtime Monitoring

**Logging**:
- All scripts emit structured JSON logs
- Logs include timestamp, level, message, context
- Logs sent to centralized logging system

**Alerting**:
- Alert on script failures (exit code ≠ 0)
- Alert on retry exhaustion
- Alert on security violations (credential exposure)

---

## VI. Override Protocol

### 6.1 Preferred Pattern Override

Users may override preferred patterns by:
- Providing explicit justification in comments
- Documenting the override decision
- Accepting responsibility for consequences

**Example**:
```bash
# Override: Using >75 LOC function due to complex state machine
# Justification: Breaking into smaller functions would obscure logic flow
# Approved by: Tech Lead (2025-01-15)
complex_state_machine() {
  # ... 120 lines of code ...
}
```

---

### 6.2 Hard-Stop Rule Override

Users **CANNOT** override hard-stop rules without:
- Formal security review
- Architecture approval
- Documented business justification
- Compensating controls

**Process**:
1. Submit override request with justification
2. Security team reviews risk
3. Architecture team approves design
4. Document compensating controls
5. Add exception to constitution

---

## VII. Related Documents

### 7.1 Source Documents

- Original `.rules` file: `vibe_cdo/automation_scripter/.rules`
- Original governance: `vibe_cdo/automation_scripter/prompts/governance_prompt.md`
- Original README: `vibe_cdo/automation_scripter/README.md`

### 7.2 Related Documents

- Workflow definitions: `.koda/workflows/automation-scripter/`
- Environment config: `.cdo-aifc/templates/automation-scripter/env-config.yaml`
- Example outputs: `.cdo-aifc/templates/automation-scripter/examples/`
- Code snippets: `.cdo-aifc/templates/automation-scripter/snippets/`

### 7.3 External Resources

- Shellcheck documentation: https://www.shellcheck.net/
- Bats testing framework: https://github.com/bats-core/bats-core
- PowerShell best practices: https://docs.microsoft.com/powershell/scripting/developer/cmdlet/cmdlet-development-guidelines

---

**Version**: 1.0.0  
**Last Updated**: 2025-10-07  
**Maintainer**: Data Engineering Team
