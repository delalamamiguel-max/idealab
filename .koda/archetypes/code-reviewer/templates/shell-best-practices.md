# Shell Script Best Practices

> Aligned with **Code Reviewer Constitution §1 (Cross-cutting) & §4 (Shell Scripts)**

---

## 1. Script Header Block (Mandatory)

Every shell script must begin with a metadata header that establishes lineage and intent.

```bash
#!/usr/bin/env ksh
# ──────────────────────────────────────────────────────────────
# SCRIPT        : load_fact_sales.ksh
# DESCRIPTION   : Extracts daily FACT_SALES delta and stages to Snowflake
# SOURCE_SYSTEMS: Oracle OLTP (PROD)
# TARGET_TABLES : STG.FACT_SALES_DELTA
# SLA_PRIORITY  : P1 — must complete by 06:00 UTC
# AUTHOR        : <team>
# CREATED       : 2026-01-15
# ──────────────────────────────────────────────────────────────
```

---

## 2. Strict Mode (✔ Mandatory)

Always enable strict error handling at the top of the script, immediately after the header.

```bash
set -euo pipefail
IFS=$'\n\t'
```

| Flag | Purpose |
|------|---------|
| `-e` | Exit immediately on any non-zero return code |
| `-u` | Treat unset variables as errors |
| `-o pipefail` | Propagate failures through pipes |

---

## 3. Path Anchoring (✘ No Relative Paths)

Never rely on `cd` or the caller's working directory. Anchor all paths.

```bash
# ✘ BAD — breaks if called from a different directory
source ./config.env

# ✔ GOOD — always resolves relative to the script's own location
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "${SCRIPT_DIR}/config.env"
```

---

## 4. Environment Validation (✔ Mandatory)

Check that all required environment variables and commands exist before doing any work.

```bash
validate_prerequisites() {
    local missing=0

    for var in SNOWFLAKE_ACCOUNT SNOWFLAKE_USER SNOWFLAKE_WAREHOUSE; do
        if [[ -z "${!var:-}" ]]; then
            echo "ERROR: Required env var ${var} is not set." >&2
            missing=1
        fi
    done

    for cmd in snowsql jq; do
        if ! command -v "${cmd}" &>/dev/null; then
            echo "ERROR: Required command '${cmd}' not found in PATH." >&2
            missing=1
        fi
    done

    if [[ ${missing} -ne 0 ]]; then
        echo "FATAL: Prerequisites check failed. Aborting." >&2
        exit 1
    fi
}

validate_prerequisites
```

---

## 5. Cleanup via Trap (✔ Mandatory)

Use `trap` to guarantee cleanup of temporary files and resources, even on unexpected exit.

```bash
TMPDIR_WORK=""

cleanup() {
    local exit_code=$?
    if [[ -n "${TMPDIR_WORK}" && -d "${TMPDIR_WORK}" ]]; then
        rm -rf "${TMPDIR_WORK}"
        echo "INFO: Cleaned up temp dir ${TMPDIR_WORK}"
    fi
    exit "${exit_code}"
}

trap cleanup EXIT INT TERM

TMPDIR_WORK="$(mktemp -d "${TMPDIR:-/tmp}/load_fact_sales.XXXXXX")"
```

---

## 6. Local Variable Scoping (✔ Mandatory)

All variables inside functions must use the `local` keyword to prevent global namespace pollution.

```bash
# ✘ BAD — leaks `record_count` into global scope
get_row_count() {
    record_count=$(wc -l < "$1")
    echo "${record_count}"
}

# ✔ GOOD — scoped to the function
get_row_count() {
    local record_count
    record_count=$(wc -l < "$1")
    echo "${record_count}"
}
```

---

## 7. Logging & Traceability (✔ Mandatory)

Log with a correlation ID, timestamps, and structured prefixes. Never use bare `echo` for operational output.

```bash
RUN_ID="$(date +%Y%m%d%H%M%S)-$$"

log_info()  { echo "$(date -u +%FT%TZ) [INFO]  [${RUN_ID}] $*"; }
log_warn()  { echo "$(date -u +%FT%TZ) [WARN]  [${RUN_ID}] $*" >&2; }
log_error() { echo "$(date -u +%FT%TZ) [ERROR] [${RUN_ID}] $*" >&2; }

log_info "Starting FACT_SALES delta extraction"
log_info "Source: Oracle OLTP | Target: STG.FACT_SALES_DELTA"
```

---

## 8. Safe Deletions (✘ No Unsafe rm -rf)

