#!/bin/bash
# Retry Logic with Exponential Backoff
# Source: Automation Scripter Constitution

# Maximum number of retry attempts
MAX_RETRIES="${MAX_RETRIES:-3}"

# Retry function with exponential backoff
# Usage: retry command arg1 arg2 ...
retry() {
  local n=1
  local delay=2
  local max_delay=60
  
  until "$@"; do
    ((n++)) || true
    
    if ((n > MAX_RETRIES)); then
      log_error "Failed after $MAX_RETRIES attempts" "{\"command\":\"$*\"}"
      return 1
    fi
    
    log_warn "Retry #$n for command" "{\"command\":\"$*\",\"delay_seconds\":$delay}"
    sleep "$delay"
    
    # Exponential backoff with cap
    delay=$((delay * 2))
    if ((delay > max_delay)); then
      delay=$max_delay
    fi
  done
  
  if ((n > 1)); then
    log_info "Command succeeded after $n attempts" "{\"command\":\"$*\"}"
  fi
  
  return 0
}

# Retry with custom max attempts
# Usage: retry_with_max 5 command arg1 arg2 ...
retry_with_max() {
  local max_attempts="$1"
  shift
  
  local original_max=$MAX_RETRIES
  MAX_RETRIES=$max_attempts
  retry "$@"
  local result=$?
  MAX_RETRIES=$original_max
  
  return $result
}

# Example usage:
# retry aws s3 sync /local/ s3://bucket/
# retry curl -f https://api.example.com/health
# retry_with_max 5 rsync -avz /source/ /dest/
