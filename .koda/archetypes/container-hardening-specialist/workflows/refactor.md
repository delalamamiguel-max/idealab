---
description: Audit an existing container's security posture and apply defense-in-depth hardening incrementally
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read all hard-stop rules from:
`${ARCHETYPES_BASEDIR}/container-hardening-specialist/container-hardening-specialist-constitution.md`

Focus on Section I (Hard-Stop Rules) and Section V (Security Checklist).

### 2. Audit Current Security Posture

Scan the existing Containerfile and runtime configuration for violations:

**2.1 Containerfile Audit**

```bash
# Check for USER instruction (Rule 1.1)
grep -n "^USER" Containerfile

# Check for secrets in ENV instructions (Rule 1.2)
grep -in "ENV.*KEY\|ENV.*SECRET\|ENV.*PASSWORD\|ENV.*TOKEN\|ENV.*CREDENTIAL" Containerfile

# Check for setuid stripping (Rule 1.7)
grep -n "perm /6000\|chmod a-s" Containerfile

# Check for ADD vs COPY (CIS 4.9)
grep -n "^ADD " Containerfile

# Check for package install flags
grep -n "apt-get install\|apk add" Containerfile | grep -v "no-install-recommends"

# Check for HEALTHCHECK
grep -n "HEALTHCHECK" Containerfile
```

**2.2 Runtime Configuration Audit**

```bash
# Check run command or compose file for hardening flags
grep -in "cap-drop\|read-only\|no-new-privileges\|tmpfs\|privileged\|pids-limit" \
  docker-compose.yml compose.yml Makefile scripts/ 2>/dev/null

# Check Kubernetes deployment for SecurityContext
grep -A20 "securityContext" k8s/*.yaml deploy/*.yaml 2>/dev/null
```

**2.3 Secret Exposure Audit**

```bash
# Check for environment-based secrets in compose/k8s
grep -in "environment:\|env:\|envFrom:" docker-compose.yml compose.yml k8s/*.yaml 2>/dev/null

# Check for hardcoded secrets in application code
grep -rn "process\.env\.\(API_KEY\|SECRET\|PASSWORD\|TOKEN\)" src/ app/ lib/ 2>/dev/null
```

### 3. Generate Posture Report

```text
## Security Posture Audit Report

**Container Image**: {image:tag}
**Audit Date**: {date}

### Hard-Stop Rule Compliance

| Rule | Status | Finding |
|------|--------|---------|
| 1.1 No Root Execution | {PASS/FAIL} | {finding} |
| 1.2 No Secrets in Env | {PASS/FAIL} | {finding} |
| 1.3 Drop ALL Caps | {PASS/FAIL} | {finding} |
| 1.4 Read-Only Rootfs | {PASS/FAIL} | {finding} |
| 1.5 No-New-Privileges | {PASS/FAIL} | {finding} |
| 1.6 Secret File Perms | {PASS/FAIL/N/A} | {finding} |
| 1.7 Setuid Stripped | {PASS/FAIL} | {finding} |
| 1.8 No Privileged Mode | {PASS/FAIL} | {finding} |

### Mandatory Pattern Compliance

| Pattern | Status | Finding |
|---------|--------|---------|
| 2.1 Multi-UID Separation | {PASS/FAIL} | {finding} |
| 2.2 Compiled Credentials | {PASS/FAIL/N/A} | {finding} |
| 2.3 File-Then-Closure | {PASS/FAIL/N/A} | {finding} |
| 2.4 tmpfs Specification | {PASS/FAIL} | {finding} |
| 2.5 K8s SecurityContext | {PASS/FAIL/N/A} | {finding} |
| 2.6 CIS Checklist | {PASS/FAIL} | {finding} |
| 2.7 Threat Model | {PASS/FAIL} | {finding} |

### Risk Summary

- **Critical (Hard-Stop Violations)**: {count}
- **High (Missing Mandatory Patterns)**: {count}
- **Medium (Missing Preferred Patterns)**: {count}
- **Low (Best Practice Suggestions)**: {count}
```

**Present the posture report to the user and get approval before applying changes.**

### 4. Apply Hardening Layers (Incremental)

Apply fixes in priority order — each layer builds on the previous:

**Layer 1: Non-Root Execution (Rule 1.1)**

If the container runs as root:

