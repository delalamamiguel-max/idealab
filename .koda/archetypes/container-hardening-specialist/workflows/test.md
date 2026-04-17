---
description: Validate container hardening for CIS compliance, capability verification, secret exposure scanning, rootfs writability testing, and setuid binary detection
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read all validation requirements from:
`${ARCHETYPES_BASEDIR}/container-hardening-specialist/container-hardening-specialist-constitution.md`

Focus on Section I (Hard-Stop Rules), Section II (Mandatory Patterns), and Section V (Checklist).

### 2. Identify Test Scope

Determine what to validate from $ARGUMENTS:

| Scope | Description | Tests Run |
|-------|-------------|-----------|
| **Full** | Complete hardening validation | All 10 test categories |
| **Build** | Containerfile-only checks | Categories 1-4 |
| **Runtime** | Running container checks | Categories 5-8 |
| **Kubernetes** | K8s SecurityContext validation | Categories 9-10 |
| **Quick** | Hard-stop rules only | Categories 1, 3, 5, 6 |

### 3. Execute Test Categories

#### Category 1: Non-Root Execution (Rule 1.1)

```bash
# Test 1.1a: USER instruction exists and is non-root
USER_LINE=$(grep "^USER" Containerfile | tail -1)
if [[ -z "$USER_LINE" ]]; then
  echo "FAIL: No USER instruction in Containerfile"
elif echo "$USER_LINE" | grep -qi "root"; then
  echo "FAIL: USER instruction sets root"
else
  echo "PASS: USER instruction present — $USER_LINE"
fi

# Test 1.1b: Running container UID is non-root
RUNNING_UID=$(podman exec <container> id -u)
if [[ "$RUNNING_UID" == "0" ]]; then
  echo "FAIL: Container main process runs as root (UID 0)"
else
  echo "PASS: Container runs as UID $RUNNING_UID"
fi
```

#### Category 2: Multi-UID Separation (Pattern 2.1)

```bash
# Test 2.1a: Multiple non-root users exist
USER_COUNT=$(podman exec <container> getent passwd | awk -F: '$3 >= 1000 && $3 < 65534 {print}' | wc -l)
if [[ "$USER_COUNT" -lt 2 ]]; then
  echo "WARN: Only $USER_COUNT non-root users found (expected 2+ for privilege separation)"
else
  echo "PASS: $USER_COUNT non-root users with UID >= 1000"
fi

# Test 2.1b: Shared group exists
GROUP_EXISTS=$(podman exec <container> getent group | awk -F: '$3 == 2000 {print $1}')
if [[ -z "$GROUP_EXISTS" ]]; then
  echo "WARN: No shared group with GID 2000 found"
else
  echo "PASS: Shared group '$GROUP_EXISTS' (GID 2000) exists"
fi
```

#### Category 3: Secret Exposure Scan (Rule 1.2)

```bash
# Test 1.2a: No secrets in Containerfile ENV
SECRET_ENVS=$(grep -in "^ENV.*\(KEY\|SECRET\|PASSWORD\|TOKEN\|CREDENTIAL\)" Containerfile 2>/dev/null)
if [[ -n "$SECRET_ENVS" ]]; then
  echo "FAIL: Potential secrets in ENV instructions:"
  echo "$SECRET_ENVS"
else
  echo "PASS: No secret-like values in ENV instructions"
fi

# Test 1.2b: No secrets in running container environment
RUNTIME_ENVS=$(podman exec <container> env 2>/dev/null | grep -i "KEY\|SECRET\|PASSWORD\|TOKEN" | grep -v "PATH\|HOME\|HOSTNAME")
if [[ -n "$RUNTIME_ENVS" ]]; then
  echo "FAIL: Secret-like values found in runtime environment:"
  echo "$RUNTIME_ENVS" | sed 's/=.*/=***REDACTED***/'
else
  echo "PASS: No secret-like values in runtime environment"
fi

# Test 1.2c: Credential file permissions
CRED_FILES=$(podman exec <container> find / -name "*.compiled" -o -name "*credentials*" -o -name "*secret*" 2>/dev/null | grep -v proc | grep -v sys)
for f in $CRED_FILES; do
  PERMS=$(podman exec <container> stat -c '%a %U:%G' "$f" 2>/dev/null)
  MODE=$(echo "$PERMS" | cut -d' ' -f1)
  if [[ "$MODE" == "400" || "$MODE" == "440" ]]; then
    echo "PASS: $f has mode $MODE"
  else
    echo "FAIL: $f has mode $MODE (expected 400 or 440) — Rule 1.6 violation"
  fi
done
```

