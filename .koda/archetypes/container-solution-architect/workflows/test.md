---
description: Validate container builds, health checks, and lifecycle operations
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read validation requirements from:
`${ARCHETYPES_BASEDIR}/container-solution-architect/container-solution-architect-constitution.md`

Focus on Section VI (Security Checklist).

### 2. Identify Test Scope

Determine what to test based on $ARGUMENTS:

| Scope | Tests |
|-------|-------|
| **Build** | Containerfile syntax, multi-stage, base image, build args |
| **Security** | Non-root user, credential permissions, no secrets in ENV |
| **Health** | Health endpoint, HEALTHCHECK instruction, startup time |
| **Lifecycle** | Start, stop, restart, destroy, rebuild |
| **Resources** | Memory limits, CPU limits, scratch storage |
| **Multi-User** | Base + overlay pattern, per-user credentials |

### 3. Build Validation Tests

#### 3.1 Containerfile Syntax

```bash
# Validate Containerfile syntax
podman build --check -f container/Containerfile . || echo "FAIL: Syntax error"
```

#### 3.2 Multi-Stage Build

```bash
# Check for multi-stage build
if grep -q "AS builder" container/Containerfile; then
  echo "PASS: Multi-stage build detected"
else
  echo "FAIL: Single-stage build - constitution violation"
fi
```

#### 3.3 Base Image Source

```bash
# Check for public registry usage
if grep -E "^FROM (docker\.io|gcr\.io|quay\.io|mcr\.microsoft)" container/Containerfile; then
  echo "FAIL: Public registry base image detected"
else
  echo "PASS: Corporate registry or local image"
fi
```

#### 3.4 Build Args

```bash
# Check credential build args exist
for arg in AUTH_KEY GITHUB_PAT LITELLM_API_KEY; do
  if grep -q "ARG $arg" container/Containerfile; then
    echo "PASS: $arg build arg defined"
  else
    echo "WARN: $arg build arg not found"
  fi
done
```

### 4. Security Validation Tests

#### 4.1 Non-Root User

```bash
# Check USER instruction exists
if grep -q "^USER [^r]" container/Containerfile; then
  echo "PASS: Non-root USER instruction found"
else
  echo "FAIL: No non-root USER instruction - constitution violation"
fi
```

#### 4.2 Credential Permissions

```bash
# Build and check permissions
podman build -t test:security -f container/Containerfile . > /dev/null 2>&1
podman run --rm test:security stat -c "%a %U:%G" /opt/app/config/credentials.compiled 2>/dev/null | \
  grep -q "440" && echo "PASS: Credentials 440 permissions" || echo "FAIL: Wrong credential permissions"
```

#### 4.3 No Secrets in ENV

```bash
# Check for secret ENV instructions
if grep -E "^ENV.*(KEY|SECRET|PASSWORD|TOKEN)=" container/Containerfile; then
  echo "FAIL: Secrets in ENV instruction - constitution violation"
else
  echo "PASS: No secrets in ENV"
fi
```

### 5. Health Validation Tests

#### 5.1 HEALTHCHECK Instruction

```bash
# Check HEALTHCHECK exists
if grep -q "^HEALTHCHECK" container/Containerfile; then
  echo "PASS: HEALTHCHECK instruction found"
else
  echo "FAIL: Missing HEALTHCHECK instruction"
fi
```

#### 5.2 Health Endpoint Response

```bash
# Start container and check health
podman run -d --name test-health -p 3099:3000 test:security
sleep 15

# Check health endpoint
if curl -sf http://localhost:3099/health > /dev/null 2>&1; then
  echo "PASS: Health endpoint responds"
else
  # Try via podman exec (macOS workaround)
  if podman exec test-health curl -sf http://127.0.0.1:3000/health > /dev/null 2>&1; then
    echo "PASS: Health endpoint responds (via exec)"
  else
    echo "FAIL: Health endpoint not responding"
  fi
fi

podman rm -f test-health
```

### 6. Lifecycle Validation Tests

#### 6.1 Start/Stop/Restart

```bash
# Test lifecycle operations
podman run -d --name test-lifecycle test:security

# Start (already running)
podman start test-lifecycle && echo "PASS: Start command"

# Stop
podman stop test-lifecycle && echo "PASS: Stop command"

# Restart
podman start test-lifecycle
podman restart test-lifecycle && echo "PASS: Restart command"

# Destroy
podman rm -f test-lifecycle && echo "PASS: Destroy command"
```

#### 6.2 Graceful Shutdown

```bash
# Test graceful shutdown
podman run -d --name test-shutdown test:security
START=$(date +%s)
podman stop test-shutdown
END=$(date +%s)
DURATION=$((END - START))

if [ $DURATION -lt 10 ]; then
  echo "PASS: Graceful shutdown in ${DURATION}s"
else
  echo "WARN: Slow shutdown (${DURATION}s) - check signal handling"
fi

podman rm -f test-shutdown
```

### 7. Resource Validation Tests

#### 7.1 Memory Limits

```bash
# Check compose has memory limits
if grep -q "memory:" deploy/dev/compose.yml; then
  echo "PASS: Memory limits defined in compose"
else
  echo "FAIL: No memory limits in compose"
fi
```

#### 7.2 CPU Limits

```bash
# Check compose has CPU limits
if grep -q "cpus:" deploy/dev/compose.yml; then
  echo "PASS: CPU limits defined in compose"
else
  echo "FAIL: No CPU limits in compose"
fi
```

### 8. Multi-User Validation Tests

#### 8.1 Base Image Exists

```bash
# Check base image builds
if podman build -t test:base -f container/Containerfile . > /dev/null 2>&1; then
  echo "PASS: Base image builds"
else
  echo "FAIL: Base image build failed"
fi
```

#### 8.2 Overlay Image Builds

```bash
# Check overlay builds with different credentials
if [ -f container/Containerfile.user ]; then
  podman build \
    --build-arg BASE_IMAGE=test:base \
    --build-arg AUTH_KEY=test-key-123 \
    -t test:user1 \
    -f container/Containerfile.user . > /dev/null 2>&1 && \
    echo "PASS: Overlay image builds" || echo "FAIL: Overlay build failed"
else
  echo "SKIP: No Containerfile.user (not multi-user)"
fi
```

### 9. Generate Test Report

```
## Container Test Report

**Test Date**: {timestamp}
**Image Tested**: {image_name}

### Build Tests
| Test | Status |
|------|--------|
| Containerfile syntax | {PASS/FAIL} |
| Multi-stage build | {PASS/FAIL} |
| Base image source | {PASS/FAIL} |
| Build args defined | {PASS/FAIL} |

### Security Tests
| Test | Status |
|------|--------|
| Non-root user | {PASS/FAIL} |
| Credential permissions | {PASS/FAIL} |
| No secrets in ENV | {PASS/FAIL} |

### Health Tests
| Test | Status |
|------|--------|
| HEALTHCHECK instruction | {PASS/FAIL} |
| Health endpoint response | {PASS/FAIL} |

### Lifecycle Tests
| Test | Status |
|------|--------|
| Start/Stop/Restart | {PASS/FAIL} |
| Graceful shutdown | {PASS/FAIL} |

### Resource Tests
| Test | Status |
|------|--------|
| Memory limits | {PASS/FAIL} |
| CPU limits | {PASS/FAIL} |

**Overall**: {PASS_COUNT}/{TOTAL_COUNT} tests passed
**Constitution Compliance**: {COMPLIANT/NON-COMPLIANT}
```

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/container-solution-architect/container-solution-architect-constitution.md` Section VI
- **Related**: debug-container-solution-architect, scaffold-container-solution-architect
