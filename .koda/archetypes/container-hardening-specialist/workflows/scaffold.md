---
description: Generate a fully hardened container with multi-UID privilege separation, read-only rootfs, capability dropping, compiled credentials, and CIS compliance documentation
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read all hard-stop rules and mandatory patterns from:
`${ARCHETYPES_BASEDIR}/container-hardening-specialist/container-hardening-specialist-constitution.md`

Every generated artifact must comply with Section I hard-stop rules. Validate each deliverable against the checklist in Section V before presenting to the user.

### 2. Gather Requirements

Extract from $ARGUMENTS or prompt the user for:

| Requirement | Example | Default |
|-------------|---------|---------|
| **Application runtime** | Node.js 22, Python 3.12, Go 1.22 | Node.js 22 |
| **Base image** | node:22-slim, python:3.12-slim, gcr.io/distroless | Language-appropriate slim |
| **Service UID name** | appservice, gateway | appservice |
| **User UID name** | appuser, agent | appuser |
| **Service UID number** | 1001 | 1001 |
| **User UID number** | 1002 | 1002 |
| **Shared GID** | 2000 | 2000 |
| **Application port(s)** | 3000, 8080 | 3000 |
| **Writable paths needed** | /tmp, /var/log, /scratch | /tmp, /var/log |
| **Secrets to compile** | API_KEY, DB_PASSWORD | API_KEY |
| **Kubernetes deployment** | Yes/No | Yes |
| **Process supervisor** | supervisord, s6-overlay, none | none |
| **Corporate proxy** | Yes/No | No |

### 3. Generate Hardened Containerfile

Create the Containerfile with all hardening layers applied:

**Structure**:

1. Base image selection with version pin
2. System packages (if needed) with `--no-install-recommends`
3. Corporate CA certificate injection (if proxy)
4. User/group creation (service UID, user UID, shared GID)
5. Directory structure with precise ownership and permissions
6. Application code copy with `--chown`
7. Dependency installation
8. Setuid/setgid binary stripping
9. Runtime writable directory preparation
10. HEALTHCHECK instruction
11. USER switch to service account
12. EXPOSE and CMD/ENTRYPOINT

**Validation**: After generation, verify:
- `USER` instruction is present and non-root (Rule 1.1)
- No `ENV` with secret values (Rule 1.2)
- Setuid stripping command present (Rule 1.7)
- `COPY` used instead of `ADD` (CIS 4.9)
- `--no-install-recommends` on all apt-get (CIS 4.3)

### 4. Generate Credential Compilation Script

Create `compile-credentials` (shell script) following constitution Section II.2:

- Accept all secrets as `--flag value` arguments (never env vars)
- Validate required arguments with clear error messages
- Compute derived values (SHA-256 hashes, HMAC signatures)
- Write single JSON output file
- Set file permissions to 400
- Set directory permissions to 510
- Print confirmation message (no secret values in output)

### 5. Generate Run Script (with Privilege Drop)

If the container uses a process supervisor or needs the file-then-closure pattern, generate a startup script:

```bash
#!/bin/bash
set -euo pipefail

# Phase 1: Running as UID 1001 (service account) — can read secrets
CRED_FILE="/opt/app/service/config/credentials.compiled"
if [[ ! -f "$CRED_FILE" ]]; then
  echo "ERROR: Credentials file not found at ${CRED_FILE}"
  exit 1
fi

# Read secrets BEFORE privilege drop
API_KEY=$(jq -r '.apiKey' "$CRED_FILE")
export __INTERNAL_KEY="$API_KEY"  # Temporary — cleared after app init

# Phase 2: Drop to UID 1002 (user account) and exec application
exec su-exec appuser:appgroup node /opt/app/server.js
```

**Note**: The above is a simplified example. For production, prefer the closure pattern from Section II.3 where the secret is passed as a constructor argument rather than an environment variable.

### 6. Generate Podman/Docker Run Command

Create the complete `podman run` command with all hardening flags:

```bash
podman run \
  --name {app-name} \
  --read-only \
  --cap-drop=ALL \
  --cap-add=SETUID --cap-add=SETGID \
  --security-opt no-new-privileges \
  --security-opt mask=/proc/modules \
  --tmpfs /tmp:rw,size=256m,nosuid,nodev,noexec \
  --tmpfs /var/log:rw,size=64m,nosuid,noexec \
  --tmpfs /var/run:rw,size=8m,nosuid,noexec \
  --pids-limit=256 \
  -p {host_port}:{container_port} \
  {image}:{tag}
```

