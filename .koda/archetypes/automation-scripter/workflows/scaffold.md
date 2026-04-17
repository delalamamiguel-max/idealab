---
description: Generate bash/PowerShell automation script with security, idempotency, and retry logic (Automation Scripter)
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
Extract from $ARGUMENTS: automation goal (file transfer/metadata harvest/infra setup), required CLIs (aws/az/gcloud), security requirements, target shell (bash/powershell/batch). Request clarification if incomplete.

### 4. Validate Constraints
Check against hard-stop rules:
- ✘ Refuse plaintext credentials or tokens
- ✘ Refuse non-idempotent operations without checks
- ✘ Refuse missing error handling or exit codes
- ✘ Refuse functions >75 LOC without refactoring
If violated, explain clearly and suggest compliant alternative.

### 5. Generate Automation Script

Create bash/PowerShell script with structure: shebang and strict mode (set -euo pipefail), configuration section with environment variables, argument parsing with getopts/param, logging function with structured JSON output (timestamp/level/message/context), retry function with exponential backoff (≥3 retries), main functions for discrete tasks (≤75 LOC each), signal trapping for cleanup (SIGINT/SIGTERM), main execution with error handling, exit with appropriate code (0 success, non-zero for errors).

Security patterns: credentials from environment variables or vault CLI (never hardcoded), file permissions checks before operations, input validation and sanitization, secure temporary file handling with cleanup, audit logging for sensitive operations.

Idempotency patterns: check if operation already completed (if [ -f ], if [ -d ]), lock files to prevent concurrent execution, dry-run flag for testing, rollback capability on failure, state tracking for resume capability.

Apply mandatory patterns: structured JSON logging, retry logic with exponential backoff, modular functions ≤75 LOC, argument parsing with help message, signal trapping and cleanup, exit codes for error classes, no plaintext credentials.

**Variable Syntax Strategy**:
- Bash: Use `${VAR}`
- PowerShell: Use `$Env:VAR`
- Batch: Use `%VAR%`

### 6. Add Recommendations

Include comments for: parallel execution opportunities, caching strategies, monitoring integration, alerting hooks, performance optimization.

### 7. Validate and Report


Generate optional Bats or pytest test harness. Report completion with file paths, applied guardrails, usage examples, next steps.

## Error Handling

**Hard-Stop Violations**: Explain violation (e.g., hardcoded credentials), suggest compliant alternative (environment variables or vault).

**Incomplete Input**: List missing information (automation goal, required CLIs, security requirements), provide well-formed example.

**Environment Failure**: Report missing shell or CLI tools, suggest installation steps.

## Examples

**S3 Archival**: `/scaffold-automation Archive daily logs from /var/logs to S3 with 30-day retention, use AWS CLI, include retry logic`
Output: Bash script with S3 sync, retry logic, structured logging, idempotency checks.

**Database Backup**: `/scaffold-automation Backup PostgreSQL database to Azure Blob Storage, encrypt before upload, verify integrity`
Output: Bash script with pg_dump, encryption, upload, verification, error handling.

**Infrastructure Setup**: `/scaffold-automation Bootstrap Kubernetes cluster with Helm charts, validate deployment, rollback on failure`
Output: Bash script with kubectl/helm commands, validation checks, rollback logic.

## References