Never delete without explicit path verification.

```bash
# ✘ BAD — if ARCHIVE_DIR is empty, this nukes /
rm -rf "${ARCHIVE_DIR}/"

# ✔ GOOD — validate before deletion
if [[ -n "${ARCHIVE_DIR}" && "${ARCHIVE_DIR}" == /data/archive/* ]]; then
    rm -rf "${ARCHIVE_DIR}/"
else
    log_error "Refusing to delete: ARCHIVE_DIR='${ARCHIVE_DIR}' looks suspicious."
    exit 1
fi
```

---

## 9. No Hardcoded Secrets (✘ Hard-Stop)

Credentials must never appear in source code. Source them from a secrets manager or secured environment.

```bash
# ✘ BAD
SNOWFLAKE_PASSWORD="SuperSecret123"

# ✔ GOOD — read from a secured credential store
SNOWFLAKE_PASSWORD="$(vault read -field=password secret/snowflake/prod)"
```

---

## 10. Idempotency (✔ Mandatory)

Scripts must be safe to rerun. Use guard clauses, watermarks, or status files.

```bash
WATERMARK_FILE="${SCRIPT_DIR}/.last_success_ts"

get_watermark() {
    if [[ -f "${WATERMARK_FILE}" ]]; then
        cat "${WATERMARK_FILE}"
    else
        echo "1970-01-01T00:00:00Z"  # First run — process everything
    fi
}

update_watermark() {
    date -u +%FT%TZ > "${WATERMARK_FILE}"
    log_info "Watermark updated to $(cat "${WATERMARK_FILE}")"
}
```

---

## 11. Error Handling — Fail Fast (✔ Mandatory)

Exit with meaningful, non-zero codes. Wrap critical sections explicitly.

```bash
snowsql -q "COPY INTO @stg_stage FROM @~/delta/" \
    || { log_error "Snowflake COPY INTO failed"; exit 2; }

log_info "COPY INTO completed successfully"
```

---

## 12. Full Template

```bash
#!/usr/bin/env ksh
# ──────────────────────────────────────────────────────────────
# SCRIPT        : example_etl.ksh
# DESCRIPTION   : Template shell script adhering to code-reviewer constitution
# SOURCE_SYSTEMS: <source>
# TARGET_TABLES : <target>
# SLA_PRIORITY  : P2
# AUTHOR        : <team>
# CREATED       : 2026-02-19
# ──────────────────────────────────────────────────────────────
set -euo pipefail
IFS=$'\n\t'

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RUN_ID="$(date +%Y%m%d%H%M%S)-$$"

# ── Logging ───────────────────────────────────────────────────
log_info()  { echo "$(date -u +%FT%TZ) [INFO]  [${RUN_ID}] $*"; }
log_warn()  { echo "$(date -u +%FT%TZ) [WARN]  [${RUN_ID}] $*" >&2; }
log_error() { echo "$(date -u +%FT%TZ) [ERROR] [${RUN_ID}] $*" >&2; }

# ── Cleanup ───────────────────────────────────────────────────
TMPDIR_WORK=""
cleanup() {
    local exit_code=$?
    [[ -n "${TMPDIR_WORK}" && -d "${TMPDIR_WORK}" ]] && rm -rf "${TMPDIR_WORK}"
    log_info "Exit code: ${exit_code}"
    exit "${exit_code}"
}
trap cleanup EXIT INT TERM

# ── Prerequisites ─────────────────────────────────────────────
validate_prerequisites() {
    local missing=0
    for var in REQUIRED_VAR_1 REQUIRED_VAR_2; do
        [[ -z "${!var:-}" ]] && { log_error "Missing env var: ${var}"; missing=1; }
    done
    for cmd in snowsql jq; do
        command -v "${cmd}" &>/dev/null || { log_error "Missing command: ${cmd}"; missing=1; }
    done
    [[ ${missing} -ne 0 ]] && exit 1
}
validate_prerequisites

# ── Config ────────────────────────────────────────────────────
source "${SCRIPT_DIR}/config.env"
TMPDIR_WORK="$(mktemp -d "${TMPDIR:-/tmp}/example_etl.XXXXXX")"

# ── Main Logic ────────────────────────────────────────────────
main() {
    log_info "Starting ETL process"
    local start_ts
    start_ts=$(date +%s)

    # ... business logic here ...

    local end_ts
    end_ts=$(date +%s)
    log_info "Completed in $((end_ts - start_ts))s"
}

main "$@"
```