### 7. Generate Kubernetes SecurityContext YAML (If Requested)

Create the complete pod spec with SecurityContext following constitution Section II.5:

- Pod-level: `runAsUser`, `runAsGroup`, `fsGroup`
- Container-level: `allowPrivilegeEscalation: false`, `readOnlyRootFilesystem: true`, `runAsNonRoot: true`, `capabilities.drop: ["ALL"]`, `seccompProfile.type: RuntimeDefault`
- Volume definitions: emptyDir with `medium: Memory` and `sizeLimit` for each tmpfs
- Namespace: Pod Security Standard `restricted` labels

### 8. Generate CIS Compliance Checklist

Create the CIS Docker Benchmark compliance document following constitution Section II.6. Pre-populate all items based on the generated artifacts:

- Section 4 items: base image, user, packages, healthcheck, secrets, COPY vs ADD
- Section 5 items: capabilities, privileged, ports, read-only rootfs, seccomp, no-new-privileges

### 9. Generate Threat Model

Create the threat model document following constitution Section II.7:

- 10 attack vectors with impact/likelihood/mitigation
- UID/GID access matrix
- Capability justification table (if any caps re-added)

### 10. Validate All Deliverables

Run the Section V checklist against all generated artifacts:

```bash
# Verify no secrets in env instructions
grep -in "ENV.*KEY\|ENV.*SECRET\|ENV.*PASSWORD\|ENV.*TOKEN" Containerfile

# Verify USER instruction is non-root
grep "^USER" Containerfile

# Verify setuid stripping
grep "perm /6000" Containerfile

# Verify HEALTHCHECK
grep "HEALTHCHECK" Containerfile

# Verify read-only flag in run command
grep "read-only" scripts/run-hardened docker-compose.yml 2>/dev/null
```

---

## Post-Scaffold Checklist

```text
✅ Containerfile with all 8 hard-stop rules enforced
✅ Credential compilation script with mode-400 output
✅ Startup script with file-then-closure pattern (if supervisor)
✅ Podman/Docker run command with full hardening flags
✅ Kubernetes SecurityContext YAML (if requested)
✅ CIS Docker Benchmark compliance checklist
✅ Threat model with vector/impact/mitigation table
✅ UID/GID access matrix

🔧 Next Steps:
1. Build the image: podman build -f Containerfile -t {image}:{tag} .
2. Run /test-container-hardening-specialist to validate compliance
3. Run /document-container-hardening-specialist for security posture docs
```

---

## Error Handling

**Missing Application Details**: If $ARGUMENTS does not specify the runtime, language, or ports, prompt the user with the requirements table from Step 2. Do not guess — incorrect assumptions about writable paths or required capabilities will cause runtime failures.

**Conflicting Requirements**: If the user requests `--privileged` or secrets in environment variables, refuse using the constitution Section VI refusal template. Explain the risk and provide the compliant alternative.

**Existing Containerfile**: If the user has an existing Containerfile, recommend `/refactor-container-hardening-specialist` instead — it audits the current posture and applies hardening incrementally.

## Examples

### Example 1: Node.js API Server
```text
/scaffold-container-hardening-specialist "
Harden a Node.js 22 Express API server.
Port 3000. Needs /tmp for file uploads.
Deploy to AKS with Kubernetes SecurityContext.
Two secrets: OPENAI_API_KEY and DATABASE_URL.
"
```

### Example 2: Python ML Service
```text
/scaffold-container-hardening-specialist "
Harden a Python 3.12 FastAPI ML inference service.
Port 8080. Needs /scratch for model cache (2GB).
No Kubernetes — running on bare Podman.
Secret: HF_TOKEN for Hugging Face model downloads.
"
```

### Example 3: Go Microservice
```text
/scaffold-container-hardening-specialist "
Harden a Go 1.22 gRPC microservice compiled as a static binary.
Port 9090. Minimal writable paths — just /tmp.
Use distroless base. Deploy to K8s with cosign signing.
"
```

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/container-hardening-specialist/container-hardening-specialist-constitution.md`
- **Related**: test-container-hardening-specialist, refactor-container-hardening-specialist
