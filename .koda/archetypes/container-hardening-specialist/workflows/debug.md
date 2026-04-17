---
description: Diagnose container hardening failures including permission denied errors, capability conflicts, read-only filesystem issues, and credential loading problems
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read troubleshooting guidance from:
`${ARCHETYPES_BASEDIR}/container-hardening-specialist/container-hardening-specialist-constitution.md`

Focus on Section IV (Troubleshooting Guide).

### 2. Identify Problem Category

Categorize the reported issue based on $ARGUMENTS:

| Category | Symptoms | Common Root Causes |
|----------|----------|--------------------|
| **Permission Denied** | App can't read/write files, exec fails | Wrong file ownership, missing chown, overly restrictive mode |
| **Read-Only FS** | "EROFS" or "Read-only file system" errors | Missing tmpfs mount for writable path |
| **Capability Failure** | "Operation not permitted" on specific syscalls | Required capability dropped without re-add |
| **Credential Loading** | "File not found" or "Permission denied" on secrets | Wrong UID reading file, privilege drop too early |
| **tmpfs Exhaustion** | "No space left on device" on tmpfs path | Size limit too small for workload |
| **K8s Admission** | Pod rejected by admission controller | SecurityContext missing required fields |
| **Health Check** | Container marked unhealthy, restarts | Health check binary not executable, wrong port |
| **Setuid Conflict** | Application breaks after setuid stripping | App depends on setuid binary (su, passwd, ping) |

### 3. Collect Diagnostic Information

**For Permission Denied Issues:**

```bash
# Check running UID/GID
podman exec <container> id

# Check file ownership and permissions at the failing path
podman exec <container> ls -la /opt/app/
podman exec <container> ls -la /opt/app/service/config/

# Check if the Containerfile has proper chown
grep -n "chown\|COPY.*chown\|chmod" Containerfile
```

**For Read-Only Filesystem Issues:**

```bash
# Identify which path the application is trying to write to
podman logs <container> 2>&1 | grep -i "read-only\|EROFS"

# List all tmpfs mounts currently active
podman exec <container> mount | grep tmpfs

# Check if the failing path is covered by a tmpfs
podman exec <container> df -h
```

**For Capability Issues:**

```bash
# Check current capabilities
podman exec <container> cat /proc/1/status | grep -i cap

# Decode capability bitmask
podman exec <container> capsh --decode=$(cat /proc/1/status | grep CapEff | cut -f2)

# Test with all caps to confirm it's a capability issue
podman run --rm --cap-add=ALL myimage:latest <failing_command>
```

**For Credential Loading Issues:**

```bash
# Check credential file exists and has correct permissions
podman exec <container> ls -la /opt/app/service/config/

# Check which UID is trying to read the credential
podman exec <container> ps aux

# Verify the startup script reads secrets before privilege drop
grep -rn "credentials\|su-exec\|setuid\|exec.*user" scripts/start-*
```

**For Kubernetes Admission Issues:**

```bash
# Check pod events for admission errors
kubectl describe pod <pod-name> | grep -A5 "Events:"

# Validate against restricted Pod Security Standard
kubectl label --dry-run=server --overwrite ns <namespace> \
  pod-security.kubernetes.io/enforce=restricted

# Check SecurityContext completeness
kubectl get pod <pod-name> -o jsonpath='{.spec.containers[0].securityContext}' | jq .
```

### 4. Common Issues and Solutions

#### 4.1 Application Files Owned by Root

**Symptom**: `EACCES: permission denied` when application tries to read its own code files.

**Cause**: `COPY` instruction in Containerfile copies files as root by default.

**Fix**: Add `--chown` to all COPY instructions:

```dockerfile
# Before (files owned by root:root)
COPY dist/ /opt/app/dist/

# After (files owned by service account)
COPY --chown=appservice:appgroup dist/ /opt/app/dist/
```

#### 4.2 npm/pip Cache Writes to Read-Only Path

**Symptom**: `EROFS: read-only file system` when npm or pip tries to write cache.

**Cause**: npm writes to `~/.npm`, pip writes to `~/.cache/pip`, and the home directory is on the read-only rootfs.

**Fix**: Add a tmpfs mount for the cache directory:

```bash
--tmpfs /home/appservice/.npm:rw,size=64m,nosuid,noexec
--tmpfs /home/appservice/.cache:rw,size=64m,nosuid,noexec
```

#### 4.3 Health Check Fails After Hardening

**Symptom**: Container restarts in a loop; health check returns non-zero.

**Cause**: Health check uses `curl` or `wget` which may not be available in distroless images, or the health check binary lost execute permission after `chmod a-s` stripping.

**Fix**: Use a language-native health check:

```dockerfile
# Node.js — no curl needed
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => { process.exit(r.statusCode === 200 ? 0 : 1) })"

# Go — compiled binary with health endpoint
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD ["/opt/app/healthcheck"]
```

#### 4.4 Supervisord Cannot Signal Children After Privilege Drop

**Symptom**: `supervisorctl stop` fails with "kill: Operation not permitted".

**Cause**: Supervisord runs as root but children dropped to UID 1002. Without `KILL` capability, root cannot signal processes owned by other UIDs after `no-new-privileges` is set.

**Fix**: Ensure `KILL` capability is in the re-add list:

```bash
--cap-add=KILL
```

### 5. Generate Debug Report

```text
## Container Hardening Debug Report

**Issue Category**: {category from Step 2}
**Root Cause**: {one-sentence description}
**Affected Container**: {image:tag}

**Diagnostic Commands Run**:
- {command_1}: {result_summary}
- {command_2}: {result_summary}

**Files Modified**:
- {file_path}: {what was changed and why}

**Solution Applied**:
{step_by_step_description}

**Verification**:
{how to confirm the fix works — e.g., rebuild and test}

**Constitution Reference**: Section {section_number}, Rule {rule_number}
```

---

## Error Handling

**Cannot Reproduce**: Ask the user for the exact `podman run` or `kubectl apply` command, the container image tag, and the complete error output. Hardening issues are often specific to the flag combination used at runtime.

**Multiple Issues**: Prioritize by severity — hard-stop violations first, then functional breaks, then warnings. Fix each issue sequentially and re-test after each fix.

**Production Container**: If debugging a live production container, prefer non-destructive diagnostics (`exec`, `logs`, `inspect`) over modifications. Recommend fixing in a development environment and redeploying.

## Examples

### Example 1: Permission Denied
```text
/debug-container-hardening-specialist "
My Node.js app fails to start with EACCES: permission denied on /opt/app/server.js.
Container runs as UID 1001. Using --read-only with tmpfs on /tmp.
"
```

### Example 2: Credential Loading Failure
```text
/debug-container-hardening-specialist "
Application says 'credentials.compiled: ENOENT' after adding privilege drop.
The file exists at /opt/app/service/config/credentials.compiled with mode 400.
Process drops from UID 1001 to UID 1002 before reading it.
"
```

### Example 3: K8s Admission Rejection
```text
/debug-container-hardening-specialist "
Pod is rejected with: 'container must not set allowPrivilegeEscalation to true'.
But I have allowPrivilegeEscalation: false in my spec. Using namespace with
pod-security.kubernetes.io/enforce: restricted.
"
```

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/container-hardening-specialist/container-hardening-specialist-constitution.md` Section IV
- **Related**: scaffold-container-hardening-specialist, test-container-hardening-specialist, refactor-container-hardening-specialist