- Add `groupadd` and `useradd` commands for service UID, user UID, shared GID
- Add `COPY --chown` for application files
- Set directory permissions
- Add `USER` instruction before ENTRYPOINT/CMD

**Layer 2: Capability Dropping (Rule 1.3)**

- Add `--cap-drop=ALL` to the run command
- Test the application to identify which capabilities are needed
- Re-add only necessary capabilities with justification

**Layer 3: Read-Only Rootfs (Rule 1.4)**

- Add `--read-only` flag
- Identify all writable paths by running without read-only and tracing writes
- Add tmpfs mounts with size limits and security flags for each writable path

**Layer 4: Credential Hardening (Rule 1.2)**

If secrets are currently in environment variables:

- Create credential compilation script
- Convert ENV-based secrets to file-based injection
- Update application code to read from file (file-then-closure pattern)
- Remove all `ENV` instructions containing secrets

**Layer 5: Setuid Stripping (Rule 1.7)**

- Add `find / -xdev -perm /6000 -type f -exec chmod a-s {} +` to Containerfile
- Test that no application functionality depends on setuid binaries

**Layer 6: Security Flags (Rules 1.5, 1.8)**

- Add `--security-opt no-new-privileges`
- Verify `--privileged` is not used anywhere
- Add `procMount: Default` for K8s

### 5. Generate Kubernetes SecurityContext (If Applicable)

If the application deploys to Kubernetes, generate or update the SecurityContext following constitution Section II.5.

### 6. Generate Compliance Documentation

- Update or create CIS Docker Benchmark checklist (Section II.6)
- Update or create threat model document (Section II.7)

### 7. Validate Refactoring

```bash
# Re-run the full audit — all rules should now pass
grep -n "^USER" Containerfile
grep -in "ENV.*KEY\|ENV.*SECRET\|ENV.*PASSWORD" Containerfile
grep -n "perm /6000" Containerfile
grep -rin "cap-drop\|read-only\|no-new-privileges" scripts/ docker-compose.yml 2>/dev/null

# Build and test
podman build -f Containerfile -t myimage:hardened .
podman run --rm myimage:hardened id  # Should show non-root UID
```

---

## Post-Refactor Checklist

```text
✅ All 8 hard-stop rules enforced
✅ Multi-UID separation with service/user/group
✅ Secrets moved from env vars to compiled credential files
✅ Read-only rootfs with all writable paths as sized tmpfs
✅ All capabilities dropped with justified re-adds only
✅ Setuid binaries stripped
✅ CIS compliance checklist updated
✅ Threat model updated

🔧 Next Steps:
1. Run /test-container-hardening-specialist to validate
2. Deploy to staging and run integration tests
3. Run container vulnerability scan (trivy/grype)
```

---

## Error Handling

**Large Legacy Containerfile**: For Containerfiles with 200+ lines and complex multi-stage builds, apply hardening layers one at a time and rebuild/test after each layer. Do not attempt to apply all layers at once.

**Application Breaks After Hardening**: Roll back the last layer applied and use `/debug-container-hardening-specialist` to diagnose the specific failure before re-applying.

**Third-Party Base Images**: If the base image is maintained by another team, document the hardening gaps that can only be fixed upstream and focus on runtime hardening (capability drop, read-only rootfs, security flags).

## Examples

### Example 1: Root Container Hardening
```text
/refactor-container-hardening-specialist "
Our Node.js container runs as root, secrets are in environment variables,
and we don't drop any capabilities. Containerfile is at ./Containerfile.
Need to bring it to full CIS compliance for security audit.
"
```

### Example 2: Partial Hardening Completion
```text
/refactor-container-hardening-specialist "
We already run as non-root (UID 1000) but don't have read-only rootfs,
capability dropping, or setuid stripping. Secrets are still in env vars.
Need to complete the hardening.
"
```

### Example 3: Kubernetes Migration
```text
/refactor-container-hardening-specialist "
Moving our container from bare Docker to AKS. Need to add full
Kubernetes SecurityContext with Pod Security Standard restricted
compliance. Currently have no SecurityContext in our deployment YAML.
"
```

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/container-hardening-specialist/container-hardening-specialist-constitution.md` Sections I, II, V
- **Related**: scaffold-container-hardening-specialist, test-container-hardening-specialist, debug-container-hardening-specialist