#### Category 4: Setuid Binary Scan (Rule 1.7)

```bash
# Test 1.7a: No setuid/setgid binaries remain
SETUID_BINS=$(podman exec <container> find / -xdev -perm /6000 -type f 2>/dev/null)
if [[ -n "$SETUID_BINS" ]]; then
  echo "FAIL: Setuid/setgid binaries found:"
  echo "$SETUID_BINS"
else
  echo "PASS: No setuid/setgid binaries found"
fi

# Test 1.7b: Stripping command in Containerfile
if grep -q "perm /6000.*chmod a-s" Containerfile; then
  echo "PASS: Setuid stripping command present in Containerfile"
else
  echo "WARN: Setuid stripping command not found in Containerfile"
fi
```

#### Category 5: Capability Verification (Rule 1.3)

```bash
# Test 1.3a: Effective capabilities are minimal
CAP_EFF=$(podman exec <container> cat /proc/1/status 2>/dev/null | grep CapEff | awk '{print $2}')
if [[ "$CAP_EFF" == "0000000000000000" ]]; then
  echo "PASS: No effective capabilities (fully dropped)"
else
  echo "INFO: Effective capabilities bitmask: $CAP_EFF"
  echo "      Decode: $(podman exec <container> capsh --decode=$CAP_EFF 2>/dev/null || echo 'capsh not available')"
  echo "      Verify each capability has documented justification"
fi

# Test 1.3b: cap-drop=ALL in run configuration
if grep -rq "cap-drop.*ALL\|drop.*ALL" scripts/ docker-compose.yml compose.yml 2>/dev/null; then
  echo "PASS: cap-drop=ALL found in run configuration"
else
  echo "FAIL: cap-drop=ALL not found in run configuration"
fi
```

#### Category 6: Read-Only Rootfs (Rule 1.4)

```bash
# Test 1.4a: Root filesystem is read-only
RO_CHECK=$(podman exec <container> touch /test-ro-check 2>&1)
if echo "$RO_CHECK" | grep -qi "read-only"; then
  echo "PASS: Root filesystem is read-only"
else
  echo "FAIL: Root filesystem is writable"
  podman exec <container> rm -f /test-ro-check 2>/dev/null
fi

# Test 1.4b: All tmpfs mounts have size limits
TMPFS_MOUNTS=$(podman exec <container> mount 2>/dev/null | grep tmpfs)
echo "$TMPFS_MOUNTS" | while read -r line; do
  MOUNT_POINT=$(echo "$line" | awk '{print $3}')
  if echo "$line" | grep -q "size="; then
    echo "PASS: $MOUNT_POINT has size limit"
  else
    echo "WARN: $MOUNT_POINT has no explicit size limit"
  fi
done

# Test 1.4c: tmpfs mounts have nosuid flag
echo "$TMPFS_MOUNTS" | while read -r line; do
  MOUNT_POINT=$(echo "$line" | awk '{print $3}')
  if echo "$line" | grep -q "nosuid"; then
    echo "PASS: $MOUNT_POINT has nosuid flag"
  else
    echo "WARN: $MOUNT_POINT missing nosuid flag"
  fi
done
```

#### Category 7: No-New-Privileges (Rule 1.5)

```bash
# Test 1.5a: no-new-privileges is set
NO_NEW_PRIV=$(podman exec <container> cat /proc/1/status 2>/dev/null | grep NoNewPrivs)
if echo "$NO_NEW_PRIV" | grep -q "1"; then
  echo "PASS: NoNewPrivs is set (1)"
else
  echo "FAIL: NoNewPrivs is not set"
fi
```

#### Category 8: Privileged Mode Check (Rule 1.8)

```bash
# Test 1.8a: Container is not running in privileged mode
PRIVILEGED=$(podman inspect <container> --format '{{.HostConfig.Privileged}}' 2>/dev/null)
if [[ "$PRIVILEGED" == "true" ]]; then
  echo "FAIL: Container is running in privileged mode — Rule 1.8 violation"
else
  echo "PASS: Container is not running in privileged mode"
fi
```

#### Category 9: Kubernetes SecurityContext (Pattern 2.5)

