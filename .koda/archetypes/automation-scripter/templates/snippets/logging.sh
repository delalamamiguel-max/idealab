#!/bin/bash
# Structured JSON Logging Functions
# Source: Automation Scripter Constitution

# Get UTC timestamp in ISO 8601 format
timestamp() {
  date --utc +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u +"%Y-%m-%dT%H:%M:%SZ"
}

# Log message in structured JSON format
# Usage: log LEVEL "message" '{"key":"value"}'
log() {
  local level="$1"
  local message="$2"
  local context="${3:-{}}"
  
  printf '{"timestamp":"%s","level":"%s","message":"%s","context":%s}\n' \
    "$(timestamp)" "$level" "$message" "$context" >&2
}

# Convenience functions for different log levels
log_debug() {
  log "DEBUG" "$1" "${2:-{}}"
}

log_info() {
  log "INFO" "$1" "${2:-{}}"
}

log_warn() {
  log "WARN" "$1" "${2:-{}}"
}

log_error() {
  log "ERROR" "$1" "${2:-{}}"
}

# Example usage:
# log_info "Starting backup process" '{"database":"prod","size_gb":100}'
# log_error "Backup failed" '{"error":"Connection timeout","retry_count":3}'