```bash
# Test 2.5a: SecurityContext completeness
REQUIRED_FIELDS=(
  "allowPrivilegeEscalation"
  "readOnlyRootFilesystem"
  "runAsNonRoot"
  "capabilities"
)
for field in "${REQUIRED_FIELDS[@]}"; do
  if grep -q "$field" k8s/*.yaml deploy/*.yaml 2>/dev/null; then
    echo "PASS: SecurityContext contains $field"
  else
    echo "FAIL: SecurityContext missing $field"
  fi
done

# Test 2.5b: Pod Security Standard namespace labels
if grep -q "pod-security.kubernetes.io/enforce: restricted" k8s/*.yaml deploy/*.yaml 2>/dev/null; then
  echo "PASS: Namespace has restricted Pod Security Standard"
else
  echo "WARN: Namespace does not enforce restricted Pod Security Standard"
fi
```

#### Category 10: Documentation Validation (Patterns 2.6, 2.7)

```bash
# Test 2.6a: CIS compliance checklist exists
if find . -name "*cis*" -o -name "*compliance*" -o -name "*benchmark*" 2>/dev/null | grep -qi "cis\|compliance\|benchmark"; then
  echo "PASS: CIS compliance document found"
else
  echo "WARN: No CIS compliance checklist found"
fi

# Test 2.7a: Threat model exists
if find . -name "*threat*" -o -name "*security-model*" 2>/dev/null | grep -qi "threat\|security.model"; then
  echo "PASS: Threat model document found"
else
  echo "WARN: No threat model document found"
fi
```

### 4. Generate Test Report

```text
## Container Hardening Test Report

**Container Image**: {image:tag}
**Test Date**: {timestamp}
**Test Scope**: {scope from Step 2}

### Summary

| Metric | Value |
|--------|-------|
| **Total Tests** | {total} |
| **Passed** | {pass_count} |
| **Failed** | {fail_count} |
| **Warnings** | {warn_count} |
| **Pass Rate** | {percentage}% |

### Hard-Stop Rule Results

| Rule | Test | Result | Detail |
|------|------|--------|--------|
| 1.1 | Non-root execution | {PASS/FAIL} | {detail} |
| 1.2 | No env secrets | {PASS/FAIL} | {detail} |
| 1.3 | Cap-drop ALL | {PASS/FAIL} | {detail} |
| 1.4 | Read-only rootfs | {PASS/FAIL} | {detail} |
| 1.5 | No-new-privileges | {PASS/FAIL} | {detail} |
| 1.6 | Secret file perms | {PASS/FAIL} | {detail} |
| 1.7 | Setuid stripped | {PASS/FAIL} | {detail} |
| 1.8 | No privileged mode | {PASS/FAIL} | {detail} |

### Mandatory Pattern Results

| Pattern | Test | Result | Detail |
|---------|------|--------|--------|
| 2.1 | Multi-UID separation | {PASS/WARN} | {detail} |
| 2.4 | tmpfs with size/flags | {PASS/WARN} | {detail} |
| 2.5 | K8s SecurityContext | {PASS/FAIL/N/A} | {detail} |
| 2.6 | CIS checklist | {PASS/WARN} | {detail} |
| 2.7 | Threat model | {PASS/WARN} | {detail} |

### Verdict

{PASS: All hard-stop rules met | FAIL: {count} hard-stop violations — must fix before deployment}

### Recommended Actions

1. {highest_priority_fix}
2. {next_priority_fix}
3. {optional_improvement}
```

---

## Error Handling

**Container Not Running**: If the user provides a Containerfile but no running container, run build-time checks only (Categories 1-4) and skip runtime checks.

**No Containerfile**: If the user provides only a running container, run runtime checks only (Categories 5-8) and note that build-time checks require the Containerfile.

**Kubernetes Not Applicable**: Skip Categories 9-10 if the user indicates no Kubernetes deployment.

## Examples

### Example 1: Full Validation
```text
/test-container-hardening-specialist "
Validate our production Node.js container.
Containerfile: ./Containerfile
Running as: podman run --name myapp ...
K8s manifest: ./k8s/deployment.yaml
"
```

### Example 2: Quick Hard-Stop Check
```text
/test-container-hardening-specialist "
Quick check on our container before security audit.
Container name: bp-workspace-dev1
Just the hard-stop rules.
"
```

### Example 3: Build-Only Validation
```text
/test-container-hardening-specialist "
Check our Containerfile for hardening compliance before we build.
File: ./container/Containerfile
No running container yet.
"
```

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/container-hardening-specialist/container-hardening-specialist-constitution.md` Sections I, II, V
- **Related**: scaffold-container-hardening-specialist, refactor-container-hardening-specialist, debug-container-hardening-specialist
